import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.api.schemas.portfolio import (
    PortfolioCreate, PortfolioUpdate, PortfolioResponse,
    TransactionCreate, TransactionResponse, PositionResponse, PortfolioSummary
)
from app.api.schemas.common import APIResponse, create_response
from app.models.portfolio import Portfolio, PortfolioPosition, PortfolioTransaction
from app.models.core import User
from app.api.deps import get_db
from app.services.portfolio.portfolio_service import PortfolioService

router = APIRouter()

async def get_default_user(db: AsyncSession) -> User:
    result = await db.execute(select(User).limit(1))
    user = result.scalar_one_or_none()
    if not user:
        user = User(
            email="test@test.com",
            hashed_password="pw",
            username="testuser",
            full_name="Test User"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

@router.get("/", response_model=APIResponse[List[PortfolioResponse]])
async def list_portfolios(db: AsyncSession = Depends(get_db)):
    user = await get_default_user(db)
    svc = PortfolioService(db)
    portfolios = await svc.get_portfolios(str(user.id))
    for p in portfolios:
        p.id = str(p.id)
        p.user_id = str(p.user_id)
    return create_response(data=portfolios)

@router.post("/", response_model=APIResponse[PortfolioResponse])
async def create_portfolio(data: PortfolioCreate, db: AsyncSession = Depends(get_db)):
    user = await get_default_user(db)

    if data.is_default:
        result = await db.execute(select(Portfolio).where(Portfolio.user_id == user.id, Portfolio.is_default == True))
        for existing in result.scalars().all():
            existing.is_default = False

    new_portfolio = Portfolio(
        user_id=user.id,
        name=data.name,
        description=data.description,
        currency=data.currency,
        is_default=data.is_default
    )

    db.add(new_portfolio)
    await db.commit()
    await db.refresh(new_portfolio)

    new_portfolio.id = str(new_portfolio.id)
    new_portfolio.user_id = str(new_portfolio.user_id)
    return create_response(data=new_portfolio)

@router.get("/{portfolio_id}", response_model=APIResponse[PortfolioResponse])
async def get_portfolio(portfolio_id: str, db: AsyncSession = Depends(get_db)):
    try:
        p_uuid = uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Portfolio).where(Portfolio.id == p_uuid, Portfolio.user_id == user.id))
    portfolio = result.scalar_one_or_none()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    portfolio.id = str(portfolio.id)
    portfolio.user_id = str(portfolio.user_id)
    return create_response(data=portfolio)

@router.patch("/{portfolio_id}", response_model=APIResponse[PortfolioResponse])
async def update_portfolio(portfolio_id: str, updates: PortfolioUpdate, db: AsyncSession = Depends(get_db)):
    try:
        p_uuid = uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Portfolio).where(Portfolio.id == p_uuid, Portfolio.user_id == user.id))
    portfolio = result.scalar_one_or_none()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    update_data = updates.model_dump(exclude_unset=True)

    if update_data.get("is_default") is True:
        others_result = await db.execute(select(Portfolio).where(Portfolio.user_id == user.id, Portfolio.id != p_uuid, Portfolio.is_default == True))
        for existing in others_result.scalars().all():
            existing.is_default = False

    for key, value in update_data.items():
        setattr(portfolio, key, value)

    await db.commit()
    await db.refresh(portfolio)

    portfolio.id = str(portfolio.id)
    portfolio.user_id = str(portfolio.user_id)
    return create_response(data=portfolio)

@router.delete("/{portfolio_id}")
async def delete_portfolio(portfolio_id: str, db: AsyncSession = Depends(get_db)):
    try:
        p_uuid = uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Portfolio).where(Portfolio.id == p_uuid, Portfolio.user_id == user.id))
    portfolio = result.scalar_one_or_none()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    if portfolio.is_default:
        raise HTTPException(status_code=400, detail="Cannot delete the default portfolio")

    await db.delete(portfolio)
    await db.commit()
    return create_response(data={"message": "Portfolio deleted successfully"})

@router.get("/{portfolio_id}/positions", response_model=APIResponse[List[PositionResponse]])
async def get_portfolio_positions(portfolio_id: str, db: AsyncSession = Depends(get_db)):
    try:
        uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    svc = PortfolioService(db)
    positions = await svc.get_positions(portfolio_id, str(user.id))

    for p in positions:
        p.id = str(p.id)
        p.portfolio_id = str(p.portfolio_id)
        p.instrument_id = str(p.instrument_id)
        if p.instrument:
            p.instrument.id = str(p.instrument.id)

    return create_response(data=positions)

@router.get("/{portfolio_id}/transactions", response_model=APIResponse[List[TransactionResponse]])
async def get_portfolio_transactions(portfolio_id: str, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        p_uuid = uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(
        select(PortfolioTransaction)
        .join(Portfolio)
        .where(PortfolioTransaction.portfolio_id == p_uuid, Portfolio.user_id == user.id)
        .order_by(PortfolioTransaction.transaction_date.desc())
        .limit(limit)
    )
    transactions = result.scalars().all()
    for t in transactions:
        t.id = str(t.id)
        t.portfolio_id = str(t.portfolio_id)
        t.instrument_id = str(t.instrument_id)
    return create_response(data=transactions)

@router.post("/{portfolio_id}/transactions", response_model=APIResponse[TransactionResponse])
async def add_portfolio_transaction(portfolio_id: str, tx: TransactionCreate, db: AsyncSession = Depends(get_db)):
    try:
        uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    svc = PortfolioService(db)

    transaction = await svc.add_transaction(portfolio_id, str(user.id), tx.model_dump())

    transaction.id = str(transaction.id)
    transaction.portfolio_id = str(transaction.portfolio_id)
    transaction.instrument_id = str(transaction.instrument_id)
    return create_response(data=transaction)

@router.get("/{portfolio_id}/summary", response_model=APIResponse[PortfolioSummary])
async def get_portfolio_summary(portfolio_id: str, db: AsyncSession = Depends(get_db)):
    try:
        uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    svc = PortfolioService(db)
    summary = await svc.get_summary(portfolio_id, str(user.id))
    return create_response(data=summary)
