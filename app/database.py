from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .settings import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator:
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
