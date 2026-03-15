import os
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.memory_service import memory_service
from app.core.config import settings

router = APIRouter()


@router.get("")
async def get_stats(session: AsyncSession = Depends(get_session)):
    stats = await memory_service.stats(session)
    db_path = settings.DATA_DIR / "memories.db"
    chroma_path = settings.DATA_DIR / "chroma"
    db_size = db_path.stat().st_size if db_path.exists() else 0
    chroma_size = sum(
        f.stat().st_size for f in chroma_path.rglob("*") if f.is_file()
    ) if chroma_path.exists() else 0
    stats["storage_bytes"] = db_size + chroma_size
    stats["storage_mb"] = round((db_size + chroma_size) / 1024 / 1024, 2)
    return stats
