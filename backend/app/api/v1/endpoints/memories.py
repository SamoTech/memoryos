from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.memory import MemoryCreate, MemoryRead, MemoryUpdate
from app.services.memory_service import memory_service

router = APIRouter()


@router.get("", response_model=List[MemoryRead])
async def list_memories(
    skip: int = 0,
    limit: int = Query(50, le=200),
    source: Optional[str] = None,
    pinned: bool = False,
    session: AsyncSession = Depends(get_session),
):
    return await memory_service.list(session, skip=skip, limit=limit, source=source, pinned_only=pinned)


@router.post("", response_model=MemoryRead, status_code=201)
async def add_memory(
    payload: MemoryCreate,
    session: AsyncSession = Depends(get_session),
):
    return await memory_service.add(
        session,
        content=payload.content,
        source=payload.source,
        session_id=payload.session_id,
        metadata=payload.metadata,
        tags=payload.tags,
    )


@router.post("/bulk", response_model=List[MemoryRead], status_code=201)
async def bulk_add_memories(
    payload: List[MemoryCreate],
    session: AsyncSession = Depends(get_session),
):
    return await memory_service.bulk_add(session, [p.model_dump() for p in payload])


@router.get("/{memory_id}", response_model=MemoryRead)
async def get_memory(
    memory_id: str,
    session: AsyncSession = Depends(get_session),
):
    memory = await memory_service.get(session, memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


@router.put("/{memory_id}", response_model=MemoryRead)
async def update_memory(
    memory_id: str,
    payload: MemoryUpdate,
    session: AsyncSession = Depends(get_session),
):
    memory = await memory_service.update(
        session, memory_id, **payload.model_dump(exclude_none=True)
    )
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


@router.delete("/{memory_id}")
async def forget_memory(
    memory_id: str,
    session: AsyncSession = Depends(get_session),
):
    ok = await memory_service.forget(session, memory_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"ok": True, "id": memory_id}


@router.post("/{memory_id}/pin", response_model=MemoryRead)
async def pin_memory(
    memory_id: str,
    session: AsyncSession = Depends(get_session),
):
    memory = await memory_service.pin(session, memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory
