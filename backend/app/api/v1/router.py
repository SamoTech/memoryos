from fastapi import APIRouter
from app.api.v1.endpoints import memories, sessions, search, summarize, export, health, tags, stats

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(memories.router, prefix="/api/v1/memories", tags=["memories"])
api_router.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
api_router.include_router(search.router, prefix="/api/v1/search", tags=["search"])
api_router.include_router(tags.router, prefix="/api/v1/tags", tags=["tags"])
api_router.include_router(stats.router, prefix="/api/v1/stats", tags=["stats"])
api_router.include_router(summarize.router, prefix="/api/v1/summarize", tags=["summarize"])
api_router.include_router(export.router, prefix="/api/v1/export", tags=["export"])
