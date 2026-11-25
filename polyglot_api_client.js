/**
 * Polyglot Riff Atelier v3.4 — Browser SDK, Instant GitHub Pages Shard Engine,
 * Cross-Tab Context Sync Bus (PolyglotSyncBus) & Mobile-Web Ergonomics.
 *
 * Works seamlessly across:
 *   1. GitHub Pages / Static Cloud Hosting (https://<user>.github.io/<repo>/ -> instant <30ms ./db/*.db.json shard hydration)
 *   2. FastAPI Live Stack (http://127.0.0.1:8765 or Wi-Fi LAN http://192.168.x.x:8765)
 *   3. Offline Mobile/Desktop Browser Mode (Service Worker + localStorage outbox replay)
 */
(function (global) {
  const DEFAULT_API_ORIGIN = 'http://127.0.0.1:8765';
  const OUTBOX_STORAGE_KEY = 'polyglot_client_outbox_v34';
  const ORIGIN_STORAGE_KEY = 'polyglot_api_origin';
  const CONTEXT_STORAGE_KEY = 'polyglot_active_context_v34';
  const SHARD_FILES = [
    'cz_ova.db.json',
    'at_vie.db.json',
    'ru_ala.db.json',
    'en_yyc.db.json',
    'es_sot.db.json'
  ];

  // Canonical 5-Culture Metadata Registry for Cross-Tab Sync
  const CULTURE_META = {
    CZ_OVA: { registerId: 'CZ_OVA', formalId: 'CZ_STD', lowerKey: 'cz_ova', langCode: 'cs', langName: 'Czech', shortCode: 'CZ', flag: '🇨🇿', city: 'Ostrava', anthemIdx: 0 },
    AT_VIE: { registerId: 'AT_VIE', formalId: 'DE_STD', lowerKey: 'at_vie', langCode: 'de', langName: 'German', shortCode: 'AT', flag: '🇦🇹', city: 'Vienna', anthemIdx: 1 },
    RU_ALA: { registerId: 'RU_ALA', formalId: 'RU_STD', lowerKey: 'ru_ala', langCode: 'ru', langName: 'Russian', shortCode: 'KZ', flag: '🇰🇿', city: 'Almaty', anthemIdx: 2 },
    EN_YYC: { registerId: 'EN_YYC', formalId: 'EN_STD', lowerKey: 'en_yyc', langCode: 'en', langName: 'English', shortCode: 'CA', flag: '🇨🇦', city: 'Calgary', anthemIdx: 3 },
    ES_SOT: { registerId: 'ES_SOT', formalId: 'ES_STD', lowerKey: 'es_sot', langCode: 'es', langName: 'Spanish', shortCode: 'ES', flag: '🇪🇸', city: 'Sotogrande', anthemIdx: 4 }
  };

  function normalizeCulture(input) {
    if (!input) return CULTURE_META.CZ_OVA;
    const raw = String(input).trim().toUpperCase();
    if (CULTURE_META[raw]) return CULTURE_META[raw];
    if (raw === 'WEEKND') return CULTURE_META.EN_YYC;
    const byCode = {
      CS: 'CZ_OVA', CZ: 'CZ_OVA', CZ_STD: 'CZ_OVA',
      DE: 'AT_VIE', AT: 'AT_VIE', DE_STD: 'AT_VIE',
      RU: 'RU_ALA', KZ: 'RU_ALA', RU_STD: 'RU_ALA',
      EN: 'EN_YYC', CA: 'EN_YYC', EN_STD: 'EN_YYC',
      ES: 'ES_SOT', ES_STD: 'ES_SOT'
    };
    return CULTURE_META[byCode[raw]] || CULTURE_META.CZ_OVA;
  }

  function hasCustomApiOrigin() {
    try {
      const custom = global.localStorage && global.localStorage.getItem(ORIGIN_STORAGE_KEY);
      return Boolean(custom && custom.trim());
    } catch (_) {
      return false;
    }
  }

  function isStaticCloudHost() {
    if (hasCustomApiOrigin()) return false;
    try {
      const loc = global.location;
      if (!loc) return false;
      if (loc.protocol === 'file:') return true;
      const host = (loc.hostname || '').toLowerCase();
      if (
        host.endsWith('.github.io') ||
        host.endsWith('.netlify.app') ||
        host.endsWith('.vercel.app') ||
        host.endsWith('.pages.dev') ||
        host.endsWith('.cloudflarepages.com')
      ) {
        return true;
      }
    } catch (_) {}
    return false;
  }

  function resolveBaseOrigin() {
    try {
      const custom = global.localStorage && global.localStorage.getItem(ORIGIN_STORAGE_KEY);
      if (custom && custom.trim()) {
        return custom.trim().replace(/\/+$/, '');
      }
      if (global.location && global.location.protocol && global.location.protocol.startsWith('http')) {
        return global.location.origin;
      }
    } catch (_) {}
    return DEFAULT_API_ORIGIN;
  }

  let baseOrigin = resolveBaseOrigin();
  let cachedOfflineState = null;

  async function requestJson(path, options = {}, timeoutMs = 6000) {
    if (isStaticCloudHost()) {
      throw new Error('Static cloud host active (instant .db.json shard mode)');
    }
    baseOrigin = resolveBaseOrigin();
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const resp = await fetch(`${baseOrigin}${path}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...(options.headers || {})
        },
        signal: controller.signal
      });
      if (!resp.ok) {
        const text = await resp.text();
        throw new Error(`HTTP ${resp.status}: ${text}`);
      }
      return await resp.json();
    } finally {
      clearTimeout(timer);
    }
  }

  // =========================================================================
  // CLIENT-SIDE OFFLINE OUTBOX (localStorage queue -> POST /api/v1/sync/client-outbox)
  // =========================================================================
  function getOutboxEvents() {
    try {
      const raw = global.localStorage ? global.localStorage.getItem(OUTBOX_STORAGE_KEY) : null;
      const parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (_) {
      return [];
    }
  }

  function saveOutboxEvents(events) {
    try {
      if (global.localStorage) {
        global.localStorage.setItem(OUTBOX_STORAGE_KEY, JSON.stringify(events));
      }
      if (typeof global.dispatchEvent === 'function') {
        global.dispatchEvent(new CustomEvent('polyglot:outbox-updated', {
          detail: { count: events.length }
        }));
      }
    } catch (_) {}
  }

  function enqueueOutboxEvent(type, payload) {
    const events = getOutboxEvents();
    const entry = {
      id: `ev_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
      type,
      payload,
      queued_at: new Date().toISOString()
    };
    events.push(entry);
    saveOutboxEvents(events);
    return entry;
  }

  // =========================================================================
  // OFFLINE .db.json SHARD ASSEMBLER (Instant on GitHub Pages or Offline)
  // =========================================================================
  const lyricShardCache = new Map();
  const frequencyResponseCache = new Map();

  async function fetchLocalShardJson(filename) {
    const resp = await fetch(`./db/${filename}`);
    if (!resp.ok) throw new Error(`Shard ${filename} HTTP ${resp.status}`);
    return await resp.json();
  }

  async function fetchLocalLyricShard(songUidOrPath) {
    const raw = String(songUidOrPath || '').trim();
    if (!raw) throw new Error('Missing songUid for lyric shard');
    const cacheKey = raw.replace(/^(\.\/)?db\/lyrics\//i, '').replace(/\.lyrics\.json$/i, '').toLowerCase();
    if (lyricShardCache.has(cacheKey)) {
      return lyricShardCache.get(cacheKey);
    }
    const targetPath = raw.includes('/')
      ? (raw.startsWith('.') ? raw : `./${raw}`)
      : `./db/lyrics/${cacheKey}.lyrics.json`;
    const resp = await fetch(targetPath);
    if (!resp.ok) throw new Error(`Lyric shard ${targetPath} HTTP ${resp.status}`);
    const data = await resp.json();
    if (!Array.isArray(data.lyric_stanzas) && Array.isArray(data.stanzas_lines)) {
      data.lyric_stanzas = data.stanzas_lines.map(lines => (Array.isArray(lines) ? lines.join('\n') : String(lines || '')));
    }
    if (!data.full_lyrics && Array.isArray(data.lyric_stanzas)) {
      data.full_lyrics = data.lyric_stanzas.join('\n\n');
    }
    lyricShardCache.set(cacheKey, data);
    return data;
  }

  function clearLyricShardCache(songUid = '') {
    if (!songUid) {
      lyricShardCache.clear();
      frequencyResponseCache.clear();
      return;
    }
    const key = String(songUid).trim().toLowerCase();
    lyricShardCache.delete(key);
    frequencyResponseCache.delete(key);
  }

  async function assembleOfflineStateFromShards(includeFormalPersonas = false) {
    if (cachedOfflineState && !includeFormalPersonas) {
      return cachedOfflineState;
    }
    const fabric = await fetchLocalShardJson('polyglot_fabric.db.json');
    const shards = await Promise.all(SHARD_FILES.map(f => fetchLocalShardJson(f)));

    const personas = {};
    const allRegisters = {};
    const idioms = {};
    const allCards = [];
    const terraceCards = [];
    const vocab = [...(fabric.vocab_alert_nodes || [])];

    shards.forEach(sh => {
      Object.entries(sh.personas || {}).forEach(([id, p]) => {
        allRegisters[id] = p;
        if (includeFormalPersonas || p.tier === 'REGIONAL') {
          personas[id] = p;
        }
      });
      Object.entries(sh.idioms || {}).forEach(([term, idm]) => {
        idioms[term] = idm;
      });
      (sh.vocab || []).forEach(v => vocab.push(v));
      (sh.cards || []).forEach(c => {
        const cardItem = {
          uid: c.uid,
          lang: c.lang,
          stage: c.stage,
          arena: c.arena || 'terrace',
          lens_id: c.lens || null,
          title: c.title || '',
          text: c.text,
          phonetics: c.phonetics || '',
          english: c.english || '',
          delivery: c.delivery || '',
          idioms: c.idioms || []
        };
        allCards.push(cardItem);
        if ((c.arena || 'terrace') === 'terrace' && !c.lens) {
          terraceCards.push(cardItem);
        }
      });
    });

    const songs = (fabric.songs || []).map(s => ({
      ...s,
      translations: s.translations || {
        ES: s.translation_es || '',
        EN: s.translation_en || '',
        CZ: s.translation_cz || '',
        DE: s.translation_de || '',
        RU: s.translation_ru || ''
      }
    }));

    const assembled = {
      offlineShardMode: true,
      schema_version: fabric.schema_version || '3.5.0',
      arenas: fabric.arenas || [],
      personas,
      allRegisters,
      idioms,
      cards: terraceCards,
      allCards,
      bridges: fabric.bridges || [],
      edges: [],
      roomStates: fabric.room_states || [],
      falseFriends: fabric.false_friends || [],
      songs,
      vocab,
      vocabFalseFriendAlerts: fabric.vocab_false_friend_alerts || [],
      vibeLinks: fabric.vibe_links || [],
      stagedWebhooks: fabric.staged_webhooks || []
    };

    if (!includeFormalPersonas) {
      cachedOfflineState = assembled;
    }
    return assembled;
  }

  async function assembleRegisterSwitcherFromShards(langCode = 'cs') {
    const meta = normalizeCulture(langCode);
    const st = await assembleOfflineStateFromShards(true);
    // Notice: English formal register in shards is EN_EXEC (while CULTURE_META.formalId uses EN_STD as alias)
    const formalKey = st.allRegisters[meta.formalId]
      ? meta.formalId
      : (meta.langCode === 'en' && st.allRegisters.EN_EXEC ? 'EN_EXEC' : meta.formalId);
    const formalRegister = st.allRegisters[formalKey] || {};
    const regionalRegister = st.allRegisters[meta.registerId] || {};

    const stageOrder = { COMPLIMENT: 1, CHAMELEON: 2, COUNTERACT: 3, CURIOSITY: 4 };
    const stripHtml = (s) => String(s || '').replace(/<[^>]+>/g, '');
    const mapCard = (c) => ({
      uid: c.uid,
      register_id: c.lang,
      stage: c.stage,
      arena: c.arena,
      title: c.title || c.stage,
      text_plain: stripHtml(c.text),
      text_html: c.text,
      phonetics: c.phonetics || '',
      english_gloss: c.english || '',
      delivery_cue: c.delivery || '',
      idiom_terms: c.idioms || []
    });

    const formalCards = st.allCards
      .filter(c => c.lang === formalKey && !c.lens_id)
      .sort((a, b) => {
        const sa = stageOrder[a.stage] || 99;
        const sb = stageOrder[b.stage] || 99;
        if (sa !== sb) return sa - sb;
        const aPref = a.uid.startsWith(formalKey) ? 0 : 1;
        const bPref = b.uid.startsWith(formalKey) ? 0 : 1;
        return aPref - bPref;
      })
      .map(mapCard);

    const regionalCandidates = st.allCards
      .filter(c => c.lang === meta.registerId && !c.lens_id && (c.arena === 'b2b' || c.arena === 'terrace'))
      .sort((a, b) => {
        const aa = a.arena === 'b2b' ? 0 : 1;
        const ab = b.arena === 'b2b' ? 0 : 1;
        if (aa !== ab) return aa - ab;
        return (stageOrder[a.stage] || 99) - (stageOrder[b.stage] || 99);
      });

    const byStage = {};
    regionalCandidates.forEach(rc => {
      if (!byStage[rc.stage]) {
        byStage[rc.stage] = mapCard(rc);
      }
    });
    const regionalCards = ['COMPLIMENT', 'CHAMELEON', 'COUNTERACT', 'CURIOSITY']
      .map(stage => byStage[stage])
      .filter(Boolean);

    const dropBridge = (st.bridges || [])
      .filter(b => b.from_register === formalKey && b.to_register === meta.registerId)
      .sort((a, b) => Number(b.weight || 0) - Number(a.weight || 0))[0] || null;

    const sequence = [];
    ['COMPLIMENT', 'CHAMELEON'].forEach(stage => {
      const fc = formalCards.find(c => c.stage === stage);
      if (fc && formalRegister.id) {
        sequence.push({
          uid: fc.uid,
          reg: formalRegister.id,
          tier: 'FORMAL',
          stage: fc.stage,
          lang: `${formalRegister.name} (${formalRegister.address_form || ''})`,
          vibe: formalRegister.subtitle || '',
          text: fc.text_plain,
          text_html: fc.text_html,
          phonetics: fc.phonetics,
          english: fc.english_gloss,
          mechanics: formalRegister.trick || formalRegister.intimacy_trick || '',
          delivery: fc.delivery_cue || formalRegister.posture || ''
        });
      }
    });

    if (dropBridge && formalRegister.id && regionalRegister.id) {
      sequence.push({
        uid: dropBridge.uid,
        reg: 'BRIDGE',
        tier: 'BRIDGE',
        stage: 'REGISTER_DROP_BRIDGE',
        lang: `Code-Switch Pivot (${formalRegister.id} → ${regionalRegister.id})`,
        vibe: `PIVOTS_VIA (Weight: ${Number(dropBridge.weight || 0).toFixed(2)})`,
        text: stripHtml(dropBridge.text),
        text_html: dropBridge.text,
        phonetics: '',
        english: dropBridge.mlf_boundary_note || '',
        mechanics: dropBridge.mlf_boundary_note || 'Mid-sentence matrix shift from formal to insider peer',
        delivery: dropBridge.vocal_cue || ''
      });
    }

    ['COUNTERACT', 'CURIOSITY'].forEach(stage => {
      const rc = byStage[stage];
      if (rc && regionalRegister.id) {
        sequence.push({
          uid: rc.uid,
          reg: regionalRegister.id,
          tier: 'REGIONAL',
          stage: rc.stage,
          lang: `${regionalRegister.name} (${regionalRegister.address_form || ''})`,
          vibe: regionalRegister.subtitle || '',
          text: rc.text_plain,
          text_html: rc.text_html,
          phonetics: rc.phonetics,
          english: rc.english_gloss,
          mechanics: regionalRegister.trick || regionalRegister.intimacy_trick || '',
          delivery: rc.delivery_cue || regionalRegister.posture || ''
        });
      }
    });

    const language = {
      code: meta.langCode,
      name: meta.langName || meta.city,
      flag: meta.flag,
      family: regionalRegister.family || ''
    };

    return {
      language,
      formal_register: formalRegister,
      regional_register: regionalRegister,
      bridge: dropBridge,
      sequence,
      all_formal_cards: formalCards,
      all_regional_cards: regionalCards,
      false_friends: st.falseFriends || [],
      offlineShardMode: true
    };
  }

  const ARENA_ALIASES = {
    general: 'terrace',
    lounge: 'terrace',
    banter: 'spark'
  };

  function normalizeArenaId(arena) {
    const raw = String(arena || 'terrace').trim().toLowerCase();
    return ARENA_ALIASES[raw] || raw || 'terrace';
  }

  // =========================================================================
  // PUBLIC POLYGLOT API CLIENT
  // =========================================================================
  const api = {
    CULTURE_META,
    normalizeCulture,
    isStaticCloudHost,

    get baseOrigin() {
      return resolveBaseOrigin();
    },
    setBaseOrigin(newOrigin) {
      try {
        if (global.localStorage) {
          if (newOrigin && newOrigin.trim()) {
            global.localStorage.setItem(ORIGIN_STORAGE_KEY, newOrigin.trim().replace(/\/+$/, ''));
          } else {
            global.localStorage.removeItem(ORIGIN_STORAGE_KEY);
          }
        }
      } catch (_) {}
      baseOrigin = resolveBaseOrigin();
      return baseOrigin;
    },
    isOnline: false,

    getOutboxCount() {
      return getOutboxEvents().length;
    },

    getOutboxEvents,

    async flushClientOutbox() {
      const events = getOutboxEvents();
      if (!events.length) return { ok: true, applied_count: 0, remaining: 0 };
      try {
        const res = await requestJson('/api/v1/sync/client-outbox', {
          method: 'POST',
          body: JSON.stringify({ events })
        }, 12000);
        if (res && res.ok) {
          saveOutboxEvents([]);
        }
        return { ...res, remaining: getOutboxEvents().length };
      } catch (err) {
        return { ok: false, offline: true, remaining: events.length, error: String(err) };
      }
    },

    async health() {
      if (isStaticCloudHost()) {
        api.isOnline = false;
        return { ok: false, offline: true, staticCloudHost: true };
      }
      try {
        const res = await requestJson('/api/v1/health', { method: 'GET' }, 3000);
        api.isOnline = Boolean(res && res.ok);
        if (api.isOnline && getOutboxEvents().length > 0) {
          api.flushClientOutbox().catch(() => {});
        }
        return res;
      } catch (err) {
        api.isOnline = false;
        return { ok: false, offline: true, error: String(err) };
      }
    },

    async checkHealth() {
      const res = await api.health();
      return res && res.ok ? res : null;
    },

    async fetchAudit() {
      try {
        return await requestJson('/api/v1/admin/audit', { method: 'GET' }, 10000);
      } catch (_) {
        const st = await assembleOfflineStateFromShards(false);
        const totalCards = (st.allCards || st.cards || []).length;
        const totalSongs = (st.songs || []).length;
        const shardOk = totalSongs >= 6 && totalCards >= 196;
        return {
          ok: shardOk,
          offlineShardMode: true,
          schema_version: st.schema_version || '3.5.0',
          checks: [
            {
              check: 'offline_db_json_shard_parity',
              ok: shardOk,
              detail: `Offline Shards Active (${totalCards} cards, ${totalSongs} songs)`
            }
          ]
        };
      }
    },

    async fetchNetworkInfo() {
      try {
        return await requestJson('/api/v1/network-info', { method: 'GET' }, 3500);
      } catch (err) {
        const currentUrl = (global.location && global.location.href) ? global.location.href : `${resolveBaseOrigin()}/index.html`;
        return {
          ok: false,
          localhost_url: currentUrl,
          primary_lan_url: currentUrl,
          lan_urls: [currentUrl],
          error: String(err)
        };
      }
    },

    async fetchFullState(includeFormalPersonas = false) {
      try {
        const res = await requestJson(
          `/api/v1/state/full?include_formal_personas=${includeFormalPersonas ? 'true' : 'false'}`,
          { method: 'GET' },
          5500
        );
        api.isOnline = true;
        return res;
      } catch (_) {
        api.isOnline = false;
        return await assembleOfflineStateFromShards(includeFormalPersonas);
      }
    },

    async fetchArenas() {
      try {
        return await requestJson('/api/v1/arenas', { method: 'GET' }, 4500);
      } catch (_) {
        const st = await assembleOfflineStateFromShards(false);
        return st.arenas || [];
      }
    },

    async fetchAuditReport() {
      return await requestJson('/api/v1/admin/audit', { method: 'GET' }, 10000);
    },

    async fetchRegisterSwitcher(langCode = 'cs') {
      try {
        return await requestJson(`/api/v1/registers/${encodeURIComponent(langCode)}/switcher`, { method: 'GET' }, 4500);
      } catch (_) {
        return await assembleRegisterSwitcherFromShards(langCode);
      }
    },

    async fetchVocab(langCode = '', registerType = '') {
      try {
        const qs = new URLSearchParams();
        if (langCode) qs.set('lang_code', langCode);
        if (registerType) qs.set('register_type', registerType);
        const suffix = qs.toString() ? `?${qs.toString()}` : '';
        return await requestJson(`/api/v1/vocab${suffix}`, { method: 'GET' }, 4500);
      } catch (_) {
        const st = await assembleOfflineStateFromShards(true);
        let rows = st.vocab || [];
        if (langCode) rows = rows.filter(v => (v.lang_code || '').toLowerCase() === langCode.toLowerCase());
        if (registerType) rows = rows.filter(v => (v.register_type || '').toUpperCase() === registerType.toUpperCase());
        return { vocab: rows, false_friend_alerts: st.vocabFalseFriendAlerts || [], offlineShardMode: true };
      }
    },

    async fetchSongs(registerId = '', langCode = '') {
      try {
        const qs = new URLSearchParams();
        if (registerId) qs.set('register_id', registerId);
        if (langCode) qs.set('lang_code', langCode);
        const suffix = qs.toString() ? `?${qs.toString()}` : '';
        return await requestJson(`/api/v1/songs${suffix}`, { method: 'GET' }, 4500);
      } catch (_) {
        const st = await assembleOfflineStateFromShards(false);
        let songs = st.songs || [];
        if (registerId) songs = songs.filter(s => s.register_id === registerId);
        if (langCode) songs = songs.filter(s => (s.original_lang || '').toLowerCase().includes(langCode.toLowerCase()));
        return { songs, count: songs.length, offlineShardMode: true };
      }
    },

    async fetchSongFrequency(songUid = 'SONG_CZ_OVA_NOHAVICA', forceRefresh = false) {
      const cacheKey = String(songUid || '').trim().toLowerCase();
      if (!forceRefresh && frequencyResponseCache.has(cacheKey)) {
        return frequencyResponseCache.get(cacheKey);
      }
      try {
        const res = await requestJson(`/api/v1/songs/${encodeURIComponent(songUid)}/frequency`, { method: 'GET' }, 5000);
        if (res && Array.isArray(res.lyric_tokens)) {
          frequencyResponseCache.set(cacheKey, res);
        }
        return res;
      } catch (_) {
        const st = await assembleOfflineStateFromShards(false);
        const sMeta = (st.songs || []).find(item => item.uid === songUid) || (st.songs || [])[0] || {};
        let shard = null;
        try {
          shard = await fetchLocalLyricShard(sMeta.lyric_shard || sMeta.uid || songUid);
        } catch (__) {
          shard = null;
        }
        const mergedSong = { ...sMeta, ...(shard || {}) };
        const tokens = mergedSong.lyric_tokens || [];
        const payload = {
          song: mergedSong,
          lyric_tokens: tokens,
          graph_summary: {
            connected_vocab_count: new Set(tokens.map(t => t.vocab_uid).filter(Boolean)).size,
            connected_idiom_count: new Set(tokens.map(t => t.idiom_term).filter(Boolean)).size,
            connected_card_count: new Set(tokens.flatMap(t => t.connected_card_uids || [])).size
          },
          offlineShardMode: true
        };
        frequencyResponseCache.set(cacheKey, payload);
        return payload;
      }
    },

    async fetchLocalLyricShard(songUidOrPath) {
      return await fetchLocalLyricShard(songUidOrPath);
    },

    clearLyricShardCache(songUid = '') {
      clearLyricShardCache(songUid);
    },

    async fetchFrequencyLeaderboard(registerId = '', limit = 25) {
      try {
        const qs = new URLSearchParams();
        if (registerId) qs.set('register_id', registerId);
        if (limit) qs.set('limit', String(limit));
        const suffix = qs.toString() ? `?${qs.toString()}` : '';
        return await requestJson(`/api/v1/frequency/leaderboard${suffix}`, { method: 'GET' }, 5000);
      } catch (_) {
        const st = await assembleOfflineStateFromShards(false);
        const songList = st.songs || [];
        const hydratedSongs = await Promise.all(
          songList.map(async s => {
            if (Array.isArray(s.lyric_tokens) && s.lyric_tokens.length > 0) return s;
            try {
              const shard = await fetchLocalLyricShard(s.lyric_shard || s.uid);
              return { ...s, ...shard };
            } catch (__) {
              return s;
            }
          })
        );
        const tokens = [];
        hydratedSongs.forEach(s => {
          (s.lyric_tokens || []).forEach(lt => {
            if (!registerId || lt.register_id === registerId) {
              tokens.push({ ...lt, song_title: s.title, song_artist: s.artist });
            }
          });
        });
        tokens.sort((a, b) => (b.frequency_score - a.frequency_score) || (b.total_frequency - a.total_frequency));
        return { register_id: registerId || 'ALL', count: tokens.slice(0, limit).length, tokens: tokens.slice(0, limit), offlineShardMode: true };
      }
    },

    async reachAndIndexSongs(useAgentReach = true) {
      const res = await requestJson(
        `/api/v1/songs/reach-index?use_agent_reach=${useAgentReach ? 'true' : 'false'}`,
        { method: 'POST' },
        25000
      );
      clearLyricShardCache();
      return res;
    },

    async scaffoldPhrase(arg1 = {}, targetRegisterArg = 'CZ_OVA', anchorLangsArg = ['DE', 'RU', 'EN']) {
      let body;
      if (typeof arg1 === 'string') {
        body = {
          card_uid: null,
          text: arg1,
          target_register: targetRegisterArg,
          anchor_langs: (anchorLangsArg || ['DE', 'RU', 'EN']).map(s => String(s).toUpperCase())
        };
      } else {
        body = {
          card_uid: arg1.cardUid || arg1.card_uid || null,
          text: arg1.text || arg1.phrase || null,
          target_register: arg1.targetRegister || arg1.target_register || 'CZ_OVA',
          anchor_langs: (arg1.anchorLangs || arg1.anchor_langs || ['DE', 'RU', 'EN']).map(s => String(s).toUpperCase())
        };
      }
      return await requestJson(
        '/api/v1/bridges/scaffold',
        {
          method: 'POST',
          body: JSON.stringify(body)
        },
        15000
      );
    },

    async findBridgePath(fromRegister, toRegister, stage = 'CHAMELEON', arena = '') {
      const qs = new URLSearchParams({
        from_register: fromRegister,
        to_register: toRegister,
        stage
      });
      if (arena) qs.set('arena', arena);
      return await requestJson(`/api/v1/bridges/path?${qs.toString()}`, { method: 'GET' }, 10000);
    },

    async resolveConverse(opts = {}) {
      const registerId = opts.registerId || opts.register_id || 'CZ_OVA';
      const arena = opts.arena || 'terrace';
      const stage = opts.stage || 'COUNTERACT';
      const lensId = opts.lensId || opts.lens_id || 'DEADPAN';
      const anchorLangs = opts.anchorLangs || opts.anchor_langs || ['DE', 'RU', 'EN'];
      const qs = new URLSearchParams({
        register_id: registerId,
        arena,
        stage,
        lens_id: lensId,
        anchor_langs: Array.isArray(anchorLangs) ? anchorLangs.join(',') : String(anchorLangs)
      });
      return await requestJson(`/api/v1/converse/resolve?${qs.toString()}`, { method: 'GET' }, 10000);
    },

    async stylizeThought(opts = {}) {
      const body = {
        thought: opts.thought || opts.raw_thought || '',
        target_register: opts.targetRegister || opts.target_register || opts.register_id || 'CZ_OVA',
        arena: opts.arena || 'terrace',
        stage: opts.stage || 'COUNTERACT',
        lens_id: opts.lensId || opts.lens_id || 'FERGUSON',
        model: opts.model || null,
        fast_mode: Boolean(opts.fastMode || opts.fast_mode || (opts.model && String(opts.model).includes('4b'))),
        commit_mode: opts.commitMode || opts.commit_mode || 'stage',
        counters_state: opts.countersState || opts.counters_state || null
      };
      return await requestJson(
        '/api/v1/converse/stylize',
        {
          method: 'POST',
          body: JSON.stringify(body)
        },
        90000
      );
    },

    async gradeTransition(edgeId, score, sourceUid = null, targetUid = null) {
      const payload = {
        edge_id: edgeId,
        score: Number(score),
        source_uid: sourceUid,
        target_uid: targetUid
      };
      try {
        const res = await requestJson(
          '/api/v1/fsrs/grade',
          {
            method: 'POST',
            body: JSON.stringify(payload)
          },
          5000
        );
        api.isOnline = true;
        return res;
      } catch (err) {
        api.isOnline = false;
        const entry = enqueueOutboxEvent('grade', payload);
        return {
          ok: true,
          queued_offline: true,
          event_id: entry.id,
          outbox_count: getOutboxEvents().length,
          edge_id: edgeId,
          score: Number(score)
        };
      }
    },

    async gradeEdge(edgeId, score, sourceUid = null, targetUid = null) {
      return await api.gradeTransition(edgeId, score, sourceUid, targetUid);
    },

    async commitNode(payload = {}) {
      const normalized = {
        uid: payload.uid || null,
        register_id: payload.register_id || payload.registerId || 'CZ_OVA',
        stage: payload.stage || 'COUNTERACT',
        arena: normalizeArenaId(payload.arena),
        lens_id: payload.lens_id || payload.lensId || null,
        text: payload.text || payload.text_html || '',
        idiom_term: payload.idiom_term || payload.idiomTerm || null,
        idiom_origin: payload.idiom_origin || 'Atelier Workbench Addition',
        idiom_meaning: payload.idiom_meaning || 'High-rapport regional marker',
        delivery_cue: payload.delivery_cue || payload.idiom_delivery || 'Grounded peer inflection',
        cousin_term: payload.cousin_term || payload.idiom_cousin || null,
        connect_from_uid: payload.connect_from_uid || null,
        counters_state: payload.counters_state || null,
        phonetics: payload.phonetics || '',
        english_gloss: payload.english_gloss || ''
      };
      try {
        const res = await requestJson(
          '/api/v1/nodes/commit',
          {
            method: 'POST',
            body: JSON.stringify(normalized)
          },
          10000
        );
        api.isOnline = true;
        return res;
      } catch (err) {
        api.isOnline = false;
        const entry = enqueueOutboxEvent('commit_node', normalized);
        return {
          ok: true,
          queued_offline: true,
          event_id: entry.id,
          outbox_count: getOutboxEvents().length,
          card: normalized
        };
      }
    },

    async approveWebhook(webhookId) {
      return await requestJson(
        `/api/v1/webhooks/${encodeURIComponent(webhookId)}/approve`,
        { method: 'POST' },
        15000
      );
    }
  };

  // =========================================================================
  // ADAPTIVE EMBEDDED MODE DETECTION (Slim Chrome Inside index.html)
  // =========================================================================
  const isEmbeddedFrame = (() => {
    try {
      return (global.self !== global.top) || /[?&]embed=1/.test(String(global.location?.search || ''));
    } catch (_) {
      return true;
    }
  })();

  const injectGlobalMobileCleanCss = () => {
    if (!global.document || global.document.getElementById('polyglot-mobile-clean-css')) return;
    const st = global.document.createElement('style');
    st.id = 'polyglot-mobile-clean-css';
    st.textContent = `
      html, body { overflow-x: clip; max-width: 100%; -webkit-overflow-scrolling: touch; }
      .no-scrollbar::-webkit-scrollbar { display: none; }
      .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
      @media (max-width: 640px) {
        html.polyglot-embedded .embed-compact-main { padding-left: 0.65rem !important; padding-right: 0.65rem !important; padding-bottom: 1.5rem !important; }
        button:not(.dial-carousel-item):not([class*="w-[18px]"]):not([data-lyric-token]):not(#hub-backend-pill) { min-height: 32px; }
      }
    `;
    (global.document.head || global.document.documentElement).appendChild(st);
  };
  if (global.document) {
    injectGlobalMobileCleanCss();
    if (global.document.readyState === 'loading') {
      global.document.addEventListener('DOMContentLoaded', injectGlobalMobileCleanCss, { once: true });
    }
  }

  if (isEmbeddedFrame && global.document && global.document.documentElement) {
    global.document.documentElement.classList.add('polyglot-embedded');
    const injectEmbeddedCss = () => {
      if (global.document.getElementById('polyglot-embedded-css')) return;
      const st = global.document.createElement('style');
      st.id = 'polyglot-embedded-css';
      st.textContent = `
        html.polyglot-embedded [data-embed-hide="true"] { display: none !important; }
        html.polyglot-embedded .embed-compact-main { padding-top: 0.75rem !important; padding-bottom: 1rem !important; }
        html.polyglot-embedded .embed-no-sticky-brand { padding-top: 0.35rem !important; padding-bottom: 0.35rem !important; }
      `;
      (global.document.head || global.document.documentElement).appendChild(st);
    };
    injectEmbeddedCss();
    if (global.document.readyState === 'loading') {
      global.document.addEventListener('DOMContentLoaded', injectEmbeddedCss, { once: true });
    }
  }

  // =========================================================================
  // CROSS-APP GLOBAL CONTEXT SYNC BUS (PolyglotSyncBus)
  // Keeps active Culture (CZ_OVA, AT_VIE, RU_ALA, EN_YYC, ES_SOT), Arena, and
  // deep-link handoffs synchronized across index.html and all 6 Studio views.
  // =========================================================================
  const LAST_APP_STORAGE_KEY = 'polyglot_suite_last_app_v36';
  let isApplyingRemoteContext = false;
  let bcChannel = null;
  try {
    if (typeof global.BroadcastChannel === 'function') {
      bcChannel = new global.BroadcastChannel('polyglot_sync_bus_v34');
    }
  } catch (_) {}

  function getSavedContext() {
    try {
      const raw = global.localStorage && global.localStorage.getItem(CONTEXT_STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        const c = normalizeCulture(parsed.registerId || parsed.langCode);
        return {
          ...c,
          arena: parsed.arena || 'terrace',
          subview: parsed.subview || null,
          updatedAt: parsed.updatedAt || 0
        };
      }
    } catch (_) {}
    return { ...CULTURE_META.CZ_OVA, arena: 'terrace', subview: null, updatedAt: 0 };
  }

  function broadcastContext(partial = {}) {
    if (isApplyingRemoteContext) return getSavedContext();
    const prev = getSavedContext();
    const culture = partial.culture
      ? normalizeCulture(partial.culture)
      : normalizeCulture(partial.registerId || partial.langCode || prev.registerId);
    const nextCtx = {
      ...culture,
      arena: partial.arena ? String(partial.arena).toLowerCase() : (prev.arena || 'terrace'),
      subview: partial.subview !== undefined ? partial.subview : null,
      updatedAt: Date.now()
    };

    try {
      if (global.localStorage) {
        global.localStorage.setItem(CONTEXT_STORAGE_KEY, JSON.stringify(nextCtx));
      }
    } catch (_) {}

    const msg = { type: 'POLYGLOT_CONTEXT_SYNC', context: nextCtx };
    try {
      if (bcChannel) bcChannel.postMessage(msg);
    } catch (_) {}
    try {
      if (global.parent && global.parent !== global) {
        global.parent.postMessage(msg, '*');
      }
    } catch (_) {}
    try {
      const frame = global.document && global.document.getElementById('suite-frame');
      if (frame && frame.contentWindow) {
        frame.contentWindow.postMessage(msg, '*');
      }
    } catch (_) {}
    try {
      if (typeof global.dispatchEvent === 'function') {
        global.dispatchEvent(new CustomEvent('polyglot:context-changed', { detail: nextCtx }));
      }
    } catch (_) {}

    return nextCtx;
  }

  function navigateApp(appUrl, opts = {}) {
    if (!appUrl) return;
    const nextCtx = broadcastContext({
      registerId: opts.registerId,
      langCode: opts.langCode,
      culture: opts.culture,
      arena: opts.arena,
      subview: opts.subview || null
    });
    try {
      if (global.localStorage) {
        global.localStorage.setItem(LAST_APP_STORAGE_KEY, appUrl);
      }
    } catch (_) {}
    if (isEmbeddedFrame && global.parent && global.parent !== global) {
      try {
        global.parent.postMessage({
          type: 'POLYGLOT_NAVIGATE_APP',
          appUrl,
          context: nextCtx
        }, '*');
        return;
      } catch (_) {}
    }
    if (typeof global.loadApp === 'function') {
      global.loadApp(appUrl, nextCtx);
    } else if (global.location) {
      global.location.href = appUrl;
    }
  }

  function applyContextToCurrentPage(ctx) {
    if (!ctx || !global.document) return;
    const c = normalizeCulture(ctx.registerId || ctx.langCode);
    isApplyingRemoteContext = true;
    try {
      // 1. Atelier v3.1, SRS Heatmap v3.0, or Lounge v1.0 (selectPersona)
      if (typeof global.selectPersona === 'function') {
        if (global.PERSONAS && global.PERSONAS[c.lowerKey]) {
          global.selectPersona(c.lowerKey);
        } else {
          global.selectPersona(c.registerId);
        }
      }
      // 2. Audio-Rhythm Studio v4.5 (loadPersona + selectV45Anthem)
      if (typeof global.loadPersona === 'function') {
        global.loadPersona(c.registerId);
      }
      if (typeof global.selectV45Anthem === 'function') {
        global.selectV45Anthem(c.anthemIdx);
      }
      // 3. Regional Lyric Flashcards (selectTrack)
      if (typeof global.selectTrack === 'function') {
        global.selectTrack(c.anthemIdx);
      }
      // 4. 5-Lang Register Switcher (Alpine x-data component)
      const alpineRoot = global.document.querySelector('[x-data]');
      if (alpineRoot && alpineRoot._x_dataStack && alpineRoot._x_dataStack[0]) {
        const scope = alpineRoot._x_dataStack[0];
        if (typeof scope.selectLang === 'function' && scope.activeLang !== c.langCode) {
          scope.selectLang(c.langCode);
        }
      }
      // 5. Sync active 8-Arena room when supported
      if (ctx.arena) {
        if (typeof global.changeArena === 'function') {
          global.changeArena(ctx.arena);
        } else if (typeof global.selectArena === 'function') {
          global.selectArena(ctx.arena);
        }
      }
      // 6. Optional cross-app subview deep-link (only when explicitly passed)
      if (ctx.subview) {
        if (typeof global.switchMode === 'function') {
          global.switchMode(ctx.subview);
        } else if (typeof global.switchView === 'function') {
          global.switchView(ctx.subview);
        } else if (typeof global.setStudioMode === 'function') {
          global.setStudioMode(ctx.subview);
        }
      }
    } catch (_) {
    } finally {
      setTimeout(() => { isApplyingRemoteContext = false; }, 60);
    }
  }

  function autoBindPageFunctions() {
    if (!global.window || !global.document) return;

    // Hook selectPersona (Atelier v3.1, SRS v3.0, Lounge v1.0)
    if (typeof global.selectPersona === 'function' && !global.selectPersona._polyglotHooked) {
      const orig = global.selectPersona;
      const wrapped = function (id, ...rest) {
        const res = orig.apply(this, [id, ...rest]);
        broadcastContext({ culture: id });
        return res;
      };
      wrapped._polyglotHooked = true;
      global.selectPersona = wrapped;
    }

    // Hook loadPersona (Audio-Rhythm Studio v4.5)
    if (typeof global.loadPersona === 'function' && !global.loadPersona._polyglotHooked) {
      const orig = global.loadPersona;
      const wrapped = function (id, ...rest) {
        const res = orig.apply(this, [id, ...rest]);
        if (id && String(id).toUpperCase() !== 'WEEKND') {
          broadcastContext({ culture: id });
        }
        return res;
      };
      wrapped._polyglotHooked = true;
      global.loadPersona = wrapped;
    }

    // Hook selectTrack (Regional Lyric Flashcards)
    if (typeof global.selectTrack === 'function' && !global.selectTrack._polyglotHooked) {
      const orig = global.selectTrack;
      const idxMap = ['CZ_OVA', 'AT_VIE', 'RU_ALA', 'EN_YYC', 'ES_SOT'];
      const wrapped = function (idx, ...rest) {
        const res = orig.apply(this, [idx, ...rest]);
        if (idxMap[idx]) {
          broadcastContext({ culture: idxMap[idx] });
        }
        return res;
      };
      wrapped._polyglotHooked = true;
      global.selectTrack = wrapped;
    }

    // Hook selectV45Anthem (Audio-Rhythm Studio v4.5)
    if (typeof global.selectV45Anthem === 'function' && !global.selectV45Anthem._polyglotHooked) {
      const orig = global.selectV45Anthem;
      const idxMap = ['CZ_OVA', 'AT_VIE', 'RU_ALA', 'EN_YYC', 'ES_SOT'];
      const wrapped = function (idx, ...rest) {
        const res = orig.apply(this, [idx, ...rest]);
        if (idxMap[idx]) {
          broadcastContext({ culture: idxMap[idx] });
        }
        return res;
      };
      wrapped._polyglotHooked = true;
      global.selectV45Anthem = wrapped;
    }

    // Hook Alpine selectLang (5-Lang Register Switcher)
    const alpineRoot = global.document.querySelector('[x-data]');
    if (alpineRoot && alpineRoot._x_dataStack && alpineRoot._x_dataStack[0]) {
      const scope = alpineRoot._x_dataStack[0];
      if (typeof scope.selectLang === 'function' && !scope.selectLang._polyglotHooked) {
        const orig = scope.selectLang.bind(scope);
        const wrapped = async function (code, ...rest) {
          const res = await orig(code, ...rest);
          broadcastContext({ culture: code });
          return res;
        };
        wrapped._polyglotHooked = true;
        scope.selectLang = wrapped;
      }
    }

    // Hook changeArena / selectArena so 8-Arena room stays synced across Atelier & Lounge
    if (typeof global.changeArena === 'function' && !global.changeArena._polyglotHooked) {
      const orig = global.changeArena;
      const wrapped = function (arenaId, ...rest) {
        const res = orig.apply(this, [arenaId, ...rest]);
        if (arenaId) broadcastContext({ arena: arenaId });
        return res;
      };
      wrapped._polyglotHooked = true;
      global.changeArena = wrapped;
    }
    if (typeof global.selectArena === 'function' && !global.selectArena._polyglotHooked) {
      const orig = global.selectArena;
      const wrapped = function (arenaId, ...rest) {
        const res = orig.apply(this, [arenaId, ...rest]);
        if (arenaId) broadcastContext({ arena: arenaId });
        return res;
      };
      wrapped._polyglotHooked = true;
      global.selectArena = wrapped;
    }

    // Apply initial context stored across tabs
    const initialCtx = getSavedContext();
    if (initialCtx && initialCtx.updatedAt > 0) {
      applyContextToCurrentPage(initialCtx);
    }
  }

  if (global.window) {
    global.window.addEventListener('message', (e) => {
      if (e && e.data && e.data.type === 'POLYGLOT_CONTEXT_SYNC' && e.data.context) {
        applyContextToCurrentPage(e.data.context);
        if (typeof global.dispatchEvent === 'function') {
          global.dispatchEvent(new CustomEvent('polyglot:context-changed', { detail: e.data.context }));
        }
      }
    });

    if (bcChannel) {
      bcChannel.onmessage = (e) => {
        if (e && e.data && e.data.type === 'POLYGLOT_CONTEXT_SYNC' && e.data.context) {
          applyContextToCurrentPage(e.data.context);
          if (typeof global.dispatchEvent === 'function') {
            global.dispatchEvent(new CustomEvent('polyglot:context-changed', { detail: e.data.context }));
          }
        }
      };
    }

    global.window.addEventListener('DOMContentLoaded', () => {
      setTimeout(autoBindPageFunctions, 120);
      setTimeout(autoBindPageFunctions, 550);
    });
  }

  // =========================================================================
  // MOBILE-WEB ERGONOMICS HELPER (WebAudio Auto-Unlock, Touch Swipe, Haptics)
  // =========================================================================
  let audioUnlocked = false;
  function unlockWebAudioOnce() {
    if (audioUnlocked) return;
    try {
      if (global.Tone && typeof global.Tone.start === 'function') {
        global.Tone.start().then(() => { audioUnlocked = true; }).catch(() => {});
      } else {
        audioUnlocked = true;
      }
    } catch (_) {}
  }

  if (global.window && global.document) {
    ['pointerdown', 'touchend', 'keydown'].forEach(evName => {
      global.window.addEventListener(evName, unlockWebAudioOnce, { passive: true, once: false });
    });
  }

  const mobileHelper = {
    haptic(ms = 12) {
      try {
        if (global.navigator && typeof global.navigator.vibrate === 'function') {
          global.navigator.vibrate(ms);
        }
      } catch (_) {}
    },

    attachSwipe(element, { onSwipeLeft, onSwipeRight, threshold = 48 } = {}) {
      if (!element) return;
      let startX = 0;
      let startY = 0;
      let tracking = false;

      element.addEventListener('touchstart', (e) => {
        if (!e.touches || e.touches.length !== 1) return;
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        tracking = true;
      }, { passive: true });

      element.addEventListener('touchend', (e) => {
        if (!tracking || !e.changedTouches || e.changedTouches.length === 0) return;
        tracking = false;
        const dx = e.changedTouches[0].clientX - startX;
        const dy = e.changedTouches[0].clientY - startY;
        if (Math.abs(dx) >= threshold && Math.abs(dx) > Math.abs(dy) * 1.35) {
          mobileHelper.haptic(10);
          if (dx < 0 && typeof onSwipeLeft === 'function') onSwipeLeft();
          if (dx > 0 && typeof onSwipeRight === 'function') onSwipeRight();
        }
      }, { passive: true });
    }
  };

  global.PolyglotAPI = api;
  global.PolyglotMobile = mobileHelper;
  global.PolyglotSyncBus = {
    CULTURE_META,
    LAST_APP_STORAGE_KEY,
    isEmbedded: isEmbeddedFrame,
    normalizeCulture,
    getContext: getSavedContext,
    setContext: broadcastContext,
    applyContext: applyContextToCurrentPage,
    navigateApp
  };
})(window);
