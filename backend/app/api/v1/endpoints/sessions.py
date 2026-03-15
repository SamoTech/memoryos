"""Session endpoints."""
from __future__ import annotations

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionRead
from app.services.summarizer import summarizer

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("", response_model=List[SessionRead])
async def list_sessions(
    limit: int = 20,
    offset: int = 0,
    source: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    q = (
        select(Session)
        .order_by(Session.started_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if source:
        q = q.where(Session.source == source)
    result = await db.execute(q)
    return result.scalars().all()


@router.post("", response_model=SessionRead, status_code=201)
async def create_session(
    payload: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    session = Session(
        id=str(uuid.uuid4()),
        source=payload.source,
        title=payload.title,
        url=payload.url,
    )
    db.add(session)
    await db.flush()
    return session


@router.get("/{session_id}", response_model=SessionRead)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Session)
        .options(selectinload(Session.memories))
        .where(Session.id == session_id)
    )
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/{session_id}/summary")
async def get_session_summary(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Session)
        .options(selectinload(Session.memories))
        .where(Session.id == session_id)
    )
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.summary:
        session.summary = await summarizer.summarize_session(session.memories)
        await db.flush()
    return {"session_id": session_id, "summary": session.summary}
