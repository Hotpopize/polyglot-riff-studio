from __future__ import annotations

import json
from typing import Any, Optional, Sequence

import asyncpg
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from backend.config import settings

SCHEMA_VERSION = "3.3.0"

SCHEMA_DDL = f"""
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS languages (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    flag TEXT NOT NULL DEFAULT '',
    family TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS registers (
    id TEXT PRIMARY KEY,
    lang_code TEXT NOT NULL REFERENCES languages(code) ON DELETE CASCADE,
    tier TEXT NOT NULL CHECK (tier IN ('FORMAL', 'REGIONAL')),
    flag TEXT NOT NULL DEFAULT '',
    name TEXT NOT NULL,
    subtitle TEXT NOT NULL DEFAULT '',
    family TEXT NOT NULL DEFAULT '',
    address_form TEXT NOT NULL DEFAULT '',
    phonetic_rhythm TEXT NOT NULL DEFAULT '',
    intimacy_trick TEXT NOT NULL DEFAULT '',
    posture TEXT NOT NULL DEFAULT '',
    paired_register_id TEXT,
    partition_file TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS style_lenses (
    id TEXT PRIMARY KEY,
    lens_group TEXT NOT NULL,
    icon TEXT NOT NULL DEFAULT '',
    name TEXT NOT NULL,
    inspirations TEXT NOT NULL DEFAULT '',
    cadence TEXT NOT NULL DEFAULT '',
    prosody TEXT NOT NULL DEFAULT '',
    delivery_rule TEXT NOT NULL DEFAULT '',
    modifier_prefix TEXT NOT NULL DEFAULT '',
    modifier_cue TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS idioms (
    term TEXT PRIMARY KEY,
    register_id TEXT NOT NULL REFERENCES registers(id) ON DELETE CASCADE,
    origin TEXT NOT NULL DEFAULT '',
    meaning TEXT NOT NULL DEFAULT '',
    delivery_cue TEXT NOT NULL DEFAULT '',
    cousin_term TEXT,
    embedding vector({settings.embedding_dim}),
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS idiom_vibe_links (
    source_term TEXT NOT NULL REFERENCES idioms(term) ON DELETE CASCADE,
    target_term TEXT NOT NULL REFERENCES idioms(term) ON DELETE CASCADE,
    shared_root TEXT NOT NULL DEFAULT '',
    pivot_tip TEXT NOT NULL DEFAULT '',
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ,
    PRIMARY KEY (source_term, target_term)
);

CREATE TABLE IF NOT EXISTS arenas (
    id TEXT PRIMARY KEY,
    icon TEXT NOT NULL DEFAULT '',
    label TEXT NOT NULL,
    short_label TEXT NOT NULL DEFAULT '',
    arena_group TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS cards (
    uid TEXT PRIMARY KEY,
    register_id TEXT NOT NULL REFERENCES registers(id) ON DELETE CASCADE,
    stage TEXT NOT NULL CHECK (stage IN ('COMPLIMENT', 'CHAMELEON', 'COUNTERACT', 'CURIOSITY')),
    arena TEXT NOT NULL DEFAULT 'terrace',
    lens_id TEXT REFERENCES style_lenses(id) ON DELETE SET NULL,
    title TEXT NOT NULL DEFAULT '',
    register_drop_note TEXT NOT NULL DEFAULT '',
    text_html TEXT NOT NULL,
    text_plain TEXT NOT NULL,
    phonetics TEXT NOT NULL DEFAULT '',
    english_gloss TEXT NOT NULL DEFAULT '',
    delivery_cue TEXT NOT NULL DEFAULT '',
    idiom_terms JSONB NOT NULL DEFAULT '[]'::jsonb,
    embedding vector({settings.embedding_dim}),
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lexical_scaffolds (
    id SERIAL PRIMARY KEY,
    card_uid TEXT REFERENCES cards(uid) ON DELETE CASCADE,
    idiom_term TEXT REFERENCES idioms(term) ON DELETE CASCADE,
    target_register_id TEXT NOT NULL REFERENCES registers(id) ON DELETE CASCADE,
    anchor_lang TEXT NOT NULL,
    scaffold_type TEXT NOT NULL CHECK (scaffold_type IN ('COGNATE', 'STRUCTURAL_CALQUE', 'LOANWORD', 'PHONETIC_BRIDGE')),
    anchor_expression TEXT NOT NULL,
    explanation TEXT NOT NULL DEFAULT '',
    UNIQUE (card_uid, idiom_term, anchor_lang, anchor_expression)
);

CREATE TABLE IF NOT EXISTS false_friends (
    id TEXT PRIMARY KEY,
    target_lang TEXT NOT NULL,
    target_term TEXT NOT NULL,
    trap_lang TEXT NOT NULL DEFAULT 'ru',
    trap_term TEXT NOT NULL,
    calque_lang TEXT NOT NULL DEFAULT 'de',
    calque_term TEXT NOT NULL DEFAULT '',
    safe_meaning TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS room_states (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    description TEXT NOT NULL,
    default_card_uid TEXT,
    default_register_id TEXT,
    effectiveness DOUBLE PRECISION NOT NULL DEFAULT 0.92,
    cue TEXT NOT NULL DEFAULT '',
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS bridges (
    uid TEXT PRIMARY KEY,
    from_register_id TEXT NOT NULL REFERENCES registers(id) ON DELETE CASCADE,
    to_register_id TEXT NOT NULL REFERENCES registers(id) ON DELETE CASCADE,
    from_card_uid TEXT,
    to_card_uid TEXT,
    bridge_type TEXT NOT NULL CHECK (bridge_type IN ('REGISTER_DROP', 'CODE_SWITCH')),
    text TEXT NOT NULL,
    mlf_boundary_note TEXT NOT NULL DEFAULT '',
    vocal_cue TEXT NOT NULL DEFAULT '',
    weight DOUBLE PRECISION NOT NULL DEFAULT 0.90,
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS graph_edges (
    id TEXT PRIMARY KEY,
    source_uid TEXT NOT NULL,
    target_uid TEXT NOT NULL,
    edge_type TEXT NOT NULL CHECK (edge_type IN ('FLOWS_TO', 'PIVOTS_VIA', 'COUNTERS_STATE')),
    bridge_uid TEXT REFERENCES bridges(uid) ON DELETE SET NULL,
    weight DOUBLE PRECISION NOT NULL DEFAULT 0.80,
    stability DOUBLE PRECISION NOT NULL DEFAULT 6.0,
    difficulty DOUBLE PRECISION NOT NULL DEFAULT 5.0,
    days_ago INTEGER NOT NULL DEFAULT 0,
    drills INTEGER NOT NULL DEFAULT 1,
    effectiveness DOUBLE PRECISION,
    cue TEXT NOT NULL DEFAULT '',
    last_drilled_at TIMESTAMPTZ DEFAULT NOW(),
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS fsrs_review_events (
    id SERIAL PRIMARY KEY,
    edge_id TEXT NOT NULL REFERENCES graph_edges(id) ON DELETE CASCADE,
    score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
    prev_weight DOUBLE PRECISION NOT NULL,
    new_weight DOUBLE PRECISION NOT NULL,
    prev_stability DOUBLE PRECISION NOT NULL,
    new_stability DOUBLE PRECISION NOT NULL,
    retrievability DOUBLE PRECISION NOT NULL,
    reviewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS staged_webhooks (
    id TEXT PRIMARY KEY,
    target_register_id TEXT NOT NULL REFERENCES registers(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL DEFAULT 'NEWSPAPER_WEBHOOK',
    paper_or_model TEXT NOT NULL DEFAULT '',
    published_label TEXT NOT NULL DEFAULT '',
    headline TEXT NOT NULL DEFAULT '',
    payload_json JSONB NOT NULL,
    validation_json JSONB NOT NULL DEFAULT '{{}}'::jsonb,
    status TEXT NOT NULL DEFAULT 'STAGED' CHECK (status IN ('STAGED', 'APPROVED', 'REJECTED')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    approved_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS vocab_items (
    uid TEXT PRIMARY KEY,
    term TEXT NOT NULL,
    lang_code TEXT NOT NULL REFERENCES languages(code) ON DELETE CASCADE,
    register_id TEXT REFERENCES registers(id) ON DELETE CASCADE,
    register_type TEXT NOT NULL CHECK (register_type IN ('FORMAL_EXAM', 'REGIONAL_RIFF', 'FALSE_FRIEND_ALERT')),
    meaning TEXT NOT NULL DEFAULT '',
    ib_source TEXT NOT NULL DEFAULT '',
    grammar_note TEXT NOT NULL DEFAULT '',
    etymology TEXT NOT NULL DEFAULT '',
    warning TEXT NOT NULL DEFAULT '',
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vocab_false_friend_alerts (
    source_uid TEXT NOT NULL REFERENCES vocab_items(uid) ON DELETE CASCADE,
    target_uid TEXT NOT NULL REFERENCES vocab_items(uid) ON DELETE CASCADE,
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ,
    PRIMARY KEY (source_uid, target_uid)
);

CREATE TABLE IF NOT EXISTS songs (
    uid TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    city_region TEXT NOT NULL DEFAULT '',
    genre TEXT NOT NULL DEFAULT '',
    bpm INTEGER NOT NULL DEFAULT 100,
    register_id TEXT REFERENCES registers(id) ON DELETE CASCADE,
    original_lang TEXT NOT NULL DEFAULT '',
    original_lyric TEXT NOT NULL,
    translation_es TEXT NOT NULL DEFAULT '',
    translation_en TEXT NOT NULL DEFAULT '',
    translation_cz TEXT NOT NULL DEFAULT '',
    translation_de TEXT NOT NULL DEFAULT '',
    translation_ru TEXT NOT NULL DEFAULT '',
    cultural_vibe TEXT NOT NULL DEFAULT '',
    pivot_line TEXT NOT NULL DEFAULT '',
    reinforces_card_uid TEXT REFERENCES cards(uid) ON DELETE SET NULL,
    slang_vocab_uids JSONB NOT NULL DEFAULT '[]'::jsonb,
    sync_status TEXT NOT NULL DEFAULT 'PENDING',
    synced_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cards_lookup
    ON cards (register_id, arena, stage, lens_id);

CREATE INDEX IF NOT EXISTS idx_cards_sync
    ON cards (sync_status);

CREATE INDEX IF NOT EXISTS idx_idioms_register
    ON idioms (register_id);

CREATE INDEX IF NOT EXISTS idx_bridges_pair
    ON bridges (from_register_id, to_register_id);

CREATE INDEX IF NOT EXISTS idx_cards_embedding_hnsw
    ON cards USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_idioms_embedding_hnsw
    ON idioms USING hnsw (embedding vector_cosine_ops);
"""


def vector_to_pg_literal(vec: Optional[Sequence[float]]) -> Optional[str]:
    if not vec:
        return None
    return "[" + ",".join(f"{float(v):.7f}" for v in vec) + "]"


class PostgresManager:
    """Async PostgreSQL + pgvector connection pool and helper methods."""

    def __init__(self, dsn: str = settings.asyncpg_dsn) -> None:
        self.dsn = dsn
        self._pool: Optional[asyncpg.Pool] = None
        self._sa_engine: Optional[AsyncEngine] = None

    @property
    def sqlalchemy_engine(self) -> AsyncEngine:
        if self._sa_engine is None:
            self._sa_engine = create_async_engine(settings.sqlalchemy_dsn, pool_pre_ping=True)
        return self._sa_engine

    async def get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=1,
                max_size=10,
                command_timeout=30,
                init=self._init_connection,
            )
        return self._pool

    @staticmethod
    async def _init_connection(conn: asyncpg.Connection) -> None:
        await conn.set_type_codec(
            "jsonb",
            encoder=json.dumps,
            decoder=json.loads,
            schema="pg_catalog",
        )

    async def init_schema(self) -> None:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(SCHEMA_DDL)
            await conn.execute(
                """
                INSERT INTO schema_meta (key, value, updated_at)
                VALUES ('schema_version', $1, NOW())
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()
                """,
                SCHEMA_VERSION,
            )
            has_arenas = await conn.fetchval("SELECT EXISTS(SELECT 1 FROM arenas LIMIT 1);")
            if has_arenas:
                await self._apply_domain_constraints_conn(conn)

    async def enforce_domain_constraints(self) -> None:
        """Normalize legacy arena aliases and idempotently attach fk_cards_arena once arenas exist."""
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            await self._apply_domain_constraints_conn(conn)

    @staticmethod
    async def _apply_domain_constraints_conn(conn: asyncpg.Connection) -> None:
        await conn.execute(
            """
            UPDATE cards
            SET arena = CASE
                WHEN arena IN ('general', 'lounge') THEN 'terrace'
                WHEN arena = 'banter' THEN 'spark'
                ELSE 'terrace'
            END
            WHERE arena NOT IN (SELECT id FROM arenas);
            """
        )
        await conn.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'fk_cards_arena'
                ) THEN
                    ALTER TABLE cards
                        ADD CONSTRAINT fk_cards_arena
                        FOREIGN KEY (arena) REFERENCES arenas(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT;
                END IF;
            END $$;
            """
        )

    async def ping(self) -> dict[str, Any]:
        try:
            pool = await self.get_pool()
            async with pool.acquire() as conn:
                version = await conn.fetchval("SELECT version();")
                has_vector = await conn.fetchval(
                    "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector');"
                )
                schema_ver = await conn.fetchval(
                    "SELECT value FROM schema_meta WHERE key = 'schema_version';"
                )
                counts = await conn.fetchrow(
                    """
                    SELECT
                        (SELECT COUNT(*) FROM arenas) AS arenas,
                        (SELECT COUNT(*) FROM registers) AS registers,
                        (SELECT COUNT(*) FROM cards) AS cards,
                        (SELECT COUNT(*) FROM idioms) AS idioms,
                        (SELECT COUNT(*) FROM vocab_items) AS vocab,
                        (SELECT COUNT(*) FROM songs) AS songs,
                        (SELECT COUNT(*) FROM bridges) AS bridges,
                        (SELECT COUNT(*) FROM graph_edges) AS edges,
                        (SELECT COUNT(*) FROM cards WHERE embedding IS NOT NULL) AS embedded_cards,
                        (SELECT COUNT(*) FROM idioms WHERE embedding IS NOT NULL) AS embedded_idioms,
                        (SELECT COUNT(*) FROM arenas WHERE sync_status = 'PENDING')
                        + (SELECT COUNT(*) FROM registers WHERE sync_status = 'PENDING')
                        + (SELECT COUNT(*) FROM cards WHERE sync_status = 'PENDING')
                        + (SELECT COUNT(*) FROM idioms WHERE sync_status = 'PENDING')
                        + (SELECT COUNT(*) FROM vocab_items WHERE sync_status = 'PENDING')
                        + (SELECT COUNT(*) FROM songs WHERE sync_status = 'PENDING')
                        + (SELECT COUNT(*) FROM bridges WHERE sync_status = 'PENDING')
                        + (SELECT COUNT(*) FROM graph_edges WHERE sync_status = 'PENDING') AS pending_sync
                    """
                )
                return {
                    "ok": True,
                    "pgvector": bool(has_vector),
                    "schema_version": schema_ver or SCHEMA_VERSION,
                    "version": version.split(",")[0] if version else "PostgreSQL",
                    "counts": dict(counts) if counts else {},
                }
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    async def fetch_all(self, query: str, *args: Any) -> list[dict[str, Any]]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(r) for r in rows]

    async def fetch_one(self, query: str, *args: Any) -> Optional[dict[str, Any]]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None

    async def execute(self, query: str, *args: Any) -> str:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
        if self._sa_engine is not None:
            await self._sa_engine.dispose()
            self._sa_engine = None


pg_manager = PostgresManager()
