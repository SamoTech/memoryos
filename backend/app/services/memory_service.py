import uuid
import asyncio
import logging
from typing import List, Optional, Tuple
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.memory import Memory, MemorySource
from app.models.tag import Tag
from app.models.session import Session
from app.core.vector_store import vector_store
from app.services.embedding_service import embedding_service
from app.services.summarizer import summarizer
from app.core.config import settings

logger = logging.getLogger(__name__)

TAG_COLORS = [
    "#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", "#f97316",
    "#eab308", "#22c55e", "#14b8a6", "#3b82f6", "#06b6d4",
]


class MemoryService:
    async def add(
        self,
        session: AsyncSession,
        content: str,
        source: MemorySource = MemorySource.manual,
        session_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        tags: Optional[List[str]] = None,
    ) -> Memory:
        memory_id = str(uuid.uuid4())
        embedding = embedding_service.embed(content)

        collection = vector_store.get_collection()
        collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            metadatas=[{"source": source.value, "is_forgotten": False}],
        )

        importance = await summarizer.score_importance(content)
        entities = await summarizer.extract_entities(content)

        memory = Memory(
            id=memory_id,
            content=content,
            source=source,
            session_id=session_id,
            embedding_id=memory_id,
            entities=entities,
            importance_score=importance,
        )

        if tags:
            memory.tags = await self._get_or_create_tags(session, tags)

        session.add(memory)
        await session.commit()
        await session.refresh(memory)

        await self._sync_fts(session, memory)

        if settings.AUTO_SUMMARIZE and len(content) >= settings.AUTO_SUMMARIZE_THRESHOLD:
            asyncio.create_task(self._background_summarize(memory_id, content))

        return memory

    async def bulk_add(
        self,
        session: AsyncSession,
        items: List[dict],
    ) -> List[Memory]:
        memories = []
        for item in items:
            m = await self.add(
                session,
                content=item["content"],
                source=MemorySource(item.get("source", "api")),
                session_id=item.get("session_id"),
                metadata=item.get("metadata"),
                tags=item.get("tags", []),
            )
            memories.append(m)
        return memories

    async def get(
        self, session: AsyncSession, memory_id: str
    ) -> Optional[Memory]:
        result = await session.execute(
            select(Memory)
            .options(selectinload(Memory.tags))
            .where(Memory.id == memory_id, Memory.is_forgotten == False)
        )
        memory = result.scalar_one_or_none()
        if memory:
            memory.access_count += 1
            memory.accessed_at = datetime.now(timezone.utc)
            await session.commit()
        return memory

    async def list(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        source: Optional[str] = None,
        pinned_only: bool = False,
    ) -> List[Memory]:
        q = (
            select(Memory)
            .options(selectinload(Memory.tags))
            .where(Memory.is_forgotten == False)
            .order_by(Memory.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        if source:
            q = q.where(Memory.source == source)
        if pinned_only:
            q = q.where(Memory.is_pinned == True)
        result = await session.execute(q)
        return list(result.scalars().all())

    async def update(
        self,
        session: AsyncSession,
        memory_id: str,
        **kwargs,
    ) -> Optional[Memory]:
        memory = await self.get(session, memory_id)
        if not memory:
            return None
        for key, val in kwargs.items():
            if val is not None and hasattr(memory, key):
                setattr(memory, key, val)
        await session.commit()
        await session.refresh(memory)
        return memory

    async def forget(
        self, session: AsyncSession, memory_id: str
    ) -> bool:
        memory = await session.get(Memory, memory_id)
        if not memory:
            return False
        memory.is_forgotten = True
        await session.commit()
        try:
            collection = vector_store.get_collection()
            collection.delete(ids=[memory_id])
        except Exception as e:
            logger.warning(f"Chroma delete failed: {e}")
        return True

    async def pin(
        self, session: AsyncSession, memory_id: str
    ) -> Optional[Memory]:
        memory = await session.get(Memory, memory_id)
        if not memory:
            return None
        memory.is_pinned = not memory.is_pinned
        await session.commit()
        await session.refresh(memory)
        return memory

    async def get_context(
        self, session: AsyncSession, query: str, max_tokens: int = 2000
    ) -> str:
        from app.services.search_service import search_service
        results = await search_service.hybrid_search(session, query, limit=10)
        lines = []
        total = 0
        for memory, score in results:
            text = memory.summary or memory.content
            tokens = len(text.split())
            if total + tokens > max_tokens:
                break
            lines.append(f"[{memory.source.value} | {memory.created_at.date()}] {text}")
            total += tokens
        return "\n\n".join(lines)

    async def stats(self, session: AsyncSession) -> dict:
        total = (await session.execute(
            select(func.count(Memory.id)).where(Memory.is_forgotten == False)
        )).scalar_one()
        pinned = (await session.execute(
            select(func.count(Memory.id)).where(Memory.is_pinned == True, Memory.is_forgotten == False)
        )).scalar_one()
        by_source = (await session.execute(
            select(Memory.source, func.count(Memory.id))
            .where(Memory.is_forgotten == False)
            .group_by(Memory.source)
        )).all()
        return {
            "total_memories": total,
            "pinned_memories": pinned,
            "by_source": {row[0].value: row[1] for row in by_source},
        }

    async def _background_summarize(self, memory_id: str, content: str):
        try:
            summary = await summarizer.summarize_memory(content)
            async with __import__("app.core.database", fromlist=["AsyncSessionLocal"]).AsyncSessionLocal() as session:
                memory = await session.get(Memory, memory_id)
                if memory:
                    memory.summary = summary
                    await session.commit()
        except Exception as e:
            logger.warning(f"Background summarize failed for {memory_id}: {e}")

    async def _sync_fts(self, session: AsyncSession, memory: Memory):
        try:
            await session.execute(
                __import__("sqlalchemy").text(
                    "INSERT INTO memories_fts(content, summary, id) VALUES (:content, :summary, :id)"
                ).bindparams(
                    content=memory.content,
                    summary=memory.summary or "",
                    id=memory.id,
                )
            )
            await session.commit()
        except Exception as e:
            logger.debug(f"FTS sync: {e}")

    async def _get_or_create_tags(
        self, session: AsyncSession, tag_names: List[str]
    ) -> List[Tag]:
        tags = []
        for i, name in enumerate(tag_names):
            name = name.strip().lower()
            existing = (await session.execute(
                select(Tag).where(Tag.name == name)
            )).scalar_one_or_none()
            if existing:
                tags.append(existing)
            else:
                tag = Tag(
                    name=name,
                    color=TAG_COLORS[i % len(TAG_COLORS)],
                )
                session.add(tag)
                await session.flush()
                tags.append(tag)
        return tags


memory_service = MemoryService()
