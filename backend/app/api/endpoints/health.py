from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from redis.asyncio import Redis
from app.api.dependencies import get_db, get_redis
from app.api.schemas.common import APIResponse
from app.api.schemas.entity import HealthResponse

router = APIRouter()

@router.get("/health", response_model=APIResponse[HealthResponse])
async def check_health(
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis)
) -> Any:
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"

    redis_status = "healthy"
    try:
        await redis_client.ping()
    except Exception:
        redis_status = "unhealthy"

    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"

    return APIResponse(
        data=HealthResponse(
            status=overall_status,
            database=db_status,
            redis=redis_status,
            providers="healthy",
            latency_ms=0
        )
    )
