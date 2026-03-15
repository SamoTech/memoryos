"""Local embedding service using sentence-transformers.

Fallback to OpenAI text-embedding-3-small if local model unavailable.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import List

from app.core.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _load_local_model():
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(
        settings.embedding_model,
        cache_folder=str(settings.models_path),
    )
    logger.info("Loaded local embedding model: %s", settings.embedding_model)
    return model


class EmbeddingService:
    """Generate embeddings locally (all-MiniLM-L6-v2) or via OpenAI fallback."""

    def embed(self, text: str) -> List[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if settings.embedding_provider == "local":
            return self._local_embed(texts)
        return self._openai_embed(texts)

    def _local_embed(self, texts: List[str]) -> List[List[float]]:
        try:
            model = _load_local_model()
            vectors = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
            return vectors.tolist()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Local embedding failed (%s), falling back to OpenAI", exc)
            return self._openai_embed(texts)

    def _openai_embed(self, texts: List[str]) -> List[List[float]]:
        if not settings.openai_api_key:
            raise RuntimeError(
                "No OpenAI API key configured and local embedding unavailable."
            )
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts,
        )
        return [item.embedding for item in response.data]


# Module-level singleton
embedding_service = EmbeddingService()
