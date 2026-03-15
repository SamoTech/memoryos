"""MemoryOS FastAPI application entrypoint."""
from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_tables
from app.core.config import settings
from app.api.v1.endpoints import memories, sessions, search, summarize, export, health
from app.workers.background import background_worker_loop

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("memoryos")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🧠 MemoryOS starting on http://%s:%s", settings.host, settings.port)
    await create_tables()
    # Start background worker
    worker_task = asyncio.create_task(background_worker_loop())
    yield
    worker_task.cancel()
    logger.info("MemoryOS stopped.")


app = FastAPI(
    title="MemoryOS API",
    description="Local-first AI memory layer. Your AI finally remembers you.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS: allow browser extension + local dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"(https?://localhost.*|chrome-extension://.*|moz-extension://.*)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(health.router)
app.include_router(memories.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(summarize.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": "MemoryOS",
        "tagline": "Your AI finally remembers you.",
        "docs": "/docs",
        "version": "1.0.0",
    }
