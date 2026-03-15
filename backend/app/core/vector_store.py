"""ChromaDB singleton — local, embedded, no external server needed."""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_chroma_client() -> chromadb.ClientAPI:
    """Return a cached ChromaDB persistent client."""
    client = chromadb.PersistentClient(
        path=str(settings.chroma_path),
        settings=ChromaSettings(anonymized_telemetry=False),
    )
    logger.info("ChromaDB initialised at %s", settings.chroma_path)
    return client


def get_memories_collection() -> chromadb.Collection:
    """Return (or create) the memories collection."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="memories",
        metadata={"hnsw:space": "cosine"},
    )


def upsert_embedding(
    embedding_id: str,
    embedding: list[float],
    document: str,
    metadata: dict[str, Any],
) -> None:
    col = get_memories_collection()
    col.upsert(
        ids=[embedding_id],
        embeddings=[embedding],
        documents=[document],
        metadatas=[metadata],
    )


def delete_embedding(embedding_id: str) -> None:
    col = get_memories_collection()
    try:
        col.delete(ids=[embedding_id])
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not delete embedding %s: %s", embedding_id, exc)


def query_embeddings(
    query_embedding: list[float],
    n_results: int = 20,
    where: dict[str, Any] | None = None,
) -> dict[str, Any]:
    col = get_memories_collection()
    kwargs: dict[str, Any] = {
        "query_embeddings": [query_embedding],
        "n_results": n_results,
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        kwargs["where"] = where
    return col.query(**kwargs)
