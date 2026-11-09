from __future__ import annotations

import json
import socket
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.config import settings
from backend.db.neo4j_client import neo4j_manager
from backend.db.postgres import pg_manager
from backend.seed.run_seed import seed_all
from backend.services.bridge_service import bridge_service
from backend.services.converse_service import converse_service
from backend.services.fsrs_service import compute_retrievability, fsrs_service
from backend.services.ollama_client import ollama_client
from backend.services.sync_service import sync_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await pg_manager.init_schema()
        await sync_service.sync_pending_to_neo4j(force_all=False)
    except Exception:
        pass
    yield
    await pg_manager.close()
    await neo4j_manager.close()


app = FastAPI(
    title="Polyglot Riff Atelier — Neo4j + PostgreSQL (pgvector) API",
    version="3.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScaffoldRequest(BaseModel):
    card_uid: Optional[str] = None
    text: Optional[str] = None
    target_register: str = "CZ_OVA"
    anchor_langs: list[str] = Field(default_factory=lambda: ["DE", "RU", "EN"])


class StylizeRequest(BaseModel):
    thought: str
    target_register: str = "CZ_OVA"
    arena: str = "terrace"
    stage: str = "COUNTERACT"
    lens_id: str = "FERGUSON"
    model: Optional[str] = None
    fast_mode: bool = False
    commit_mode: str = "stage"
    counters_state: Optional[str] = None


class GradeRequest(BaseModel):
    edge_id: str
    score: int = Field(ge=1, le=5)
    source_uid: Optional[str] = None
    target_uid: Optional[str] = None


class CommitNodeRequest(BaseModel):
    uid: Optional[str] = None
    register_id: str
    stage: str = "COUNTERACT"
    arena: str = "terrace"
    lens_id: Optional[str] = None
    text: str
    idiom_term: Optional[str] = None
    idiom_origin: str = "Atelier Workbench Addition"
    idiom_meaning: str = "High-rapport regional marker"
    delivery_cue: str = "Grounded peer inflection"
    cousin_term: Optional[str] = None
    connect_from_uid: Optional[str] = None
    counters_state: Optional[str] = None
    phonetics: str = ""
    english_gloss: str = ""


@app.get("/api/v1/health")
async def get_health() -> dict[str, Any]:
    pg_status = await pg_manager.ping()
    neo_status = await neo4j_manager.ping()
    ol_status = await ollama_client.ping()
    return {
        "ok": bool(pg_status.get("ok") and neo_status.get("ok")),
        "postgres": pg_status,
        "neo4j": neo_status,
        "ollama": ol_status,
        "models": {
            "stylizer_default": settings.ollama_stylizer_model,
            "stylizer_fast": settings.ollama_fast_model,
            "embeddings": settings.ollama_embed_model,
        },
    }


@app.get("/api/v1/languages")
async def list_languages() -> dict[str, Any]:
    langs = await pg_manager.fetch_all("SELECT * FROM languages ORDER BY code")
    regs = await pg_manager.fetch_all("SELECT * FROM registers ORDER BY lang_code, tier ASC")
    return {"languages": langs, "registers": regs}


@app.get("/api/v1/registers")
async def list_registers(
    lang_code: Optional[str] = None,
    tier: Optional[str] = None,
) -> list[dict[str, Any]]:
    rows = await pg_manager.fetch_all(
        """
        SELECT * FROM registers
        WHERE ($1::text IS NULL OR lang_code = $1)
          AND ($2::text IS NULL OR tier = $2)
        ORDER BY lang_code, tier ASC
        """,
        lang_code.lower() if lang_code else None,
        tier.upper() if tier else None,
    )
    return rows


@app.get("/api/v1/registers/{lang_code}/switcher")
async def get_register_switcher(lang_code: str) -> dict[str, Any]:
    try:
        return await bridge_service.get_register_switcher_deck(lang_code=lang_code)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/v1/arenas")
async def list_arenas() -> list[dict[str, Any]]:
    return await pg_manager.fetch_all("SELECT * FROM arenas ORDER BY id")


@app.get("/api/v1/vocab")
async def list_vocab(
    lang_code: Optional[str] = None,
    register_type: Optional[str] = None,
) -> dict[str, Any]:
    rows = await pg_manager.fetch_all(
        """
        SELECT uid, term, lang_code, register_id, register_type, meaning, ib_source, grammar_note, etymology, warning
        FROM vocab_items
        WHERE ($1::text IS NULL OR lang_code = $1)
          AND ($2::text IS NULL OR register_type = $2)
        ORDER BY lang_code, register_type, uid
        """,
        lang_code.lower() if lang_code else None,
        register_type.upper() if register_type else None,
    )
    alerts = await pg_manager.fetch_all("SELECT source_uid, target_uid FROM vocab_false_friend_alerts ORDER BY source_uid")
    return {"vocab": rows, "false_friend_alerts": alerts}


@app.get("/api/v1/songs")
async def list_songs(
    register_id: Optional[str] = None,
    lang_code: Optional[str] = None,
) -> dict[str, Any]:
    rows = await pg_manager.fetch_all(
        """
        SELECT uid, title, artist, city_region, genre, bpm, register_id,
               original_lang, original_lyric, translation_es, translation_en,
               translation_cz, translation_de, translation_ru, cultural_vibe,
               pivot_line, reinforces_card_uid, slang_vocab_uids
        FROM songs
        WHERE ($1::text IS NULL OR register_id = $1)
          AND ($2::text IS NULL OR LOWER(original_lang) LIKE '%' || $2 || '%')
        ORDER BY uid
        """,
        register_id,
        lang_code.lower() if lang_code else None,
    )
    songs = [
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
            "translations": {
                "ES": s["translation_es"],
                "EN": s["translation_en"],
                "CZ": s["translation_cz"],
                "DE": s["translation_de"],
                "RU": s["translation_ru"],
            },
            "cultural_vibe": s["cultural_vibe"],
            "pivot_line": s["pivot_line"],
            "reinforces_card_uid": s["reinforces_card_uid"],
            "slang_vocab_uids": list(s.get("slang_vocab_uids") or []),
        }
        for s in rows
    ]
    return {"songs": songs, "count": len(songs)}


@app.get("/api/v1/state/full")
async def get_full_studio_state(include_formal_personas: bool = False) -> dict[str, Any]:
    """Hydrate Atelier Studio v3.1+ in a single JSON payload compatible with DEFAULT_STATE."""
    reg_filter = "" if include_formal_personas else "WHERE tier = 'REGIONAL'"
    reg_rows = await pg_manager.fetch_all(f"SELECT * FROM registers {reg_filter} ORDER BY id")
    all_reg_rows = await pg_manager.fetch_all("SELECT * FROM registers ORDER BY lang_code, tier")
    arena_rows = await pg_manager.fetch_all("SELECT id, icon, label, short_label, arena_group, description FROM arenas ORDER BY id")
    idiom_rows = await pg_manager.fetch_all("SELECT * FROM idioms ORDER BY term")
    card_rows = await pg_manager.fetch_all(
        """
        SELECT uid, register_id, stage, arena, lens_id, title, text_html, phonetics, english_gloss, delivery_cue, idiom_terms
        FROM cards
        ORDER BY arena, uid
        """
    )
    bridge_rows = await pg_manager.fetch_all("SELECT * FROM bridges ORDER BY uid")
    edge_rows = await pg_manager.fetch_all(
        "SELECT * FROM graph_edges WHERE edge_type IN ('FLOWS_TO', 'PIVOTS_VIA') ORDER BY id"
    )
    state_rows = await pg_manager.fetch_all("SELECT * FROM room_states ORDER BY id")
    ff_rows = await pg_manager.fetch_all("SELECT * FROM false_friends ORDER BY id")
    wh_rows = await pg_manager.fetch_all(
        "SELECT * FROM staged_webhooks WHERE status = 'STAGED' ORDER BY created_at DESC"
    )
    song_rows = await pg_manager.fetch_all(
        """
        SELECT uid, title, artist, city_region, genre, bpm, register_id,
               original_lang, original_lyric, translation_es, translation_en,
               translation_cz, translation_de, translation_ru, cultural_vibe,
               pivot_line, reinforces_card_uid, slang_vocab_uids
        FROM songs
        ORDER BY uid
        """
    )
    lenses = await pg_manager.fetch_all("SELECT * FROM style_lenses ORDER BY id")

    # Core terrace 4-C cards for Studio Tab 1 + all cards accessible under allCards
    terrace_cards = [
        {
            "uid": c["uid"],
            "lang": c["register_id"],
            "stage": c["stage"],
            "arena": c["arena"],
            "text": c["text_html"],
            "phonetics": c["phonetics"],
            "english": c["english_gloss"],
            "idioms": c["idiom_terms"],
        }
        for c in card_rows
        if c["arena"] == "terrace" and c["lens_id"] is None
    ]

    return {
        "arenas": arena_rows,
        "personas": {
            r["id"]: {
                "id": r["id"],
                "tier": r["tier"],
                "lang_code": r["lang_code"],
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
        "allRegisters": {r["id"]: r for r in all_reg_rows},
        "styleLenses": {l["id"]: l for l in lenses},
        "idioms": {
            i["term"]: {
                "term": i["term"],
                "lang": i["register_id"],
                "origin": i["origin"],
                "meaning": i["meaning"],
                "delivery": i["delivery_cue"],
                "cousin": i["cousin_term"],
            }
            for i in idiom_rows
        },
        "cards": terrace_cards,
        "allCards": [
            {
                "uid": c["uid"],
                "lang": c["register_id"],
                "stage": c["stage"],
                "arena": c["arena"],
                "lens_id": c["lens_id"],
                "title": c["title"],
                "text": c["text_html"],
                "phonetics": c["phonetics"],
                "english": c["english_gloss"],
                "delivery": c["delivery_cue"],
                "idioms": c["idiom_terms"],
            }
            for c in card_rows
        ],
        "bridges": [
            {
                "uid": b["uid"],
                "from": b["from_card_uid"] or b["from_register_id"],
                "to": b["to_card_uid"] or b["to_register_id"],
                "from_register": b["from_register_id"],
                "to_register": b["to_register_id"],
                "bridge_type": b["bridge_type"],
                "text": b["text"],
                "vocal_cue": b["vocal_cue"],
                "mlf_boundary_note": b["mlf_boundary_note"],
                "weight": b["weight"],
            }
            for b in bridge_rows
        ],
        "edges": [
            {
                "id": e["id"],
                "source": e["source_uid"],
                "target": e["target_uid"],
                "type": e["edge_type"],
                "weight": e["weight"],
                "daysAgo": e["days_ago"],
                "drills": e["drills"],
                "stability": e["stability"],
                "bridgeUid": e["bridge_uid"],
                "retrievability": compute_retrievability(
                    float(e["stability"] or 4.0), int(e["days_ago"] or 0), int(e["drills"] or 1)
                ),
            }
            for e in edge_rows
        ],
        "roomStates": [
            {
                "id": s["id"],
                "label": s["label"],
                "desc": s["description"],
                "targetCardUid": s["default_card_uid"],
                "lang": s["default_register_id"],
                "effectiveness": s["effectiveness"],
                "cue": s["cue"],
            }
            for s in state_rows
        ],
        "falseFriends": [
            {
                "id": ff["id"],
                "cz": ff["target_term"],
                "ru_trap": ff["trap_term"],
                "de_calque": ff["calque_term"],
                "meaning": ff["safe_meaning"],
            }
            for ff in ff_rows
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
                "translations": {
                    "ES": s["translation_es"],
                    "EN": s["translation_en"],
                    "CZ": s["translation_cz"],
                    "DE": s["translation_de"],
                    "RU": s["translation_ru"],
                },
                "cultural_vibe": s["cultural_vibe"],
                "pivot_line": s["pivot_line"],
                "reinforces_card_uid": s["reinforces_card_uid"],
                "slang_vocab_uids": list(s.get("slang_vocab_uids") or []),
            }
            for s in song_rows
        ],
        "stagedWebhooks": [w["payload_json"] for w in wh_rows],
    }


@app.post("/api/v1/bridges/scaffold")
async def api_scaffold_bridge(req: ScaffoldRequest) -> dict[str, Any]:
    return await bridge_service.scaffold_phrase(
        card_uid=req.card_uid,
        text=req.text,
        target_register=req.target_register,
        anchor_langs=req.anchor_langs,
    )


@app.get("/api/v1/bridges/path")
async def api_find_bridge_path(
    from_register: str = Query(..., description="Source register ID, e.g. AT_VIE or CZ_STD"),
    to_register: str = Query(..., description="Target register ID, e.g. CZ_OVA or RU_ALA"),
    stage: str = Query("CHAMELEON"),
    arena: Optional[str] = Query(None),
) -> dict[str, Any]:
    return await bridge_service.find_bridge_path(
        from_register=from_register,
        to_register=to_register,
        current_stage=stage,
        arena=arena,
    )


@app.get("/api/v1/converse/resolve")
async def api_resolve_converse_style(
    register_id: str = Query("CZ_OVA"),
    arena: str = Query("terrace"),
    stage: str = Query("COUNTERACT"),
    lens_id: str = Query("DEADPAN"),
    anchor_langs: str = Query("DE,RU,EN"),
) -> dict[str, Any]:
    anchors = [a.strip().upper() for a in anchor_langs.split(",") if a.strip()]
    try:
        return await converse_service.resolve_style(
            register_id=register_id,
            arena=arena,
            stage=stage,
            lens_id=lens_id,
            anchor_langs=anchors,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/v1/converse/stylize")
async def api_stylize_thought(req: StylizeRequest) -> dict[str, Any]:
    try:
        return await converse_service.stylize_thought(
            thought=req.thought,
            target_register=req.target_register,
            arena=req.arena,
            stage=req.stage,
            lens_id=req.lens_id,
            model=req.model,
            fast_mode=req.fast_mode,
            commit_mode=req.commit_mode,
            counters_state=req.counters_state,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/v1/fsrs/grade")
async def api_grade_transition(req: GradeRequest) -> dict[str, Any]:
    try:
        return await fsrs_service.grade_transition(
            edge_id=req.edge_id,
            score=req.score,
            source_uid=req.source_uid,
            target_uid=req.target_uid,
        )
    except (LookupError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/v1/fsrs/rusty")
async def api_get_rusty_edges(register_id: Optional[str] = None) -> list[dict[str, Any]]:
    return await fsrs_service.get_rusty_edges(register_id=register_id)


@app.get("/api/v1/objections/{state_id}/resolve")
async def api_resolve_objection(state_id: str, register_id: Optional[str] = None) -> dict[str, Any]:
    try:
        cypher = """
        MATCH (c:Card)-[r:COUNTERS_STATE]->(s:State {id: $state_id})
        WHERE $reg IS NULL OR c.register_id = $reg
        RETURN c.uid AS card_uid,
               c.register_id AS register_id,
               c.stage AS stage,
               c.text AS text_plain,
               c.text_html AS text_html,
               r.effectiveness AS effectiveness,
               r.cue AS cue,
               s.label AS state_label,
               s.description AS state_description
        ORDER BY r.effectiveness DESC
        """
        matches = await neo4j_manager.run_query(cypher, {"state_id": state_id, "reg": register_id})
        if matches:
            return {"source": "neo4j_1hop", "state_id": state_id, "matches": matches}
    except Exception:
        pass

    st = await pg_manager.fetch_one("SELECT * FROM room_states WHERE id = $1", state_id)
    if not st:
        raise HTTPException(status_code=404, detail=f"State '{state_id}' not found.")
    card = await pg_manager.fetch_one("SELECT * FROM cards WHERE uid = $1", st["default_card_uid"])
    return {"source": "postgres_fallback", "state": st, "card": card}


@app.post("/api/v1/nodes/commit")
async def api_commit_node(req: CommitNodeRequest) -> dict[str, Any]:
    import random
    import time

    uid = (req.uid or "").strip() or f"{req.register_id}_{req.stage[:4]}_{int(time.time()) % 10000}_{random.randint(10, 99)}"
    idiom_obj = (
        {
            "term": req.idiom_term,
            "register_id": req.register_id,
            "origin": req.idiom_origin,
            "meaning": req.idiom_meaning,
            "delivery": req.delivery_cue,
            "cousin": req.cousin_term,
        }
        if req.idiom_term
        else None
    )
    card_obj = {
        "uid": uid,
        "register_id": req.register_id,
        "stage": req.stage,
        "arena": req.arena,
        "lens_id": req.lens_id,
        "text_html": req.text,
        "phonetics": req.phonetics,
        "english_gloss": req.english_gloss,
        "delivery_cue": req.delivery_cue,
        "idiom_terms": [req.idiom_term] if req.idiom_term else [],
        "counters_state": req.counters_state,
    }
    return await converse_service.commit_card_and_idiom(
        card=card_obj,
        idiom=idiom_obj,
        connect_from_uid=req.connect_from_uid,
    )


@app.get("/api/v1/webhooks")
async def api_list_webhooks(status: str = "STAGED") -> list[dict[str, Any]]:
    rows = await pg_manager.fetch_all(
        "SELECT * FROM staged_webhooks WHERE status = $1 ORDER BY created_at DESC",
        status.upper(),
    )
    return rows


@app.post("/api/v1/webhooks/{webhook_id}/approve")
async def api_approve_webhook(webhook_id: str) -> dict[str, Any]:
    wh = await pg_manager.fetch_one("SELECT * FROM staged_webhooks WHERE id = $1", webhook_id)
    if not wh:
        raise HTTPException(status_code=404, detail=f"Webhook '{webhook_id}' not found.")

    payload = wh["payload_json"]
    target_reg = wh["target_register_id"]
    idm = payload.get("idiom")
    card_data = payload.get("card", {})
    uid = card_data.get("uid") or f"{target_reg}_{card_data.get('stage', 'COUN')[:4]}_{webhook_id}"

    committed = await converse_service.commit_card_and_idiom(
        card={
            "uid": uid,
            "register_id": target_reg,
            "stage": card_data.get("stage", "COUNTERACT"),
            "arena": card_data.get("arena", "terrace"),
            "lens_id": card_data.get("lens_id"),
            "text_html": card_data.get("text", ""),
            "phonetics": card_data.get("phonetics", ""),
            "english_gloss": card_data.get("english_gloss", ""),
            "delivery_cue": (idm or {}).get("delivery", ""),
            "idiom_terms": [idm["term"]] if idm and idm.get("term") else [],
            "counters_state": card_data.get("counters_state"),
        },
        idiom=idm,
    )
    await pg_manager.execute(
        "UPDATE staged_webhooks SET status = 'APPROVED', approved_at = NOW() WHERE id = $1",
        webhook_id,
    )
    return {"approved": webhook_id, "committed": committed}


class ClientOutboxEvent(BaseModel):
    id: Optional[str] = None
    type: str = Field(..., description="'grade' or 'commit_node'")
    payload: dict[str, Any]
    queued_at: Optional[str] = None


class ClientOutboxBatchRequest(BaseModel):
    events: list[ClientOutboxEvent] = Field(default_factory=list)


@app.get("/api/v1/network-info")
async def api_get_network_info() -> dict[str, Any]:
    """Return local and LAN IPv4 URLs so mobile browsers on the same Wi-Fi can open the Suite Hub."""
    lan_ips: list[str] = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127.") and not ip.startswith("169.254.") and ip not in lan_ips:
                lan_ips.append(ip)
    except Exception:
        pass
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            if primary_ip and not primary_ip.startswith("127.") and primary_ip not in lan_ips:
                lan_ips.insert(0, primary_ip)
    except Exception:
        pass

    port = settings.api_port
    urls = [f"http://{ip}:{port}/index.html" for ip in lan_ips]
    return {
        "ok": True,
        "port": port,
        "localhost_url": f"http://127.0.0.1:{port}/index.html",
        "lan_ips": lan_ips,
        "lan_urls": urls,
        "primary_lan_url": urls[0] if urls else f"http://127.0.0.1:{port}/index.html",
    }


@app.post("/api/v1/sync/client-outbox")
async def api_sync_client_outbox(req: ClientOutboxBatchRequest) -> dict[str, Any]:
    """Replay offline-queued FSRS grades and custom card commits from mobile/desktop browser localStorage."""
    import random
    import time

    applied: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for ev in req.events:
        try:
            p = ev.payload or {}
            if ev.type == "grade":
                res = await fsrs_service.grade_transition(
                    edge_id=str(p.get("edge_id") or p.get("edgeId") or ""),
                    score=int(p.get("score") or 4),
                    source_uid=p.get("source_uid") or p.get("sourceUid"),
                    target_uid=p.get("target_uid") or p.get("targetUid"),
                )
                applied.append({"id": ev.id, "type": "grade", "result": res})
            elif ev.type == "commit_node":
                reg_id = str(p.get("register_id") or p.get("registerId") or "CZ_OVA")
                stage = str(p.get("stage") or "COUNTERACT")
                uid = (p.get("uid") or "").strip() or f"{reg_id}_{stage[:4]}_{int(time.time()) % 10000}_{random.randint(10, 99)}"
                idiom_term = p.get("idiom_term") or p.get("idiomTerm")
                idiom_obj = (
                    {
                        "term": idiom_term,
                        "register_id": reg_id,
                        "origin": p.get("idiom_origin") or "Mobile / Studio Outbox Addition",
                        "meaning": p.get("idiom_meaning") or "High-rapport regional marker",
                        "delivery": p.get("delivery_cue") or "Grounded peer inflection",
                        "cousin": p.get("cousin_term"),
                    }
                    if idiom_term
                    else None
                )
                card_obj = {
                    "uid": uid,
                    "register_id": reg_id,
                    "stage": stage,
                    "arena": p.get("arena") or "terrace",
                    "lens_id": p.get("lens_id"),
                    "text_html": p.get("text") or p.get("text_html") or "",
                    "phonetics": p.get("phonetics") or "",
                    "english_gloss": p.get("english_gloss") or "",
                    "delivery_cue": p.get("delivery_cue") or "Grounded peer inflection",
                    "idiom_terms": [idiom_term] if idiom_term else [],
                    "counters_state": p.get("counters_state"),
                }
                res = await converse_service.commit_card_and_idiom(
                    card=card_obj,
                    idiom=idiom_obj,
                    connect_from_uid=p.get("connect_from_uid"),
                )
                applied.append({"id": ev.id, "type": "commit_node", "result": res})
            else:
                errors.append({"id": ev.id, "type": ev.type, "error": f"Unknown event type '{ev.type}'"})
        except Exception as exc:
            errors.append({"id": ev.id, "type": ev.type, "error": str(exc)})

    sync_res = await sync_service.sync_pending_to_neo4j(force_all=False)
    return {
        "ok": len(errors) == 0,
        "applied_count": len(applied),
        "error_count": len(errors),
        "applied": applied,
        "errors": errors,
        "sync": sync_res,
    }


@app.post("/api/v1/sync/replay")
async def api_replay_sync(force_all: bool = False, prune_orphans: bool = False) -> dict[str, Any]:
    return await sync_service.sync_pending_to_neo4j(force_all=force_all, prune_orphans=prune_orphans)


@app.get("/api/v1/admin/audit")
async def api_audit_data_integrity() -> dict[str, Any]:
    return await sync_service.audit_data_integrity()


@app.post("/api/v1/admin/backup")
async def api_create_backup_snapshot(keep_last: int = 10) -> dict[str, Any]:
    return await sync_service.create_backup_snapshot(keep_last=keep_last)


@app.post("/api/v1/seed")
async def api_run_seed(compute_embeddings: bool = True) -> dict[str, Any]:
    return await seed_all(compute_embeddings=compute_embeddings)


# Mount workspace static files last so http://127.0.0.1:8765/ serves index.html & Studio HTMLs directly
app.mount("/", StaticFiles(directory=str(settings.root_dir), html=True), name="studio_static")
