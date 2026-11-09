from __future__ import annotations

import json
from typing import Optional

try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

from backend.db.neo4j_client import neo4j_manager
from backend.db.postgres import pg_manager
from backend.services.bridge_service import bridge_service
from backend.services.converse_service import converse_service
from backend.services.fsrs_service import fsrs_service
from backend.services.ollama_client import ollama_client

mcp = FastMCP("Polyglot Riff Atelier")


@mcp.tool()
async def get_backend_status() -> str:
    """Check live PostgreSQL (pgvector), Neo4j (+APOC), and Ollama model status and node/edge counts."""
    res = {
        "postgres": await pg_manager.ping(),
        "neo4j": await neo4j_manager.ping(),
        "ollama": await ollama_client.ping(),
    }
    return json.dumps(res, ensure_ascii=False, default=str, indent=2)


@mcp.tool()
async def resolve_bridge_path(
    from_register: str,
    to_register: str,
    stage: str = "CHAMELEON",
    arena: Optional[str] = None,
) -> str:
    """Find optimal multi-hop code-switch or register-drop (:PIVOTS_VIA) bridge paths between two registers (e.g. CZ_STD -> CZ_OVA or AT_VIE -> CZ_OVA)."""
    res = await bridge_service.find_bridge_path(
        from_register=from_register,
        to_register=to_register,
        current_stage=stage,
        arena=arena,
    )
    return json.dumps(res, ensure_ascii=False, default=str, indent=2)


@mcp.tool()
async def scaffold_phrase_bridges(
    target_register: str = "CZ_OVA",
    card_uid: Optional[str] = None,
    text: Optional[str] = None,
    anchor_langs: str = "DE,RU,EN",
) -> str:
    """Return 3-layer bridge scaffolding: (1) cognates, calques & false-friend shields, (2) :PIVOTS_VIA switches, (3) :SHARES_VIBE_WITH + pgvector semantic cousins."""
    anchors = [a.strip().upper() for a in anchor_langs.split(",") if a.strip()]
    res = await bridge_service.scaffold_phrase(
        card_uid=card_uid,
        text=text,
        target_register=target_register,
        anchor_langs=anchors,
    )
    return json.dumps(res, ensure_ascii=False, default=str, indent=2)


@mcp.tool()
async def get_register_switcher_flow(lang_code: str = "cs") -> str:
    """Fetch the Formal Boardroom -> Register-Drop Bridge -> Regional Insider 4-C sequence for cs, de, ru, en, or es."""
    res = await bridge_service.get_register_switcher_deck(lang_code=lang_code)
    return json.dumps(res, ensure_ascii=False, default=str, indent=2)


@mcp.tool()
async def resolve_regional_converse(
    register_id: str = "CZ_OVA",
    arena: str = "terrace",
    stage: str = "COUNTERACT",
    lens_id: str = "DEADPAN",
    anchor_langs: str = "DE,RU,EN",
) -> str:
    """Lookup regional converse phrasing, prosody cues, posture, and cross-language bridges for (register x arena x 4-C stage x comic/salon lens)."""
    anchors = [a.strip().upper() for a in anchor_langs.split(",") if a.strip()]
    res = await converse_service.resolve_style(
        register_id=register_id,
        arena=arena,
        stage=stage,
        lens_id=lens_id,
        anchor_langs=anchors,
    )
    return json.dumps(res, ensure_ascii=False, default=str, indent=2)


@mcp.tool()
async def stylize_thought_into_register(
    thought: str,
    target_register: str = "CZ_OVA",
    arena: str = "terrace",
    stage: str = "COUNTERACT",
    lens_id: str = "FERGUSON",
    fast_mode: bool = False,
    commit: bool = False,
) -> str:
    """Rewrite any raw EN/DE/RU thought into authentic regional speech using local Ollama (gemma4:12b / gemma3:4b) with idiom anchoring and false-friend validation."""
    res = await converse_service.stylize_thought(
        thought=thought,
        target_register=target_register,
        arena=arena,
        stage=stage,
        lens_id=lens_id,
        fast_mode=fast_mode,
        commit_mode="commit" if commit else "stage",
    )
    return json.dumps(res, ensure_ascii=False, default=str, indent=2)


@mcp.tool()
async def resolve_room_objection(state_id: str, register_id: Optional[str] = None) -> str:
    """1-hop Neo4j (:COUNTERS_STATE) objection resolver for MANUAL_GRIND, CORPORATE_SHIELD, OVERTHINKING, or PLAYING_IT_SAFE."""
    cypher = """
    MATCH (c:Card)-[r:COUNTERS_STATE]->(s:State {id: $state_id})
    WHERE $reg IS NULL OR c.register_id = $reg
    RETURN c.uid AS card_uid, c.register_id AS register_id, c.text AS text, r.effectiveness AS effectiveness, r.cue AS cue
    ORDER BY r.effectiveness DESC
    """
    rows = await neo4j_manager.run_query(cypher, {"state_id": state_id, "reg": register_id})
    return json.dumps({"state_id": state_id, "matches": rows}, ensure_ascii=False, indent=2)


@mcp.tool()
async def grade_fsrs_transition(edge_id: str, score: int) -> str:
    """Grade an FSRS conversational transition edge (score 1-5), log to PostgreSQL review history, and update Neo4j edge weight/stability."""
    res = await fsrs_service.grade_transition(edge_id=edge_id, score=score)
    return json.dumps(res, ensure_ascii=False, default=str, indent=2)


if __name__ == "__main__":
    mcp.run()
