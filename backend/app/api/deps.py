from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a database session from the application state pool.
    """
    session_maker = request.app.state.db_session_maker
    async with session_maker() as session:
        yield session
