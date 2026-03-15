"""Core memory business logic."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.vector_store import upsert_embedding, delete_embedding
from app.models.memory import Memory
from app.models.session import Session
from app.models.tag import Tag
from app.schemas.memory import MemoryCreate, MemoryUpdate
from app.services.embedding_service import embedding_service
from app.services.extractor import extract_auto_tags, score_importance
from app.services.search_service import search_service
from app.core.config import settings


class MemoryService:
    async def add(
        self,
        db: AsyncSession,
        payload: MemoryCreate,
    ) -> Memory:
        """Create a new memory: embed → store in Chroma → store in DB → tag → score."""
        embedding_id = str(uuid.uuid4())

        # 1. Generate embedding
        vector = embedding_service.embed(payload.content)

        # 2. Upsert into ChromaDB
        upsert_embedding(
            embedding_id=embedding_id,
            embedding=vector,
            document=payload.content,
            metadata={
                "source": payload.source,
                "session_id": payload.session_id or "",
            },
        )

        # 3. Create DB record
        memory = Memory(
            id=str(uuid.uuid4()),
            content=payload.content,
            embedding_id=embedding_id,
            source=payload.source,
            session_id=payload.session_id,
            entities={},
            importance_score=0.5,
        )
        db.add(memory)
        await db.flush()  # get memory.id

        # 4. Auto-tag
        tag_names = list(set(payload.tags + extract_auto_tags(payload.content)))
        await self._attach_tags(db, memory, tag_names)

        # 5. Score importance (entities populated by background task later)
        memory.importance_score = score_importance(payload.content, {})

        await db.flush()

        # 6. Trigger background summarization if content is long enough
        if (
            settings.auto_summarize
            and len(payload.content) >= settings.auto_summarize_threshold
        ):
            from app.workers.background import schedule_summarization
            await schedule_summarization(memory.id)

        return memory

    async def get(
        self, db: AsyncSession, memory_id: str
    ) -> Optional[Memory]:
        result = await db.execute(
            select(Memory)
            .options(selectinload(Memory.tags))
            .where(Memory.id == memory_id, Memory.is_forgotten == False)  # noqa: E712
        )
        memory = result.scalars().first()
        if memory:
            memory.accessed_at = datetime.now(timezone.utc)
            memory.access_count += 1
        return memory

    async def list(
        self,
        db: AsyncSession,
        limit: int = 20,
        offset: int = 0,
        source: Optional[str] = None,
        tag: Optional[str] = None,
        pinned_only: bool = False,
    ) -> List[Memory]:
        q = (
            select(Memory)
            .options(selectinload(Memory.tags))
            .where(Memory.is_forgotten == False)  # noqa: E712
            .order_by(Memory.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        if source:
            q = q.where(Memory.source == source)
        if pinned_only:
            q = q.where(Memory.is_pinned == True)  # noqa: E712
        if tag:
            q = q.join(Memory.tags).where(Tag.name == tag)
        result = await db.execute(q)
        return list(result.scalars().all())

    async def update(
        self, db: AsyncSession, memory_id: str, payload: MemoryUpdate
    ) -> Optional[Memory]:
        memory = await self.get(db, memory_id)
        if not memory:
            return None
        if payload.content is not None:
            memory.content = payload.content
            # Re-embed
            vector = embedding_service.embed(payload.content)
            if memory.embedding_id:
                upsert_embedding(memory.embedding_id, vector, payload.content, {"source": memory.source})
        if payload.summary is not None:
            memory.summary = payload.summary
        if payload.is_pinned is not None:
            memory.is_pinned = payload.is_pinned
        if payload.importance_score is not None:
            memory.importance_score = payload.importance_score
        if payload.tags is not None:
            await self._attach_tags(db, memory, payload.tags)
        return memory

    async def forget(self, db: AsyncSession, memory_id: str) -> bool:
        """Soft-delete: mark is_forgotten + remove from ChromaDB."""
        memory = await self.get(db, memory_id)
        if not memory:
            return False
        memory.is_forgotten = True
        if memory.embedding_id:
            delete_embedding(memory.embedding_id)
        return True

    async def pin(self, db: AsyncSession, memory_id: str) -> Optional[Memory]:
        memory = await self.get(db, memory_id)
        if not memory:
            return None
        memory.is_pinned = not memory.is_pinned
        return memory

    async def get_context(
        self,
        db: AsyncSession,
        query: str,
        max_tokens: int = 2000,
    ) -> str:
        """Return formatted context string ready to inject into an LLM prompt."""
        results = await search_service.hybrid_search(db, query, limit=10)
        lines = []
        token_count = 0
        for memory, score in results:
            snippet = memory.content[:300]
            entry = f"- [{memory.source}] {snippet}"
            token_count += len(entry.split())
            if token_count > max_tokens:
                break
            lines.append(entry)
        header = "### Relevant memories from MemoryOS:\n"
        return header + "\n".join(lines) if lines else ""

    async def bulk_add(
        self, db: AsyncSession, memories: List[MemoryCreate]
    ) -> List[Memory]:
        return [await self.add(db, m) for m in memories]

    async def _attach_tags(
        self, db: AsyncSession, memory: Memory, tag_names: List[str]
    ) -> None:
        memory.tags.clear()
        for name in tag_names[:10]:  # cap at 10 tags
            name = name.lower().strip()[:64]
            if not name:
                continue
            result = await db.execute(select(Tag).where(Tag.name == name))
            tag = result.scalars().first()
            if not tag:
                tag = Tag(id=str(uuid.uuid4()), name=name)
                db.add(tag)
                await db.flush()
            memory.tags.append(tag)


memory_service = MemoryService()
