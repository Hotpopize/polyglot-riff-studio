# Polyglot Riff Atelier — Graph Relation Rules, Per-Language Databases, Ollama & Newspaper Webhook Specification

See the interactive implementation plan artifact or review the core schema below:

## 1. Per-Language Database Partitioning (`/db`)
- `db/cz_ova.db.json` (`polyglot.cz`) — *Spisovná čeština* (`CZ_STD`) & *Ostravština* (`CZ_OVA`)
- `db/at_vie.db.json` (`polyglot.at`) — *Wiener Schmäh* (`AT_VIE`)
- `db/ru_ala.db.json` (`polyglot.ru`) — *Almaty Insider* (`RU_ALA`)
- `db/en_yyc.db.json` (`polyglot.en`) — *Calgary Flair* (`EN_YYC`)
- `db/es_sot.db.json` (`polyglot.es`) — *Sotogrande Duende* (`ES_SOT`)
- `db/polyglot_fabric.db.json` (`polyglot.fabric`) — Cross-language `:Bridge`, `:SHARES_VIBE_WITH`, `:State`, and `:FalseFriend` nodes.

## 2. Strict Graph Relation Rules
- `(:Persona)-[:HAS_CARD]->(:Card)` (must match `lang`)
- `(:Card)-[:SET_IN_ARENA]->(:Arena)` (maps every card to one of the 8 unified rooms: `terrace`, `spark`, `adventure`, `runway`, `hochkultur`, `polo`, `wien`, `b2b`)
- `(:Card)-[:FLOWS_TO {weight, stability, difficulty, days_ago, drills}]->(:Card)` (same `lang`, sequential 4-C stages)
- `(:Card)-[:PIVOTS_VIA {weight, stability}]->(:Bridge)-[:LANDS_ON]->(:Card)` (cross-register or cross-language transition)
- `(:Card)-[:INJECTS_SLANG {slot}]->(:Idiom)` (same `lang`, must appear as `<span class="slang-token">` in `Card.text`)
- `(:Card {stage: 'COUNTERACT'})-[:COUNTERS_STATE {effectiveness, cue}]->(:State)`
- `(:Idiom)-[:SHARES_VIBE_WITH {shared_root, pivot_tip}]->(:Idiom)` (cross-language conceptual/etymological bridge)
- `(:Idiom | :Card)-[:HARVESTED_FROM {harvested_at}]->(:NewsContext)` (local newspaper webhook provenance)

> Full PostgreSQL (`pgvector`), Neo4j 5 (`+APOC`), outbox sync, port/credential table, and Cypher query cookbook: see `database_and_neo4j_notes.md`.

