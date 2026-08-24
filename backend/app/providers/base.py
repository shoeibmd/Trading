from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Callable, Dict, Any
from datetime import datetime
from .models import (
    NormalizedInstrument, NormalizedQuote, NormalizedOHLCV,
    NormalizedMarketStatus, ProviderHealth, ProviderConfig
)

class MarketDataProvider(ABC):
    """Abstract base class for all market data providers."""

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    @abstractmethod
    async def search_instruments(self, query: str, limit: int = 10) -> List[NormalizedInstrument]:
        pass

    @abstractmethod
    async def get_instrument(self, symbol: str, exchange: str) -> Optional[NormalizedInstrument]:
        pass

    @abstractmethod
    async def list_instruments(self, exchange: Optional[str] = None) -> List[NormalizedInstrument]:
        pass

    @abstractmethod
    async def get_quote(self, symbol: str, exchange: str) -> Optional[NormalizedQuote]:
        pass

    @abstractmethod
    async def get_quotes(self, symbols: List[Tuple[str, str]]) -> List[NormalizedQuote]:
        pass

    @abstractmethod
    async def subscribe_quotes(self, symbols: List[Tuple[str, str]], callback: Callable[[NormalizedQuote], None]) -> None:
        pass

    @abstractmethod
    async def unsubscribe_quotes(self, symbols: List[Tuple[str, str]]) -> None:
        pass

    @abstractmethod
    async def get_ohlcv(self, symbol: str, exchange: str, interval: str, start: datetime, end: datetime) -> List[NormalizedOHLCV]:
        pass

    @abstractmethod
    async def get_latest_ohlcv(self, symbol: str, exchange: str, interval: str, limit: int = 100) -> List[NormalizedOHLCV]:
        pass

    @abstractmethod
    async def get_market_status(self, exchange: str) -> NormalizedMarketStatus:
        pass

    @abstractmethod
    async def list_exchanges(self) -> List[str]:
        pass

    @abstractmethod
    async def check_health(self) -> ProviderHealth:
        pass

    @abstractmethod
    def get_provider_info(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_supported_exchanges(self) -> List[str]:
        pass

    @abstractmethod
    def get_supported_intervals(self) -> List[str]:
        pass
