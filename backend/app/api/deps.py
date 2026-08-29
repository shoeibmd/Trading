from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a database session from the application state pool.
    """
    # Assuming standard FastAPI asyncpg engine configuration on app.state
    # where engine is stored as request.app.state.db_engine
    if hasattr(request.app.state, "db_engine"):
        from sqlalchemy.ext.asyncio import async_sessionmaker
        session_maker = async_sessionmaker(
            request.app.state.db_engine, expire_on_commit=False
        )
        async with session_maker() as session:
            yield session
    else:
        # Fallback for tests if db_engine isn't explicitly set on state
        yield None

def get_provider(request: Request):
    """
    Dummy dependency for testing since the actual one is mocked in conftest.
    """
    return None
