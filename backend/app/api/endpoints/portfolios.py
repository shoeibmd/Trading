from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.dependencies import get_db, get_current_user
from app.api.schemas.common import APIResponse
from app.api.schemas.entity import PortfolioResponse, PortfolioPositionResponse, PortfolioTransactionResponse
from app.models.core import Portfolio, PortfolioPosition, PortfolioTransaction

router = APIRouter()

@router.get("/portfolios", response_model=APIResponse[List[PortfolioResponse]])
async def list_portfolios(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user)
) -> Any:
    result = await db.execute(select(Portfolio).where(Portfolio.user_id == user_id))
    items = result.scalars().all()
    return APIResponse(data=[PortfolioResponse.model_validate(i) for i in items])

@router.post("/portfolios", response_model=APIResponse[dict])
async def create_portfolio() -> Any:
    return APIResponse(data={"status": "not implemented"})

@router.get("/portfolios/{portfolio_id}", response_model=APIResponse[PortfolioResponse])
async def get_portfolio(portfolio_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Portfolio).where(Portfolio.id == portfolio_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return APIResponse(data=PortfolioResponse.model_validate(item))

@router.put("/portfolios/{portfolio_id}", response_model=APIResponse[dict])
async def update_portfolio(portfolio_id: UUID) -> Any:
    return APIResponse(data={"status": "updated"})

@router.delete("/portfolios/{portfolio_id}", response_model=APIResponse[dict])
async def delete_portfolio(portfolio_id: UUID) -> Any:
    return APIResponse(data={"status": "deleted"})

@router.get("/portfolios/{portfolio_id}/positions", response_model=APIResponse[List[PortfolioPositionResponse]])
async def get_positions(portfolio_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(PortfolioPosition).where(PortfolioPosition.portfolio_id == portfolio_id))
    items = result.scalars().all()
    return APIResponse(data=[PortfolioPositionResponse.model_validate(i) for i in items])

@router.post("/portfolios/{portfolio_id}/transactions", response_model=APIResponse[dict])
async def add_transaction(portfolio_id: UUID) -> Any:
    return APIResponse(data={"status": "transaction added"})

@router.get("/portfolios/{portfolio_id}/transactions", response_model=APIResponse[List[PortfolioTransactionResponse]])
async def get_transactions(portfolio_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(PortfolioTransaction).where(PortfolioTransaction.portfolio_id == portfolio_id).order_by(PortfolioTransaction.transaction_date.desc()))
    items = result.scalars().all()
    return APIResponse(data=[PortfolioTransactionResponse.model_validate(i) for i in items])

@router.get("/portfolios/{portfolio_id}/summary", response_model=APIResponse[dict])
async def get_summary(portfolio_id: UUID) -> Any:
    return APIResponse(data={"total_value": 0, "total_pnl": 0})
