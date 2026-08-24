from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from .enums import InstrumentType, ProviderType

class NormalizedInstrument(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    instrument_id: Optional[UUID] = None
    symbol: str
    exchange: str
    name: str
    instrument_type: InstrumentType
    isin: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    lot_size: int = 1
    tick_size: Decimal
    currency: str
    is_active: bool = True


class NormalizedQuote(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    instrument_id: UUID
    symbol: str
    timestamp: datetime
    bid_price: Optional[Decimal] = None
    ask_price: Optional[Decimal] = None
    last_price: Decimal
    volume: Optional[int] = None
    bid_size: Optional[int] = None
    ask_size: Optional[int] = None
    source: str


class NormalizedOHLCV(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    instrument_id: UUID
    symbol: str
    timestamp: datetime
    interval: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    trades_count: Optional[int] = None
    source: str


class NormalizedMarketStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    exchange: str
    is_open: bool
    current_session: Optional[str] = None
    next_open: Optional[datetime] = None
    next_close: Optional[datetime] = None


class ProviderHealth(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider_code: str
    is_healthy: bool
    last_check: datetime
    latency_ms: Optional[int] = None
    error_message: Optional[str] = None
    rate_limit_remaining: Optional[int] = None


class ProviderConfig(BaseModel):
    code: str
    name: str
    provider_type: ProviderType
    is_active: bool = True
    rate_limit_per_minute: Optional[int] = None


class RESTProviderConfig(ProviderConfig):
    base_url: str
    api_key: Optional[str] = None
    headers: Dict[str, str] = {}
    timeout_seconds: int = 30


class WebSocketProviderConfig(ProviderConfig):
    ws_url: str
    api_key: Optional[str] = None
    reconnect_attempts: int = 5
    heartbeat_interval_seconds: int = 30
