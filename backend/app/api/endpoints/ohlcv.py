from typing import Any
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.dependencies import get_db
from app.api.schemas.common import APIResponse
from app.api.schemas.entity import OHLCVResponse
from app.models.core import OHLCV

router = APIRouter()

@router.get("/ohlcv/{instrument_id}", response_model=APIResponse[List[OHLCVResponse]])
async def get_ohlcv(
    instrument_id: UUID,
    interval: str = Query(..., description="E.g. 1m, 5m, 1h, 1d"),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db)
) -> Any:
    query = select(OHLCV).where(
        OHLCV.instrument_id == instrument_id,
        OHLCV.interval == interval
    )

    if start_time:
        query = query.where(OHLCV.time >= start_time)
    if end_time:
        query = query.where(OHLCV.time <= end_time)

    query = query.order_by(OHLCV.time.asc()).limit(limit)

    result = await db.execute(query)
    bars = result.scalars().all()

    return APIResponse(data=[OHLCVResponse.model_validate(b) for b in bars])

@router.get("/ohlcv/{instrument_id}/latest", response_model=APIResponse[List[OHLCVResponse]])
async def get_latest_ohlcv(
    instrument_id: UUID,
    interval: str = Query(...),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
) -> Any:
    query = select(OHLCV).where(
        OHLCV.instrument_id == instrument_id,
        OHLCV.interval == interval
    ).order_by(OHLCV.time.desc()).limit(limit)

    result = await db.execute(query)
    bars = result.scalars().all()

    return APIResponse(data=[OHLCVResponse.model_validate(b) for b in bars])
