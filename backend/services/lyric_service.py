from __future__ import annotations

import asyncio
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Optional

import httpx

from backend.db.neo4j_client import neo4j_manager
from backend.db.postgres import pg_manager
from backend.validators.graph_rules import strip_html_tags

AGENT_REACH_EXE = Path(r"C:\Users\iamab\.agent-reach-venv\Scripts\agent-reach.exe")

# Regional discourse particles and dialect anchors to never drop as stop-words
REGIONAL_ANCHOR_TOKENS = {
    "bo",
    "kaj",
    "fachat",
    "šichta",
    "fajront",
    "ostrava",
    "ostravo",
    "oida",
    "schmäh",
    "eh",
    "halt",
    "ja",
    "mal",
    "wien",
    "vienna",
    "garderobe",
    "родной",
    "алматы",
    "медеу",
    "джулия",
    "джули",
    "красоте",
    "базару",
    "дастархан",
    "дастарханом",
    "душам",
    "bud",
    "weekend",
    "cattle",
    "mustang",
    "tío",
    "tio",
    "duende",
    "volando",
    "vengo",
    "sotogrande",
    "toros",
    "barrera",
    "candela",
    "tough",
    "loyal",
    "rovinu",
    "parou",
    "bledsinn",
    "anreißen",
    "pflanzerei",
    "беркут",
    "понтов",
    "garage",
    "muñeca",
    "mójate",
    "jugada",
    "postureo",
}

STOP_WORDS = {
    # Czech / Silesian function words
    "a", "i", "v", "ve", "s", "se", "si", "z", "ze", "k", "ke", "u", "o", "na", "do",
    "po", "od", "pro", "za", "mezi", "nad", "kam", "když", "že", "ten", "to", "ta",
    "je", "jsou", "jsem", "jsi", "byl", "byla", "aby", "ale", "jen", "jenom", "jak",
    "tak", "teď", "při", "kdo", "co", "moje", "tvoje", "mě", "mít", "maju", "mají",
    "musí", "jiným", "všecku", "do", "od", "ní", "ně", "níž", "který",
    # German / Viennese function words
    "der", "die", "das", "ein", "eine", "einen", "einem", "einer", "und", "oder",
    "aber", "in", "im", "an", "am", "auf", "aus", "bei", "mit", "nach", "von", "vor",
    "zu", "zum", "zur", "für", "über", "unter", "ist", "sind", "war", "du", "ich",
    "sie", "es", "wir", "ihr", "ihm", "ihn", "dir", "mich", "dich", "sich", "da",
    "hier", "dort", "heute", "nun", "wie", "wo", "was", "wer", "nur", "kein", "keine",
    "nicht", "noch", "auch", "so", "wird", "kann", "musst", "alles", "den", "dem", "des",
    # Russian function words
    "и", "в", "во", "на", "с", "со", "к", "по", "о", "об", "от", "до", "из", "у", "за",
    "под", "над", "не", "ни", "но", "а", "что", "как", "кто", "где", "когда", "я", "ты",
    "он", "она", "мы", "вы", "они", "меня", "тебя", "мне", "тебе", "нас", "вас", "мой",
    "моя", "моё", "твой", "твоя", "твоё", "его", "её", "их", "это", "этот", "эта", "эти",
    "всё", "все", "бы", "же", "ли", "уже", "ещё", "разве", "если", "лишь", "чтобы",
    "буду", "есть", "быть", "может", "будет", "без", "при", "там", "тут", "вот", "для",
    # English function words
    "the", "a", "an", "and", "or", "but", "if", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "up", "out", "off", "over", "into", "is", "are", "was", "were",
    "be", "been", "being", "am", "i", "you", "he", "she", "it", "we", "they", "me", "him",
    "her", "us", "them", "my", "your", "his", "our", "their", "this", "that", "these",
    "those", "what", "who", "when", "where", "how", "will", "would", "can", "could",
    "just", "so", "not", "no", "all", "get", "got", "see", "oh", "im", "i'm", "you're",
    "everyone's", "everybody's", "you've",
    # Spanish function words
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero", "si", "en",
    "de", "del", "al", "a", "por", "para", "con", "sin", "sobre", "entre", "que", "quien",
    "como", "cuando", "donde", "yo", "tú", "tu", "él", "ella", "me", "te", "se", "nos",
    "lo", "le", "les", "mi", "mis", "su", "sus", "este", "esta", "esto", "ese", "esa",
    "es", "son", "ser", "estar", "ha", "hay", "va", "vamos", "porque", "más", "muy",
    "todo", "todos", "nunca", "algo", "mí", "ti", "pa", "pa'",
}

LEMMA_CONSOLIDATION = {
    "ostravo": ("ostrava", "ostrava", "Industrial Moravian city anchor & identity core"),
    "ostrava": ("ostrava", "ostrava", "Industrial Moravian city anchor & identity core"),
    "šichtu": ("šichta", "šichta", "Heavy mining/engineering shift or pointless manual grind"),
    "šichta": ("šichta", "šichta", "Heavy mining/engineering shift or pointless manual grind"),
    "šichty": ("šichta", "šichta", "Heavy mining/engineering shift or pointless manual grind"),
    "fajront": ("fajront", "fajront", "Clean quitting time once the engine runs by itself"),
    "fachat": ("fachat", "fachat", "Run reliably on all cylinders without babysitting"),
    "fachá": ("fachat", "fachat", "Run reliably on all cylinders without babysitting"),
    "bo": ("bo", "bo", 'Silesian causal connector ("because", never "or")'),
    "kaj": ("kaj", "kaj", 'Silesian spatial connector ("where")'),
    "hvězdo": ("hvězda", "hvězda", "Black industrial star / signature horizon motif"),
    "srdce": ("srdce", "srdce", "Red heart of Ostrava resilience"),
    "osude": ("osud", "osud", "Sealed industrial destiny & commitment"),
    "motor": ("motor", "motor", "Self-running system engine after setup"),
    "vienna": ("vienna", "vienna", "Metropolitan Viennese pulse & hook refrain"),
    "wien": ("wien", "wien", "Vienna inner-city irony & peer familiarity"),
    "calling": ("calling", "calling", "Urgent direct reach-out hook"),
    "stella": ("stella", "stella", "Cosmopolitan traveler motif (Rio / Tokyo)"),
    "oida": ("oida", "oida", "Iconic Viennese peer interjection (status equalizer)"),
    "schmäh": ("schmäh", "schmäh", "Charming Viennese irony & velvet wit"),
    "garderobe": ("garderobe", "an der Garderobe abgeben", "Checking stiff corporate caution at the coat check"),
    "abgeben": ("abgeben", "an der Garderobe abgeben", "Handing over caution at the coat check"),
    "g’schichtldrucken": ("g’schichtldrucken", "g’schichtldrucken", "Spinning corporate tall tales or hollow hype"),
    "g'schichtldrucken": ("g’schichtldrucken", "g’schichtldrucken", "Spinning corporate tall tales or hollow hype"),
    "eh": ("eh", "eh", "Austrian modal particle (anyway / inherently)"),
    "джули": ("джулия", "джулия", "Almaty romantic & nostalgic hook refrain"),
    "джулия": ("джулия", "джулия", "Almaty romantic & nostalgic hook refrain"),
    "алматы": ("алматы", "алматы", "Southern Capital warmth & direct hospitality"),
    "красоте": ("красота", "по красоте", "Built cleanly with soul, precision, and mastery"),
    "базару": ("базар", "базару нет", "Undeniably true — zero doubt"),
    "дастарханом": ("дастархан", "дастархан", "Generous table of high-trust partnership"),
    "дастархан": ("дастархан", "дастархан", "Generous table of high-trust partnership"),
    "родной": ("родной", "родной", "Kinship vocative dissolving formal walls"),
    "медеу": ("медеу", "медеу", "High-altitude Almaty ambition & scale"),
    "душам": ("душа", "по душам", "Heart-to-heart straight talk without masks"),
    "имя": ("имя", "имя", "Personal name & unforgettable connection motif"),
    "working": ("work", "working", "High-momentum execution before the reward"),
    "weekend": ("weekend", "weekend", "Release valve / celebration after clean execution"),
    "everybody": ("everybody", "everybody", "Crowd cadence chorus opener"),
    "everyone": ("everyone", "everyone", "Room-wide anticipation motif"),
    "cattle": ("cattle", "all hat and no cattle", "Real underlying traction vs empty talk"),
    "bud": ("bud", "bud", "Warm Canadian peer equalizing vocative"),
    "mustang": ("mustang", "69 mustang", "High-horsepower potential idle in the garage"),
    "give": ("give", "give ’er", "Commit at full throttle without hesitation"),
    "chance": ("chance", "chance", "Window for bold action right now"),
    "show": ("show", "show", "Stepping onto the main arena floor"),
    "volando": ("volar", "volando", "Moving effortlessly in full flow state"),
    "vengo": ("venir", "vengo", "Natural back-and-forth momentum"),
    "camino": ("camino", "camino", "Enjoying the journey & shared rapport"),
    "entretengo": ("entretener", "entretengo", "Keeping the exchange playfully alive"),
    "enamorao": ("enamorado", "enamorao", "Andaluz dropped-d passion for life & craft"),
    "vida": ("vida", "vida", "Living energy & vitality even under edge"),
    "duende": ("duende", "duende", "Unmanufacturable soul & spine-tingling charisma"),
    "toros": ("toro", "mirar los toros desde la barrera", "Stepping into the ring rather than watching"),
    "barrera": ("barrera", "mirar los toros desde la barrera", "Sidelines safety vs active arena play"),
    "tío": ("tío", "tío", "Conspiratorial Spanish peer vocative"),
    "sotogrande": ("sotogrande", "sotogrande", "Polo & coastal high-society candor hub"),
    "candela": ("candela", "candela", "Searching for fire & spark when things feel cold"),
    "tough": ("tough", "tough love", "Uncompromising intensity without corporate gloss"),
    "love": ("love", "love", "High-stakes emotional pull & devotion"),
    "breath": ("breath", "no breath", "Breathless nocturnal pace & edge"),
    "world": ("world", "world", "High-stakes ownership & total commitment"),
    "control": ("control", "control", "Velvet power dynamic & tension"),
    "loyal": ("loyal", "loyal", "Unspoken allegiance beneath surface poise"),
    "girls": ("girls", "one of your girls", "Iconic chorus hook of One of the Girls"),
    "tonight": ("tonight", "tonight", "Nocturnal high-stakes immediacy"),
    "secret": ("secret", "secret", "Shared nocturnal confidence & unspoken bond"),
    "rovinu": ("na rovinu", "na rovinu", "Straight talk without corporate spin (CZ_OVA Curiosity hook)"),
    "parou": ("s plnou parou", "s plnou parou", "Full steam ahead once brakes come off (CZ_OVA Curiosity)"),
    "bledsinn": ("bledsinn", "bledsinn", "Playful Viennese mischief / bold next adventure (AT_VIE Curiosity)"),
    "anreißen": ("anreißen", "anreißen", "Kick off / spark something bold together (AT_VIE Curiosity)"),
    "pflanzerei": ("pflanzerei", "pflanzerei", "Viennese teasing / hollow posturing (AT_VIE Chameleon)"),
    "беркут": ("горный беркут в золотой клетке", "горный беркут в золотой клетке", "Golden eagle caged by hesitation (RU_ALA Counteract)"),
    "понтов": ("без лишних понтов", "без лишних понтов", "Zero show-off posture, pure substance (RU_ALA Chameleon)"),
    "garage": ("garage", "garage", "Kick the garage doors open & ship (EN_YYC Counteract/Curiosity)"),
    "muñeca": ("tener buena muñeca", "tener buena muñeca", "Effortless wrist finesse & polo poise (ES_SOT Chameleon)"),
    "mójate": ("mójate un poco", "mójate un poco", "Get some skin in the game with me (ES_SOT Curiosity)"),
    "jugada": ("jugada", "jugada", "The bold play your gut actually wants (ES_SOT Curiosity)"),
    "postureo": ("postureo", "sin postureo", "Zero social pretense or artificial posing (ES_SOT Chameleon)"),
}


def _slugify(text: str) -> str:
    norm = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(ch for ch in norm if not unicodedata.combining(ch))
    cleaned = re.sub(r"[^a-zA-Z0-9\u0400-\u04FF]+", "_", ascii_only).strip("_").upper()
    if not cleaned:
        import hashlib
        return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10].upper()
    if len(cleaned) > 36:
        import hashlib
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:6].upper()
        return f"{cleaned[:29]}_{digest}"
    return cleaned


def _tokenize_words(text: str) -> list[str]:
    if not text:
        return []
    return re.findall(r"[^\W\d_]+(?:[’'][^\W\d_]+)?", text.lower(), flags=re.UNICODE)


class LyricFrequencyService:
    """Agent-Reach Lyric Fetcher, Frequency Indexer, and Neo4j Graph Connector."""

    async def get_agent_reach_health(self) -> dict[str, Any]:
        """Run agent-reach doctor once to verify channel availability without spawning parallel subprocesses."""
        available = AGENT_REACH_EXE.exists()
        doctor_summary: dict[str, Any] = {}
        if available:
            proc = None
            try:
                proc = await asyncio.create_subprocess_exec(
                    str(AGENT_REACH_EXE),
                    "doctor",
                    "--json",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout_b, _ = await asyncio.wait_for(proc.communicate(), timeout=8.0)
                raw = stdout_b.decode("utf-8", errors="ignore").strip()
                if raw.startswith("{") or raw.startswith("["):
                    doctor_summary = json.loads(raw)
            except Exception as exc:
                if proc is not None and proc.returncode is None:
                    try:
                        proc.kill()
                        await proc.wait()
                    except Exception:
                        pass
                doctor_summary = {"note": f"agent-reach doctor probe skipped: {exc}"}
        return {
            "agent_reach_installed": available,
            "executable": str(AGENT_REACH_EXE) if available else None,
            "channel": "agent-reach+jina+canonical_seed",
            "doctor_summary": doctor_summary,
        }

    async def probe_agent_reach(
        self,
        url: Optional[str] = None,
        doctor_info: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Fetch public lyric reference via Jina Reader while strictly skipping anti-bot/CAPTCHA gates."""
        health = doctor_info if doctor_info is not None else await self.get_agent_reach_health()
        fetched_excerpt = ""
        fetched_ok = False
        gated_by_challenge = False
        if url:
            try:
                async with httpx.AsyncClient(timeout=4.0, follow_redirects=True) as client:
                    resp = await client.get(
                        f"https://r.jina.ai/{url}",
                        headers={"User-Agent": "agent-reach/1.0 PolyglotRiffAtelier/3.5"},
                    )
                    if resp.status_code == 200 and resp.text.strip():
                        txt = resp.text.strip()
                        low = txt.lower()
                        if any(
                            marker in low
                            for marker in ("captcha", "nejsi robot", "not a robot", "just a moment", "503 error")
                        ):
                            gated_by_challenge = True
                        else:
                            fetched_ok = True
                            fetched_excerpt = txt[:320]
            except Exception:
                fetched_ok = False

        return {
            **health,
            "url": url,
            "live_web_fetched": fetched_ok,
            "challenge_gated_skipped": gated_by_challenge,
            "fetched_excerpt": fetched_excerpt,
        }

    async def index_all_songs(self, use_agent_reach: bool = False) -> dict[str, Any]:
        """Tokenize & index full song lyrics across PostgreSQL cards/vocab/idioms and mark PENDING for Neo4j sync."""
        songs = await pg_manager.fetch_all("SELECT * FROM songs ORDER BY uid")
        registers = await pg_manager.fetch_all("SELECT id, lang_code FROM registers")
        reg_to_lang = {r["id"]: r["lang_code"] for r in registers}

        vocab_rows = await pg_manager.fetch_all("SELECT uid, term, lang_code, meaning FROM vocab_items")
        vocab_by_uid = {v["uid"]: v for v in vocab_rows}
        idiom_rows = await pg_manager.fetch_all("SELECT term, register_id, meaning FROM idioms")
        idiom_by_lower = {i["term"].lower(): i for i in idiom_rows}
        card_rows = await pg_manager.fetch_all(
            "SELECT uid, register_id, text_plain, idiom_terms FROM cards"
        )

        reach_reports: list[dict[str, Any]] = []
        if use_agent_reach and songs:
            doctor_info = await self.get_agent_reach_health()
            probe_tasks = [
                self.probe_agent_reach(s.get("source_url") or None, doctor_info=doctor_info)
                for s in songs
            ]
            reach_reports = list(await asyncio.gather(*probe_tasks))

        total_tokens_written = 0
        per_song_summary: list[dict[str, Any]] = []

        pool = await pg_manager.get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                for song in songs:
                    reg_id = song["register_id"] or "EN_YYC"
                    lang_code = reg_to_lang.get(reg_id, "en")
                    stanzas = list(song.get("lyric_stanzas") or [])
                    if not stanzas:
                        stanzas = [song.get("original_lyric") or ""]
                    full_text = song.get("full_lyrics") or "\n\n".join(stanzas)
                    chorus_text = (
                        "\n".join(stanzas[2:])
                        if len(stanzas) > 4
                        else (stanzas[-1] if stanzas else (song.get("original_lyric") or ""))
                    )
                    pivot_text = song.get("pivot_line") or ""
                    combined_song_text = f"{full_text}\n{song.get('original_lyric') or ''}\n{pivot_text}"
                    combined_lower = combined_song_text.lower()
                    chorus_lower = f"{chorus_text}\n{song.get('original_lyric') or ''}".lower()

                    all_words = _tokenize_words(full_text)
                    total_word_count = len(all_words)
                    unique_word_count = len(set(all_words))

                    same_lang_cards = [
                        c for c in card_rows if reg_to_lang.get(c["register_id"]) == lang_code
                    ]

                    # Build candidate frequency entries
                    candidates: dict[str, dict[str, Any]] = {}

                    # 1. Index linked slang_vocab_uids & matching idioms
                    for vuid in list(song.get("slang_vocab_uids") or []):
                        voc = vocab_by_uid.get(vuid)
                        if not voc:
                            continue
                        base_phrase = re.sub(r"\s*\([^)]*\)", "", voc["term"]).strip().lower()
                        search_terms = [base_phrase]
                        # Handle key stem keywords for Slavonic/German/Spanish phrases
                        if "šicht" in base_phrase:
                            search_terms.append("šicht")
                        elif "fachat" in base_phrase:
                            search_terms.append("fach")
                        elif "schmäh" in base_phrase:
                            search_terms.append("schmäh")
                        elif "дастархан" in base_phrase:
                            search_terms.append("дастархан")
                        elif "красоте" in base_phrase:
                            search_terms.append("по красоте")
                        elif "duende" in base_phrase:
                            search_terms.append("duende")
                        elif "toros" in base_phrase:
                            search_terms.append("toros desde la barrera")
                        elif "cattle" in base_phrase:
                            search_terms.append("all hat and no cattle")
                        elif "tough love" in base_phrase:
                            search_terms.append("tough love")

                        matched_idiom = None
                        for iterm_low, iobj in idiom_by_lower.items():
                            if iterm_low in base_phrase or base_phrase in iterm_low:
                                matched_idiom = iobj["term"]
                                break

                        song_cnt = max(
                            1,
                            sum(len(re.findall(re.escape(st), combined_lower)) for st in search_terms[:1]),
                        )
                        if len(search_terms) > 1:
                            song_cnt = max(song_cnt, len(re.findall(re.escape(search_terms[1]), combined_lower)))
                        chorus_cnt = max(
                            len(re.findall(re.escape(st), chorus_lower)) for st in search_terms
                        )

                        token_key = base_phrase
                        candidates[token_key] = {
                            "token": base_phrase,
                            "lemma": base_phrase,
                            "meaning_gloss": voc.get("meaning") or base_phrase,
                            "is_chorus_hook": chorus_cnt > 0,
                            "song_count": song_cnt,
                            "chorus_count": chorus_cnt,
                            "vocab_uid": voc["uid"],
                            "idiom_term": matched_idiom,
                            "search_terms": search_terms,
                        }

                    # 2. Check all register idioms inside combined_lower
                    for iterm_low, iobj in idiom_by_lower.items():
                        if reg_to_lang.get(iobj["register_id"]) != lang_code:
                            continue
                        probe_stem = iterm_low[:-1] if len(iterm_low) > 6 else iterm_low
                        if iterm_low in combined_lower or probe_stem in combined_lower:
                            if iterm_low not in candidates:
                                sc = len(re.findall(re.escape(probe_stem), combined_lower))
                                cc = len(re.findall(re.escape(probe_stem), chorus_lower))
                                # Also match vocab if exact substring
                                matched_vuid = None
                                for vuid, voc in vocab_by_uid.items():
                                    if voc["lang_code"] == lang_code and iterm_low in voc["term"].lower():
                                        matched_vuid = vuid
                                        break
                                candidates[iterm_low] = {
                                    "token": iterm_low,
                                    "lemma": iterm_low,
                                    "meaning_gloss": iobj.get("meaning") or iterm_low,
                                    "is_chorus_hook": cc > 0,
                                    "song_count": max(1, sc),
                                    "chorus_count": cc,
                                    "vocab_uid": matched_vuid,
                                    "idiom_term": iobj["term"],
                                    "search_terms": [iterm_low, probe_stem],
                                }

                    # 3. Single-word frequency scan across full lyrics + pivot
                    word_counts: Counter[str] = Counter()
                    chorus_word_counts: Counter[str] = Counter()
                    for w in _tokenize_words(combined_lower):
                        if w in STOP_WORDS and w not in REGIONAL_ANCHOR_TOKENS:
                            continue
                        if len(w) <= 2 and w not in REGIONAL_ANCHOR_TOKENS:
                            continue
                        cons = LEMMA_CONSOLIDATION.get(w)
                        canon_key = cons[1].lower() if cons else w
                        word_counts[canon_key] += 1
                    for w in _tokenize_words(chorus_lower):
                        if w in STOP_WORDS and w not in REGIONAL_ANCHOR_TOKENS:
                            continue
                        if len(w) <= 2 and w not in REGIONAL_ANCHOR_TOKENS:
                            continue
                        cons = LEMMA_CONSOLIDATION.get(w)
                        canon_key = cons[1].lower() if cons else w
                        chorus_word_counts[canon_key] += 1

                    # Include top 28 frequent tokens PLUS any regional dialect anchor present in the song
                    seen_scan_keys: set[str] = set()
                    scan_pairs: list[tuple[str, int]] = []
                    for canon_key, cnt in word_counts.most_common(28):
                        seen_scan_keys.add(canon_key)
                        scan_pairs.append((canon_key, cnt))
                    for canon_key, cnt in word_counts.items():
                        if canon_key not in seen_scan_keys and (
                            canon_key in REGIONAL_ANCHOR_TOKENS or canon_key in LEMMA_CONSOLIDATION
                        ):
                            seen_scan_keys.add(canon_key)
                            scan_pairs.append((canon_key, cnt))

                    for canon_key, cnt in scan_pairs:
                        if canon_key in candidates:
                            # Boost counts if word scan found more occurrences
                            candidates[canon_key]["song_count"] = max(candidates[canon_key]["song_count"], cnt)
                            candidates[canon_key]["chorus_count"] = max(
                                candidates[canon_key]["chorus_count"], chorus_word_counts.get(canon_key, 0)
                            )
                            candidates[canon_key]["is_chorus_hook"] = candidates[canon_key]["chorus_count"] > 0
                            continue
                        # Find sample consolidation metadata
                        cons_meta = None
                        for raw_k, meta_t in LEMMA_CONSOLIDATION.items():
                            if meta_t[1].lower() == canon_key:
                                cons_meta = meta_t
                                break
                        matched_idiom = idiom_by_lower[canon_key]["term"] if canon_key in idiom_by_lower else None
                        matched_vuid = None
                        for vuid, voc in vocab_by_uid.items():
                            if voc["lang_code"] == lang_code and canon_key == re.sub(r"\s*\([^)]*\)", "", voc["term"]).strip().lower():
                                matched_vuid = vuid
                                break
                        gloss = (
                            cons_meta[2]
                            if cons_meta
                            else (
                                idiom_by_lower[canon_key]["meaning"]
                                if canon_key in idiom_by_lower
                                else f"High-frequency motif in {song['title']}"
                            )
                        )
                        cc = chorus_word_counts.get(canon_key, 0)
                        candidates[canon_key] = {
                            "token": canon_key,
                            "lemma": cons_meta[0] if cons_meta else canon_key,
                            "meaning_gloss": gloss,
                            "is_chorus_hook": cc > 0,
                            "song_count": cnt,
                            "chorus_count": cc,
                            "vocab_uid": matched_vuid,
                            "idiom_term": matched_idiom,
                            "search_terms": [canon_key, cons_meta[0] if cons_meta else canon_key],
                        }

                    # Connect cards + compute frequency scores
                    ranked_items: list[dict[str, Any]] = []
                    for key, item in candidates.items():
                        connected_cards: list[str] = []
                        for c in same_lang_cards:
                            card_plain_low = (c.get("text_plain") or "").lower()
                            card_idioms = [str(x).lower() for x in (c.get("idiom_terms") or [])]
                            if item.get("idiom_term") and item["idiom_term"].lower() in card_idioms:
                                connected_cards.append(c["uid"])
                                continue
                            if any(
                                re.search(rf"(?<!\w){re.escape(st[:5] if len(st) > 6 else st)}", card_plain_low)
                                for st in item["search_terms"]
                                if len(st) >= 2
                            ):
                                connected_cards.append(c["uid"])

                        card_cnt = len(connected_cards)
                        song_cnt = int(item["song_count"])
                        chorus_cnt = int(item["chorus_count"])
                        total_freq = song_cnt + card_cnt
                        freq_score = round(min(1.0, (song_cnt * 1.5 + chorus_cnt * 0.7 + card_cnt * 1.1) / 9.5), 3)

                        if item["is_chorus_hook"] and song_cnt >= 2:
                            freq_tier = "CHORUS_EARWORM"
                        elif card_cnt >= 2 and (item["vocab_uid"] or item["idiom_term"]):
                            freq_tier = "CROSS_CORPUS_ANCHOR"
                        elif item["vocab_uid"] or item["idiom_term"]:
                            freq_tier = "REGIONAL_SLANG_HOOK"
                        else:
                            freq_tier = "LYRIC_MOTIF"

                        sample_line = ""
                        for st in stanzas + [pivot_text]:
                            if any(t in st.lower() for t in item["search_terms"]):
                                sample_line = st.strip()[:220]
                                break

                        ranked_items.append(
                            {
                                "uid": f"LT_{song['uid']}_{_slugify(item['token'])}",
                                "song_uid": song["uid"],
                                "register_id": reg_id,
                                "lang_code": lang_code,
                                "token": item["token"],
                                "lemma": item["lemma"],
                                "meaning_gloss": item["meaning_gloss"],
                                "is_chorus_hook": bool(item["is_chorus_hook"]),
                                "song_count": song_cnt,
                                "chorus_count": chorus_cnt,
                                "card_count": card_cnt,
                                "total_frequency": total_freq,
                                "frequency_score": freq_score,
                                "freq_tier": freq_tier,
                                "vocab_uid": item["vocab_uid"],
                                "idiom_term": item["idiom_term"],
                                "connected_card_uids": connected_cards[:12],
                                "sample_lyric_line": sample_line,
                            }
                        )

                    # Prioritize idioms/vocab & 4-C card-connected dialect hooks (keep top 12 unique UIDs per song)
                    ranked_items.sort(
                        key=lambda r: (
                            2 if (r["vocab_uid"] or r["idiom_term"]) else (1 if r["card_count"] > 0 else 0),
                            r["frequency_score"],
                            r["total_frequency"],
                        ),
                        reverse=True,
                    )
                    top_tokens: list[dict[str, Any]] = []
                    seen_uids: set[str] = set()
                    for item in ranked_items:
                        if item["uid"] in seen_uids:
                            continue
                        seen_uids.add(item["uid"])
                        top_tokens.append(item)
                        if len(top_tokens) >= 12:
                            break

                    await conn.execute(
                        "DELETE FROM song_lyric_tokens WHERE song_uid = $1",
                        song["uid"],
                    )
                    for lt in top_tokens:
                        await conn.execute(
                            """
                            INSERT INTO song_lyric_tokens (
                                uid, song_uid, register_id, lang_code, token, lemma, meaning_gloss,
                                is_chorus_hook, song_count, chorus_count, card_count, total_frequency,
                                frequency_score, freq_tier, vocab_uid, idiom_term, connected_card_uids,
                                sample_lyric_line, sync_status
                            ) VALUES (
                                $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,'PENDING'
                            )
                            """,
                            lt["uid"],
                            lt["song_uid"],
                            lt["register_id"],
                            lt["lang_code"],
                            lt["token"],
                            lt["lemma"],
                            lt["meaning_gloss"],
                            lt["is_chorus_hook"],
                            lt["song_count"],
                            lt["chorus_count"],
                            lt["card_count"],
                            lt["total_frequency"],
                            lt["frequency_score"],
                            lt["freq_tier"],
                            lt["vocab_uid"],
                            lt["idiom_term"],
                            lt["connected_card_uids"],
                            lt["sample_lyric_line"],
                        )
                        total_tokens_written += 1

                    await conn.execute(
                        """
                        UPDATE songs
                        SET total_token_count = $2,
                            unique_token_count = $3,
                            sync_status = 'PENDING',
                            updated_at = NOW()
                        WHERE uid = $1
                        """,
                        song["uid"],
                        total_word_count,
                        unique_word_count,
                    )
                    per_song_summary.append(
                        {
                            "song_uid": song["uid"],
                            "title": song["title"],
                            "register_id": reg_id,
                            "stanza_count": len(stanzas),
                            "total_words": total_word_count,
                            "unique_words": unique_word_count,
                            "indexed_tokens": len(top_tokens),
                        }
                    )

        return {
            "ok": True,
            "songs_indexed": len(per_song_summary),
            "total_lyric_tokens": total_tokens_written,
            "per_song": per_song_summary,
            "agent_reach_probes": reach_reports,
        }

    async def get_song_frequency_profile(self, song_uid: str) -> dict[str, Any]:
        """Return full stanzas, indexed LyricTokens sorted by frequency, and Neo4j graph summary for one song."""
        song = await pg_manager.fetch_one("SELECT * FROM songs WHERE uid = $1", song_uid)
        if not song:
            raise LookupError(f"Song '{song_uid}' not found.")

        tokens = await pg_manager.fetch_all(
            """
            SELECT uid, song_uid, register_id, lang_code, token, lemma, meaning_gloss,
                   is_chorus_hook, song_count, chorus_count, card_count, total_frequency,
                   frequency_score, freq_tier, vocab_uid, idiom_term, connected_card_uids,
                   sample_lyric_line
            FROM song_lyric_tokens
            WHERE song_uid = $1
            ORDER BY frequency_score DESC, total_frequency DESC, token ASC
            """,
            song_uid,
        )

        neo_summary = {
            "connected_vocab_count": len({t["vocab_uid"] for t in tokens if t.get("vocab_uid")}),
            "connected_idiom_count": len({t["idiom_term"] for t in tokens if t.get("idiom_term")}),
            "connected_card_count": len(
                {cid for t in tokens for cid in (t.get("connected_card_uids") or [])}
            ),
        }
        try:
            neo_rows = await neo4j_manager.run_query(
                """
                MATCH (s:Song {uid: $uid})-[:HAS_LYRIC_TOKEN]->(lt:LyricToken)
                OPTIONAL MATCH (lt)-[:REINFORCES_VOCAB]->(v:Vocab)
                OPTIONAL MATCH (lt)-[:REINFORCES_IDIOM]->(i:Idiom)
                OPTIONAL MATCH (lt)-[:BOOSTS_CARD_FREQUENCY]->(c:Card)
                RETURN count(DISTINCT lt) AS token_nodes,
                       count(DISTINCT v) AS vocab_links,
                       count(DISTINCT i) AS idiom_links,
                       count(DISTINCT c) AS card_links
                """,
                {"uid": song_uid},
            )
            if neo_rows:
                neo_summary["neo4j_live"] = neo_rows[0]
        except Exception:
            pass

        return {
            "song": {
                "uid": song["uid"],
                "title": song["title"],
                "artist": song["artist"],
                "city_region": song["city_region"],
                "genre": song["genre"],
                "bpm": song["bpm"],
                "register_id": song["register_id"],
                "source_url": song.get("source_url", ""),
                "reach_channel": song.get("reach_channel", "agent-reach+jina"),
                "total_token_count": song.get("total_token_count", 0),
                "unique_token_count": song.get("unique_token_count", 0),
                "full_lyrics": song.get("full_lyrics", ""),
                "lyric_stanzas": song.get("lyric_stanzas", []),
                "reinforces_card_uid": song.get("reinforces_card_uid"),
            },
            "lyric_tokens": tokens,
            "graph_summary": neo_summary,
        }

    async def get_frequency_leaderboard(
        self,
        register_id: Optional[str] = None,
        limit: int = 25,
    ) -> dict[str, Any]:
        """Return cross-corpus frequency leaderboard joining songs, LyricTokens, Vocab, Idioms, and Cards."""
        rows = await pg_manager.fetch_all(
            """
            SELECT lt.uid, lt.song_uid, s.title AS song_title, s.artist AS song_artist,
                   lt.register_id, lt.lang_code, lt.token, lt.lemma, lt.meaning_gloss,
                   lt.is_chorus_hook, lt.song_count, lt.chorus_count, lt.card_count,
                   lt.total_frequency, lt.frequency_score, lt.freq_tier,
                   lt.vocab_uid, lt.idiom_term, lt.connected_card_uids, lt.sample_lyric_line
            FROM song_lyric_tokens lt
            JOIN songs s ON s.uid = lt.song_uid
            WHERE ($1::text IS NULL OR lt.register_id = $1)
            ORDER BY lt.frequency_score DESC, lt.total_frequency DESC, lt.token ASC
            LIMIT $2
            """,
            register_id,
            limit,
        )
        return {
            "register_id": register_id or "ALL",
            "count": len(rows),
            "tokens": rows,
        }


lyric_service = LyricFrequencyService()
