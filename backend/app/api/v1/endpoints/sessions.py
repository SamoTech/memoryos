import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.database import get_session
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionRead, SessionDetail
from app.services.summarizer import summarizer

router = APIRouter()


@router.get("", response_model=List[SessionRead])
async def list_sessions(
    skip: int = 0, limit: int = 50,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Session).order_by(Session.started_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.post("", response_model=SessionRead, status_code=201)
async def create_session(
    payload: SessionCreate,
    session: AsyncSession = Depends(get_session)
):
    s = Session(id=str(uuid.uuid4()), **payload.model_dump())
    session.add(s)
    await session.commit()
    await session.refresh(s)
    return s


@router.get("/{session_id}", response_model=SessionDetail)
async def get_session_detail(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Session)
        .options(selectinload(Session.memories))
        .where(Session.id == session_id)
    )
    s = result.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return s


@router.get("/{session_id}/summary")
async def get_session_summary(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Session)
        .options(selectinload(Session.memories))
        .where(Session.id == session_id)
    )
    s = result.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    if not s.summary:
        s.summary = await summarizer.summarize_session(s.memories)
        await db.commit()
    return {"summary": s.summary}
