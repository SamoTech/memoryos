"""Trigger summarization of pending memories."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.memory import Memory
from app.workers.background import schedule_summarization

router = APIRouter(prefix="/summarize", tags=["summarize"])


@router.post("")
async def trigger_summarization(
    db: AsyncSession = Depends(get_db),
):
    """Queue all memories without summaries for background summarization."""
    result = await db.execute(
        select(Memory.id).where(
            Memory.summary.is_(None),
            Memory.is_forgotten == False,  # noqa: E712
        )
    )
    ids = result.scalars().all()
    for mid in ids:
        await schedule_summarization(mid)
    return {"queued": len(ids)}
