from typing import Any
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from sqlalchemy.orm import joinedload
from app.api.dependencies import get_db
from app.api.schemas.common import APIResponse, PaginatedResponse
from app.api.schemas.entity import InstrumentResponse
from app.models.core import Instrument, Exchange

router = APIRouter()

@router.get("/instruments", response_model=APIResponse[PaginatedResponse[InstrumentResponse]])
async def list_instruments(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    instrument_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    sector: Optional[str] = None,
    industry: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> Any:
    query = select(Instrument).options(joinedload(Instrument.exchange))

    if instrument_type:
        query = query.where(Instrument.instrument_type == instrument_type)
    if is_active is not None:
        query = query.where(Instrument.is_active == is_active)
    if sector:
        query = query.where(Instrument.sector == sector)
    if industry:
        query = query.where(Instrument.industry == industry)

    total_query = select(func.count()).select_from(query.subquery())
    total_res = await db.execute(total_query)
    total = total_res.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return APIResponse(
        data=PaginatedResponse(
            items=[InstrumentResponse.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total,
            has_previous=page > 1
        )
    )

@router.get("/instruments/search", response_model=APIResponse[PaginatedResponse[InstrumentResponse]])
async def search_instruments(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
) -> Any:
    query = select(Instrument).options(joinedload(Instrument.exchange)).where(
        or_(
            Instrument.symbol.ilike(f"%{q}%"),
            Instrument.name.ilike(f"%{q}%")
        )
    )

    total_query = select(func.count()).select_from(query.subquery())
    total_res = await db.execute(total_query)
    total = total_res.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return APIResponse(
        data=PaginatedResponse(
            items=[InstrumentResponse.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total,
            has_previous=page > 1
        )
    )

@router.get("/instruments/{instrument_id}", response_model=APIResponse[InstrumentResponse])
async def get_instrument(instrument_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(
        select(Instrument).options(joinedload(Instrument.exchange)).where(Instrument.id == instrument_id)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Instrument not found")

    return APIResponse(data=InstrumentResponse.model_validate(item))

@router.get("/instruments/exchange/{exchange_code}", response_model=APIResponse[PaginatedResponse[InstrumentResponse]])
async def get_exchange_instruments(
    exchange_code: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
) -> Any:
    ex_res = await db.execute(select(Exchange).where(Exchange.code == exchange_code))
    ex = ex_res.scalars().first()
    if not ex:
        raise HTTPException(status_code=404, detail="Exchange not found")

    query = select(Instrument).options(joinedload(Instrument.exchange)).where(Instrument.exchange_id == ex.id)

    total_query = select(func.count()).select_from(query.subquery())
    total_res = await db.execute(total_query)
    total = total_res.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return APIResponse(
        data=PaginatedResponse(
            items=[InstrumentResponse.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total,
            has_previous=page > 1
        )
    )
