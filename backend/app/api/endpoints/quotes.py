from typing import Any
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from redis.asyncio import Redis
from app.api.dependencies import get_db, get_redis
from app.api.schemas.common import APIResponse
from app.api.schemas.entity import QuoteResponse
from app.models.core import Quote

router = APIRouter()

@router.get("/quotes/{instrument_id}", response_model=APIResponse[QuoteResponse])
async def get_latest_quote(
    instrument_id: UUID,
    redis_client: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db)
) -> Any:
    # Try Redis first for latest quote
    key = f"quotes:{instrument_id}"
    cached = await redis_client.get(key)

    if cached:
        data = json.loads(cached)
        return APIResponse(data=QuoteResponse(**data))

    # Fallback to DB
    result = await db.execute(
        select(Quote)
        .where(Quote.instrument_id == instrument_id)
        .order_by(Quote.time.desc())
        .limit(1)
    )
    quote = result.scalars().first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    response_data = QuoteResponse.model_validate(quote)
    # Determine staleness
    if (datetime.now(timezone.utc) - quote.time).total_seconds() > 3600:
        response_data.is_stale = True

    return APIResponse(data=response_data)

@router.post("/quotes/batch", response_model=APIResponse[List[QuoteResponse]])
async def get_quotes_batch(
    instrument_ids: List[UUID],
    redis_client: Redis = Depends(get_redis)
) -> Any:
    if not instrument_ids:
        return APIResponse(data=[])

    keys = [f"quotes:{iid}" for iid in instrument_ids]
    results = await redis_client.mget(keys)

    quotes = []
    for data in results:
        if data:
            quotes.append(QuoteResponse(**json.loads(data)))

    return APIResponse(data=quotes)

@router.get("/quotes/history/{instrument_id}", response_model=APIResponse[List[QuoteResponse]])
async def get_quote_history(
    instrument_id: UUID,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db)
) -> Any:
    query = select(Quote).where(Quote.instrument_id == instrument_id)

    if start_time:
        query = query.where(Quote.time >= start_time)
    if end_time:
        query = query.where(Quote.time <= end_time)

    query = query.order_by(Quote.time.desc()).limit(limit)

    result = await db.execute(query)
    quotes = result.scalars().all()

    return APIResponse(
        data=[QuoteResponse.model_validate(q) for q in quotes]
    )
