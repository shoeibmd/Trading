import uuid
from typing import List
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.portfolio import Portfolio, PortfolioPosition, PortfolioTransaction
from app.models.core import User
from app.api.schemas.portfolio import CreateTransactionDto, PortfolioSummary

class PortfolioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_portfolios(self, user_id: str) -> List[Portfolio]:
        result = await self.db.execute(select(Portfolio).where(Portfolio.user_id == uuid.UUID(user_id)))
        return result.scalars().all()

    async def get_positions(self, portfolio_id: str, user_id: str) -> List[PortfolioPosition]:
        result = await self.db.execute(
            select(PortfolioPosition)
            .join(Portfolio)
            .options(selectinload(PortfolioPosition.instrument))
            .where(PortfolioPosition.portfolio_id == uuid.UUID(portfolio_id), Portfolio.user_id == uuid.UUID(user_id))
        )
        return result.scalars().all()

    async def add_transaction(self, portfolio_id: str, user_id: str, data: dict) -> PortfolioTransaction:
        p_uuid = uuid.UUID(portfolio_id)
        u_uuid = uuid.UUID(user_id)
        i_uuid = uuid.UUID(data["instrument_id"])

        # Verify portfolio ownership
        result = await self.db.execute(select(Portfolio).where(Portfolio.id == p_uuid, Portfolio.user_id == u_uuid))
        portfolio = result.scalar_one_or_none()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        tx_type = data["transaction_type"].upper()
        quantity = Decimal(str(data["quantity"]))
        price = Decimal(str(data["price"]))
        fees = Decimal(str(data.get("fees", 0)))

        if quantity <= 0 or price <= 0:
            raise HTTPException(status_code=400, detail="Quantity and price must be greater than 0")

        # Get or create position
        pos_result = await self.db.execute(
            select(PortfolioPosition)
            .where(PortfolioPosition.portfolio_id == p_uuid, PortfolioPosition.instrument_id == i_uuid)
        )
        position = pos_result.scalar_one_or_none()

        if not position:
            if tx_type == "SELL":
                raise HTTPException(status_code=400, detail="Cannot sell instrument not in portfolio")
            position = PortfolioPosition(
                portfolio_id=p_uuid,
                instrument_id=i_uuid,
                quantity=Decimal('0'),
                average_cost=Decimal('0'),
                realized_pnl=Decimal('0')
            )
            self.db.add(position)

        if tx_type == "SELL" and quantity > position.quantity:
             raise HTTPException(status_code=400, detail="Insufficient quantity to sell")

        # Calculate new position metrics
        if tx_type == "BUY":
            total_cost_before = position.quantity * position.average_cost
            total_cost_new = quantity * price + fees
            new_quantity = position.quantity + quantity
            position.average_cost = (total_cost_before + total_cost_new) / new_quantity
            position.quantity = new_quantity
        elif tx_type == "SELL":
            # Realized PNL: (sell_price - average_cost) * quantity - fees
            pnl = (price - position.average_cost) * quantity - fees
            position.realized_pnl += pnl
            position.quantity -= quantity

            # If closed out, handle cleanup or zeroing average cost depending on strategy
            if position.quantity == 0:
                position.average_cost = Decimal('0')

        # Add transaction
        transaction = PortfolioTransaction(
            portfolio_id=p_uuid,
            instrument_id=i_uuid,
            transaction_type=tx_type,
            quantity=quantity,
            price=price,
            fees=fees,
            transaction_date=data["transaction_date"],
            notes=data.get("notes")
        )
        self.db.add(transaction)

        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def get_summary(self, portfolio_id: str, user_id: str) -> dict:
        # In a real system, we'd fetch live quotes from Redis here.
        # For Phase 15 skeleton we just aggregate the realized amounts.
        positions = await self.get_positions(portfolio_id, user_id)

        total_cost = sum(p.quantity * p.average_cost for p in positions)
        total_realized = sum(p.realized_pnl for p in positions)

        return {
            "portfolio_id": portfolio_id,
            "total_market_value": total_cost, # Mocked to cost
            "total_cost_basis": total_cost,
            "total_unrealized_pnl": Decimal('0'), # Computed on frontend
            "total_realized_pnl": total_realized
        }
