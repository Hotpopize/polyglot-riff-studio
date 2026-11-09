from __future__ import annotations

import random
import time
from typing import Any, Optional, Sequence

from backend.config import settings
from backend.db.postgres import pg_manager, vector_to_pg_literal
from backend.services.bridge_service import bridge_service
from backend.services.ollama_client import ollama_client
from backend.services.sync_service import sync_service
from backend.validators.graph_rules import ensure_slang_spans, strip_html_tags, validate_graph_commit


CANONICAL_ARENAS = {"terrace", "spark", "adventure", "runway", "hochkultur", "polo", "wien", "b2b"}
ARENA_ALIASES = {
    "general": "terrace",
    "lounge": "terrace",
    "banter": "spark",
}


def normalize_arena_id(arena: Optional[str]) -> str:
    raw = (arena or "terrace").strip().lower()
    mapped = ARENA_ALIASES.get(raw, raw)
    return mapped if mapped in CANONICAL_ARENAS else "terrace"


class ConverseStyleService:
    """Coordinate lookup + Live Thought-to-Register Stylizer across regional registers, arenas, and comic/salon lenses."""

    async def resolve_style(
        self,
        *,
        register_id: str = "CZ_OVA",
        arena: str = "terrace",
        stage: str = "COUNTERACT",
        lens_id: str = "DEADPAN",
        anchor_langs: Sequence[str] = ("DE", "RU", "EN"),
    ) -> dict[str, Any]:
        arena = normalize_arena_id(arena)
        reg = await pg_manager.fetch_one("SELECT * FROM registers WHERE id = $1", register_id)
        if not reg:
            raise LookupError(f"Register '{register_id}' not found.")

        lens = await pg_manager.fetch_one("SELECT * FROM style_lenses WHERE id = $1", lens_id)

        # 1. Exact (register, arena, stage, lens) match
        card = await pg_manager.fetch_one(
            """
            SELECT * FROM cards
            WHERE register_id = $1 AND arena = $2 AND stage = $3 AND lens_id = $4
            LIMIT 1
            """,
            register_id,
            arena,
            stage,
            lens_id,
        )
        match_tier = "EXACT_ARENA_AND_LENS"

        # 2. Same (register, arena, lens) at any stage or same (register, arena) base card
        if not card:
            card = await pg_manager.fetch_one(
                """
                SELECT * FROM cards
                WHERE register_id = $1 AND arena = $2
                ORDER BY
                    CASE WHEN stage = $3 THEN 0 ELSE 1 END,
                    CASE WHEN lens_id = $4 THEN 0 WHEN lens_id IS NULL THEN 1 ELSE 2 END
                LIMIT 1
                """,
                register_id,
                arena,
                stage,
                lens_id,
            )
            match_tier = "ARENA_CURATED_WITH_LENS_OVERLAY"

        # 3. Nearest stage card in the same register
        if not card:
            card = await pg_manager.fetch_one(
                """
                SELECT * FROM cards
                WHERE register_id = $1 AND stage = $2
                ORDER BY CASE WHEN lens_id IS NULL THEN 0 ELSE 1 END
                LIMIT 1
                """,
                register_id,
                stage,
            )
            match_tier = "REGISTER_STAGE_WITH_LENS_OVERLAY"

        if not card:
            raise LookupError(f"No cards found for register '{register_id}'.")

        scaffold = await bridge_service.scaffold_phrase(
            card_uid=card["uid"],
            target_register=register_id,
            anchor_langs=anchor_langs,
        )

        combined_delivery = " • ".join(
            part
            for part in [
                lens["modifier_prefix"] if lens else "",
                card["delivery_cue"] or reg["posture"],
                lens["modifier_cue"] if lens else "",
            ]
            if part
        )

        return {
            "match_tier": match_tier,
            "coordinates": {
                "register_id": register_id,
                "arena": arena,
                "stage": stage,
                "lens_id": lens_id,
            },
            "register": {
                "id": reg["id"],
                "tier": reg["tier"],
                "name": reg["name"],
                "address_form": reg["address_form"],
                "rhythm": reg["phonetic_rhythm"],
                "trick": reg["intimacy_trick"],
                "posture": reg["posture"],
                "paired_register_id": reg["paired_register_id"],
            },
            "lens": lens,
            "card": {
                "uid": card["uid"],
                "stage": card["stage"],
                "arena": card["arena"],
                "lens_id": card["lens_id"] or lens_id,
                "title": card["title"],
                "text_html": card["text_html"],
                "text_plain": card["text_plain"],
                "phonetics": card["phonetics"],
                "english_gloss": card["english_gloss"],
                "idioms": card["idiom_terms"],
                "combined_delivery_cue": combined_delivery,
            },
            "bridges": scaffold,
        }

    async def stylize_thought(
        self,
        *,
        thought: str,
        target_register: str = "CZ_OVA",
        arena: str = "terrace",
        stage: str = "COUNTERACT",
        lens_id: str = "FERGUSON",
        model: Optional[str] = None,
        fast_mode: bool = False,
        commit_mode: str = "stage",
        counters_state: Optional[str] = None,
    ) -> dict[str, Any]:
        """Rewrite any raw EN/DE/RU thought into target regional register with idiom + false-friend enforcement."""
        arena = normalize_arena_id(arena)
        reg = await pg_manager.fetch_one("SELECT * FROM registers WHERE id = $1", target_register)
        if not reg:
            raise LookupError(f"Register '{target_register}' not found.")

        lens = await pg_manager.fetch_one("SELECT * FROM style_lenses WHERE id = $1", lens_id)
        reg_idioms = await pg_manager.fetch_all(
            "SELECT term, origin, meaning, delivery_cue, cousin_term FROM idioms WHERE register_id = $1 LIMIT 12",
            target_register,
        )
        false_friends = await pg_manager.fetch_all(
            "SELECT * FROM false_friends WHERE target_lang = $1",
            reg["lang_code"],
        )

        chosen_model = model or (settings.ollama_fast_model if fast_mode else settings.ollama_stylizer_model)
        idiom_list_str = ", ".join(f"{i['term']} ({i['meaning']})" for i in reg_idioms) or "authentic local colloquialism"
        ff_str = (
            "; ".join(f"{ff['target_term']} = {ff['safe_meaning']} (NOT {ff['trap_term']})" for ff in false_friends[:6])
            if false_friends
            else "None"
        )

        system_prompt = (
            "You are the Polyglot Riff Atelier Sociolinguistic Engine. "
            "Transform the user's raw thought into natural, high-charisma spoken dialogue in the exact target regional register. "
            "Never sound like a textbook or stiff corporate translation. "
            "Return ONLY valid JSON with keys: "
            '{"term": "...", "origin": "...", "meaning": "...", "delivery": "...", "cousin": "...", '
            '"stage": "COMPLIMENT|CHAMELEON|COUNTERACT|CURIOSITY", '
            '"text": "Full spoken line naturally embedding the regional term", '
            '"phonetics": "Readable syllable-stress guide", '
            '"cognate_bridge": "DE/RU/EN cognate or structural calque memory hook", '
            '"english_gloss": "Idiomatic English translation"}'
        )
        user_prompt = (
            f"Raw thought / situation: {thought}\n"
            f"Target Register: {reg['id']} — {reg['name']} ({reg['address_form']})\n"
            f"Phonetic Rhythm: {reg['phonetic_rhythm']}\n"
            f"Grammar & Intimacy Trick: {reg['intimacy_trick']}\n"
            f"Social Arena: {arena}\n"
            f"4-C Stage: {stage}\n"
            f"Persona / Comic Lens: {lens['name'] if lens else lens_id} — {lens['cadence'] if lens else ''}\n"
            f"Existing Regional Idioms you may weave in (or mint a crisp regional one): {idiom_list_str}\n"
            f"False-Friend Interference Guardrails: {ff_str}\n"
        )

        used_source = f"ollama:{chosen_model}"
        try:
            draft = await ollama_client.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=chosen_model,
            )
        except Exception:
            used_source = "deterministic_offline_synthesizer"
            fallback_idiom = reg_idioms[0] if reg_idioms else {
                "term": "na první dobrou",
                "origin": reg["name"],
                "meaning": "Clean execution on the first pass",
                "delivery_cue": reg["posture"],
                "cousin_term": "сделали по красоте",
            }
            draft = {
                "term": fallback_idiom["term"],
                "origin": fallback_idiom.get("origin", reg["name"]),
                "meaning": fallback_idiom.get("meaning", "Authentic regional anchor"),
                "delivery": fallback_idiom.get("delivery_cue", reg["posture"]),
                "cousin": fallback_idiom.get("cousin_term"),
                "stage": stage,
                "text": f"{thought} — {fallback_idiom['term']}.",
                "phonetics": "",
                "cognate_bridge": reg["intimacy_trick"],
                "english_gloss": thought,
            }

        term = (draft.get("term") or (reg_idioms[0]["term"] if reg_idioms else "fachat")).strip()
        raw_line = (draft.get("text") or thought).strip()
        anchored_html = ensure_slang_spans(raw_line, [term])
        final_stage = draft.get("stage") if draft.get("stage") in ("COMPLIMENT", "CHAMELEON", "COUNTERACT", "CURIOSITY") else stage
        uid = f"{target_register}_{final_stage[:4]}_{int(time.time()) % 100000}_{random.randint(10, 99)}"

        candidate_idiom = {
            "term": term,
            "register_id": target_register,
            "origin": draft.get("origin") or f"{reg['name']} regional usage",
            "meaning": draft.get("meaning") or "High-rapport regional marker",
            "delivery": draft.get("delivery") or reg["posture"],
            "cousin": draft.get("cousin"),
        }
        candidate_card = {
            "uid": uid,
            "register_id": target_register,
            "stage": final_stage,
            "arena": arena,
            "lens_id": lens_id if lens else None,
            "text_html": anchored_html,
            "text_plain": strip_html_tags(anchored_html),
            "phonetics": draft.get("phonetics") or "",
            "english_gloss": draft.get("english_gloss") or "",
            "cognate_bridge": draft.get("cognate_bridge") or "",
            "delivery_cue": draft.get("delivery") or (lens["modifier_cue"] if lens else reg["posture"]),
            "idiom_terms": [term],
            "counters_state": counters_state,
        }

        validation = validate_graph_commit(
            card=candidate_card,
            idiom=candidate_idiom,
            edge={"weight": 0.78, "stability": 6.0},
            target_register=target_register,
            false_friends=false_friends,
        )

        if commit_mode == "commit" and validation["valid"]:
            committed = await self.commit_card_and_idiom(
                card=candidate_card,
                idiom=candidate_idiom,
            )
            return {
                "status": "COMMITTED",
                "generator": used_source,
                "validation": validation,
                "idiom": candidate_idiom,
                "card": candidate_card,
                "commit_result": committed,
            }

        # Stage in staged_webhooks for review/one-click approval
        wh_id = f"STYL_{target_register}_{int(time.time()) % 100000}"
        payload = {
            "id": wh_id,
            "target_db": target_register,
            "paper": f"Live Stylizer ({used_source} • {lens_id})",
            "published": time.strftime("%Y-%m-%d %H:%M CET"),
            "headline": f"Thought Stylizer [{arena}]: {thought[:120]}",
            "idiom": candidate_idiom,
            "card": {
                "uid": uid,
                "stage": final_stage,
                "arena": arena,
                "lens_id": lens_id if lens else None,
                "text": anchored_html,
                "phonetics": candidate_card["phonetics"],
                "english_gloss": candidate_card["english_gloss"],
                "counters_state": counters_state,
            },
        }
        await pg_manager.execute(
            """
            INSERT INTO staged_webhooks (
                id, target_register_id, source_type, paper_or_model, published_label, headline, payload_json, validation_json, status
            ) VALUES ($1, $2, 'OLLAMA_STYLIZER', $3, $4, $5, $6, $7, 'STAGED')
            ON CONFLICT (id) DO UPDATE SET payload_json = EXCLUDED.payload_json, validation_json = EXCLUDED.validation_json
            """,
            wh_id,
            target_register,
            used_source,
            payload["published"],
            payload["headline"],
            payload,
            validation,
        )
        return {
            "status": "STAGED",
            "staged_id": wh_id,
            "generator": used_source,
            "validation": validation,
            "idiom": candidate_idiom,
            "card": candidate_card,
        }

    async def commit_card_and_idiom(
        self,
        *,
        card: dict[str, Any],
        idiom: Optional[dict[str, Any]] = None,
        connect_from_uid: Optional[str] = None,
    ) -> dict[str, Any]:
        target_reg = card["register_id"]
        text_html = card.get("text_html") or card.get("text") or ""
        idiom_terms = list(card.get("idiom_terms") or ([] if not idiom else [idiom["term"]]))
        text_html = ensure_slang_spans(text_html, idiom_terms)
        text_plain = strip_html_tags(text_html)

        card_emb = await ollama_client.embed_one(f"{text_plain} | {card.get('english_gloss', '')}")
        idiom_emb = (
            await ollama_client.embed_one(f"{idiom['term']}: {idiom.get('meaning', '')}")
            if idiom and idiom.get("term")
            else None
        )

        pool = await pg_manager.get_pool()
        created_edge_id: Optional[str] = None
        async with pool.acquire() as conn:
            async with conn.transaction():
                if idiom and idiom.get("term"):
                    await conn.execute(
                        """
                        INSERT INTO idioms (term, register_id, origin, meaning, delivery_cue, cousin_term, embedding, sync_status)
                        VALUES ($1, $2, $3, $4, $5, $6, $7::vector, 'PENDING')
                        ON CONFLICT (term) DO UPDATE SET
                            meaning = EXCLUDED.meaning,
                            delivery_cue = EXCLUDED.delivery_cue,
                            cousin_term = COALESCE(EXCLUDED.cousin_term, idioms.cousin_term),
                            embedding = COALESCE(EXCLUDED.embedding, idioms.embedding),
                            sync_status = 'PENDING',
                            updated_at = NOW()
                        """,
                        idiom["term"],
                        target_reg,
                        idiom.get("origin", ""),
                        idiom.get("meaning", ""),
                        idiom.get("delivery") or idiom.get("delivery_cue") or "",
                        idiom.get("cousin"),
                        vector_to_pg_literal(idiom_emb),
                    )
                    if idiom.get("cousin"):
                        cousin_exists = await conn.fetchval(
                            "SELECT EXISTS(SELECT 1 FROM idioms WHERE term = $1)",
                            idiom["cousin"],
                        )
                        if cousin_exists:
                            await conn.execute(
                                """
                                INSERT INTO idiom_vibe_links (source_term, target_term, shared_root, pivot_tip, sync_status)
                                VALUES ($1, $2, 'Cross-Regional Pragmatic Bridge', 'Match vocal posture across both registers.', 'PENDING')
                                ON CONFLICT (source_term, target_term) DO NOTHING
                                """,
                                idiom["term"],
                                idiom["cousin"],
                            )

                await conn.execute(
                    """
                    INSERT INTO cards (
                        uid, register_id, stage, arena, lens_id, title, text_html, text_plain,
                        phonetics, english_gloss, delivery_cue, idiom_terms, embedding, sync_status
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8,
                        $9, $10, $11, $12, $13::vector, 'PENDING'
                    )
                    ON CONFLICT (uid) DO UPDATE SET
                        text_html = EXCLUDED.text_html,
                        text_plain = EXCLUDED.text_plain,
                        phonetics = EXCLUDED.phonetics,
                        english_gloss = EXCLUDED.english_gloss,
                        idiom_terms = EXCLUDED.idiom_terms,
                        embedding = COALESCE(EXCLUDED.embedding, cards.embedding),
                        sync_status = 'PENDING',
                        updated_at = NOW()
                    """,
                    card["uid"],
                    target_reg,
                    card["stage"],
                    normalize_arena_id(card.get("arena")),
                    card.get("lens_id"),
                    card.get("title") or "",
                    text_html,
                    text_plain,
                    card.get("phonetics") or "",
                    card.get("english_gloss") or "",
                    card.get("delivery_cue") or "",
                    idiom_terms,
                    vector_to_pg_literal(card_emb),
                )

                source_uid = connect_from_uid
                if not source_uid:
                    source_uid = await conn.fetchval(
                        """
                        SELECT uid FROM cards
                        WHERE register_id = $1 AND uid <> $2
                        ORDER BY CASE WHEN stage = 'CHAMELEON' THEN 0 ELSE 1 END
                        LIMIT 1
                        """,
                        target_reg,
                        card["uid"],
                    )
                if source_uid:
                    src_reg = await conn.fetchval("SELECT register_id FROM cards WHERE uid = $1", source_uid)
                    edge_type = "FLOWS_TO" if src_reg == target_reg else "PIVOTS_VIA"
                    created_edge_id = f"E_{card['uid']}"
                    await conn.execute(
                        """
                        INSERT INTO graph_edges (
                            id, source_uid, target_uid, edge_type, weight, stability, days_ago, drills, sync_status
                        ) VALUES ($1, $2, $3, $4, 0.78, 6.0, 0, 1, 'PENDING')
                        ON CONFLICT (id) DO NOTHING
                        """,
                        created_edge_id,
                        source_uid,
                        card["uid"],
                        edge_type,
                    )

                if card.get("counters_state"):
                    cs_edge_id = f"EC_{card['uid']}_{card['counters_state']}"
                    await conn.execute(
                        """
                        INSERT INTO graph_edges (
                            id, source_uid, target_uid, edge_type, weight, effectiveness, cue, sync_status
                        ) VALUES ($1, $2, $3, 'COUNTERS_STATE', 0.94, 0.94, $4, 'PENDING')
                        ON CONFLICT (id) DO NOTHING
                        """,
                        cs_edge_id,
                        card["uid"],
                        card["counters_state"],
                        card.get("delivery_cue") or "Drop half an octave",
                    )

        sync_res = await sync_service.sync_pending_to_neo4j()
        return {
            "card_uid": card["uid"],
            "edge_id": created_edge_id,
            "embedded": card_emb is not None,
            "sync": sync_res,
        }


converse_service = ConverseStyleService()

