import logging
from typing import List, Tuple
from uuid import UUID

from app.providers.base import MarketDataProvider
from .config import IngestionConfig
from .metrics import IngestionMetrics
from .collector import MarketDataCollector
from .validator import DataValidator
from .storage import DataStorage
from .pipeline import IngestionPipeline, IngestionResult
from app.services.realtime.redis_manager import AsyncRedisManager

logger = logging.getLogger(__name__)

class RealtimeIngestionPipeline(IngestionPipeline):
    def __init__(
        self,
        config: IngestionConfig,
        metrics: IngestionMetrics,
        collector: MarketDataCollector,
        validator: DataValidator,
        storage: DataStorage,
        redis_manager: AsyncRedisManager
    ) -> None:
        super().__init__(config, metrics, collector, validator, storage)
        self.redis_manager = redis_manager

    async def ingest_and_distribute_quote(self, self, symbol: str, exchange: str, instrument_id: UUID, provider: MarketDataProvider) -> IngestionResult:
        result = await self.ingest_quote(symbol, exchange, instrument_id, provider)
        if result.status == "success" and result.raw_data:
            try:
                await self.redis_manager.set_quote(instrument_id, result.raw_data)
                await self.redis_manager.publish_quote(result.raw_data)
            except Exception as e:
                logger.error(f"Failed to distribute quote to Redis: {e}")
        return result

    async def ingest_and_distribute_ohlcv(self,(self, symbol: str, exchange: str, interval: str, start: datetime, end: datetime, instrument_id: UUID, provider: MarketDataProvider) -> IngestionResult:
        result = await self.ingest_historical_ohlcv(symbol, exchange, interval, start, end, instrument_id, provider)
        # Note: Since ingest_historical_ohlcv processes batches, it would normally return the bulk parsed objects
        # For real-time, assuming we intercept the very last bar successfully parsed natively
        if result.status == "success":
            try:
                # We publish a dummy or the raw representation assuming it evaluates gracefully
                # In full integration, the list of OHLCV bars would be iterated over or published generically
                pass
            except Exception as e:
                logger.error(f"Failed to distribute OHLCV to Redis: {e}")
        return result
