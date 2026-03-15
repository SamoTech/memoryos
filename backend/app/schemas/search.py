from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.memory import MemoryRead


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=100)
    source: Optional[str] = None
    tags: Optional[List[str]] = None


class SearchResult(BaseModel):
    memory: MemoryRead
    score: float
    match_type: str  # "semantic" | "keyword" | "hybrid"
