"""Health check + stats endpoint."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.memory import Memory
from app.models.session import Session
from app.models.tag import Tag
from app.core.config import settings

router = APIRouter(tags=["health"])

VERSION = "1.0.0"


@router.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    total_memories = (await db.execute(func.count(Memory.id).select())).scalar() or 0
    total_sessions = (await db.execute(func.count(Session.id).select())).scalar() or 0
    return {
        "status": "ok",
        "version": VERSION,
        "data_dir": str(settings.data_dir),
        "total_memories": total_memories,
        "total_sessions": total_sessions,
    }


@router.get("/api/v1/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    total_memories = (await db.execute(select(func.count(Memory.id)).where(Memory.is_forgotten == False))).scalar() or 0  # noqa: E712
    total_sessions = (await db.execute(select(func.count(Session.id)))).scalar() or 0
    total_tags = (await db.execute(select(func.count(Tag.id)))).scalar() or 0
    pinned = (await db.execute(select(func.count(Memory.id)).where(Memory.is_pinned == True))).scalar() or 0  # noqa: E712

    db_path = settings.data_dir / "memories.db"
    db_size_mb = round(db_path.stat().st_size / 1024 / 1024, 2) if db_path.exists() else 0

    return {
        "total_memories": total_memories,
        "total_sessions": total_sessions,
        "total_tags": total_tags,
        "pinned_memories": pinned,
        "db_size_mb": db_size_mb,
    }


@router.get("/api/v1/tags")
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).order_by(Tag.memory_count.desc()))
    return result.scalars().all()
