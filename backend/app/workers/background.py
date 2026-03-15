import asyncio
import logging
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.memory import Memory
from sqlalchemy import select

logger = logging.getLogger(__name__)


async def run_retention_cleanup():
    if settings.DATA_RETENTION_DAYS == 0:
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.DATA_RETENTION_DAYS)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Memory).where(
                Memory.created_at < cutoff,
                Memory.is_forgotten == False,
                Memory.is_pinned == False,
            )
        )
        memories = result.scalars().all()
        for memory in memories:
            memory.is_forgotten = True
            logger.info(f"Retention cleanup: forgetting {memory.id}")
        await session.commit()


async def background_worker():
    while True:
        try:
            await run_retention_cleanup()
        except Exception as e:
            logger.error(f"Background worker error: {e}")
        await asyncio.sleep(3600)
