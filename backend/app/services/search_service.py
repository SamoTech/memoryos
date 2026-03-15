"""Hybrid search: semantic (ChromaDB) + keyword (SQLite FTS5)."""
from __future__ import annotations

import math
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.vector_store import query_embeddings
from app.models.memory import Memory
from app.services.embedding_service import embedding_service


class SearchService:
    async def semantic_search(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 20,
        source: Optional[str] = None,
    ) -> List[Tuple[Memory, float]]:
        """ChromaDB cosine similarity search."""
        vector = embedding_service.embed(query)
        where = {"source": source} if source else None
        results = query_embeddings(vector, n_results=limit, where=where)

        ids = results["ids"][0] if results["ids"] else []
        distances = results["distances"][0] if results["distances"] else []

        if not ids:
            return []

        # Convert cosine distance (0=identical, 2=opposite) to similarity score
        scores = {eid: 1 - (d / 2) for eid, d in zip(ids, distances)}

        # Fetch from DB to get full objects (filter forgotten)
        result = await db.execute(
            select(Memory)
            .options(selectinload(Memory.tags))
            .where(Memory.embedding_id.in_(ids), Memory.is_forgotten == False)  # noqa: E712
        )
        memories = result.scalars().all()
        return [
            (m, scores.get(m.embedding_id, 0.0))
            for m in sorted(memories, key=lambda m: scores.get(m.embedding_id, 0), reverse=True)
        ]

    async def keyword_search(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 20,
    ) -> List[Memory]:
        """Simple LIKE-based keyword search (SQLite FTS5 upgrade path)."""
        like_q = f"%{query}%"
        result = await db.execute(
            select(Memory)
            .options(selectinload(Memory.tags))
            .where(
                Memory.is_forgotten == False,  # noqa: E712
                Memory.content.ilike(like_q),
            )
            .order_by(Memory.importance_score.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def hybrid_search(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 10,
        source: Optional[str] = None,
    ) -> List[Tuple[Memory, float]]:
        """
        Merge semantic + keyword results.
        Final score = (0.7 × semantic_score) + (0.3 × keyword_score)
        Boost pinned ×1.5x
        Penalise memories older than 30 days by ×0.8
        """
        semantic_results = await self.semantic_search(db, query, limit=limit * 2, source=source)
        keyword_results = await self.keyword_search(db, query, limit=limit * 2)

        scores: dict[str, float] = {}

        for memory, score in semantic_results:
            scores[memory.id] = 0.7 * score

        kw_set = {m.id: m for m in keyword_results}
        for mid in kw_set:
            scores[mid] = scores.get(mid, 0.0) + 0.3 * 1.0  # keyword hit = 1.0 score

        all_memories: dict[str, Memory] = {m.id: m for m, _ in semantic_results}
        all_memories.update(kw_set)

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=30)

        ranked: List[Tuple[Memory, float]] = []
        for mid, raw_score in scores.items():
            memory = all_memories.get(mid)
            if not memory:
                continue
            final = raw_score * memory.importance_score
            if memory.is_pinned:
                final *= 1.5
            created = memory.created_at
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            if created < cutoff:
                final *= 0.8
            ranked.append((memory, round(final, 6)))

        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked[:limit]


search_service = SearchService()
