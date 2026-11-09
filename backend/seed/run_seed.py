from __future__ import annotations

import asyncio
from typing import Any

from backend.db.neo4j_client import neo4j_manager
from backend.db.postgres import pg_manager, vector_to_pg_literal
from backend.seed.corpus_data import (
    ARENAS,
    BRIDGES,
    CARDS,
    FALSE_FRIENDS,
    GRAPH_EDGES,
    IDIOMS,
    LANGUAGES,
    LEXICAL_SCAFFOLDS,
    REGISTERS,
    ROOM_STATES,
    SONGS,
    STAGED_WEBHOOKS,
    STYLE_LENSES,
    VIBE_LINKS,
    VOCAB_FALSE_FRIEND_ALERTS,
    VOCAB_ITEMS,
)
from backend.services.ollama_client import ollama_client
from backend.services.sync_service import sync_service
from backend.validators.graph_rules import strip_html_tags


async def seed_all(compute_embeddings: bool = True, force_neo4j: bool = True) -> dict[str, Any]:
    """Idempotently initialize PostgreSQL schema, seed full 5-language 2-tier corpus, backfill bge-m3 embeddings, and sync Neo4j + JSON shards."""
    await pg_manager.init_schema()
    pool = await pg_manager.get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            for lang in LANGUAGES:
                await conn.execute(
                    """
                    INSERT INTO languages (code, name, flag, family)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (code) DO UPDATE SET
                        name = EXCLUDED.name, flag = EXCLUDED.flag, family = EXCLUDED.family
                    """,
                    lang["code"],
                    lang["name"],
                    lang["flag"],
                    lang["family"],
                )

            for reg in REGISTERS:
                await conn.execute(
                    """
                    INSERT INTO registers (
                        id, lang_code, tier, flag, name, subtitle, family, address_form,
                        phonetic_rhythm, intimacy_trick, posture, paired_register_id, partition_file, sync_status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,'PENDING')
                    ON CONFLICT (id) DO UPDATE SET
                        subtitle = EXCLUDED.subtitle,
                        address_form = EXCLUDED.address_form,
                        phonetic_rhythm = EXCLUDED.phonetic_rhythm,
                        intimacy_trick = EXCLUDED.intimacy_trick,
                        posture = EXCLUDED.posture,
                        paired_register_id = EXCLUDED.paired_register_id,
                        partition_file = EXCLUDED.partition_file,
                        sync_status = 'PENDING',
                        updated_at = NOW()
                    """,
                    reg["id"],
                    reg["lang_code"],
                    reg["tier"],
                    reg["flag"],
                    reg["name"],
                    reg["subtitle"],
                    reg["family"],
                    reg["address_form"],
                    reg["phonetic_rhythm"],
                    reg["intimacy_trick"],
                    reg["posture"],
                    reg["paired_register_id"],
                    reg["partition_file"],
                )

            for ar in ARENAS:
                await conn.execute(
                    """
                    INSERT INTO arenas (id, icon, label, short_label, arena_group, description, sync_status)
                    VALUES ($1, $2, $3, $4, $5, $6, 'PENDING')
                    ON CONFLICT (id) DO UPDATE SET
                        icon = EXCLUDED.icon,
                        label = EXCLUDED.label,
                        short_label = EXCLUDED.short_label,
                        arena_group = EXCLUDED.arena_group,
                        description = EXCLUDED.description,
                        sync_status = 'PENDING'
                    """,
                    ar["id"],
                    ar["icon"],
                    ar["label"],
                    ar["short_label"],
                    ar["arena_group"],
                    ar["description"],
                )

            for lens in STYLE_LENSES:
                await conn.execute(
                    """
                    INSERT INTO style_lenses (
                        id, lens_group, icon, name, inspirations, cadence, prosody,
                        delivery_rule, modifier_prefix, modifier_cue
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
                    ON CONFLICT (id) DO UPDATE SET
                        cadence = EXCLUDED.cadence,
                        prosody = EXCLUDED.prosody,
                        delivery_rule = EXCLUDED.delivery_rule,
                        modifier_prefix = EXCLUDED.modifier_prefix,
                        modifier_cue = EXCLUDED.modifier_cue
                    """,
                    lens["id"],
                    lens["lens_group"],
                    lens["icon"],
                    lens["name"],
                    lens["inspirations"],
                    lens["cadence"],
                    lens["prosody"],
                    lens["delivery_rule"],
                    lens["modifier_prefix"],
                    lens["modifier_cue"],
                )

            for idm in IDIOMS:
                await conn.execute(
                    """
                    INSERT INTO idioms (term, register_id, origin, meaning, delivery_cue, cousin_term, sync_status)
                    VALUES ($1,$2,$3,$4,$5,$6,'PENDING')
                    ON CONFLICT (term) DO UPDATE SET
                        register_id = EXCLUDED.register_id,
                        origin = EXCLUDED.origin,
                        meaning = EXCLUDED.meaning,
                        delivery_cue = EXCLUDED.delivery_cue,
                        cousin_term = EXCLUDED.cousin_term,
                        sync_status = 'PENDING'
                    """,
                    idm["term"],
                    idm["register_id"],
                    idm["origin"],
                    idm["meaning"],
                    idm["delivery_cue"],
                    idm["cousin_term"],
                )

            for vl in VIBE_LINKS:
                await conn.execute(
                    """
                    INSERT INTO idiom_vibe_links (source_term, target_term, shared_root, pivot_tip, sync_status)
                    VALUES ($1,$2,$3,$4,'PENDING')
                    ON CONFLICT (source_term, target_term) DO UPDATE SET
                        shared_root = EXCLUDED.shared_root,
                        pivot_tip = EXCLUDED.pivot_tip,
                        sync_status = 'PENDING'
                    """,
                    vl["source_term"],
                    vl["target_term"],
                    vl["shared_root"],
                    vl["pivot_tip"],
                )

            for c in CARDS:
                plain = strip_html_tags(c["text_html"])
                await conn.execute(
                    """
                    INSERT INTO cards (
                        uid, register_id, stage, arena, lens_id, title, text_html, text_plain,
                        phonetics, english_gloss, delivery_cue, idiom_terms, sync_status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,'PENDING')
                    ON CONFLICT (uid) DO UPDATE SET
                        register_id = EXCLUDED.register_id,
                        stage = EXCLUDED.stage,
                        arena = EXCLUDED.arena,
                        lens_id = EXCLUDED.lens_id,
                        title = EXCLUDED.title,
                        text_html = EXCLUDED.text_html,
                        text_plain = EXCLUDED.text_plain,
                        phonetics = EXCLUDED.phonetics,
                        english_gloss = EXCLUDED.english_gloss,
                        delivery_cue = EXCLUDED.delivery_cue,
                        idiom_terms = EXCLUDED.idiom_terms,
                        sync_status = 'PENDING'
                    """,
                    c["uid"],
                    c["register_id"],
                    c["stage"],
                    c.get("arena", "terrace"),
                    c.get("lens_id"),
                    c.get("title", ""),
                    c["text_html"],
                    plain,
                    c.get("phonetics", ""),
                    c.get("english_gloss", ""),
                    c.get("delivery_cue", ""),
                    c.get("idiom_terms", []),
                )

            for sc in LEXICAL_SCAFFOLDS:
                await conn.execute(
                    """
                    INSERT INTO lexical_scaffolds (
                        card_uid, idiom_term, target_register_id, anchor_lang,
                        scaffold_type, anchor_expression, explanation
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7)
                    ON CONFLICT (card_uid, idiom_term, anchor_lang, anchor_expression) DO UPDATE SET
                        explanation = EXCLUDED.explanation
                    """,
                    sc["card_uid"],
                    sc["idiom_term"],
                    sc["target_register_id"],
                    sc["anchor_lang"],
                    sc["scaffold_type"],
                    sc["anchor_expression"],
                    sc["explanation"],
                )

            for ff in FALSE_FRIENDS:
                await conn.execute(
                    """
                    INSERT INTO false_friends (
                        id, target_lang, target_term, trap_lang, trap_term,
                        calque_lang, calque_term, safe_meaning, sync_status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,'PENDING')
                    ON CONFLICT (id) DO UPDATE SET
                        safe_meaning = EXCLUDED.safe_meaning,
                        sync_status = 'PENDING'
                    """,
                    ff["id"],
                    ff["target_lang"],
                    ff["target_term"],
                    ff["trap_lang"],
                    ff["trap_term"],
                    ff["calque_lang"],
                    ff["calque_term"],
                    ff["safe_meaning"],
                )

            for st in ROOM_STATES:
                await conn.execute(
                    """
                    INSERT INTO room_states (
                        id, label, description, default_card_uid, default_register_id, effectiveness, cue, sync_status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,'PENDING')
                    ON CONFLICT (id) DO UPDATE SET
                        label = EXCLUDED.label,
                        description = EXCLUDED.description,
                        default_card_uid = EXCLUDED.default_card_uid,
                        default_register_id = EXCLUDED.default_register_id,
                        effectiveness = EXCLUDED.effectiveness,
                        cue = EXCLUDED.cue,
                        sync_status = 'PENDING'
                    """,
                    st["id"],
                    st["label"],
                    st["description"],
                    st["default_card_uid"],
                    st["default_register_id"],
                    st["effectiveness"],
                    st["cue"],
                )

            for br in BRIDGES:
                await conn.execute(
                    """
                    INSERT INTO bridges (
                        uid, from_register_id, to_register_id, from_card_uid, to_card_uid,
                        bridge_type, text, mlf_boundary_note, vocal_cue, weight, sync_status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,'PENDING')
                    ON CONFLICT (uid) DO UPDATE SET
                        text = EXCLUDED.text,
                        mlf_boundary_note = EXCLUDED.mlf_boundary_note,
                        vocal_cue = EXCLUDED.vocal_cue,
                        weight = EXCLUDED.weight,
                        sync_status = 'PENDING'
                    """,
                    br["uid"],
                    br["from_register_id"],
                    br["to_register_id"],
                    br["from_card_uid"],
                    br["to_card_uid"],
                    br["bridge_type"],
                    br["text"],
                    br["mlf_boundary_note"],
                    br["vocal_cue"],
                    br["weight"],
                )

            for e in GRAPH_EDGES:
                await conn.execute(
                    """
                    INSERT INTO graph_edges (
                        id, source_uid, target_uid, edge_type, bridge_uid,
                        weight, stability, days_ago, drills, effectiveness, cue, sync_status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,'PENDING')
                    ON CONFLICT (id) DO NOTHING
                    """,
                    e["id"],
                    e["source_uid"],
                    e["target_uid"],
                    e["edge_type"],
                    e.get("bridge_uid"),
                    e["weight"],
                    e.get("stability", 8.0),
                    e.get("days_ago", 1),
                    e.get("drills", 1),
                    e.get("effectiveness"),
                    e.get("cue", ""),
                )

            for wh in STAGED_WEBHOOKS:
                await conn.execute(
                    """
                    INSERT INTO staged_webhooks (
                        id, target_register_id, source_type, paper_or_model, published_label, headline, payload_json, status
                    ) VALUES ($1,$2,'NEWSPAPER_WEBHOOK',$3,$4,$5,$6,'STAGED')
                    ON CONFLICT (id) DO NOTHING
                    """,
                    wh["id"],
                    wh["target_db"],
                    wh["paper"],
                    wh["published"],
                    wh["headline"],
                    wh,
                )

            for voc in VOCAB_ITEMS:
                await conn.execute(
                    """
                    INSERT INTO vocab_items (
                        uid, term, lang_code, register_id, register_type, meaning,
                        ib_source, grammar_note, etymology, warning, sync_status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,'PENDING')
                    ON CONFLICT (uid) DO UPDATE SET
                        term = EXCLUDED.term,
                        lang_code = EXCLUDED.lang_code,
                        register_id = EXCLUDED.register_id,
                        register_type = EXCLUDED.register_type,
                        meaning = EXCLUDED.meaning,
                        ib_source = EXCLUDED.ib_source,
                        grammar_note = EXCLUDED.grammar_note,
                        etymology = EXCLUDED.etymology,
                        warning = EXCLUDED.warning,
                        sync_status = 'PENDING',
                        updated_at = NOW()
                    """,
                    voc["uid"],
                    voc["term"],
                    voc["lang_code"],
                    voc["register_id"],
                    voc["register_type"],
                    voc["meaning"],
                    voc["ib_source"],
                    voc["grammar_note"],
                    voc["etymology"],
                    voc["warning"],
                )

            for ffa in VOCAB_FALSE_FRIEND_ALERTS:
                await conn.execute(
                    """
                    INSERT INTO vocab_false_friend_alerts (source_uid, target_uid, sync_status)
                    VALUES ($1, $2, 'PENDING')
                    ON CONFLICT (source_uid, target_uid) DO UPDATE SET sync_status = 'PENDING'
                    """,
                    ffa["source_uid"],
                    ffa["target_uid"],
                )

            for s in SONGS:
                await conn.execute(
                    """
                    INSERT INTO songs (
                        uid, title, artist, city_region, genre, bpm, register_id,
                        original_lang, original_lyric, translation_es, translation_en,
                        translation_cz, translation_de, translation_ru, cultural_vibe,
                        pivot_line, reinforces_card_uid, slang_vocab_uids, sync_status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,'PENDING')
                    ON CONFLICT (uid) DO UPDATE SET
                        title = EXCLUDED.title,
                        artist = EXCLUDED.artist,
                        city_region = EXCLUDED.city_region,
                        genre = EXCLUDED.genre,
                        bpm = EXCLUDED.bpm,
                        register_id = EXCLUDED.register_id,
                        original_lang = EXCLUDED.original_lang,
                        original_lyric = EXCLUDED.original_lyric,
                        translation_es = EXCLUDED.translation_es,
                        translation_en = EXCLUDED.translation_en,
                        translation_cz = EXCLUDED.translation_cz,
                        translation_de = EXCLUDED.translation_de,
                        translation_ru = EXCLUDED.translation_ru,
                        cultural_vibe = EXCLUDED.cultural_vibe,
                        pivot_line = EXCLUDED.pivot_line,
                        reinforces_card_uid = EXCLUDED.reinforces_card_uid,
                        slang_vocab_uids = EXCLUDED.slang_vocab_uids,
                        sync_status = 'PENDING',
                        updated_at = NOW()
                    """,
                    s["uid"],
                    s["title"],
                    s["artist"],
                    s["city_region"],
                    s["genre"],
                    s["bpm"],
                    s["register_id"],
                    s["original_lang"],
                    s["original_lyric"],
                    s["translation_es"],
                    s["translation_en"],
                    s["translation_cz"],
                    s["translation_de"],
                    s["translation_ru"],
                    s["cultural_vibe"],
                    s["pivot_line"],
                    s["reinforces_card_uid"],
                    s["slang_vocab_uids"],
                )

    await pg_manager.enforce_domain_constraints()

    embedded_counts = {"cards": 0, "idioms": 0}
    if compute_embeddings:
        embedded_counts = await backfill_embeddings()

    sync_res = await sync_service.sync_pending_to_neo4j(force_all=force_neo4j, prune_orphans=force_neo4j)
    return {
        "seeded": {
            "languages": len(LANGUAGES),
            "arenas": len(ARENAS),
            "registers": len(REGISTERS),
            "style_lenses": len(STYLE_LENSES),
            "idioms": len(IDIOMS),
            "vocab": len(VOCAB_ITEMS),
            "songs": len(SONGS),
            "cards": len(CARDS),
            "bridges": len(BRIDGES),
            "edges": len(GRAPH_EDGES),
            "false_friends": len(FALSE_FRIENDS),
            "scaffolds": len(LEXICAL_SCAFFOLDS),
        },
        "embedded": embedded_counts,
        "sync": sync_res,
    }


async def backfill_embeddings() -> dict[str, int]:
    """Batch-compute 1024-dim bge-m3 cross-lingual embeddings for any cards/idioms missing vectors."""
    missing_cards = await pg_manager.fetch_all(
        "SELECT uid, register_id, stage, text_plain, english_gloss FROM cards WHERE embedding IS NULL ORDER BY uid"
    )
    missing_idioms = await pg_manager.fetch_all(
        "SELECT term, register_id, meaning, origin FROM idioms WHERE embedding IS NULL ORDER BY term"
    )

    cards_done = 0
    idioms_done = 0

    if missing_cards:
        texts = [
            f"[{c['register_id']} • {c['stage']}] {c['text_plain']} | {c['english_gloss']}"
            for c in missing_cards
        ]
        vecs = await ollama_client.embed_batch(texts)
        pool = await pg_manager.get_pool()
        async with pool.acquire() as conn:
            for c, v in zip(missing_cards, vecs):
                if v:
                    await conn.execute(
                        "UPDATE cards SET embedding = $2::vector WHERE uid = $1",
                        c["uid"],
                        vector_to_pg_literal(v),
                    )
                    cards_done += 1

    if missing_idioms:
        texts = [f"[{i['register_id']}] {i['term']}: {i['meaning']} ({i['origin']})" for i in missing_idioms]
        vecs = await ollama_client.embed_batch(texts)
        pool = await pg_manager.get_pool()
        async with pool.acquire() as conn:
            for i, v in zip(missing_idioms, vecs):
                if v:
                    await conn.execute(
                        "UPDATE idioms SET embedding = $2::vector WHERE term = $1",
                        i["term"],
                        vector_to_pg_literal(v),
                    )
                    idioms_done += 1

    return {"cards": cards_done, "idioms": idioms_done}


async def _cli_main() -> None:
    try:
        res = await seed_all()
        print(res)
    finally:
        await pg_manager.close()
        await neo4j_manager.close()


if __name__ == "__main__":
    asyncio.run(_cli_main())
