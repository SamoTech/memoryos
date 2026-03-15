from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.memory import MemorySearchResult, MemoryRead
from app.services.search_service import search_service
from app.services.memory_service import memory_service

router = APIRouter()


class SimilarRequest(BaseModel):
    text: str
    limit: int = 10
    source: Optional[str] = None


@router.get("", response_model=List[MemorySearchResult])
async def hybrid_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, le=50),
    source: Optional[str] = None,
    tags: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    tag_list = tags.split(",") if tags else None
    results = await search_service.hybrid_search(
        session, q, limit=limit, source=source, tags=tag_list
    )
    return [{"memory": m, "score": s} for m, s in results]


@router.post("/similar", response_model=List[MemorySearchResult])
async def find_similar(
    payload: SimilarRequest,
    session: AsyncSession = Depends(get_session),
):
    results = await search_service.semantic_search(
        session, payload.text, limit=payload.limit, source=payload.source
    )
    return [{"memory": m, "score": s} for m, s in results]


@router.get("/context")
async def get_context(
    q: str = Query(...),
    max_tokens: int = 2000,
    session: AsyncSession = Depends(get_session),
):
    context = await memory_service.get_context(session, q, max_tokens=max_tokens)
    return {"context": context, "query": q}
