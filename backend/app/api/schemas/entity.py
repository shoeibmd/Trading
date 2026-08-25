from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

class ExchangeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    code: str
    name: str
    country: str
    timezone: str
    currency: str
    is_active: bool

class InstrumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    symbol: str
    isin: Optional[str]
    instrument_type: str
    name: str
    sector: Optional[str]
    industry: Optional[str]
    lot_size: int
    tick_size: Decimal
    is_active: bool
    exchange: ExchangeBase

class QuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    instrument_id: UUID
    time: datetime
    bid_price: Optional[Decimal]
    ask_price: Optional[Decimal]
    last_price: Decimal
    volume: Optional[int]
    bid_size: Optional[int]
    ask_size: Optional[int]
    source: str
    is_stale: bool = False

class OHLCVResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    instrument_id: UUID
    time: datetime
    interval: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    trades_count: Optional[int]

class MarketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    exchange_code: str
    is_open: bool
    current_session: Optional[str]
    next_open: Optional[datetime]
    next_close: Optional[datetime]

class WatchlistItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    instrument_id: UUID
    position: int
    notes: Optional[str]
    added_at: datetime
    current_quote: Optional[QuoteResponse] = None

class WatchlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: Optional[str]
    is_default: bool
    items: List[WatchlistItemResponse] = []

class NewsArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    summary: str
    content: str
    url: str
    source: str
    author: Optional[str]
    published_at: datetime
    related_instruments: List[UUID] = []

class FundamentalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    instrument_id: UUID
    fiscal_year: int
    fiscal_quarter: Optional[int]
    period_end_date: date
    market_cap: Optional[int]
    pe_ratio: Optional[Decimal]
    pb_ratio: Optional[Decimal]
    eps: Optional[Decimal]
    dividend_yield: Optional[Decimal]
    revenue: Optional[int]
    net_income: Optional[int]

class PortfolioTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    instrument_id: UUID
    transaction_type: str
    quantity: Decimal
    price: Decimal
    fees: Decimal
    transaction_date: datetime
    notes: Optional[str]

class PortfolioPositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    instrument_id: UUID
    quantity: Decimal
    average_cost: Decimal
    current_price: Optional[Decimal]
    unrealized_pnl: Optional[Decimal]
    realized_pnl: Decimal

class PortfolioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: Optional[str]
    currency: str
    is_default: bool

class WorkspacePanelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    panel_type: str
    panel_config: Dict[str, Any]
    position_x: int
    position_y: int
    width: int
    height: int
    z_index: int

class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: Optional[str]
    is_default: bool
    layout_config: Dict[str, Any]
    panels: List[WorkspacePanelResponse] = []

class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
    providers: str
    latency_ms: int

class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
