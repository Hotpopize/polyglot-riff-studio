from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.config import settings
from backend.db.neo4j_client import neo4j_manager
from backend.db.postgres import SCHEMA_VERSION, pg_manager
from backend.validators.graph_rules import validate_graph_commit


def _atomic_write_text(target_path: Path, text: str) -> str:
    """Atomically write UTF-8 text via sibling temporary file + os.replace() and return SHA-256 hex digest."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    payload_bytes = text.encode("utf-8")
    digest = hashlib.sha256(payload_bytes).hexdigest()
    fd, tmp_name = tempfile.mkstemp(
        dir=str(target_path.parent),
        prefix=f".{target_path.name}.",
        suffix=".tmp",
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target_path)
    except Exception:
        if os.path.exists(tmp_name):
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
        raise
    return digest


def _atomic_write_json(target_path: Path, doc: dict[str, Any]) -> str:
    """Atomically serialize deterministic UTF-8 JSON to disk and return SHA-256 hex digest."""
    content = json.dumps(doc, ensure_ascii=False, indent=2, default=str) + "\n"
    return _atomic_write_text(target_path, content)


class SyncService:
    """Transactional outbox synchronizer, cross-store auditor & snapshot manager (PostgreSQL -> Neo4j + db/*.db.json)."""

    async def sync_pending_to_neo4j(self, force_all: bool = False, prune_orphans: bool = False) -> dict[str, Any]:
        where_clause = "" if force_all else "WHERE sync_status = 'PENDING'"
        counts: dict[str, int] = {}
        neo4j_ok = False
        error_msg = None

        try:
            await neo4j_manager.init_constraints()

            languages = await pg_manager.fetch_all("SELECT code, name, flag, family FROM languages")
            if languages:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (l:Language {code: row.code})
                    SET l.name = row.name, l.flag = row.flag, l.family = row.family
                    """,
                    {"rows": languages},
                )
                counts["languages"] = len(languages)

            arenas = await pg_manager.fetch_all(
                f"SELECT id, icon, label, short_label, arena_group, description FROM arenas {where_clause}"
            )
            if arenas:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (a:Arena {id: row.id})
                    SET a.icon = row.icon,
                        a.label = row.label,
                        a.short_label = row.short_label,
                        a.arena_group = row.arena_group,
                        a.description = row.description
                    """,
                    {"rows": arenas},
                )
                await pg_manager.execute(
                    "UPDATE arenas SET sync_status = 'SYNCED', synced_at = NOW() WHERE id = ANY($1::text[])",
                    [a["id"] for a in arenas],
                )
                counts["arenas"] = len(arenas)

            registers = await pg_manager.fetch_all(
                f"""
                SELECT id, lang_code, tier, flag, name, subtitle, family, address_form,
                       phonetic_rhythm, intimacy_trick, posture, paired_register_id, partition_file
                FROM registers {where_clause}
                """
            )
            if registers:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (r:Register {id: row.id})
                    SET r:Persona,
                        r.lang_code = row.lang_code,
                        r.tier = row.tier,
                        r.register_type = CASE WHEN row.tier = 'FORMAL' THEN 'FORMAL_EXAM' ELSE 'REGIONAL_RIFF' END,
                        r.flag = row.flag,
                        r.name = row.name,
                        r.subtitle = row.subtitle,
                        r.family = row.family,
                        r.address_form = row.address_form,
                        r.rhythm = row.phonetic_rhythm,
                        r.trick = row.intimacy_trick,
                        r.posture = row.posture,
                        r.partition_file = row.partition_file
                    FOREACH (_ IN CASE WHEN row.tier = 'FORMAL' THEN [1] ELSE [] END | SET r:FORMAL_EXAM)
                    FOREACH (_ IN CASE WHEN row.tier = 'REGIONAL' THEN [1] ELSE [] END | SET r:REGIONAL_RIFF)
                    WITH r, row
                    MATCH (l:Language {code: row.lang_code})
                    MERGE (l)-[:HAS_REGISTER]->(r)
                    """,
                    {"rows": registers},
                )
                paired = [r for r in registers if r.get("paired_register_id")]
                if paired:
                    await neo4j_manager.run_query(
                        """
                        UNWIND $rows AS row
                        MATCH (r1:Register {id: row.id}), (r2:Register {id: row.paired_register_id})
                        MERGE (r1)-[p:PAIRS_WITH]->(r2)
                        SET p.direction = CASE WHEN row.tier = 'FORMAL' THEN 'REGISTER_DROP' ELSE 'REGISTER_ESCALATE' END
                        """,
                        {"rows": paired},
                    )
                await pg_manager.execute(
                    "UPDATE registers SET sync_status = 'SYNCED', synced_at = NOW() WHERE id = ANY($1::text[])",
                    [r["id"] for r in registers],
                )
                counts["registers"] = len(registers)

            idioms = await pg_manager.fetch_all(
                f"""
                SELECT term, register_id, origin, meaning, delivery_cue, cousin_term
                FROM idioms {where_clause}
                """
            )
            if idioms:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (i:Idiom {term: row.term})
                    SET i.lang = row.register_id,
                        i.register_id = row.register_id,
                        i.origin = row.origin,
                        i.meaning = row.meaning,
                        i.delivery = row.delivery_cue,
                        i.cousin = row.cousin_term
                    """,
                    {"rows": idioms},
                )
                await pg_manager.execute(
                    "UPDATE idioms SET sync_status = 'SYNCED', synced_at = NOW() WHERE term = ANY($1::text[])",
                    [i["term"] for i in idioms],
                )
                counts["idioms"] = len(idioms)

            vibe_links = await pg_manager.fetch_all(
                f"SELECT source_term, target_term, shared_root, pivot_tip FROM idiom_vibe_links {where_clause}"
            )
            if vibe_links:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MATCH (i1:Idiom {term: row.source_term}), (i2:Idiom {term: row.target_term})
                    MERGE (i1)-[v:SHARES_VIBE_WITH]->(i2)
                    SET v.shared_root = row.shared_root, v.pivot_tip = row.pivot_tip
                    """,
                    {"rows": vibe_links},
                )
                await pg_manager.execute(
                    "UPDATE idiom_vibe_links SET sync_status = 'SYNCED', synced_at = NOW() WHERE sync_status = 'PENDING' OR $1",
                    force_all,
                )
                counts["vibe_links"] = len(vibe_links)

            vocab_rows = await pg_manager.fetch_all(
                f"""
                SELECT uid, term, lang_code, register_id, register_type, meaning, ib_source, grammar_note, etymology, warning
                FROM vocab_items {where_clause}
                """
            )
            if vocab_rows:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (v:Vocab {uid: row.uid})
                    SET v.term = row.term,
                        v.lang = row.lang_code,
                        v.register_id = row.register_id,
                        v.register_type = row.register_type,
                        v.meaning = row.meaning,
                        v.ib_source = row.ib_source,
                        v.grammar = row.grammar_note,
                        v.etymology = row.etymology,
                        v.warning = row.warning
                    WITH v, row
                    OPTIONAL MATCH (r:Register {id: row.register_id})
                    FOREACH (_ IN CASE WHEN r IS NOT NULL THEN [1] ELSE [] END |
                        MERGE (r)-[:CONTAINS_VOCAB]->(v)
                    )
                    """,
                    {"rows": vocab_rows},
                )
                await pg_manager.execute(
                    "UPDATE vocab_items SET sync_status = 'SYNCED', synced_at = NOW() WHERE uid = ANY($1::text[])",
                    [v["uid"] for v in vocab_rows],
                )
                counts["vocab"] = len(vocab_rows)

            vocab_alerts = await pg_manager.fetch_all(
                f"SELECT source_uid, target_uid FROM vocab_false_friend_alerts {where_clause}"
            )
            if vocab_alerts:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MATCH (v1:Vocab {uid: row.source_uid}), (v2:Vocab {uid: row.target_uid})
                    MERGE (v1)-[:FALSE_FRIEND_ALERT]->(v2)
                    """,
                    {"rows": vocab_alerts},
                )
                await pg_manager.execute(
                    "UPDATE vocab_false_friend_alerts SET sync_status = 'SYNCED', synced_at = NOW() WHERE sync_status = 'PENDING' OR $1",
                    force_all,
                )
                counts["vocab_alerts"] = len(vocab_alerts)

            song_rows = await pg_manager.fetch_all(
                f"""
                SELECT uid, title, artist, city_region, genre, bpm, register_id,
                       original_lang, original_lyric, translation_es, translation_en,
                       translation_cz, translation_de, translation_ru, cultural_vibe,
                       pivot_line, reinforces_card_uid, slang_vocab_uids
                FROM songs {where_clause}
                """
            )
            if song_rows:
                song_payload = [
                    {
                        **s,
                        "slang_vocab_uids": list(s["slang_vocab_uids"])
                        if isinstance(s.get("slang_vocab_uids"), list)
                        else [],
                    }
                    for s in song_rows
                ]
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (s:Song {uid: row.uid})
                    SET s.title = row.title,
                        s.artist = row.artist,
                        s.city_region = row.city_region,
                        s.genre = row.genre,
                        s.bpm = row.bpm,
                        s.register_id = row.register_id,
                        s.original_lang = row.original_lang,
                        s.original_lyric = row.original_lyric,
                        s.translation_es = row.translation_es,
                        s.translation_en = row.translation_en,
                        s.translation_cz = row.translation_cz,
                        s.translation_de = row.translation_de,
                        s.translation_ru = row.translation_ru,
                        s.cultural_vibe = row.cultural_vibe,
                        s.pivot_line = row.pivot_line,
                        s.reinforces_card_uid = row.reinforces_card_uid
                    WITH s, row
                    OPTIONAL MATCH (r:Register {id: row.register_id})
                    FOREACH (_ IN CASE WHEN r IS NOT NULL THEN [1] ELSE [] END |
                        MERGE (r)-[:HAS_REGIONAL_ANTHEM]->(s)
                    )
                    WITH s, row
                    OPTIONAL MATCH (c:Card {uid: row.reinforces_card_uid})
                    FOREACH (_ IN CASE WHEN c IS NOT NULL THEN [1] ELSE [] END |
                        MERGE (s)-[:REINFORCES_CARD_VIBE]->(c)
                    )
                    WITH s, row
                    UNWIND row.slang_vocab_uids AS vuid
                    MATCH (v:Vocab {uid: vuid})
                    MERGE (s)-[:INJECTS_SLANG]->(v)
                    """,
                    {"rows": song_payload},
                )
                await pg_manager.execute(
                    "UPDATE songs SET sync_status = 'SYNCED', synced_at = NOW() WHERE uid = ANY($1::text[])",
                    [s["uid"] for s in song_rows],
                )
                counts["songs"] = len(song_rows)

            cards = await pg_manager.fetch_all(
                f"""
                SELECT uid, register_id, stage, arena, lens_id, title, text_html, text_plain,
                       phonetics, english_gloss, delivery_cue, idiom_terms
                FROM cards {where_clause}
                """
            )
            if cards:
                card_payload = [
                    {
                        **c,
                        "idiom_terms": list(c["idiom_terms"]) if isinstance(c["idiom_terms"], list) else [],
                    }
                    for c in cards
                ]
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (c:Card {uid: row.uid})
                    SET c.lang = row.register_id,
                        c.register_id = row.register_id,
                        c.stage = row.stage,
                        c.arena = row.arena,
                        c.lens_id = row.lens_id,
                        c.title = row.title,
                        c.text = row.text_plain,
                        c.text_html = row.text_html,
                        c.phonetics = row.phonetics,
                        c.english_gloss = row.english_gloss,
                        c.delivery = row.delivery_cue
                    WITH c, row
                    MATCH (r:Register {id: row.register_id})
                    MERGE (r)-[:HAS_CARD]->(c)
                    WITH c, row
                    OPTIONAL MATCH (ar:Arena {id: row.arena})
                    FOREACH (_ IN CASE WHEN ar IS NOT NULL THEN [1] ELSE [] END |
                        MERGE (c)-[:SET_IN_ARENA]->(ar)
                    )
                    WITH c, row
                    UNWIND row.idiom_terms AS iterm
                    MATCH (i:Idiom {term: iterm})
                    MERGE (c)-[:INJECTS_SLANG]->(i)
                    """,
                    {"rows": card_payload},
                )
                await pg_manager.execute(
                    "UPDATE cards SET sync_status = 'SYNCED', synced_at = NOW() WHERE uid = ANY($1::text[])",
                    [c["uid"] for c in cards],
                )
                counts["cards"] = len(cards)

            states = await pg_manager.fetch_all(
                f"SELECT id, label, description, default_card_uid, effectiveness, cue FROM room_states {where_clause}"
            )
            if states:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (s:State {id: row.id})
                    SET s.label = row.label, s.description = row.description
                    """,
                    {"rows": states},
                )
                await pg_manager.execute(
                    "UPDATE room_states SET sync_status = 'SYNCED', synced_at = NOW() WHERE id = ANY($1::text[])",
                    [s["id"] for s in states],
                )
                counts["room_states"] = len(states)

            false_friends = await pg_manager.fetch_all(
                f"""
                SELECT id, target_lang, target_term, trap_lang, trap_term, calque_lang, calque_term, safe_meaning
                FROM false_friends {where_clause}
                """
            )
            if false_friends:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (f:FalseFriend {id: row.id})
                    SET f.cz_term = row.target_term,
                        f.target_lang = row.target_lang,
                        f.target_term = row.target_term,
                        f.ru_trap = row.trap_term,
                        f.de_calque = row.calque_term,
                        f.meaning = row.safe_meaning
                    WITH f, row
                    MATCH (l:Language {code: row.target_lang})-[:HAS_REGISTER]->(r:Register)
                    MERGE (r)-[:GUARDS_AGAINST]->(f)
                    """,
                    {"rows": false_friends},
                )
                await pg_manager.execute(
                    "UPDATE false_friends SET sync_status = 'SYNCED', synced_at = NOW() WHERE id = ANY($1::text[])",
                    [ff["id"] for ff in false_friends],
                )
                counts["false_friends"] = len(false_friends)

            bridges = await pg_manager.fetch_all(
                f"""
                SELECT uid, from_register_id, to_register_id, from_card_uid, to_card_uid,
                       bridge_type, text, mlf_boundary_note, vocal_cue, weight
                FROM bridges {where_clause}
                """
            )
            if bridges:
                await neo4j_manager.run_query(
                    """
                    UNWIND $rows AS row
                    MERGE (b:Bridge {uid: row.uid})
                    SET b.from_lang = row.from_register_id,
                        b.to_lang = row.to_register_id,
                        b.bridge_type = row.bridge_type,
                        b.text = row.text,
                        b.mlf_boundary_note = row.mlf_boundary_note,
                        b.vocal_cue = row.vocal_cue,
                        b.weight = row.weight
                    WITH b, row
                    MATCH (r1:Register {id: row.from_register_id}), (r2:Register {id: row.to_register_id})
                    MERGE (r1)-[:BRIDGES_TO {bridge_uid: row.uid, bridge_type: row.bridge_type}]->(r2)
                    """,
                    {"rows": bridges},
                )
                card_wired = [b for b in bridges if b.get("from_card_uid") and b.get("to_card_uid")]
                if card_wired:
                    await neo4j_manager.run_query(
                        """
                        UNWIND $rows AS row
                        MATCH (c1:Card {uid: row.from_card_uid}),
                              (b:Bridge {uid: row.uid}),
                              (c2:Card {uid: row.to_card_uid})
                        MERGE (c1)-[pv:PIVOTS_VIA]->(b)
                        SET pv.weight = row.weight, pv.context = row.bridge_type
                        MERGE (b)-[:LANDS_ON]->(c2)
                        """,
                        {"rows": card_wired},
                    )
                await pg_manager.execute(
                    "UPDATE bridges SET sync_status = 'SYNCED', synced_at = NOW() WHERE uid = ANY($1::text[])",
                    [b["uid"] for b in bridges],
                )
                counts["bridges"] = len(bridges)

            edges = await pg_manager.fetch_all(
                f"""
                SELECT id, source_uid, target_uid, edge_type, bridge_uid,
                       weight, stability, difficulty, days_ago, drills, effectiveness, cue
                FROM graph_edges {where_clause}
                """
            )
            if edges:
                flows = [e for e in edges if e["edge_type"] == "FLOWS_TO"]
                pivots = [e for e in edges if e["edge_type"] == "PIVOTS_VIA"]
                counters = [e for e in edges if e["edge_type"] == "COUNTERS_STATE"]

                if flows:
                    await neo4j_manager.run_query(
                        """
                        UNWIND $rows AS row
                        MATCH (a:Card {uid: row.source_uid}), (b:Card {uid: row.target_uid})
                        MERGE (a)-[r:FLOWS_TO {id: row.id}]->(b)
                        SET r.weight = row.weight,
                            r.stability = row.stability,
                            r.difficulty = row.difficulty,
                            r.days_ago = row.days_ago,
                            r.drills = row.drills
                        """,
                        {"rows": flows},
                    )
                if pivots:
                    await neo4j_manager.run_query(
                        """
                        UNWIND $rows AS row
                        MATCH (a:Card {uid: row.source_uid}), (b:Card {uid: row.target_uid})
                        MERGE (a)-[r:PIVOTS_VIA {id: row.id}]->(b)
                        SET r.weight = row.weight,
                            r.stability = row.stability,
                            r.difficulty = row.difficulty,
                            r.days_ago = row.days_ago,
                            r.drills = row.drills,
                            r.bridge_uid = row.bridge_uid
                        """,
                        {"rows": pivots},
                    )
                if counters:
                    await neo4j_manager.run_query(
                        """
                        UNWIND $rows AS row
                        MATCH (c:Card {uid: row.source_uid}), (s:State {id: row.target_uid})
                        MERGE (c)-[r:COUNTERS_STATE {id: row.id}]->(s)
                        SET r.effectiveness = COALESCE(row.effectiveness, row.weight),
                            r.cue = row.cue
                        """,
                        {"rows": counters},
                    )

                await pg_manager.execute(
                    "UPDATE graph_edges SET sync_status = 'SYNCED', synced_at = NOW() WHERE id = ANY($1::text[])",
                    [e["id"] for e in edges],
                )
                counts["edges"] = len(edges)

            if prune_orphans or force_all:
                pruned = await self._prune_neo4j_orphans()
                counts["pruned_orphans"] = sum(pruned.values())

            neo4j_ok = True
        except Exception as exc:
            error_msg = str(exc)

        snapshots = await self.export_db_json_snapshots()
        return {"neo4j_ok": neo4j_ok, "synced_counts": counts, "snapshots": snapshots, "error": error_msg}

    async def _prune_neo4j_orphans(self) -> dict[str, int]:
        """Reconcile Neo4j against PostgreSQL source-of-truth by pruning orphan nodes/edges."""
        card_uids = [r["uid"] for r in await pg_manager.fetch_all("SELECT uid FROM cards")]
        idiom_terms = [r["term"] for r in await pg_manager.fetch_all("SELECT term FROM idioms")]
        vocab_uids = [r["uid"] for r in await pg_manager.fetch_all("SELECT uid FROM vocab_items")]
        song_uids = [r["uid"] for r in await pg_manager.fetch_all("SELECT uid FROM songs")]
        arena_ids = [r["id"] for r in await pg_manager.fetch_all("SELECT id FROM arenas")]
        edge_ids = [r["id"] for r in await pg_manager.fetch_all("SELECT id FROM graph_edges")]

        c_res = await neo4j_manager.run_query(
            "MATCH (c:Card) WHERE NOT c.uid IN $uids WITH collect(c) AS obs FOREACH (n IN obs | DETACH DELETE n) RETURN size(obs) AS n",
            {"uids": card_uids},
        )
        i_res = await neo4j_manager.run_query(
            "MATCH (i:Idiom) WHERE NOT i.term IN $terms WITH collect(i) AS obs FOREACH (n IN obs | DETACH DELETE n) RETURN size(obs) AS n",
            {"terms": idiom_terms},
        )
        v_res = await neo4j_manager.run_query(
            "MATCH (v:Vocab) WHERE NOT v.uid IN $uids WITH collect(v) AS obs FOREACH (n IN obs | DETACH DELETE n) RETURN size(obs) AS n",
            {"uids": vocab_uids},
        )
        s_res = await neo4j_manager.run_query(
            "MATCH (s:Song) WHERE NOT s.uid IN $uids WITH collect(s) AS obs FOREACH (n IN obs | DETACH DELETE n) RETURN size(obs) AS n",
            {"uids": song_uids},
        )
        a_res = await neo4j_manager.run_query(
            "MATCH (a:Arena) WHERE NOT a.id IN $ids WITH collect(a) AS obs FOREACH (n IN obs | DETACH DELETE n) RETURN size(obs) AS n",
            {"ids": arena_ids},
        )
        e_res = await neo4j_manager.run_query(
            """
            MATCH ()-[r:FLOWS_TO|PIVOTS_VIA|COUNTERS_STATE]->()
            WHERE r.id IS NOT NULL AND NOT r.id IN $eids
            WITH collect(r) AS rels
            FOREACH (rel IN rels | DELETE rel)
            RETURN size(rels) AS n
            """,
            {"eids": edge_ids},
        )
        return {
            "cards": int(c_res[0]["n"]) if c_res else 0,
            "idioms": int(i_res[0]["n"]) if i_res else 0,
            "vocab": int(v_res[0]["n"]) if v_res else 0,
            "songs": int(s_res[0]["n"]) if s_res else 0,
            "arenas": int(a_res[0]["n"]) if a_res else 0,
            "edges": int(e_res[0]["n"]) if e_res else 0,
        }

    async def export_db_json_snapshots(self) -> list[str]:
        """Export fresh per-language db/*.db.json shards + polyglot_fabric.db.json for offline fallback & Git diffs."""
        settings.db_json_dir.mkdir(parents=True, exist_ok=True)
        written_files: list[str] = []

        registers = await pg_manager.fetch_all("SELECT * FROM registers ORDER BY lang_code, tier DESC")
        by_partition: dict[str, list[dict[str, Any]]] = {}
        for reg in registers:
            by_partition.setdefault(reg["partition_file"], []).append(reg)

        for partition_file, reg_rows in by_partition.items():
            reg_ids = [r["id"] for r in reg_rows]
            idioms = await pg_manager.fetch_all(
                "SELECT term, register_id, origin, meaning, delivery_cue, cousin_term FROM idioms WHERE register_id = ANY($1::text[]) ORDER BY term",
                reg_ids,
            )
            vocab_rows = await pg_manager.fetch_all(
                """
                SELECT uid, term, lang_code, register_id, register_type, meaning, ib_source, grammar_note, etymology, warning
                FROM vocab_items
                WHERE register_id = ANY($1::text[])
                ORDER BY register_type, uid
                """,
                reg_ids,
            )
            song_rows = await pg_manager.fetch_all(
                """
                SELECT uid, title, artist, city_region, genre, bpm, register_id,
                       original_lang, original_lyric, translation_es, translation_en,
                       translation_cz, translation_de, translation_ru, cultural_vibe,
                       pivot_line, reinforces_card_uid, slang_vocab_uids
                FROM songs
                WHERE register_id = ANY($1::text[])
                ORDER BY uid
                """,
                reg_ids,
            )
            cards = await pg_manager.fetch_all(
                """
                SELECT uid, register_id, stage, arena, lens_id, text_html, phonetics, english_gloss, idiom_terms
                FROM cards
                WHERE register_id = ANY($1::text[])
                ORDER BY arena, uid
                """,
                reg_ids,
            )
            primary_reg = next((r for r in reg_rows if r["tier"] == "REGIONAL"), reg_rows[0])
            shard_doc = {
                "db_id": f"polyglot.{partition_file.replace('.db.json', '')}",
                "primary_focus": f"{primary_reg['id']} ({primary_reg['name']})",
                "registers": reg_ids,
                "personas": {
                    r["id"]: {
                        "id": r["id"],
                        "tier": r["tier"],
                        "flag": r["flag"],
                        "name": r["name"],
                        "subtitle": r["subtitle"],
                        "family": r["family"],
                        "address_form": r["address_form"],
                        "rhythm": r["phonetic_rhythm"],
                        "trick": r["intimacy_trick"],
                        "posture": r["posture"],
                        "paired_register_id": r["paired_register_id"],
                    }
                    for r in reg_rows
                },
                "idioms": {
                    i["term"]: {
                        "term": i["term"],
                        "lang": i["register_id"],
                        "origin": i["origin"],
                        "meaning": i["meaning"],
                        "delivery": i["delivery_cue"],
                        "cousin": i["cousin_term"],
                    }
                    for i in idioms
                },
                "vocab": [
                    {
                        "uid": v["uid"],
                        "term": v["term"],
                        "lang_code": v["lang_code"],
                        "register_id": v["register_id"],
                        "register_type": v["register_type"],
                        "meaning": v["meaning"],
                        "ib_source": v["ib_source"],
                        "grammar_note": v["grammar_note"],
                        "etymology": v["etymology"],
                        "warning": v["warning"],
                    }
                    for v in vocab_rows
                ],
                "songs": [
                    {
                        "uid": s["uid"],
                        "title": s["title"],
                        "artist": s["artist"],
                        "city_region": s["city_region"],
                        "genre": s["genre"],
                        "bpm": s["bpm"],
                        "register_id": s["register_id"],
                        "original_lang": s["original_lang"],
                        "original_lyric": s["original_lyric"],
                        "translation_es": s["translation_es"],
                        "translation_en": s["translation_en"],
                        "translation_cz": s["translation_cz"],
                        "translation_de": s["translation_de"],
                        "translation_ru": s["translation_ru"],
                        "cultural_vibe": s["cultural_vibe"],
                        "pivot_line": s["pivot_line"],
                        "reinforces_card_uid": s["reinforces_card_uid"],
                        "slang_vocab_uids": list(s.get("slang_vocab_uids") or []),
                    }
                    for s in song_rows
                ],
                "cards": [
                    {
                        "uid": c["uid"],
                        "lang": c["register_id"],
                        "stage": c["stage"],
                        "arena": c["arena"],
                        "lens": c["lens_id"],
                        "text": c["text_html"],
                        "phonetics": c["phonetics"],
                        "english": c["english_gloss"],
                        "idioms": c["idiom_terms"],
                    }
                    for c in cards
                ],
            }
            target_path = settings.db_json_dir / partition_file
            _atomic_write_json(target_path, shard_doc)
            written_files.append(partition_file)

        arenas = await pg_manager.fetch_all("SELECT id, icon, label, short_label, arena_group, description FROM arenas ORDER BY id")
        bridges = await pg_manager.fetch_all("SELECT * FROM bridges ORDER BY uid")
        vibe_links = await pg_manager.fetch_all("SELECT * FROM idiom_vibe_links ORDER BY source_term")
        room_states = await pg_manager.fetch_all("SELECT * FROM room_states ORDER BY id")
        false_friends = await pg_manager.fetch_all("SELECT * FROM false_friends ORDER BY id")
        vocab_alert_nodes = await pg_manager.fetch_all(
            "SELECT uid, term, lang_code, register_type, meaning, ib_source, warning FROM vocab_items WHERE register_id IS NULL ORDER BY uid"
        )
        vocab_alert_edges = await pg_manager.fetch_all(
            "SELECT source_uid, target_uid FROM vocab_false_friend_alerts ORDER BY source_uid, target_uid"
        )
        all_songs = await pg_manager.fetch_all(
            """
            SELECT uid, title, artist, city_region, genre, bpm, register_id,
                   original_lang, original_lyric, translation_es, translation_en,
                   translation_cz, translation_de, translation_ru, cultural_vibe,
                   pivot_line, reinforces_card_uid, slang_vocab_uids
            FROM songs
            ORDER BY uid
            """
        )
        webhooks = await pg_manager.fetch_all(
            "SELECT * FROM staged_webhooks WHERE status = 'STAGED' ORDER BY created_at ASC"
        )

        fabric_doc = {
            "db_id": "polyglot.fabric",
            "schema_version": SCHEMA_VERSION,
            "description": "Cross-language :Arena rooms, :Bridge nodes, :SHARES_VIBE_WITH etymology edges, :State objection nodes, :FalseFriend traps, IB :Vocab :FALSE_FRIEND_ALERT triggers, and Staged Regional Newspaper Webhooks.",
            "arenas": arenas,
            "bridges": [
                {
                    "uid": b["uid"],
                    "from_register": b["from_register_id"],
                    "to_register": b["to_register_id"],
                    "from": b["from_card_uid"],
                    "to": b["to_card_uid"],
                    "bridge_type": b["bridge_type"],
                    "text": b["text"],
                    "vocal_cue": b["vocal_cue"],
                    "weight": b["weight"],
                }
                for b in bridges
            ],
            "vibe_links": [
                {
                    "source_term": v["source_term"],
                    "target_term": v["target_term"],
                    "shared_root": v["shared_root"],
                    "pivot_tip": v["pivot_tip"],
                }
                for v in vibe_links
            ],
            "room_states": [
                {
                    "id": s["id"],
                    "label": s["label"],
                    "desc": s["description"],
                    "targetCardUid": s["default_card_uid"],
                    "lang": s["default_register_id"],
                    "effectiveness": s["effectiveness"],
                    "cue": s["cue"],
                }
                for s in room_states
            ],
            "false_friends": [
                {
                    "id": ff["id"],
                    "cz": ff["target_term"],
                    "ru_trap": ff["trap_term"],
                    "de_calque": ff["calque_term"],
                    "meaning": ff["safe_meaning"],
                }
                for ff in false_friends
            ],
            "vocab_alert_nodes": vocab_alert_nodes,
            "vocab_false_friend_alerts": vocab_alert_edges,
            "songs": [
                {
                    "uid": s["uid"],
                    "title": s["title"],
                    "artist": s["artist"],
                    "city_region": s["city_region"],
                    "genre": s["genre"],
                    "bpm": s["bpm"],
                    "register_id": s["register_id"],
                    "original_lang": s["original_lang"],
                    "original_lyric": s["original_lyric"],
                    "translation_es": s["translation_es"],
                    "translation_en": s["translation_en"],
                    "translation_cz": s["translation_cz"],
                    "translation_de": s["translation_de"],
                    "translation_ru": s["translation_ru"],
                    "cultural_vibe": s["cultural_vibe"],
                    "pivot_line": s["pivot_line"],
                    "reinforces_card_uid": s["reinforces_card_uid"],
                    "slang_vocab_uids": list(s.get("slang_vocab_uids") or []),
                }
                for s in all_songs
            ],
            "staged_webhooks": [w["payload_json"] for w in webhooks],
        }
        fabric_path = settings.db_json_dir / "polyglot_fabric.db.json"
        _atomic_write_json(fabric_path, fabric_doc)
        written_files.append("polyglot_fabric.db.json")
        return written_files

    def export_offline_db_json_from_seed(self) -> list[str]:
        """Generate db/*.db.json shards directly from backend.seed.corpus_data without requiring live Postgres."""
        from backend.seed.corpus_data import (
            ARENAS,
            BRIDGES,
            CARDS,
            FALSE_FRIENDS,
            IDIOMS,
            REGISTERS,
            ROOM_STATES,
            SONGS,
            STAGED_WEBHOOKS,
            VIBE_LINKS,
            VOCAB_FALSE_FRIEND_ALERTS,
            VOCAB_ITEMS,
        )

        settings.db_json_dir.mkdir(parents=True, exist_ok=True)
        written_files: list[str] = []

        by_partition: dict[str, list[dict[str, Any]]] = {}
        for reg in REGISTERS:
            by_partition.setdefault(reg["partition_file"], []).append(reg)

        for partition_file, reg_rows in by_partition.items():
            reg_ids = [r["id"] for r in reg_rows]
            idioms = sorted(
                [i for i in IDIOMS if i["register_id"] in reg_ids],
                key=lambda x: x["term"],
            )
            vocab_rows = sorted(
                [v for v in VOCAB_ITEMS if v.get("register_id") in reg_ids],
                key=lambda x: (x.get("register_type", ""), x["uid"]),
            )
            song_rows = sorted(
                [s for s in SONGS if s.get("register_id") in reg_ids],
                key=lambda x: x["uid"],
            )
            cards = sorted(
                [c for c in CARDS if c["register_id"] in reg_ids],
                key=lambda x: (x.get("arena", "terrace"), x["uid"]),
            )
            primary_reg = next((r for r in reg_rows if r["tier"] == "REGIONAL"), reg_rows[0])
            shard_doc = {
                "db_id": f"polyglot.{partition_file.replace('.db.json', '')}",
                "primary_focus": f"{primary_reg['id']} ({primary_reg['name']})",
                "registers": reg_ids,
                "personas": {
                    r["id"]: {
                        "id": r["id"],
                        "tier": r["tier"],
                        "flag": r["flag"],
                        "name": r["name"],
                        "subtitle": r["subtitle"],
                        "family": r["family"],
                        "address_form": r["address_form"],
                        "rhythm": r["phonetic_rhythm"],
                        "trick": r["intimacy_trick"],
                        "posture": r["posture"],
                        "paired_register_id": r["paired_register_id"],
                    }
                    for r in reg_rows
                },
                "idioms": {
                    i["term"]: {
                        "term": i["term"],
                        "lang": i["register_id"],
                        "origin": i["origin"],
                        "meaning": i["meaning"],
                        "delivery": i["delivery_cue"],
                        "cousin": i["cousin_term"],
                    }
                    for i in idioms
                },
                "vocab": [
                    {
                        "uid": v["uid"],
                        "term": v["term"],
                        "lang_code": v["lang_code"],
                        "register_id": v["register_id"],
                        "register_type": v["register_type"],
                        "meaning": v["meaning"],
                        "ib_source": v.get("ib_source", ""),
                        "grammar_note": v.get("grammar_note", ""),
                        "etymology": v.get("etymology", ""),
                        "warning": v.get("warning", ""),
                    }
                    for v in vocab_rows
                ],
                "songs": [
                    {
                        "uid": s["uid"],
                        "title": s["title"],
                        "artist": s["artist"],
                        "city_region": s["city_region"],
                        "genre": s["genre"],
                        "bpm": s["bpm"],
                        "register_id": s["register_id"],
                        "original_lang": s["original_lang"],
                        "original_lyric": s["original_lyric"],
                        "translation_es": s["translation_es"],
                        "translation_en": s["translation_en"],
                        "translation_cz": s["translation_cz"],
                        "translation_de": s["translation_de"],
                        "translation_ru": s["translation_ru"],
                        "cultural_vibe": s["cultural_vibe"],
                        "pivot_line": s["pivot_line"],
                        "reinforces_card_uid": s["reinforces_card_uid"],
                        "slang_vocab_uids": s.get("slang_vocab_uids", []),
                    }
                    for s in song_rows
                ],
                "cards": [
                    {
                        "uid": c["uid"],
                        "lang": c["register_id"],
                        "stage": c["stage"],
                        "arena": c.get("arena", "terrace"),
                        "lens": c.get("lens_id"),
                        "text": c["text_html"],
                        "phonetics": c.get("phonetics", ""),
                        "english": c.get("english_gloss", ""),
                        "idioms": c.get("idiom_terms", []),
                    }
                    for c in cards
                ],
            }
            target_path = settings.db_json_dir / partition_file
            _atomic_write_json(target_path, shard_doc)
            written_files.append(partition_file)

        fabric_doc = {
            "db_id": "polyglot.fabric",
            "schema_version": SCHEMA_VERSION,
            "description": "Cross-language :Arena rooms, :Bridge nodes, :SHARES_VIBE_WITH etymology edges, :State objection nodes, :FalseFriend traps, IB :Vocab :FALSE_FRIEND_ALERT triggers, and Staged Regional Newspaper Webhooks.",
            "arenas": ARENAS,
            "bridges": [
                {
                    "uid": b["uid"],
                    "from_register": b["from_register_id"],
                    "to_register": b["to_register_id"],
                    "from": b["from_card_uid"],
                    "to": b["to_card_uid"],
                    "bridge_type": b["bridge_type"],
                    "text": b["text"],
                    "vocal_cue": b["vocal_cue"],
                    "weight": b["weight"],
                }
                for b in BRIDGES
            ],
            "vibe_links": VIBE_LINKS,
            "room_states": [
                {
                    "id": s["id"],
                    "label": s["label"],
                    "desc": s["description"],
                    "targetCardUid": s["default_card_uid"],
                    "lang": s["default_register_id"],
                    "effectiveness": s["effectiveness"],
                    "cue": s["cue"],
                }
                for s in ROOM_STATES
            ],
            "false_friends": [
                {
                    "id": ff["id"],
                    "cz": ff["target_term"],
                    "ru_trap": ff["trap_term"],
                    "de_calque": ff["calque_term"],
                    "meaning": ff["safe_meaning"],
                }
                for ff in FALSE_FRIENDS
            ],
            "vocab_alert_nodes": [
                {
                    "uid": v["uid"],
                    "term": v["term"],
                    "lang_code": v["lang_code"],
                    "register_type": v["register_type"],
                    "meaning": v["meaning"],
                    "ib_source": v.get("ib_source", ""),
                    "warning": v.get("warning", ""),
                }
                for v in VOCAB_ITEMS
                if v.get("register_id") is None
            ],
            "vocab_false_friend_alerts": VOCAB_FALSE_FRIEND_ALERTS,
            "songs": SONGS,
            "staged_webhooks": STAGED_WEBHOOKS,
        }
        fabric_path = settings.db_json_dir / "polyglot_fabric.db.json"
        _atomic_write_json(fabric_path, fabric_doc)
        written_files.append("polyglot_fabric.db.json")
        return written_files

    async def audit_data_integrity(self) -> dict[str, Any]:
        """Run end-to-end 4-layer data integrity audit across PostgreSQL, Neo4j, and db/*.db.json shards."""
        checks: list[dict[str, Any]] = []
        pg_info = await pg_manager.ping()
        neo_info = await neo4j_manager.ping()

        checks.append(
            {
                "check": "postgresql_online_and_pgvector",
                "ok": bool(pg_info.get("ok") and pg_info.get("pgvector")),
                "detail": pg_info.get("version", pg_info.get("error")),
            }
        )
        checks.append(
            {
                "check": "neo4j_online_and_apoc",
                "ok": bool(neo_info.get("ok") and neo_info.get("apoc_version")),
                "detail": f"APOC {neo_info.get('apoc_version')}" if neo_info.get("ok") else neo_info.get("error"),
            }
        )

        if not pg_info.get("ok"):
            return {"ok": False, "checks": checks, "postgres": pg_info, "neo4j": neo_info}

        fk_row = await pg_manager.fetch_one(
            "SELECT conname FROM pg_constraint WHERE conname = 'fk_cards_arena'"
        )
        checks.append(
            {
                "check": "postgres_fk_cards_arena_enforced",
                "ok": bool(fk_row),
                "detail": "cards.arena -> arenas(id)",
            }
        )

        pg_counts = await pg_manager.fetch_one(
            """
            SELECT
                (SELECT COUNT(*) FROM languages) AS languages,
                (SELECT COUNT(*) FROM arenas) AS arenas,
                (SELECT COUNT(*) FROM registers) AS registers,
                (SELECT COUNT(*) FROM cards) AS cards,
                (SELECT COUNT(*) FROM idioms) AS idioms,
                (SELECT COUNT(*) FROM vocab_items) AS vocab,
                (SELECT COUNT(*) FROM songs) AS songs,
                (SELECT COUNT(*) FROM bridges) AS bridges,
                (SELECT COUNT(*) FROM room_states) AS room_states,
                (SELECT COUNT(*) FROM false_friends) AS false_friends,
                (SELECT COUNT(*) FROM graph_edges) AS edges,
                (SELECT COUNT(*) FROM cards WHERE embedding IS NULL) AS cards_missing_embeddings,
                (SELECT COUNT(*) FROM idioms WHERE embedding IS NULL) AS idioms_missing_embeddings,
                (SELECT COUNT(*) FROM arenas WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM registers WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM cards WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM idioms WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM vocab_items WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM songs WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM bridges WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM room_states WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM false_friends WHERE sync_status = 'PENDING')
                + (SELECT COUNT(*) FROM graph_edges WHERE sync_status = 'PENDING') AS pending_outbox
            """
        ) or {}

        checks.append(
            {
                "check": "outbox_zero_pending_drift",
                "ok": int(pg_counts.get("pending_outbox", 1)) == 0,
                "detail": f"pending_outbox={pg_counts.get('pending_outbox', 0)}",
            }
        )
        checks.append(
            {
                "check": "bge_m3_vector_coverage",
                "ok": int(pg_counts.get("cards_missing_embeddings", 0)) == 0
                and int(pg_counts.get("idioms_missing_embeddings", 0)) == 0,
                "detail": (
                    f"cards_missing={pg_counts.get('cards_missing_embeddings', 0)}, "
                    f"idioms_missing={pg_counts.get('idioms_missing_embeddings', 0)}"
                ),
            }
        )

        # Validate structural & FSRS rules on every card and edge in Postgres
        all_cards = await pg_manager.fetch_all("SELECT uid, register_id, stage, text_html, idiom_terms FROM cards")
        all_idioms = {
            r["term"]: r
            for r in await pg_manager.fetch_all("SELECT term, register_id, cousin_term FROM idioms")
        }
        all_edges = await pg_manager.fetch_all("SELECT id, source_uid, target_uid, edge_type, weight, stability FROM graph_edges")
        card_uid_set = {c["uid"] for c in all_cards}
        state_id_set = {s["id"] for s in await pg_manager.fetch_all("SELECT id FROM room_states")}

        rule_failures: list[str] = []
        for c in all_cards:
            terms = list(c["idiom_terms"]) if isinstance(c["idiom_terms"], list) else []
            first_idiom = all_idioms.get(terms[0]) if terms else None
            idiom_arg = (
                {
                    "term": first_idiom["term"],
                    "register_id": first_idiom["register_id"],
                    "cousin": first_idiom["cousin_term"],
                }
                if first_idiom
                else None
            )
            val = validate_graph_commit(
                card={
                    "uid": c["uid"],
                    "register_id": c["register_id"],
                    "stage": c["stage"],
                    "text_html": c["text_html"],
                    "idiom_terms": terms,
                },
                idiom=idiom_arg,
                target_register=c["register_id"],
            )
            if not val["valid"]:
                rule_failures.append(f"Card {c['uid']}: {val['checks']}")

        dangling_edges: list[str] = []
        for e in all_edges:
            if e["source_uid"] not in card_uid_set:
                dangling_edges.append(f"{e['id']} missing source {e['source_uid']}")
            if e["edge_type"] in ("FLOWS_TO", "PIVOTS_VIA") and e["target_uid"] not in card_uid_set:
                dangling_edges.append(f"{e['id']} missing target card {e['target_uid']}")
            if e["edge_type"] == "COUNTERS_STATE" and e["target_uid"] not in state_id_set:
                dangling_edges.append(f"{e['id']} missing target state {e['target_uid']}")
            if not (0.15 <= float(e["weight"]) <= 0.99) or float(e["stability"]) < 1.5:
                rule_failures.append(f"Edge {e['id']} out-of-bounds FSRS weight/stability")

        checks.append(
            {
                "check": "graph_relation_and_fsrs_rules",
                "ok": len(rule_failures) == 0 and len(dangling_edges) == 0,
                "detail": f"rule_failures={len(rule_failures)}, dangling_edges={len(dangling_edges)}",
            }
        )

        neo_parity: dict[str, Any] = {}
        if neo_info.get("ok"):
            neo_rows = await neo4j_manager.run_query(
                """
                RETURN
                     COUNT { (:Language) } AS languages,
                     COUNT { (:Arena) } AS arenas,
                     COUNT { (:Register) } AS registers,
                     COUNT { (:Card) } AS cards,
                     COUNT { (:Idiom) } AS idioms,
                     COUNT { (:Vocab) } AS vocab,
                     COUNT { (:Song) } AS songs,
                     COUNT { (:Bridge) } AS bridges,
                     COUNT { (:State) } AS room_states,
                     COUNT { (:FalseFriend) } AS false_friends,
                     COUNT { (:Card)-[:FLOWS_TO]->(:Card) }
                     + COUNT { (:Card)-[r:PIVOTS_VIA]->(:Card) WHERE r.id IS NOT NULL }
                     + COUNT { (:Card)-[:COUNTERS_STATE]->(:State) } AS edges,
                     COUNT { (c:Card) WHERE NOT (:Register)-[:HAS_CARD]->(c) } AS orphan_cards,
                     COUNT { (c:Card) WHERE NOT (c)-[:SET_IN_ARENA]->(:Arena) } AS cards_without_arena
                """
            )
            neo_parity = dict(neo_rows[0]) if neo_rows else {}
            compared_keys = (
                "languages",
                "arenas",
                "registers",
                "cards",
                "idioms",
                "vocab",
                "songs",
                "bridges",
                "room_states",
                "false_friends",
                "edges",
            )
            mismatches = {
                k: {"postgres": int(pg_counts.get(k, -1)), "neo4j": int(neo_parity.get(k, -2))}
                for k in compared_keys
                if int(pg_counts.get(k, -1)) != int(neo_parity.get(k, -2))
            }
            checks.append(
                {
                    "check": "postgres_neo4j_entity_parity",
                    "ok": len(mismatches) == 0,
                    "detail": "100% count match across all 11 entity/edge classes" if not mismatches else mismatches,
                }
            )
            checks.append(
                {
                    "check": "neo4j_zero_orphan_cards_and_full_arena_wiring",
                    "ok": int(neo_parity.get("orphan_cards", 1)) == 0
                    and int(neo_parity.get("cards_without_arena", 1)) == 0,
                    "detail": (
                        f"orphan_cards={neo_parity.get('orphan_cards', 0)}, "
                        f"cards_without_arena={neo_parity.get('cards_without_arena', 0)}"
                    ),
                }
            )

        # Audit db/*.db.json offline shards
        expected_shards = ["cz_ova.db.json", "at_vie.db.json", "ru_ala.db.json", "en_yyc.db.json", "es_sot.db.json"]
        shard_cards_total = 0
        shard_idioms_total = 0
        shard_vocab_total = 0
        shard_songs_total = 0
        shard_digests: dict[str, str] = {}
        missing_shards: list[str] = []
        for sname in expected_shards + ["polyglot_fabric.db.json"]:
            spath = settings.db_json_dir / sname
            if not spath.exists():
                missing_shards.append(sname)
                continue
            raw = spath.read_bytes()
            shard_digests[sname] = hashlib.sha256(raw).hexdigest()
            parsed = json.loads(raw.decode("utf-8"))
            if sname != "polyglot_fabric.db.json":
                shard_cards_total += len(parsed.get("cards", []))
                shard_idioms_total += len(parsed.get("idioms", {}))
                shard_vocab_total += len(parsed.get("vocab", []))
            else:
                fabric_arenas = len(parsed.get("arenas", []))
                shard_vocab_total += len(parsed.get("vocab_alert_nodes", []))
                shard_songs_total = len(parsed.get("songs", []))
                if fabric_arenas != int(pg_counts.get("arenas", 0)):
                    missing_shards.append(f"polyglot_fabric.arenas={fabric_arenas}")

        shard_parity_ok = (
            len(missing_shards) == 0
            and shard_cards_total == int(pg_counts.get("cards", -1))
            and shard_idioms_total == int(pg_counts.get("idioms", -1))
            and shard_vocab_total == int(pg_counts.get("vocab", -1))
            and shard_songs_total == int(pg_counts.get("songs", -1))
        )
        checks.append(
            {
                "check": "offline_db_json_shard_parity",
                "ok": shard_parity_ok,
                "detail": (
                    f"shards=6/6, cards={shard_cards_total}/{pg_counts.get('cards')}, "
                    f"idioms={shard_idioms_total}/{pg_counts.get('idioms')}, "
                    f"vocab={shard_vocab_total}/{pg_counts.get('vocab')}, "
                    f"songs={shard_songs_total}/{pg_counts.get('songs')}"
                    if not missing_shards
                    else f"issues={missing_shards}"
                ),
            }
        )

        overall_ok = all(bool(c["ok"]) for c in checks)
        return {
            "ok": overall_ok,
            "audited_at": datetime.now(timezone.utc).isoformat(),
            "schema_version": pg_info.get("schema_version", SCHEMA_VERSION),
            "checks": checks,
            "postgres_counts": pg_counts,
            "neo4j_counts": neo_parity,
            "shard_sha256": shard_digests,
        }

    async def create_backup_snapshot(self, keep_last: int = 10) -> dict[str, Any]:
        """Write an atomic, SHA-256-verified backup snapshot (PostgreSQL JSON dump + Neo4j Cypher + manifest) with retention."""
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backups_root = settings.root_dir / "backups"
        snap_dir = backups_root / f"snapshot_{ts}"
        snap_dir.mkdir(parents=True, exist_ok=True)

        table_queries = {
            "schema_meta": "SELECT * FROM schema_meta ORDER BY key",
            "languages": "SELECT * FROM languages ORDER BY code",
            "arenas": "SELECT * FROM arenas ORDER BY id",
            "registers": "SELECT * FROM registers ORDER BY id",
            "style_lenses": "SELECT * FROM style_lenses ORDER BY id",
            "idioms": (
                "SELECT term, register_id, origin, meaning, delivery_cue, cousin_term, "
                "(embedding IS NOT NULL) AS has_embedding, sync_status, synced_at, updated_at "
                "FROM idioms ORDER BY term"
            ),
            "idiom_vibe_links": "SELECT * FROM idiom_vibe_links ORDER BY source_term, target_term",
            "cards": (
                "SELECT uid, register_id, stage, arena, lens_id, title, register_drop_note, "
                "text_html, text_plain, phonetics, english_gloss, delivery_cue, idiom_terms, "
                "(embedding IS NOT NULL) AS has_embedding, sync_status, synced_at, updated_at "
                "FROM cards ORDER BY uid"
            ),
            "lexical_scaffolds": "SELECT * FROM lexical_scaffolds ORDER BY id",
            "false_friends": "SELECT * FROM false_friends ORDER BY id",
            "room_states": "SELECT * FROM room_states ORDER BY id",
            "bridges": "SELECT * FROM bridges ORDER BY uid",
            "graph_edges": "SELECT * FROM graph_edges ORDER BY id",
            "fsrs_review_events": "SELECT * FROM fsrs_review_events ORDER BY id",
            "staged_webhooks": "SELECT * FROM staged_webhooks ORDER BY created_at",
            "vocab_items": "SELECT * FROM vocab_items ORDER BY uid",
            "vocab_false_friend_alerts": "SELECT * FROM vocab_false_friend_alerts ORDER BY source_uid, target_uid",
            "songs": "SELECT * FROM songs ORDER BY uid",
        }

        tables_dump: dict[str, list[dict[str, Any]]] = {}
        row_counts: dict[str, int] = {}
        for tname, sql in table_queries.items():
            rows = await pg_manager.fetch_all(sql)
            tables_dump[tname] = rows
            row_counts[tname] = len(rows)

        pg_dump_path = snap_dir / "postgres_full_dump.json"
        pg_sha = _atomic_write_json(
            pg_dump_path,
            {
                "snapshot_id": f"snapshot_{ts}",
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "schema_version": SCHEMA_VERSION,
                "row_counts": row_counts,
                "tables": tables_dump,
            },
        )

        def _esc(val: Any) -> str:
            return str(val or "").replace("\\", "\\\\").replace("'", "\\'")

        cypher_lines = [
            "// =====================================================================",
            f"// POLYGLOT RIFF ATELIER — NEO4J RECONSTRUCTION SNAPSHOT ({ts})",
            "// =====================================================================",
            "CREATE CONSTRAINT language_code_unique IF NOT EXISTS FOR (l:Language) REQUIRE l.code IS UNIQUE;",
            "CREATE CONSTRAINT arena_id_unique IF NOT EXISTS FOR (a:Arena) REQUIRE a.id IS UNIQUE;",
            "CREATE CONSTRAINT register_id_unique IF NOT EXISTS FOR (r:Register) REQUIRE r.id IS UNIQUE;",
            "CREATE CONSTRAINT card_uid_unique IF NOT EXISTS FOR (c:Card) REQUIRE c.uid IS UNIQUE;",
            "CREATE CONSTRAINT idiom_term_unique IF NOT EXISTS FOR (i:Idiom) REQUIRE i.term IS UNIQUE;",
            "CREATE CONSTRAINT vocab_uid_unique IF NOT EXISTS FOR (v:Vocab) REQUIRE v.uid IS UNIQUE;",
            "CREATE CONSTRAINT song_uid_unique IF NOT EXISTS FOR (s:Song) REQUIRE s.uid IS UNIQUE;",
            "CREATE CONSTRAINT state_id_unique IF NOT EXISTS FOR (s:State) REQUIRE s.id IS UNIQUE;",
            "CREATE CONSTRAINT ff_id_unique IF NOT EXISTS FOR (f:FalseFriend) REQUIRE f.id IS UNIQUE;",
            "CREATE CONSTRAINT bridge_uid_unique IF NOT EXISTS FOR (b:Bridge) REQUIRE b.uid IS UNIQUE;",
            "",
        ]
        for ar in tables_dump["arenas"]:
            cypher_lines.append(
                f"MERGE (a:Arena {{id: '{_esc(ar['id'])}'}}) "
                f"SET a.icon = '{_esc(ar['icon'])}', a.label = '{_esc(ar['label'])}', "
                f"a.short_label = '{_esc(ar['short_label'])}', a.arena_group = '{_esc(ar['arena_group'])}';"
            )
        for reg in tables_dump["registers"]:
            reg_label = ":FORMAL_EXAM" if reg["tier"] == "FORMAL" else ":REGIONAL_RIFF"
            cypher_lines.append(
                f"MERGE (r:Register {{id: '{_esc(reg['id'])}'}}) "
                f"SET r:Persona{reg_label}, r.lang_code = '{_esc(reg['lang_code'])}', r.tier = '{_esc(reg['tier'])}', "
                f"r.name = '{_esc(reg['name'])}', r.partition_file = '{_esc(reg['partition_file'])}';"
            )
        for idm in tables_dump["idioms"]:
            cypher_lines.append(
                f"MERGE (i:Idiom {{term: '{_esc(idm['term'])}'}}) "
                f"SET i.register_id = '{_esc(idm['register_id'])}', i.origin = '{_esc(idm['origin'])}', "
                f"i.meaning = '{_esc(idm['meaning'])}', i.cousin = '{_esc(idm['cousin_term'])}';"
            )
        for voc in tables_dump["vocab_items"]:
            cypher_lines.append(
                f"MERGE (v:Vocab {{uid: '{_esc(voc['uid'])}'}}) "
                f"SET v.term = '{_esc(voc['term'])}', v.lang_code = '{_esc(voc['lang_code'])}', "
                f"v.register_type = '{_esc(voc['register_type'])}', v.meaning = '{_esc(voc['meaning'])}', "
                f"v.ib_source = '{_esc(voc['ib_source'])}', v.grammar_note = '{_esc(voc['grammar_note'])}', "
                f"v.etymology = '{_esc(voc['etymology'])}', v.warning = '{_esc(voc['warning'])}';"
            )
            if voc.get("register_id"):
                cypher_lines.append(
                    f"MATCH (r:Register {{id: '{_esc(voc['register_id'])}'}}), (v:Vocab {{uid: '{_esc(voc['uid'])}'}}) "
                    f"MERGE (r)-[:CONTAINS_VOCAB]->(v);"
                )
        for fa in tables_dump["vocab_false_friend_alerts"]:
            cypher_lines.append(
                f"MATCH (a:Vocab {{uid: '{_esc(fa['source_uid'])}'}}), (b:Vocab {{uid: '{_esc(fa['target_uid'])}'}}) "
                f"MERGE (a)-[:FALSE_FRIEND_ALERT]->(b);"
            )
        for sng in tables_dump["songs"]:
            cypher_lines.append(
                f"MERGE (s:Song {{uid: '{_esc(sng['uid'])}'}}) "
                f"SET s.title = '{_esc(sng['title'])}', s.artist = '{_esc(sng['artist'])}', "
                f"s.city_region = '{_esc(sng['city_region'])}', s.genre = '{_esc(sng['genre'])}', "
                f"s.bpm = {int(sng['bpm'])}, s.original_lang = '{_esc(sng['original_lang'])}', "
                f"s.original_lyric = '{_esc(sng['original_lyric'])}', s.cultural_vibe = '{_esc(sng['cultural_vibe'])}', "
                f"s.pivot_line = '{_esc(sng['pivot_line'])}';"
            )
            if sng.get("register_id"):
                cypher_lines.append(
                    f"MATCH (r:Register {{id: '{_esc(sng['register_id'])}'}}), (s:Song {{uid: '{_esc(sng['uid'])}'}}) "
                    f"MERGE (r)-[:HAS_REGIONAL_ANTHEM]->(s);"
                )
            if sng.get("reinforces_card_uid"):
                cypher_lines.append(
                    f"MATCH (s:Song {{uid: '{_esc(sng['uid'])}'}}), (c:Card {{uid: '{_esc(sng['reinforces_card_uid'])}'}}) "
                    f"MERGE (s)-[:REINFORCES_CARD_VIBE]->(c);"
                )
            for vuid in (sng.get("slang_vocab_uids") or []):
                cypher_lines.append(
                    f"MATCH (s:Song {{uid: '{_esc(sng['uid'])}'}}), (v:Vocab {{uid: '{_esc(vuid)}'}}) "
                    f"MERGE (s)-[:INJECTS_SLANG]->(v);"
                )
        for c in tables_dump["cards"]:
            cypher_lines.append(
                f"MERGE (c:Card {{uid: '{_esc(c['uid'])}'}}) "
                f"SET c.register_id = '{_esc(c['register_id'])}', c.stage = '{_esc(c['stage'])}', "
                f"c.arena = '{_esc(c['arena'])}', c.text = '{_esc(c['text_plain'])}';"
            )
            cypher_lines.append(
                f"MATCH (r:Register {{id: '{_esc(c['register_id'])}'}}), (c:Card {{uid: '{_esc(c['uid'])}'}}) "
                f"MERGE (r)-[:HAS_CARD]->(c);"
            )
            cypher_lines.append(
                f"MATCH (c:Card {{uid: '{_esc(c['uid'])}'}}), (a:Arena {{id: '{_esc(c['arena'])}'}}) "
                f"MERGE (c)-[:SET_IN_ARENA]->(a);"
            )
        for e in tables_dump["graph_edges"]:
            if e["edge_type"] in ("FLOWS_TO", "PIVOTS_VIA"):
                cypher_lines.append(
                    f"MATCH (a:Card {{uid: '{_esc(e['source_uid'])}'}}), (b:Card {{uid: '{_esc(e['target_uid'])}'}}) "
                    f"MERGE (a)-[r:{e['edge_type']} {{id: '{_esc(e['id'])}'}}]->(b) "
                    f"SET r.weight = {float(e['weight'])}, r.stability = {float(e['stability'])}, "
                    f"r.days_ago = {int(e['days_ago'])}, r.drills = {int(e['drills'])};"
                )

        cypher_path = snap_dir / "neo4j_reconstruction.cypher"
        cypher_sha = _atomic_write_text(cypher_path, "\n".join(cypher_lines) + "\n")

        manifest = {
            "snapshot_id": f"snapshot_{ts}",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "schema_version": SCHEMA_VERSION,
            "row_counts": row_counts,
            "artifacts": {
                "postgres_full_dump.json": {"sha256": pg_sha, "bytes": pg_dump_path.stat().st_size},
                "neo4j_reconstruction.cypher": {"sha256": cypher_sha, "bytes": cypher_path.stat().st_size},
            },
        }
        manifest_path = snap_dir / "manifest.json"
        manifest_sha = _atomic_write_json(manifest_path, manifest)

        # Enforce retention policy
        pruned_snapshots: list[str] = []
        if keep_last > 0 and backups_root.exists():
            all_snaps = sorted([d for d in backups_root.iterdir() if d.is_dir() and d.name.startswith("snapshot_")])
            while len(all_snaps) > keep_last:
                old = all_snaps.pop(0)
                shutil.rmtree(old, ignore_errors=True)
                pruned_snapshots.append(old.name)

        return {
            "ok": True,
            "snapshot_dir": str(snap_dir),
            "manifest_sha256": manifest_sha,
            "row_counts": row_counts,
            "artifacts": manifest["artifacts"],
            "pruned_old_snapshots": pruned_snapshots,
        }


sync_service = SyncService()
