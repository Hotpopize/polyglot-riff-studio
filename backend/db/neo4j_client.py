from __future__ import annotations

from typing import Any, Optional
from neo4j import AsyncDriver, AsyncGraphDatabase

from backend.config import settings

NEO4J_CONSTRAINTS = [
    "CREATE CONSTRAINT lang_code_unique IF NOT EXISTS FOR (l:Language) REQUIRE l.code IS UNIQUE",
    "CREATE CONSTRAINT register_id_unique IF NOT EXISTS FOR (r:Register) REQUIRE r.id IS UNIQUE",
    "CREATE CONSTRAINT persona_id_unique IF NOT EXISTS FOR (p:Persona) REQUIRE p.id IS UNIQUE",
    "CREATE CONSTRAINT arena_id_unique IF NOT EXISTS FOR (a:Arena) REQUIRE a.id IS UNIQUE",
    "CREATE CONSTRAINT card_uid_unique IF NOT EXISTS FOR (c:Card) REQUIRE c.uid IS UNIQUE",
    "CREATE CONSTRAINT vocab_uid_unique IF NOT EXISTS FOR (v:Vocab) REQUIRE v.uid IS UNIQUE",
    "CREATE CONSTRAINT song_uid_unique IF NOT EXISTS FOR (s:Song) REQUIRE s.uid IS UNIQUE",
    "CREATE CONSTRAINT bridge_uid_unique IF NOT EXISTS FOR (b:Bridge) REQUIRE b.uid IS UNIQUE",
    "CREATE CONSTRAINT idiom_term_unique IF NOT EXISTS FOR (i:Idiom) REQUIRE i.term IS UNIQUE",
    "CREATE CONSTRAINT state_id_unique IF NOT EXISTS FOR (s:State) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT false_friend_id_unique IF NOT EXISTS FOR (f:FalseFriend) REQUIRE f.id IS UNIQUE",
    "CREATE INDEX card_stage_idx IF NOT EXISTS FOR (c:Card) ON (c.stage)",
    "CREATE INDEX card_arena_idx IF NOT EXISTS FOR (c:Card) ON (c.arena)",
]


class Neo4jManager:
    """Async Neo4j 5 driver wrapper for multi-hop bridge and 4-C traversals."""

    def __init__(
        self,
        uri: str = settings.neo4j_uri,
        user: str = settings.neo4j_user,
        password: str = settings.neo4j_password,
        database: str = settings.neo4j_database,
    ) -> None:
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        self._driver: Optional[AsyncDriver] = None

    def get_driver(self) -> AsyncDriver:
        if self._driver is None:
            self._driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                max_connection_lifetime=1800,
            )
        return self._driver

    async def init_constraints(self) -> None:
        driver = self.get_driver()
        async with driver.session(database=self.database) as session:
            for stmt in NEO4J_CONSTRAINTS:
                await session.run(stmt)

    async def run_query(
        self,
        cypher: str,
        params: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        driver = self.get_driver()
        async with driver.session(database=self.database) as session:
            result = await session.run(cypher, params or {})
            records = await result.data()
            return records

    async def ping(self) -> dict[str, Any]:
        try:
            driver = self.get_driver()
            await driver.verify_connectivity()
            stats = await self.run_query(
                """
                MATCH (n)
                WITH count(n) AS nodes
                OPTIONAL MATCH ()-[r]->()
                RETURN nodes, count(r) AS relationships
                """
            )
            apoc_check = await self.run_query("RETURN apoc.version() AS apoc_version")
            row = stats[0] if stats else {"nodes": 0, "relationships": 0}
            return {
                "ok": True,
                "uri": self.uri,
                "database": self.database,
                "apoc_version": apoc_check[0]["apoc_version"] if apoc_check else None,
                "counts": row,
            }
        except Exception as exc:
            return {"ok": False, "uri": self.uri, "error": str(exc)}

    async def close(self) -> None:
        if self._driver is not None:
            await self._driver.close()
            self._driver = None


neo4j_manager = Neo4jManager()
