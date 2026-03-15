"""Async background task worker."""
from __future__ import annotations

import asyncio
import logging
from collections import deque
from typing import Deque

logger = logging.getLogger(__name__)

# Simple in-process task queue
_pending_memory_ids: Deque[str] = deque(maxlen=500)


async def schedule_summarization(memory_id: str) -> None:
    """Enqueue a memory for background summarization."""
    _pending_memory_ids.append(memory_id)


async def process_pending_summarizations() -> None:
    """Process queued summarization jobs — called by background task loop."""
    from app.core.database import AsyncSessionLocal
    from app.models.memory import Memory
    from app.services.summarizer import summarizer
    from app.services.extractor import score_importance
    from sqlalchemy import select

    while _pending_memory_ids:
        memory_id = _pending_memory_ids.popleft()
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(select(Memory).where(Memory.id == memory_id))
                memory = result.scalars().first()
                if not memory:
                    continue
                summary = await summarizer.summarize_memory(memory.content)
                entities = await summarizer.extract_entities(memory.content)
                memory.summary = summary or memory.summary
                memory.entities = entities
                memory.importance_score = score_importance(memory.content, entities)
                await db.commit()
                logger.info("Summarised memory %s", memory_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to summarise memory %s: %s", memory_id, exc)


async def background_worker_loop() -> None:
    """Runs indefinitely, processing jobs every 10 seconds."""
    while True:
        await asyncio.sleep(10)
        await process_pending_summarizations()
