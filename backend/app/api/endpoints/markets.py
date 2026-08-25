from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.dependencies import get_db
from app.api.schemas.common import APIResponse
from app.api.schemas.entity import ExchangeBase, MarketResponse
from app.models.core import Exchange

router = APIRouter()

@router.get("/markets", response_model=APIResponse[List[ExchangeBase]])
async def list_markets(db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Exchange).where(Exchange.is_active == True))
    exchanges = result.scalars().all()
    return APIResponse(data=[ExchangeBase.model_validate(ex) for ex in exchanges])

@router.get("/markets/{exchange_code}", response_model=APIResponse[ExchangeBase])
async def get_market(exchange_code: str, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Exchange).where(Exchange.code == exchange_code.upper()))
    exchange = result.scalars().first()
    if not exchange:
        raise HTTPException(status_code=404, detail="Market not found")
    return APIResponse(data=ExchangeBase.model_validate(exchange))

@router.get("/markets/{exchange_code}/status", response_model=APIResponse[MarketResponse])
async def get_market_status(exchange_code: str, db: AsyncSession = Depends(get_db)) -> Any:
    return APIResponse(
        data=MarketResponse(
            exchange_code=exchange_code.upper(),
            is_open=True,
            current_session="REGULAR",
            next_open=None,
            next_close=None
        )
    )

@router.get("/markets/overview", response_model=APIResponse[dict])
async def get_market_overview() -> Any:
    return APIResponse(data={"message": "Market overview skeleton."})
