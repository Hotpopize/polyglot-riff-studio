from __future__ import annotations

import json
import re
from typing import Any, Optional, Sequence

import httpx

from backend.config import settings


class OllamaClient:
    """Async client for local Ollama (:11434) supporting bge-m3 embeddings and gemma4/gemma3 JSON generation."""

    def __init__(self, base_url: str = settings.ollama_base_url) -> None:
        self.base_url = base_url.rstrip("/")

    async def ping(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                resp.raise_for_status()
                models = [m.get("name") for m in resp.json().get("models", [])]
                return {
                    "ok": True,
                    "base_url": self.base_url,
                    "models": models,
                    "has_embed_model": settings.ollama_embed_model in models,
                    "has_stylizer_model": settings.ollama_stylizer_model in models,
                    "has_fast_model": settings.ollama_fast_model in models,
                }
        except Exception as exc:
            return {"ok": False, "base_url": self.base_url, "error": str(exc), "models": []}

    async def embed_batch(
        self,
        texts: Sequence[str],
        model: str = settings.ollama_embed_model,
    ) -> list[Optional[list[float]]]:
        if not texts:
            return []
        cleaned = [t.strip() or " " for t in texts]
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{self.base_url}/api/embed",
                    json={"model": model, "input": cleaned},
                )
                if resp.status_code == 200:
                    embeddings = resp.json().get("embeddings", [])
                    if len(embeddings) == len(cleaned):
                        return embeddings

                # Fallback for older Ollama /api/embeddings endpoint
                results: list[Optional[list[float]]] = []
                for item in cleaned:
                    single = await client.post(
                        f"{self.base_url}/api/embeddings",
                        json={"model": model, "prompt": item},
                    )
                    single.raise_for_status()
                    results.append(single.json().get("embedding"))
                return results
        except Exception:
            return [None for _ in cleaned]

    async def embed_one(
        self,
        text: str,
        model: str = settings.ollama_embed_model,
    ) -> Optional[list[float]]:
        res = await self.embed_batch([text], model=model)
        return res[0] if res else None

    async def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.45,
    ) -> dict[str, Any]:
        chosen_model = model or settings.ollama_stylizer_model
        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": chosen_model,
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": temperature},
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
            )
            resp.raise_for_status()
            content = resp.json().get("message", {}).get("content", "{}")
            return self._extract_json(content)

    @staticmethod
    def _extract_json(raw: str) -> dict[str, Any]:
        raw = raw.strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise


ollama_client = OllamaClient()

