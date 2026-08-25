import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
import logging

logger = logging.getLogger(__name__)

async def create_db_engine() -> AsyncEngine:
    db_url = os.getenv("APP_POSTGRES_DSN", "postgresql+asyncpg://postgres:password@localhost:5432/financial_terminal")
    logger.info("Initializing database engine...")
    engine = create_async_engine(db_url, echo=False)
    return engine

async def close_db_engine(engine: AsyncEngine) -> None:
    logger.info("Closing database engine...")
    await engine.dispose()
