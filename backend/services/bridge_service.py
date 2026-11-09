from __future__ import annotations

from typing import Any, Optional, Sequence

from backend.db.neo4j_client import neo4j_manager
from backend.db.postgres import pg_manager, vector_to_pg_literal
from backend.services.fsrs_service import compute_retrievability
from backend.services.ollama_client import ollama_client
from backend.validators.graph_rules import strip_html_tags

ANCHOR_LANG_TO_PREFIXES = {
    "DE": ("DE_", "AT_"),
    "RU": ("RU_",),
    "EN": ("EN_",),
    "ES": ("ES_",),
    "CS": ("CZ_",),
    "CZ": ("CZ_",),
}


def _registers_for_anchor_langs(anchor_langs: Sequence[str], exclude_reg: Optional[str] = None) -> list[str]:
    prefixes: list[str] = []
    for code in anchor_langs:
        prefixes.extend(ANCHOR_LANG_TO_PREFIXES.get(code.upper(), (f"{code.upper()}_",)))
    return prefixes


class BridgeService:
    """First-class 3-Layer Bridge Language Resolver + pgvector cross-lingual fallback."""

    async def scaffold_phrase(
        self,
        *,
        card_uid: Optional[str] = None,
        text: Optional[str] = None,
        target_register: str = "CZ_OVA",
        anchor_langs: Sequence[str] = ("DE", "RU", "EN"),
    ) -> dict[str, Any]:
        card_row: Optional[dict[str, Any]] = None
        if card_uid:
            card_row = await pg_manager.fetch_one("SELECT * FROM cards WHERE uid = $1", card_uid)
            if card_row:
                target_register = card_row["register_id"]
                text = card_row["text_plain"]

        reg_row = await pg_manager.fetch_one("SELECT * FROM registers WHERE id = $1", target_register)
        lang_code = reg_row["lang_code"] if reg_row else target_register[:2].lower()
        normalized_anchors = [a.upper() for a in anchor_langs]

        # Layer 1A: Curated cognates, loanwords, and structural calques
        idiom_terms: list[str] = []
        if card_row and isinstance(card_row.get("idiom_terms"), list):
            idiom_terms = list(card_row["idiom_terms"])
        elif text:
            matched_idioms = await pg_manager.fetch_all(
                "SELECT term FROM idioms WHERE register_id = $1",
                target_register,
            )
            lowered_text = text.lower()
            idiom_terms = [m["term"] for m in matched_idioms if m["term"].lower() in lowered_text]

        scaffolds = await pg_manager.fetch_all(
            """
            SELECT anchor_lang, scaffold_type, anchor_expression, explanation, card_uid, idiom_term
            FROM lexical_scaffolds
            WHERE anchor_lang = ANY($1::text[])
              AND (
                  ($2::text IS NOT NULL AND card_uid = $2)
                  OR (idiom_term = ANY($3::text[]))
                  OR ($2::text IS NULL AND target_register_id = $4)
              )
            ORDER BY scaffold_type, anchor_lang
            """,
            normalized_anchors,
            card_uid,
            idiom_terms,
            target_register,
        )

        # Layer 1B: Active False-Friend Shields for target language
        false_friends = await pg_manager.fetch_all(
            "SELECT * FROM false_friends WHERE target_lang = $1 ORDER BY target_term",
            lang_code,
        )
        plain_probe = strip_html_tags(text or "").lower()
        triggered_shields = [
            ff for ff in false_friends if ff["target_term"].lower() in plain_probe
        ]

        # Layer 2: Mid-Sentence Code-Switch & Register-Drop Bridges (:PIVOTS_VIA)
        neo_pivots: list[dict[str, Any]] = []
        try:
            neo_pivots = await neo4j_manager.run_query(
                """
                MATCH (b:Bridge)
                WHERE b.from_lang = $reg OR b.to_lang = $reg
                OPTIONAL MATCH (c1:Card)-[pv:PIVOTS_VIA]->(b)-[:LANDS_ON]->(c2:Card)
                RETURN b.uid AS bridge_uid,
                       b.bridge_type AS bridge_type,
                       b.from_lang AS from_register,
                       b.to_lang AS to_register,
                       b.text AS bridge_text,
                       b.vocal_cue AS vocal_cue,
                       b.mlf_boundary_note AS mlf_boundary_note,
                       COALESCE(pv.weight, b.weight, 0.88) AS weight,
                       c1.uid AS from_card_uid,
                       c2.uid AS to_card_uid,
                       c2.text AS landing_text
                ORDER BY weight DESC
                """,
                {"reg": target_register},
            )
        except Exception:
            sql_bridges = await pg_manager.fetch_all(
                """
                SELECT uid AS bridge_uid, bridge_type, from_register_id AS from_register,
                       to_register_id AS to_register, text AS bridge_text, vocal_cue,
                       mlf_boundary_note, weight, from_card_uid, to_card_uid
                FROM bridges
                WHERE from_register_id = $1 OR to_register_id = $1
                ORDER BY weight DESC
                """,
                target_register,
            )
            neo_pivots = sql_bridges

        # Layer 3A: Explicit :SHARES_VIBE_WITH cousins in Neo4j / Postgres
        vibe_cousins: list[dict[str, Any]] = []
        if idiom_terms:
            try:
                vibe_cousins = await neo4j_manager.run_query(
                    """
                    MATCH (i1:Idiom)-[v:SHARES_VIBE_WITH]-(i2:Idiom)
                    WHERE i1.term IN $terms AND i2.register_id <> $reg
                    RETURN DISTINCT i1.term AS source_idiom,
                                    i2.term AS cousin_idiom,
                                    i2.register_id AS cousin_register,
                                    i2.meaning AS cousin_meaning,
                                    i2.delivery AS cousin_delivery,
                                    v.shared_root AS shared_root,
                                    v.pivot_tip AS pivot_tip
                    """,
                    {"terms": idiom_terms, "reg": target_register},
                )
            except Exception:
                vibe_cousins = await pg_manager.fetch_all(
                    """
                    SELECT v.source_term AS source_idiom,
                           i2.term AS cousin_idiom,
                           i2.register_id AS cousin_register,
                           i2.meaning AS cousin_meaning,
                           i2.delivery_cue AS cousin_delivery,
                           v.shared_root,
                           v.pivot_tip
                    FROM idiom_vibe_links v
                    JOIN idioms i2 ON i2.term = v.target_term
                    WHERE v.source_term = ANY($1::text[]) AND i2.register_id <> $2
                    """,
                    idiom_terms,
                    target_register,
                )

        # Layer 3B: Cross-lingual pgvector semantic bridges via bge-m3:latest
        semantic_bridges = await self._find_pgvector_equivalents(
            query_text=plain_probe or (card_row["english_gloss"] if card_row else ""),
            exclude_register=target_register,
            anchor_langs=normalized_anchors,
            limit=4,
        )

        return {
            "target_register": target_register,
            "register_profile": reg_row,
            "card": {
                "uid": card_row["uid"],
                "stage": card_row["stage"],
                "arena": card_row["arena"],
                "text_plain": card_row["text_plain"],
                "phonetics": card_row["phonetics"],
                "english_gloss": card_row["english_gloss"],
            }
            if card_row
            else {"text_plain": text},
            "layer_1_acquisition_scaffold": {
                "cognates_and_calques": scaffolds,
                "active_false_friend_shields": triggered_shields,
                "all_language_false_friends_count": len(false_friends),
            },
            "layer_2_code_switch_pivots": neo_pivots,
            "layer_3_pragmatic_vibe_bridges": {
                "curated_vibe_cousins": vibe_cousins,
                "semantic_pgvector_matches": semantic_bridges,
            },
        }

    async def find_bridge_path(
        self,
        *,
        from_register: str,
        to_register: str,
        current_stage: str = "CHAMELEON",
        arena: Optional[str] = None,
    ) -> dict[str, Any]:
        """Multi-hop Neo4j pathfinder between any two regional/formal registers, with pgvector fallback."""
        graph_paths: list[dict[str, Any]] = []
        try:
            graph_paths = await neo4j_manager.run_query(
                """
                MATCH (cStart:Card {register_id: $from_reg})
                WHERE cStart.stage = $stage OR $stage = 'ANY'
                MATCH path = (cStart)-[:FLOWS_TO|PIVOTS_VIA|LANDS_ON*1..4]->(cEnd:Card {register_id: $to_reg})
                WITH path,
                     [n IN nodes(path) | {
                         labels: labels(n),
                         uid: COALESCE(n.uid, n.id, n.term),
                         register_id: COALESCE(n.register_id, n.to_lang, n.lang),
                         stage: n.stage,
                         text: n.text,
                         vocal_cue: COALESCE(n.vocal_cue, n.delivery)
                     }] AS steps,
                     [r IN relationships(path) | {
                         type: type(r),
                         weight: COALESCE(r.weight, 0.88),
                         stability: COALESCE(r.stability, 8.0),
                         days_ago: COALESCE(r.days_ago, 1)
                     }] AS rels
                RETURN steps, rels, size(rels) AS hops
                ORDER BY hops ASC
                LIMIT 5
                """,
                {"from_reg": from_register, "to_reg": to_register, "stage": current_stage},
            )
        except Exception:
            graph_paths = []

        scored_paths = []
        for p in graph_paths:
            rels = p["rels"]
            combined_score = 1.0
            for r in rels:
                ret = compute_retrievability(float(r["stability"]), int(r["days_ago"]))
                combined_score *= float(r["weight"]) * ret
            scored_paths.append(
                {
                    "hops": p["hops"],
                    "fluency_score": round(combined_score ** (1.0 / max(1, len(rels))), 3),
                    "steps": p["steps"],
                    "relationships": rels,
                }
            )
        scored_paths.sort(key=lambda item: (-item["fluency_score"], item["hops"]))

        direct_bridge = await pg_manager.fetch_one(
            """
            SELECT * FROM bridges
            WHERE from_register_id = $1 AND to_register_id = $2
            ORDER BY weight DESC LIMIT 1
            """,
            from_register,
            to_register,
        )

        # Semantic fallback card in target register if no explicit graph path exists yet
        source_card = await pg_manager.fetch_one(
            """
            SELECT uid, stage, arena, text_plain, english_gloss
            FROM cards
            WHERE register_id = $1 AND ($2 = 'ANY' OR stage = $2)
            ORDER BY CASE WHEN arena = COALESCE($3, 'terrace') THEN 0 ELSE 1 END
            LIMIT 1
            """,
            from_register,
            current_stage,
            arena,
        )
        semantic_landing = []
        if source_card:
            semantic_landing = await self._find_pgvector_equivalents(
                query_text=source_card["text_plain"],
                exclude_register=from_register,
                target_register_only=to_register,
                limit=3,
            )

        return {
            "from_register": from_register,
            "to_register": to_register,
            "requested_stage": current_stage,
            "direct_bridge": direct_bridge,
            "neo4j_paths": scored_paths,
            "semantic_fallback_targets": semantic_landing,
        }

    async def get_register_switcher_deck(self, lang_code: str = "cs") -> dict[str, Any]:
        """Return synchronized Formal (Boardroom) <-> Pivot Bridge <-> Regional (Insider) sequence for any language."""
        lang = await pg_manager.fetch_one("SELECT * FROM languages WHERE code = $1", lang_code.lower())
        if not lang:
            raise LookupError(f"Language '{lang_code}' not found.")

        regs = await pg_manager.fetch_all(
            "SELECT * FROM registers WHERE lang_code = $1 ORDER BY tier ASC",
            lang_code.lower(),
        )
        formal_reg = next((r for r in regs if r["tier"] == "FORMAL"), None)
        regional_reg = next((r for r in regs if r["tier"] == "REGIONAL"), None)

        formal_cards = (
            await pg_manager.fetch_all(
                """
                SELECT uid, register_id, stage, arena, text_plain, text_html, phonetics, english_gloss, delivery_cue
                FROM cards
                WHERE register_id = $1 AND lens_id IS NULL
                ORDER BY CASE stage
                    WHEN 'COMPLIMENT' THEN 1
                    WHEN 'CHAMELEON' THEN 2
                    WHEN 'COUNTERACT' THEN 3
                    WHEN 'CURIOSITY' THEN 4
                END
                """,
                formal_reg["id"],
            )
            if formal_reg
            else []
        )

        regional_cards = (
            await pg_manager.fetch_all(
                """
                SELECT uid, register_id, stage, arena, text_plain, text_html, phonetics, english_gloss, delivery_cue
                FROM cards
                WHERE register_id = $1 AND lens_id IS NULL AND arena IN ('b2b', 'terrace')
                ORDER BY CASE WHEN arena = 'b2b' THEN 0 ELSE 1 END,
                         CASE stage
                             WHEN 'COMPLIMENT' THEN 1
                             WHEN 'CHAMELEON' THEN 2
                             WHEN 'COUNTERACT' THEN 3
                             WHEN 'CURIOSITY' THEN 4
                         END
                """,
                regional_reg["id"],
            )
            if regional_reg
            else []
        )
        # Deduplicate regional cards by stage keeping b2b preference
        by_stage: dict[str, dict[str, Any]] = {}
        for rc in regional_cards:
            by_stage.setdefault(rc["stage"], rc)

        drop_bridge = None
        if formal_reg and regional_reg:
            drop_bridge = await pg_manager.fetch_one(
                """
                SELECT * FROM bridges
                WHERE from_register_id = $1 AND to_register_id = $2
                ORDER BY weight DESC LIMIT 1
                """,
                formal_reg["id"],
                regional_reg["id"],
            )

        sequence: list[dict[str, Any]] = []
        for st in ("COMPLIMENT", "CHAMELEON"):
            fc = next((c for c in formal_cards if c["stage"] == st), None)
            if fc and formal_reg:
                sequence.append(
                    {
                        "uid": fc["uid"],
                        "reg": formal_reg["id"],
                        "tier": "FORMAL",
                        "stage": fc["stage"],
                        "lang": f"{formal_reg['name']} ({formal_reg['address_form']})",
                        "vibe": formal_reg["subtitle"],
                        "text": fc["text_plain"],
                        "text_html": fc["text_html"],
                        "phonetics": fc["phonetics"],
                        "english": fc["english_gloss"],
                        "mechanics": formal_reg["intimacy_trick"],
                        "delivery": fc["delivery_cue"] or formal_reg["posture"],
                    }
                )

        if drop_bridge:
            sequence.append(
                {
                    "uid": drop_bridge["uid"],
                    "reg": "BRIDGE",
                    "tier": "BRIDGE",
                    "stage": "REGISTER_DROP_BRIDGE",
                    "lang": f"Code-Switch Pivot ({formal_reg['id']} → {regional_reg['id']})",
                    "vibe": f"PIVOTS_VIA (Weight: {drop_bridge['weight']:.2f})",
                    "text": drop_bridge["text"],
                    "text_html": drop_bridge["text"],
                    "phonetics": "",
                    "english": drop_bridge["mlf_boundary_note"],
                    "mechanics": drop_bridge["mlf_boundary_note"] or "Mid-sentence matrix shift from formal to insider peer",
                    "delivery": drop_bridge["vocal_cue"],
                }
            )

        for st in ("COUNTERACT", "CURIOSITY"):
            rc = by_stage.get(st)
            if rc and regional_reg:
                sequence.append(
                    {
                        "uid": rc["uid"],
                        "reg": regional_reg["id"],
                        "tier": "REGIONAL",
                        "stage": rc["stage"],
                        "lang": f"{regional_reg['name']} ({regional_reg['address_form']})",
                        "vibe": regional_reg["subtitle"],
                        "text": rc["text_plain"],
                        "text_html": rc["text_html"],
                        "phonetics": rc["phonetics"],
                        "english": rc["english_gloss"],
                        "mechanics": regional_reg["intimacy_trick"],
                        "delivery": rc["delivery_cue"] or regional_reg["posture"],
                    }
                )

        return {
            "language": lang,
            "formal_register": formal_reg,
            "regional_register": regional_reg,
            "bridge": drop_bridge,
            "sequence": sequence,
            "all_formal_cards": formal_cards,
            "all_regional_cards": list(by_stage.values()),
        }

    async def _find_pgvector_equivalents(
        self,
        *,
        query_text: str,
        exclude_register: str,
        anchor_langs: Sequence[str] = ("DE", "RU", "EN"),
        target_register_only: Optional[str] = None,
        limit: int = 4,
    ) -> list[dict[str, Any]]:
        if not query_text.strip():
            return []
        vec = await ollama_client.embed_one(query_text)
        if not vec:
            return []
        vec_lit = vector_to_pg_literal(vec)

        if target_register_only:
            return await pg_manager.fetch_all(
                """
                SELECT uid, register_id, stage, arena, text_plain, english_gloss,
                       ROUND((1 - (embedding <=> $1::vector))::numeric, 4)::float AS similarity
                FROM cards
                WHERE embedding IS NOT NULL AND register_id = $2
                ORDER BY embedding <=> $1::vector
                LIMIT $3
                """,
                vec_lit,
                target_register_only,
                limit,
            )

        prefixes = _registers_for_anchor_langs(anchor_langs)
        like_patterns = [f"{p}%" for p in prefixes]
        return await pg_manager.fetch_all(
            """
            SELECT uid, register_id, stage, arena, text_plain, english_gloss,
                   ROUND((1 - (embedding <=> $1::vector))::numeric, 4)::float AS similarity
            FROM cards
            WHERE embedding IS NOT NULL
              AND register_id <> $2
              AND register_id LIKE ANY($3::text[])
            ORDER BY embedding <=> $1::vector
            LIMIT $4
            """,
            vec_lit,
            exclude_register,
            like_patterns,
            limit,
        )


bridge_service = BridgeService()
