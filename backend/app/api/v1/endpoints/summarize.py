from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_session
from app.models.memory import Memory
from app.services.summarizer import summarizer

router = APIRouter()


class SummarizeRequest(BaseModel):
    text: str


@router.post("")
async def summarize_text(payload: SummarizeRequest):
    summary = await summarizer.summarize_memory(payload.text)
    return {"summary": summary}


@router.post("/pending")
async def summarize_pending(
    limit: int = 50,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Memory)
        .where(Memory.summary == None, Memory.is_forgotten == False)
        .limit(limit)
    )
    memories = result.scalars().all()
    updated = 0
    for memory in memories:
        if len(memory.content) >= 100:
            memory.summary = await summarizer.summarize_memory(memory.content)
            updated += 1
    await session.commit()
    return {"updated": updated}
