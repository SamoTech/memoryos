from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.models.tag import Tag
from app.schemas.memory import TagRead, MemoryRead

router = APIRouter()


@router.get("", response_model=List[TagRead])
async def list_tags(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Tag).order_by(Tag.memory_count.desc()))
    return result.scalars().all()


@router.get("/{name}/memories", response_model=List[MemoryRead])
async def memories_by_tag(
    name: str,
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_session),
):
    tag = (await session.execute(select(Tag).where(Tag.name == name))).scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return [
        m for m in tag.memories
        if not m.is_forgotten
    ][skip : skip + limit]
