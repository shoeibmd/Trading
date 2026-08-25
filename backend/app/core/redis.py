import os
import redis.asyncio as redis
from redis.asyncio import Redis
import logging
from typing import Any

logger = logging.getLogger(__name__)

async def create_redis_pool() -> Redis:
    redis_url = os.getenv("APP_REDIS_URL", "redis://localhost:6379/0")
    logger.info("Initializing Redis pool...")
    pool: Any = redis.ConnectionPool.from_url(redis_url, decode_responses=True)
    return redis.Redis(connection_pool=pool)

async def close_redis_pool(redis_client: Redis) -> None:
    logger.info("Closing Redis pool...")
    await redis_client.close()
    await redis_client.connection_pool.disconnect()
