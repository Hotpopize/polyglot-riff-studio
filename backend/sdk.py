from __future__ import annotations

from typing import Any, Optional, Sequence

from backend.db.neo4j_client import neo4j_manager
from backend.db.postgres import pg_manager
from backend.seed.run_seed import seed_all
from backend.services.bridge_service import bridge_service
from backend.services.converse_service import converse_service
from backend.services.fsrs_service import fsrs_service
from backend.services.ollama_client import ollama_client
from backend.services.sync_service import sync_service


class PolyglotFacade:
    """Ergonomic Python SDK facade for bridge languages, regional converse styles, and FSRS graph state."""

    async def status(self) -> dict[str, Any]:
        pg_info = await pg_manager.ping()
        neo_info = await neo4j_manager.ping()
        ol_info = await ollama_client.ping()
        return {"postgres": pg_info, "neo4j": neo_info, "ollama": ol_info}

    async def seed(self, compute_embeddings: bool = True) -> dict[str, Any]:
        return await seed_all(compute_embeddings=compute_embeddings)

    async def sync(self, force_all: bool = False, prune_orphans: bool = False) -> dict[str, Any]:
        return await sync_service.sync_pending_to_neo4j(force_all=force_all, prune_orphans=prune_orphans)

    async def audit(self) -> dict[str, Any]:
        return await sync_service.audit_data_integrity()

    async def backup(self, keep_last: int = 10) -> dict[str, Any]:
        return await sync_service.create_backup_snapshot(keep_last=keep_last)

    async def scaffold(
        self,
        card_uid: Optional[str] = None,
        *,
        text: Optional[str] = None,
        target_register: str = "CZ_OVA",
        anchor_langs: Sequence[str] = ("DE", "RU", "EN"),
    ) -> dict[str, Any]:
        return await bridge_service.scaffold_phrase(
            card_uid=card_uid,
            text=text,
            target_register=target_register,
            anchor_langs=anchor_langs,
        )

    async def bridge(
        self,
        from_register: str,
        to_register: str,
        *,
        stage: str = "CHAMELEON",
        arena: Optional[str] = None,
    ) -> dict[str, Any]:
        return await bridge_service.find_bridge_path(
            from_register=from_register,
            to_register=to_register,
            current_stage=stage,
            arena=arena,
        )

    async def switcher(self, lang_code: str = "cs") -> dict[str, Any]:
        return await bridge_service.get_register_switcher_deck(lang_code=lang_code)

    async def converse(
        self,
        register: str = "CZ_OVA",
        *,
        arena: str = "terrace",
        stage: str = "COUNTERACT",
        lens: str = "DEADPAN",
        anchor_langs: Sequence[str] = ("DE", "RU", "EN"),
    ) -> dict[str, Any]:
        return await converse_service.resolve_style(
            register_id=register,
            arena=arena,
            stage=stage,
            lens_id=lens,
            anchor_langs=anchor_langs,
        )

    async def stylize(
        self,
        thought: str,
        *,
        target_register: str = "CZ_OVA",
        arena: str = "terrace",
        stage: str = "COUNTERACT",
        lens: str = "FERGUSON",
        fast_mode: bool = False,
        commit: bool = False,
    ) -> dict[str, Any]:
        return await converse_service.stylize_thought(
            thought=thought,
            target_register=target_register,
            arena=arena,
            stage=stage,
            lens_id=lens,
            fast_mode=fast_mode,
            commit_mode="commit" if commit else "stage",
        )

    async def grade(self, edge_id: str, score: int) -> dict[str, Any]:
        return await fsrs_service.grade_transition(edge_id=edge_id, score=score)

    async def close(self) -> None:
        await pg_manager.close()
        await neo4j_manager.close()


polyglot = PolyglotFacade()

