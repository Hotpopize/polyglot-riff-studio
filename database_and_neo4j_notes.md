# Polyglot Riff Atelier — Database (`PostgreSQL + pgvector`) & Neo4j Architecture Notes

This reference documents how **PostgreSQL 17 (`pgvector`)**, **Neo4j 5 (`+APOC`)**, **offline JSON shards (`db/*.db.json`)**, and **Browser `localStorage` / Cypher Export** work together across the **5 Languages (`10` Formal ↔ Regional Registers)** and **8 Unified Social Arenas**.

---

## 1. 4-Layer Persistence & Transactional Outbox Architecture

```text
  [1. PostgreSQL 17 + pgvector (:5433)]   <-- ACID Source of Truth + 1024-dim bge-m3 HNSW vectors
                 |
                 |  sync_status = 'PENDING' -> SyncService.sync_pending_to_neo4j()
                 +-----------------------------------------------+
                 |                                               |
                 v                                               v
  [2. Neo4j 5 Community + APOC (:7687)]           [3. Git-Tracked Shards (db/*.db.json)]
      Multi-hop 4-C flows, :PIVOTS_VIA                cz_ova, at_vie, ru_ala, en_yyc, es_sot
      bridges, :COUNTERS_STATE & FSRS edges           + polyglot_fabric.db.json (offline fallback)
                 \                                               /
                  \---- FastAPI (:8765) / polyglot_api_client.js /
                                         |
                                         v
            [4. Browser UI (Atelier v3.1 & Zero-Corporate v1.0)]
                localStorage ('POLYGLOT_NEO4J_RIFF_STATE_V3_1') + Tab 5 Cypher Exporter
```

- **Why Dual-Store (`Postgres` + `Neo4j`)?**
  - **PostgreSQL + `pgvector`** stores normalized relational records, FSRS review audit logs (`fsrs_review_events`), staged newspaper/Ollama candidates (`staged_webhooks`), and `1024`-dimensional `bge-m3` embeddings with HNSW cosine indexes for semantic phrase/idiom lookup.
  - **Neo4j 5 + APOC** executes 1-hop objection routing (`(:Card)-[:COUNTERS_STATE]->(:State)`), sequential 4-C transition chains (`:FLOWS_TO`), and multi-hop Myers-Scotton code-switching / register-drop traversals (`(:Card)-[:PIVOTS_VIA]->(:Bridge)-[:LANDS_ON]->(:Card)`).
  - **Graceful Offline Mode:** Both HTML studios work `100%` standalone over `file://` using `localStorage` and `db/*.db.json` shards when Docker is stopped, and automatically hydrate/sync through `polyglot_api_client.js` when FastAPI (`:8765`) is running.

---

## 2. Ports, Credentials & Windows Runtime Notes

Configured via `.env` (mirrored in `.env.example`) and `docker-compose.yml`:

| Service | Container / Runtime | Host Endpoint | Default Credentials / Models |
| :--- | :--- | :--- | :--- |
| **PostgreSQL 17 + `pgvector`** | `pgvector/pgvector:pg17` (`polyglot-postgres`) | `127.0.0.1:5433` | DB: `polyglot_sales` • User: `polyglot` • Pass: `polyglot_atelier_dev` |
| **Neo4j 5 Browser (HTTP)** | `neo4j:5-community` (`polyglot-neo4j`) | `http://127.0.0.1:7474` | User: `neo4j` • Pass: `polyglot_atelier_dev` • DB: `neo4j` |
| **Neo4j 5 Bolt Driver** | `neo4j:5-community` (`+APOC`) | `bolt://127.0.0.1:7687` | `NEO4J_PLUGINS=["apoc"]` unrestricted & allowlisted |
| **Ollama Local LLM / Embed** | Native Windows Ollama | `http://127.0.0.1:11434` | Embed: `bge-m3:latest` (`1024d`) • Stylizer: `gemma4:12b` • Fast: `gemma3:4b` |
| **FastAPI + Suite Hub** | `.venv` Uvicorn (`backend.api.main:app`) | `http://127.0.0.1:8765` | Serves REST API (`/api/v1/*`) + static HTML suite |

> **Windows Package Note (`neo4j-2026.10.1-1.noarch.rpm`):**
> The `.rpm` file in the workspace root is a RedHat/Fedora Linux installer package and cannot be installed natively on Windows. On Windows, always launch Neo4j + PostgreSQL via `docker compose up -d` or `.\start_polyglot_stack.ps1` (or Neo4j Desktop pointed to `bolt://127.0.0.1:7687`).

---

## 3. PostgreSQL (`pgvector`) Schema (`backend/db/postgres.py`)

`PostgresManager.init_schema()` idempotently creates `vector` extension + **13 tables**:

1. `languages` (`code` PK: `cs`, `de`, `ru`, `en`, `es`)
2. `registers` (`id` PK — **10 paired registers**: `CZ_STD`↔`CZ_OVA`, `DE_STD`↔`AT_VIE`, `RU_STD`↔`RU_ALA`, `EN_EXEC`↔`EN_YYC`, `ES_STD`↔`ES_SOT`, with `partition_file` mapping to `db/*.db.json`)
3. `arenas` (`id` PK — **8 unified social arenas**: `terrace`, `spark`, `adventure`, `runway`, `hochkultur`, `polo`, `wien`, `b2b`)
4. `style_lenses` (`DEADPAN`, `SABOTEUR`, `RACONTEUR`, `FERGUSON`, `ONEAL`, `WILLIAMS`)
5. `idioms` (`term` PK, `register_id` FK, `cousin_term`, `embedding vector(1024)`, `sync_status`)
6. `idiom_vibe_links` (`(source_term, target_term)` PK, `shared_root`, `pivot_tip`)
7. `cards` (`uid` PK, `register_id` FK, `stage`, `arena`, `lens_id`, `text_html`, `text_plain`, `phonetics`, `english_gloss`, `idiom_terms JSONB`, `embedding vector(1024)`, `sync_status`)
8. `lexical_scaffolds` (DE/RU/EN `COGNATE`, `STRUCTURAL_CALQUE`, `LOANWORD`, `PHONETIC_BRIDGE` hooks for Czech-from-Zero)
9. `false_friends` (`FF_CZ_UZASNY`, `FF_CZ_CERSTVY`, `FF_CZ_NAPAD`, `FF_CZ_VYPRODAT`, `FF_CZ_POZOR`, `FF_CZ_HODINA`, `FF_CZ_ZAPOMENOUT`, `FF_CZ_PRESNY`, `FF_CZ_SMESNY`)
10. `room_states` (`MANUAL_GRIND`, `CORPORATE_SHIELD`, `OVERTHINKING`, `PLAYING_IT_SAFE`)
11. `bridges` (`REGISTER_DROP` & `CODE_SWITCH` connectors with Myers-Scotton `mlf_boundary_note`)
12. `graph_edges` (`FLOWS_TO`, `PIVOTS_VIA`, `COUNTERS_STATE` with `weight`, `stability`, `difficulty`, `days_ago`, `drills`)
13. `fsrs_review_events` & `staged_webhooks` (audit trail for FSRS practice scores `1..5` and moderation queue for newspaper/Ollama riffs)

---

## 4. Neo4j Property Graph Schema & Strict Relation Rules

Enforced by `backend/db/neo4j_client.py`, `backend/validators/graph_rules.py`, and `db/graph_relation_validator.js`:

### Node Labels & Uniqueness Constraints
- `(:Language {code})`
- `(:Register:Persona {id, tier, lang_code, name, rhythm, trick, posture})`
- `(:Arena {id, icon, label, short_label, arena_group, description})`
- `(:Card {uid, register_id, lang, stage, arena, lens_id, text, text_html, phonetics, english_gloss})` — indexed on `(stage)` and `(arena)`
- `(:Idiom {term, register_id, origin, meaning, delivery, cousin})`
- `(:Bridge {uid, from_lang, to_lang, bridge_type, text, mlf_boundary_note, vocal_cue, weight})`
- `(:State {id, label, description})`
- `(:FalseFriend {id, cz_term, ru_trap, de_calque, meaning})`

### Validated Graph Relationships
- `(:Language)-[:HAS_REGISTER]->(:Register:Persona)`
- `(:Register)-[:PAIRS_WITH {direction: 'REGISTER_DROP' | 'REGISTER_ESCALATE'}]->(:Register)`
- `(:Register:Persona)-[:HAS_CARD]->(:Card)` *(same register partition)*
- `(:Card)-[:SET_IN_ARENA]->(:Arena)` *(binds every card to one of the 8 unified rooms)*
- `(:Card)-[:FLOWS_TO {id, weight, stability, difficulty, days_ago, drills}]->(:Card)` *(sequential 4-C chain: `COMPLIMENT → CHAMELEON → COUNTERACT → CURIOSITY`)*
- `(:Card)-[:PIVOTS_VIA {weight, bridge_uid}]->(:Card)` & `(:Card)-[:PIVOTS_VIA]->(:Bridge)-[:LANDS_ON]->(:Card)` *(cross-register drop or cross-language pivot)*
- `(:Card)-[:INJECTS_SLANG]->(:Idiom)` *(must appear as `<span class="slang-token" data-term="...">` inside `text_html`)*
- `(:Card {stage: 'COUNTERACT'})-[:COUNTERS_STATE {effectiveness, cue}]->(:State)` *(1-hop live room-friction resolver)*
- `(:Idiom)-[:SHARES_VIBE_WITH {shared_root, pivot_tip}]->(:Idiom)` *(cross-cultural conceptual cousin)*
- `(:Register)-[:GUARDS_AGAINST]->(:FalseFriend)` *(blocks Russian homonym traps in Czech)*

### FSRS Edge Decay Formula
Retrievability $R(t)$ on `:FLOWS_TO` and `:PIVOTS_VIA` edges is computed dynamically as:

$$R(t) = \left(1 + \frac{t}{9 \cdot S}\right)^{-1}$$

where $t$ is `days_ago` and $S$ is `stability` (in days). An edge is flagged **Rusty** (`#fbbf24`) when $R(t) < 0.75$, `weight < 0.60`, or `days_ago >= 7`.

---

## 5. Unified 8 Social Arenas Corpus Summary (`192` Cards • `141` Edges • `26` Idioms)

Seeded via `backend/seed/corpus_data.py` + `backend/seed/arena_decks_8.py` and mirrored into `db/*.db.json`:

| Arena ID | Group | Seeded Cards | UID Pattern in DB & Neo4j |
| :--- | :--- | :---: | :--- |
| `terrace` | Zero-Corporate Lounge | `20` | `<LANG>_<STAGE>` (e.g. `CZ_OVA_COMP` .. `ES_SOT_CUR`) |
| `spark` | Zero-Corporate Lounge | `20` | `<LANG>_SPARK_<STAGE>` (e.g. `CZ_OVA_SPARK_COMP`) |
| `adventure` | Zero-Corporate Lounge | `20` | `<LANG>_ADVENTURE_<STAGE>` |
| `runway` | Haute Salon Trio | `28` | `<LANG>_RUNWAY_<STAGE>` + `RUNWAY_*_BASE` + `HAUTE_RUNWAY_*` |
| `hochkultur` | Haute Salon Trio | `26` | `<LANG>_HOCHKULTUR_<STAGE>` + `HOCH_*_BASE` + `HAUTE_HOCH_*` |
| `polo` | Haute Salon Trio | `26` | `<LANG>_POLO_<STAGE>` + `POLO_*_BASE` + `HAUTE_POLO_*` |
| `wien` | Station Wien Café | `20` | `<LANG>_WIEN_<STAGE>` |
| `b2b` | Executive → Trench | `32` | `<LANG>_B2B_<STAGE>` + Formal `*_STD_COMP_01` / `*_CHAM_01` |

> **Why Tab 1 (`Atelier v3.1`) Preserves Canonical UIDs in the Live Grader:**
> In the browser UI (`getEffectiveCardsForArena`), switching arenas overlays the active arena's 4-C text onto the 20 canonical UIDs (`CZ_OVA_COMP`..`ES_SOT_CUR`) during live teleprompter practice so `:COUNTERS_STATE` hotkeys and FSRS edge weights transfer seamlessly across rooms, while **Tab 5 (`Cypher Export`)** and **`backend/seed/corpus_data.py`** materialize all `160`–`192` distinct arena-qualified `:Card` nodes (`<LANG>_<ARENA>_<STAGE>`) in Neo4j and PostgreSQL.

---

## 6. Essential CLI Commands & Neo4j Cypher Queries

### PowerShell Operations (`C:\Assets\PolyglotSales`)
```powershell
# 1. Regenerate offline db/*.db.json shards anytime (no Docker required)
.\.venv\Scripts\python.exe -m backend.cli shards

# 2. Check health of Postgres (:5433), Neo4j (:7687), and Ollama (:11434)
.\.venv\Scripts\python.exe -m backend.cli status

# 3. Boot full stack (Docker Postgres + Neo4j -> Seed + Embeddings -> FastAPI :8765)
.\start_polyglot_stack.ps1

# 4. Seed / re-seed Postgres + Neo4j + db/*.db.json (fast mode without re-embedding)
.\.venv\Scripts\python.exe -m backend.cli seed --no-embed

# 5. Query any of the 8 arenas from CLI
.\.venv\Scripts\python.exe -m backend.cli converse --reg CZ_OVA --arena wien --stage CHAMELEON --lens FERGUSON

# 6. Run full 4-layer data integrity audit (Postgres <-> Neo4j <-> Vectors <-> Shards)
.\.venv\Scripts\python.exe -m backend.cli audit

# 7. Create a timestamped, SHA-256-verified backup snapshot (with retention)
.\.venv\Scripts\python.exe -m backend.cli backup --keep-last 10

# 8. Reconcile & prune any orphan Neo4j nodes/edges against PostgreSQL source-of-truth
.\.venv\Scripts\python.exe -m backend.cli sync --force --prune-orphans
```

### Useful Neo4j Browser (`http://127.0.0.1:7474`) Cypher Queries

```cypher
// 1. Inspect the full 4-C flow for a specific Social Arena & Persona (e.g. Station Wien in Ostravština)
MATCH (r:Register {id: 'CZ_OVA'})-[:HAS_CARD]->(c1:Card {arena: 'wien', stage: 'COMPLIMENT'})
MATCH path = (c1)-[:FLOWS_TO*1..3]->(cEnd:Card {arena: 'wien'})
OPTIONAL MATCH (cEnd)-[:SET_IN_ARENA]->(ar:Arena)
RETURN path, ar;

// 2. 1-Hop Live Room-Friction Objection Resolver (:COUNTERS_STATE)
MATCH (c:Card)-[cs:COUNTERS_STATE]->(s:State {id: 'MANUAL_GRIND'})
OPTIONAL MATCH (c)-[:INJECTS_SLANG]->(i:Idiom)
RETURN c.uid, c.register_id, c.arena, c.text, cs.effectiveness, cs.cue, collect(i.term) AS idioms
ORDER BY cs.effectiveness DESC;

// 3. Multi-Hop Executive Boardroom -> Regional Trench Register Drop (Spisovná -> Ostravština)
MATCH path = (cFormal:Card {register_id: 'CZ_STD'})-[:FLOWS_TO*0..1]->()-[:PIVOTS_VIA]->(b:Bridge)-[:LANDS_ON]->(cTrench:Card {register_id: 'CZ_OVA'})
RETURN path;

// 4. Find Rusty Conversational Transitions Requiring Pre-Call Drill (FSRS Retrievability < 75%)
MATCH (a:Card)-[r:FLOWS_TO|PIVOTS_VIA]->(b:Card)
WITH a, r, b, (1.0 / (1.0 + (toFloat(coalesce(r.days_ago, 0)) / (9.0 * coalesce(r.stability, 4.0))))) AS retrievability
WHERE retrievability < 0.75 OR r.weight < 0.60
RETURN a.uid AS from_card, b.uid AS to_card, a.arena AS arena, round(r.weight * 100) AS weight_pct, round(retrievability * 100) AS R_pct
ORDER BY R_pct ASC;

// 5. Cross-Cultural Idiom Vibe Network (:SHARES_VIBE_WITH)
MATCH (i1:Idiom)-[v:SHARES_VIBE_WITH]->(i2:Idiom)
RETURN i1.term, i1.register_id, v.shared_root, i2.term, i2.register_id, v.pivot_tip;

// 6. IB Past Paper :Vocab (:FORMAL_EXAM ↔ :REGIONAL_RIFF) & :FALSE_FRIEND_ALERT Shield
MATCH (r:Register)-[:CONTAINS_VOCAB]->(v:Vocab)
OPTIONAL MATCH (v)-[:FALSE_FRIEND_ALERT]->(ff:Vocab)
RETURN r.id AS register_id, r.ib_alias AS ib_alias, v.uid, v.term, v.register_type, v.ib_source, ff.uid AS alert_uid, ff.warning;
```

> **Cypher Migration Artifact:** See [polyglot-srs-cypher-migration.cypher](file:///C:/Assets/PolyglotSales/polyglot-srs-cypher-migration.cypher) for the complete standalone idempotent Cypher migration script integrating all `34` `:Vocab` nodes (`31` formal/regional + `3` `FF_CZ_*` alert nodes), `:CONTAINS_VOCAB`, `:FALSE_FRIEND_ALERT`, `CZ_EXEC_*` formal outreach cards, and `BRIDGE_CZ_FORMAL_TO_OVA` / `BRIDGE_DE_FORMAL_TO_VIE`.

---

## 7. Data Management & Governance Best Practices

1. **Single ACID Source of Truth + Domain Foreign Keys (`PostgreSQL 17`)**:
   - Schema version is tracked in `schema_meta` (`3.2.0`), including `vocab_items` and `vocab_false_friend_alerts`.
   - `cards.arena` enforces `fk_cards_arena -> arenas(id) ON UPDATE CASCADE ON DELETE RESTRICT`, while `normalize_arena_id()` maps legacy aliases (`lounge`/`general` → `terrace`, `banter` → `spark`) before insert.
2. **Transactional Outbox + Orphan Reconciliation (`Neo4j 5`)**:
   - Every write marks `sync_status = 'PENDING'`; `SyncService.sync_pending_to_neo4j()` replays `MERGE` upserts idempotently (harmonizing `:Register` labels `:FORMAL_EXAM` / `:REGIONAL_RIFF`, `ib_alias`, `:Vocab`, `:CONTAINS_VOCAB`, and `:FALSE_FRIEND_ALERT`) and `--prune-orphans` removes any Neo4j `:Card`, `:Idiom`, `:Vocab`, `:Arena`, or SRS relationship absent from PostgreSQL.
3. **Crash-Atomic Offline Shards (`db/*.db.json`)**:
   - `_atomic_write_json()` writes to a sibling `.tmp` file, calls `os.fsync()`, and atomically swaps via `os.replace()`, preventing half-written JSON shards on power loss or interruption.
4. **Browser Hydration & Write-Through Hygiene (`PolyglotAPI` + `localStorage`)**:
   - Client mutations (`gradeActiveTransition`, `addCustomNodeToGraph`, `injectHauteRiffToGraph`, `commitOllamaCandidate`, `approveWebhookItem`) preserve deterministic `uid`s on write-through to `/api/v1/nodes/commit` so browser `localStorage` and PostgreSQL never diverge or create duplicate UIDs.
   - `hydrateBackendState()` and `initApp()` strictly validate both endpoints (`validCardUids.has(source) && validCardUids.has(target)`) to self-heal and prevent orphan edges in `state.edges`.
5. **Continuous Verification & Checksummed Backups (`audit` & `backup`)**:
   - `python -m backend.cli audit` (or `GET /api/v1/admin/audit`) verifies 9 invariants across all 4 layers (Postgres health/FK, Neo4j APOC, zero outbox lag, 100% `bge-m3` vector coverage, graph relation & FSRS bounds on every row, 10-class Postgres ↔ Neo4j count parity including `:Vocab`, zero Neo4j orphan cards, and 6/6 `db/*.db.json` shard SHA-256 + `cards`/`idioms`/`vocab` count parity).
   - `python -m backend.cli backup --keep-last 10` (or `POST /api/v1/admin/backup`) writes `postgres_full_dump.json`, `neo4j_reconstruction.cypher`, and `manifest.json` (with SHA-256 digests and automatic snapshot retention) into `backups/snapshot_<UTC_TS>/`.
6. **Secret & Artifact Hygiene (`.gitignore`)**:
   - `.env`, `.venv/`, `backups/`, `.tmp_*`, and local binary installers (`*.rpm`) are excluded from version control while `.env.example` and `db/*.db.json` remain tracked.
