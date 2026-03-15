import logging
from datetime import datetime, timezone
from typing import List, Tuple, Optional
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.memory import Memory
from app.core.vector_store import vector_store
from app.services.embedding_service import embedding_service

logger = logging.getLogger(__name__)


class SearchService:
    async def semantic_search(
        self, session: AsyncSession, query: str, limit: int = 20, source: Optional[str] = None
    ) -> List[Tuple[Memory, float]]:
        embedding = embedding_service.embed(query)
        collection = vector_store.get_collection()
        where = {"is_forgotten": {"$eq": False}}
        if source:
            where["source"] = {"$eq": source}
        try:
            results = collection.query(
                query_embeddings=[embedding],
                n_results=min(limit, max(1, collection.count())),
                where=where,
                include=["metadatas", "distances"],
            )
        except Exception:
            return []

        ids = results["ids"][0]
        scores = [max(0.0, 1.0 - d) for d in results["distances"][0]]
        if not ids:
            return []
        rows = (
            await session.execute(
                select(Memory).where(Memory.id.in_(ids), Memory.is_forgotten == False)
            )
        ).scalars().all()
        mem_by_id = {m.id: m for m in rows}
        return [(mem_by_id[i], s) for i, s in zip(ids, scores) if i in mem_by_id]

    async def keyword_search(
        self, session: AsyncSession, query: str, limit: int = 20
    ) -> List[Memory]:
        try:
            rows = await session.execute(
                text(
                    "SELECT id FROM memories_fts WHERE memories_fts MATCH :q LIMIT :limit"
                ).bindparams(q=query, limit=limit)
            )
            ids = [r[0] for r in rows]
        except Exception:
            ids = []

        if not ids:
            rows = await session.execute(
                select(Memory).where(
                    Memory.content.contains(query),
                    Memory.is_forgotten == False,
                ).limit(limit)
            )
            return list(rows.scalars().all())

        result = await session.execute(
            select(Memory).where(Memory.id.in_(ids), Memory.is_forgotten == False)
        )
        return list(result.scalars().all())

    async def hybrid_search(
        self,
        session: AsyncSession,
        query: str,
        limit: int = 10,
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Tuple[Memory, float]]:
        semantic = await self.semantic_search(session, query, limit=limit * 2, source=source)
        keyword = await self.keyword_search(session, query, limit=limit * 2)

        kw_ids = {m.id for m in keyword}
        combined: dict = {}
        for mem, s_score in semantic:
            combined[mem.id] = {"memory": mem, "semantic": s_score, "keyword": 1.0 if mem.id in kw_ids else 0.0}
        for mem in keyword:
            if mem.id not in combined:
                combined[mem.id] = {"memory": mem, "semantic": 0.0, "keyword": 1.0}

        now = datetime.now(timezone.utc)
        for item in combined.values():
            m: Memory = item["memory"]
            age_days = (now - m.created_at.replace(tzinfo=timezone.utc) if m.created_at.tzinfo is None else now - m.created_at).days
            recency = 0.8 if age_days > 30 else 1.0
            base = 0.7 * item["semantic"] + 0.3 * item["keyword"]
            if m.is_pinned:
                base *= 1.5
            base *= recency
            base *= (m.importance_score or 0.5)
            item["score"] = base

        ranked = sorted(combined.values(), key=lambda x: x["score"], reverse=True)

        if tags:
            ranked = [
                i for i in ranked
                if any(t.name in tags for t in i["memory"].tags)
            ]

        return [(i["memory"], i["score"]) for i in ranked[:limit]]


search_service = SearchService()
