from __future__ import annotations

from typing import Any

from backend.db.postgres import pg_manager
from backend.services.sync_service import sync_service


def compute_retrievability(stability: float, days_ago: int, drills: int = 1) -> float:
    eff_stability = stability if stability and stability > 0 else max(1, drills) * 3.0
    days = max(0, days_ago or 0)
    return round((1.0 + days / (9.0 * eff_stability)) ** -1, 4)


def is_edge_rusty(weight: float, stability: float, days_ago: int, drills: int = 1) -> bool:
    r_val = compute_retrievability(stability, days_ago, drills)
    return r_val < 0.75 or weight < 0.60 or days_ago >= 7


class FSRSService:
    """Spaced-Repetition Edge Mastery Engine backed by PostgreSQL ledger + Neo4j edge sync."""

    async def grade_transition(
        self,
        edge_id: str,
        score: int,
        source_uid: str | None = None,
        target_uid: str | None = None,
    ) -> dict[str, Any]:
        if score not in (1, 2, 3, 4, 5):
            raise ValueError("FSRS score must be an integer between 1 and 5.")

        edge = await pg_manager.fetch_one("SELECT * FROM graph_edges WHERE id = $1", edge_id)
        if not edge and source_uid and target_uid:
            edge = await pg_manager.fetch_one(
                "SELECT * FROM graph_edges WHERE source_uid = $1 AND target_uid = $2 LIMIT 1",
                source_uid,
                target_uid,
            )
        if not edge:
            raise LookupError(f"Edge '{edge_id}' not found.")
        edge_id = edge["id"]

        prev_w = float(edge["weight"])
        prev_s = float(edge["stability"] or 4.0)
        prev_days = int(edge["days_ago"] or 0)
        drills = int(edge["drills"] or 1) + 1

        delta = (score - 3) * 0.07
        new_w = round(max(0.15, min(0.99, prev_w + delta)), 2)

        if score <= 2:
            new_s = round(max(1.5, prev_s * 0.45), 2)
            new_days = prev_days
        else:
            mult = 1.85 if score == 5 else (1.50 if score == 4 else 1.25)
            new_s = round(prev_s * mult, 2)
            new_days = 0

        new_r = compute_retrievability(new_s, new_days, drills)

        pool = await pg_manager.get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    UPDATE graph_edges
                    SET weight = $2,
                        stability = $3,
                        days_ago = $4,
                        drills = $5,
                        last_drilled_at = NOW(),
                        sync_status = 'PENDING'
                    WHERE id = $1
                    """,
                    edge_id,
                    new_w,
                    new_s,
                    new_days,
                    drills,
                )
                await conn.execute(
                    """
                    INSERT INTO fsrs_review_events (
                        edge_id, score, prev_weight, new_weight, prev_stability, new_stability, retrievability
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                    edge_id,
                    score,
                    prev_w,
                    new_w,
                    prev_s,
                    new_s,
                    new_r,
                )

        sync_result = await sync_service.sync_pending_to_neo4j()
        return {
            "edge_id": edge_id,
            "source_uid": edge["source_uid"],
            "target_uid": edge["target_uid"],
            "score": score,
            "prev_weight": prev_w,
            "new_weight": new_w,
            "weight": new_w,
            "prev_stability": prev_s,
            "new_stability": new_s,
            "stability": new_s,
            "days_ago": new_days,
            "drills": drills,
            "retrievability": new_r,
            "rusty": is_edge_rusty(new_w, new_s, new_days, drills),
            "neo4j_synced": sync_result.get("neo4j_ok", False),
        }

    async def get_rusty_edges(self, register_id: str | None = None) -> list[dict[str, Any]]:
        rows = await pg_manager.fetch_all(
            """
            SELECT e.*, c1.register_id AS source_register, c2.register_id AS target_register
            FROM graph_edges e
            LEFT JOIN cards c1 ON c1.uid = e.source_uid
            LEFT JOIN cards c2 ON c2.uid = e.target_uid
            WHERE e.edge_type IN ('FLOWS_TO', 'PIVOTS_VIA')
            ORDER BY e.weight ASC, e.days_ago DESC
            """
        )
        rusty_list = []
        for r in rows:
            if register_id and register_id != "ALL":
                if r.get("source_register") != register_id and r.get("target_register") != register_id:
                    continue
            w = float(r["weight"])
            s = float(r["stability"] or 4.0)
            d = int(r["days_ago"] or 0)
            drills = int(r["drills"] or 1)
            if is_edge_rusty(w, s, d, drills):
                r["retrievability"] = compute_retrievability(s, d, drills)
                rusty_list.append(r)
        return rusty_list


fsrs_service = FSRSService()
