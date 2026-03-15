from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from app.models.memory import MemorySource


class MemoryCreate(BaseModel):
    content: str = Field(..., min_length=1)
    source: MemorySource = MemorySource.manual
    session_id: Optional[str] = None
    tags: List[str] = []
    metadata: Optional[dict] = None


class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    is_pinned: Optional[bool] = None
    importance_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class TagRead(BaseModel):
    id: str
    name: str
    color: str

    class Config:
        from_attributes = True


class MemoryRead(BaseModel):
    id: str
    content: str
    summary: Optional[str]
    source: MemorySource
    session_id: Optional[str]
    entities: Optional[Any]
    importance_score: float
    is_pinned: bool
    is_forgotten: bool
    created_at: datetime
    accessed_at: datetime
    access_count: int
    tags: List[TagRead] = []

    class Config:
        from_attributes = True


class MemorySearchResult(BaseModel):
    memory: MemoryRead
    score: float
