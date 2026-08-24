import asyncio
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional, Tuple, Callable, Dict, Any
from uuid import uuid4

from .base import MarketDataProvider
from .enums import InstrumentType, ProviderType
from .models import (
    NormalizedInstrument, NormalizedQuote, NormalizedOHLCV,
    NormalizedMarketStatus, ProviderHealth, RESTProviderConfig
)

class MockProvider(MarketDataProvider):
    """A mock market data provider used for testing and development."""

    def __init__(self, config: RESTProviderConfig) -> None:
        super().__init__(config)
        self.mock_delay = 0.01  # Simulate slight network delay
        self.force_error = False # Configurable flag for testing failure conditions

    async def _simulate_delay(self) -> None:
        if self.mock_delay > 0:
            await asyncio.sleep(self.mock_delay)
        if self.force_error:
            from .exceptions import ProviderDataError
            raise ProviderDataError("Simulated error in MockProvider.")

    async def search_instruments(self, query: str, limit: int = 10) -> List[NormalizedInstrument]:
        await self._simulate_delay()
        return [self._generate_mock_instrument(query)]

    async def get_instrument(self, symbol: str, exchange: str) -> Optional[NormalizedInstrument]:
        await self._simulate_delay()
        return self._generate_mock_instrument(symbol, exchange)

    async def list_instruments(self, exchange: Optional[str] = None) -> List[NormalizedInstrument]:
        await self._simulate_delay()
        return [self._generate_mock_instrument(f"MOCK{i}", exchange or "MOCKEX") for i in range(5)]

    async def get_quote(self, symbol: str, exchange: str) -> Optional[NormalizedQuote]:
        await self._simulate_delay()
        return self._generate_mock_quote(symbol)

    async def get_quotes(self, symbols: List[Tuple[str, str]]) -> List[NormalizedQuote]:
        await self._simulate_delay()
        return [self._generate_mock_quote(sym) for sym, _ in symbols]

    async def subscribe_quotes(self, symbols: List[Tuple[str, str]], callback: Callable[[NormalizedQuote], None]) -> None:
        # Mock immediate single callback execution
        for sym, _ in symbols:
            callback(self._generate_mock_quote(sym))

    async def unsubscribe_quotes(self, symbols: List[Tuple[str, str]]) -> None:
        pass

    async def get_ohlcv(self, symbol: str, exchange: str, interval: str, start: datetime, end: datetime) -> List[NormalizedOHLCV]:
        await self._simulate_delay()
        return [self._generate_mock_ohlcv(symbol, interval)]

    async def get_latest_ohlcv(self, symbol: str, exchange: str, interval: str, limit: int = 100) -> List[NormalizedOHLCV]:
        await self._simulate_delay()
        return [self._generate_mock_ohlcv(symbol, interval) for _ in range(limit)]

    async def get_market_status(self, exchange: str) -> NormalizedMarketStatus:
        await self._simulate_delay()
        return NormalizedMarketStatus(
            exchange=exchange,
            is_open=True,
            current_session="REGULAR"
        )

    async def list_exchanges(self) -> List[str]:
        return ["MOCKEX", "NYSE", "NSE"]

    async def check_health(self) -> ProviderHealth:
        return ProviderHealth(
            provider_code=self.config.code,
            is_healthy=not self.force_error,
            last_check=datetime.now(timezone.utc),
            latency_ms=int(self.mock_delay * 1000)
        )

    def get_provider_info(self) -> Dict[str, Any]:
        return {"name": "MockProvider", "version": "1.0", "description": "Synthetic data provider."}

    def get_supported_exchanges(self) -> List[str]:
        return ["MOCKEX", "NYSE", "NSE"]

    def get_supported_intervals(self) -> List[str]:
        return ["1m", "5m", "1d"]

    # --- Generators ---
    def _generate_mock_instrument(self, symbol: str, exchange: str = "MOCKEX") -> NormalizedInstrument:
        return NormalizedInstrument(
            instrument_id=uuid4(),
            symbol=symbol.upper(),
            exchange=exchange,
            name=f"Mock Co. {symbol}",
            instrument_type=InstrumentType.EQUITY,
            tick_size=Decimal("0.01"),
            currency="USD",
            is_active=True
        )

    def _generate_mock_quote(self, symbol: str) -> NormalizedQuote:
        return NormalizedQuote(
            instrument_id=uuid4(),
            symbol=symbol,
            timestamp=datetime.now(timezone.utc),
            last_price=Decimal("150.00"),
            source=self.config.code
        )

    def _generate_mock_ohlcv(self, symbol: str, interval: str) -> NormalizedOHLCV:
        return NormalizedOHLCV(
            instrument_id=uuid4(),
            symbol=symbol,
            timestamp=datetime.now(timezone.utc),
            interval=interval,
            open=Decimal("149.00"),
            high=Decimal("151.00"),
            low=Decimal("148.50"),
            close=Decimal("150.00"),
            volume=1000,
            source=self.config.code
        )
