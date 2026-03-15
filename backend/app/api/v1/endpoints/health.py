from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_session
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    db_ok = False
    try:
        await session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass
    return {
        "status": "ok" if db_ok else "degraded",
        "version": "1.0.0",
        "database": "ok" if db_ok else "error",
        "data_dir": str(settings.DATA_DIR),
        "embedding_provider": settings.EMBEDDING_PROVIDER,
        "summarizer_provider": settings.SUMMARIZER_PROVIDER,
    }
