import uuid
from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from .entity import InstrumentResponse

class TransactionCreate(BaseModel):
    instrument_id: str
    transaction_type: str = Field(..., description="BUY, SELL, DIVIDEND")
    quantity: Decimal
    price: Decimal
    fees: Decimal = Decimal('0')
    transaction_date: datetime
    notes: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    portfolio_id: str
    instrument_id: str
    transaction_type: str
    quantity: Decimal
    price: Decimal
    fees: Decimal
    transaction_date: datetime
    notes: Optional[str] = None
    created_at: datetime

    @field_serializer('quantity', 'price', 'fees', when_used='json')
    def serialize_decimal(self, value: Decimal) -> str:
        return str(value)

    class Config:
        from_attributes = True

class PositionResponse(BaseModel):
    id: str
    portfolio_id: str
    instrument_id: str
    quantity: Decimal
    average_cost: Decimal
    realized_pnl: Decimal
    instrument: Optional[InstrumentResponse] = None

    @field_serializer('quantity', 'average_cost', 'realized_pnl', when_used='json')
    def serialize_decimal(self, value: Decimal) -> str:
        return str(value)

    class Config:
        from_attributes = True

class PortfolioCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    currency: str = "USD"
    is_default: bool = False

class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None
    is_default: Optional[bool] = None

class PortfolioResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    currency: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PortfolioSummary(BaseModel):
    portfolio_id: str
    total_market_value: Decimal
    total_cost_basis: Decimal
    total_unrealized_pnl: Decimal
    total_realized_pnl: Decimal

    @field_serializer('total_market_value', 'total_cost_basis', 'total_unrealized_pnl', 'total_realized_pnl', when_used='json')
    def serialize_decimal(self, value: Decimal) -> str:
        return str(value)
