from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    root_dir: Path = ROOT_DIR
    db_json_dir: Path = ROOT_DIR / "db"

    postgres_user: str = os.getenv("POSTGRES_USER", "polyglot")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "polyglot_atelier_dev")
    postgres_db: str = os.getenv("POSTGRES_DB", "polyglot_sales")
    postgres_host: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    postgres_port: int = int(os.getenv("POSTGRES_HOST_PORT", "5433"))

    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "polyglot_atelier_dev")
    neo4j_database: str = os.getenv("NEO4J_DATABASE", "neo4j")
    neo4j_http_port: int = int(os.getenv("NEO4J_HTTP_PORT", "7474"))

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    ollama_stylizer_model: str = os.getenv("OLLAMA_STYLIZER_MODEL", "gemma4:12b")
    ollama_fast_model: str = os.getenv("OLLAMA_FAST_MODEL", "gemma3:4b")
    ollama_embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "bge-m3:latest")
    embedding_dim: int = int(os.getenv("EMBEDDING_DIM", "1024"))

    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8765"))

    @property
    def asyncpg_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def sqlalchemy_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()

