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
    CZ_OVA: { registerId: 'CZ_OVA', formalId: 'CZ_STD', lowerKey: 'cz_ova', langCode: 'cs', shortCode: 'CZ', flag: '🇨🇿', city: 'Ostrava', anthemIdx: 0 },
    AT_VIE: { registerId: 'AT_VIE', formalId: 'DE_STD', lowerKey: 'at_vie', langCode: 'de', shortCode: 'AT', flag: '🇦🇹', city: 'Vienna', anthemIdx: 1 },
    RU_ALA: { registerId: 'RU_ALA', formalId: 'RU_STD', lowerKey: 'ru_ala', langCode: 'ru', shortCode: 'KZ', flag: '🇰🇿', city: 'Almaty', anthemIdx: 2 },
    EN_YYC: { registerId: 'EN_YYC', formalId: 'EN_STD', lowerKey: 'en_yyc', langCode: 'en', shortCode: 'CA', flag: '🇨🇦', city: 'Calgary', anthemIdx: 3 },
    ES_SOT: { registerId: 'ES_SOT', formalId: 'ES_STD', lowerKey: 'es_sot', langCode: 'es', shortCode: 'ES', flag: '🇪🇸', city: 'Sotogrande', anthemIdx: 4 }
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
  async function fetchLocalShardJson(filename) {
    const resp = await fetch(`./db/${filename}`);
    if (!resp.ok) throw new Error(`Shard ${filename} HTTP ${resp.status}`);
    return await resp.json();
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
    const formalRegister = st.allRegisters[meta.formalId] || {};
    const regionalRegister = st.allRegisters[meta.registerId] || {};
    const formalCards = st.allCards
      .filter(c => c.lang === meta.formalId && c.arena === 'terrace')
      .map(c => ({
        uid: c.uid,
        stage: c.stage,
        title: c.title || c.stage,
        text_html: c.text,
        phonetics: c.phonetics,
        english_gloss: c.english,
        idiom_terms: c.idioms
      }));
    const regionalCards = st.allCards
      .filter(c => c.lang === meta.registerId && c.arena === 'terrace' && !c.lens_id)
      .map(c => ({
        uid: c.uid,
        stage: c.stage,
        title: c.title || c.stage,
        text_html: c.text,
        phonetics: c.phonetics,
        english_gloss: c.english,
        idiom_terms: c.idioms
      }));
    const bridges = (st.bridges || []).filter(
      b => b.from_register === meta.formalId || b.to_register === meta.registerId
    );
    return {
      lang_code: meta.langCode,
      formal_register: formalRegister,
      regional_register: regionalRegister,
      formal_cards: formalCards,
      regional_cards: regionalCards,
      bridges,
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
  // CROSS-APP GLOBAL CONTEXT SYNC BUS (PolyglotSyncBus)
  // Keeps active Culture (CZ_OVA, AT_VIE, RU_ALA, EN_YYC, ES_SOT) and Arena
  // synchronized across index.html and all 6 Studio iframes/tabs.
  // =========================================================================
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
          updatedAt: parsed.updatedAt || 0
        };
      }
    } catch (_) {}
    return { ...CULTURE_META.CZ_OVA, arena: 'terrace', updatedAt: 0 };
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
    } catch (_) {
    } finally {
      setTimeout(() => { isApplyingRemoteContext = false; }, 50);
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
    normalizeCulture,
    getContext: getSavedContext,
    setContext: broadcastContext,
    applyContext: applyContextToCurrentPage
  };
})(window);
