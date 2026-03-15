"""Semantic + hybrid search endpoints."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.memory import MemoryRead
from app.schemas.search import SearchResult
from app.services.search_service import search_service
from app.services.memory_service import memory_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=List[SearchResult])
async def hybrid_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=50),
    source: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    results = await search_service.hybrid_search(db, q, limit=limit, source=source)
    return [
        SearchResult(memory=MemoryRead.model_validate(m), score=score, match_type="hybrid")
        for m, score in results
    ]


@router.get("/context")
async def get_context(
    q: str = Query(..., min_length=1),
    max_tokens: int = Query(default=2000, ge=100, le=8000),
    db: AsyncSession = Depends(get_db),
):
    context = await memory_service.get_context(db, q, max_tokens)
    return {"query": q, "context": context}
