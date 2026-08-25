from typing import Any
from typing import AsyncGenerator
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    engine = request.app.state.db_engine
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()

async def get_redis(request: Request) -> Any:
    return request.app.state.redis_pool

async def get_current_user(request: Request) -> None:
    pass

async def get_provider_registry(request: Request) -> None:
    pass
