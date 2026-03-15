from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.DB_URL,
    future=True,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in (settings.DB_URL or "") else {},
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    from app.models import memory, session, tag, source  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Create FTS5 virtual table for keyword search
        await conn.execute(
            __import__("sqlalchemy").text(
                "CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts "
                "USING fts5(content, summary, id UNINDEXED)"
            )
        )
