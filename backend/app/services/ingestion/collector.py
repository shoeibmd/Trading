import asyncio
import logging
import random
from typing import List, Tuple, Optional, Any, Dict
from datetime import datetime
from app.providers.base import MarketDataProvider
from app.providers.models import NormalizedQuote, NormalizedOHLCV, NormalizedInstrument
from app.providers.exceptions import (
    ProviderRateLimitError, ProviderTimeoutError, ProviderDataError, ProviderNotAvailableError
)
from app.providers.utils import calculate_rate_limit_delay

logger = logging.getLogger(__name__)

class MarketDataCollector:
    def __init__(self, retry_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 60.0) -> None:
        self.retry_attempts = retry_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._provider_locks: Dict[str, asyncio.Lock] = {}
        self._last_request_time: Dict[str, float] = {}

    def _get_provider_lock(self, provider_code: str) -> asyncio.Lock:
        if provider_code not in self._provider_locks:
            self._provider_locks[provider_code] = asyncio.Lock()
        return self._provider_locks[provider_code]

    async def _enforce_rate_limit(self, provider: MarketDataProvider) -> None:
        code = provider.config.code
        limit = provider.config.rate_limit_per_minute
        if not limit:
            return

        delay_needed = calculate_rate_limit_delay(limit, 60)
        lock = self._get_provider_lock(code)

        async with lock:
            now = asyncio.get_event_loop().time()
            last = self._last_request_time.get(code, 0.0)
            elapsed = now - last

            if elapsed < delay_needed:
                # Add jitter up to 10%
                jitter = delay_needed * 0.1 * random.random()
                sleep_time = (delay_needed - elapsed) + jitter
                await asyncio.sleep(sleep_time)

            self._last_request_time[code] = asyncio.get_event_loop().time()

    async def _execute_with_retry(self, operation: str, provider: MarketDataProvider, coro: Any, *args: Any, **kwargs: Any) -> Any:
        """Execute a coroutine with proactive rate limiting, exponential backoff, and explicit error handling."""
        attempt = 0
        while attempt < self.retry_attempts:
            try:
                await self._enforce_rate_limit(provider)
                return await coro(*args, **kwargs)
            except ProviderRateLimitError as e:
                attempt += 1
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                logger.warning(f"[{operation}] Rate limit exceeded. Retrying in {delay}s. Error: {e}")
                await asyncio.sleep(delay)
            except ProviderTimeoutError as e:
                attempt += 1
                delay = self.base_delay * attempt
                logger.warning(f"[{operation}] Timeout. Retrying in {delay}s. Error: {e}")
                await asyncio.sleep(delay)
            except ProviderDataError as e:
                logger.error(f"[{operation}] Provider Data Error. Skipping. Error: {e}")
                raise e
            except ProviderNotAvailableError as e:
                logger.error(f"[{operation}] Provider Not Available (Circuit Breaker Tripped). Error: {e}")
                raise e
            except Exception as e:
                logger.error(f"[{operation}] Unexpected error: {e}")
                raise e

        logger.error(f"[{operation}] Failed after {self.retry_attempts} attempts.")
        return None

    async def collect_quote(self, symbol: str, exchange: str, provider: MarketDataProvider) -> Optional[NormalizedQuote]:
        res = await self._execute_with_retry(
            f"collect_quote:{symbol}:{exchange}",
            provider,
            provider.get_quote,
            symbol,
            exchange
        )
        return res if isinstance(res, NormalizedQuote) else None

    async def collect_quotes_batch(self, symbols: List[Tuple[str, str]], provider: MarketDataProvider) -> List[NormalizedQuote]:
        res = await self._execute_with_retry(
            "collect_quotes_batch",
            provider,
            provider.get_quotes,
            symbols
        )
        return res if res else []

    async def collect_ohlcv(self, symbol: str, exchange: str, interval: str, start: datetime, end: datetime, provider: MarketDataProvider) -> List[NormalizedOHLCV]:
        res = await self._execute_with_retry(
            f"collect_ohlcv:{symbol}:{exchange}",
            provider,
            provider.get_ohlcv,
            symbol,
            exchange,
            interval,
            start,
            end
        )
        return res if res else []

    async def collect_instrument(self, symbol: str, exchange: str, provider: MarketDataProvider) -> Optional[NormalizedInstrument]:
        res = await self._execute_with_retry(
            f"collect_instrument:{symbol}:{exchange}",
            provider,
            provider.get_instrument,
            symbol,
            exchange
        )
        return res if isinstance(res, NormalizedInstrument) else None

    async def collect_instruments_batch(self, provider: MarketDataProvider) -> List[NormalizedInstrument]:
        res = await self._execute_with_retry(
            "collect_instruments_batch",
            provider,
            provider.list_instruments
        )
        return res if res else []
