import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.workers.background import background_worker
from app.api.v1.router import api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("MemoryOS starting up...")
    await init_db()
    task = asyncio.create_task(background_worker())
    yield
    task.cancel()
    logger.info("MemoryOS shut down.")


app = FastAPI(
    title="MemoryOS",
    description="Local-first AI memory layer",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "chrome-extension://*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    from app.core.config import settings
    return {
        "status": "ok",
        "version": "1.0.0",
        "data_dir": str(settings.DATA_DIR),
    }
