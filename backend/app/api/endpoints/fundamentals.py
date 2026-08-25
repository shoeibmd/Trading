from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.dependencies import get_db
from app.api.schemas.common import APIResponse
from app.api.schemas.entity import FundamentalResponse
from app.models.core import Fundamental

router = APIRouter()

@router.get("/fundamentals/{instrument_id}", response_model=APIResponse[List[FundamentalResponse]])
async def get_fundamentals(instrument_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(
        select(Fundamental).where(Fundamental.instrument_id == instrument_id).order_by(Fundamental.period_end_date.desc())
    )
    items = result.scalars().all()
    return APIResponse(data=[FundamentalResponse.model_validate(i) for i in items])

@router.get("/fundamentals/{instrument_id}/statements", response_model=APIResponse[dict])
async def get_statements(instrument_id: UUID) -> Any:
    return APIResponse(data={"message": "Statements skeleton"})

@router.get("/fundamentals/{instrument_id}/ratios", response_model=APIResponse[dict])
async def get_ratios(instrument_id: UUID) -> Any:
    return APIResponse(data={"message": "Ratios skeleton"})
