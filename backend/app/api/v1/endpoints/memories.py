"""CRUD endpoints for memories."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.memory import MemoryBulkCreate, MemoryCreate, MemoryRead, MemoryUpdate
from app.services.memory_service import memory_service

router = APIRouter(prefix="/memories", tags=["memories"])


@router.get("", response_model=List[MemoryRead])
async def list_memories(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    source: Optional[str] = None,
    tag: Optional[str] = None,
    pinned_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    return await memory_service.list(db, limit, offset, source, tag, pinned_only)


@router.post("", response_model=MemoryRead, status_code=status.HTTP_201_CREATED)
async def create_memory(
    payload: MemoryCreate,
    db: AsyncSession = Depends(get_db),
):
    return await memory_service.add(db, payload)


@router.post("/bulk", response_model=List[MemoryRead], status_code=status.HTTP_201_CREATED)
async def bulk_create_memories(
    payload: MemoryBulkCreate,
    db: AsyncSession = Depends(get_db),
):
    memories = [
        MemoryCreate(
            content=m.content,
            source=payload.source or m.source,
            session_id=payload.session_id or m.session_id,
            tags=m.tags,
        )
        for m in payload.memories
    ]
    return await memory_service.bulk_add(db, memories)


@router.get("/{memory_id}", response_model=MemoryRead)
async def get_memory(
    memory_id: str,
    db: AsyncSession = Depends(get_db),
):
    memory = await memory_service.get(db, memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


@router.put("/{memory_id}", response_model=MemoryRead)
async def update_memory(
    memory_id: str,
    payload: MemoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    memory = await memory_service.update(db, memory_id, payload)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def forget_memory(
    memory_id: str,
    db: AsyncSession = Depends(get_db),
):
    success = await memory_service.forget(db, memory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Memory not found")


@router.post("/{memory_id}/pin", response_model=MemoryRead)
async def pin_memory(
    memory_id: str,
    db: AsyncSession = Depends(get_db),
):
    memory = await memory_service.pin(db, memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory
