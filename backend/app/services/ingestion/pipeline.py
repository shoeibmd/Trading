import asyncio
import logging
from typing import List, Tuple, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from .config import IngestionConfig
from .metrics import IngestionMetrics
from .collector import MarketDataCollector
from .validator import DataValidator
from .normalizer import DataNormalizer
from .storage import DataStorage
from .exceptions import PipelineError

from app.providers.base import MarketDataProvider
from app.providers.models import NormalizedQuote

logger = logging.getLogger(__name__)

class IngestionResult(BaseModel):
    status: str
    errors: List[str] = []
    warnings: List[str] = []
    stored_count: int = 0

class IngestionPipeline:
    def __init__(
        self,
        config: IngestionConfig,
        metrics: IngestionMetrics,
        collector: MarketDataCollector,
        validator: DataValidator,
        storage: DataStorage
    ) -> None:
        self.config = config
        self.metrics = metrics
        self.collector = collector
        self.validator = validator
        self.storage = storage
        self.normalizer = DataNormalizer()

    async def ingest_quote(self, symbol: str, exchange: str, instrument_id: UUID, provider: MarketDataProvider) -> IngestionResult:
        self.metrics.record_request()
        try:
            raw_quote = await self.collector.collect_quote(symbol, exchange, provider)
            if not raw_quote:
                self.metrics.record_failure()
                return IngestionResult(status="error", errors=["Collection failed"])

            if self.config.enable_validation:
                val_res = self.validator.validate_quote(raw_quote)
                if not val_res.is_valid:
                    self.metrics.record_validation_failure()
                    return IngestionResult(status="validation_failed", errors=val_res.errors, warnings=val_res.warnings)

            raw_quote.instrument_id = instrument_id
            storage_res = await self.storage.store_quote(raw_quote)
            self.metrics.record_success()
            self.metrics.record_stored_items(storage_res.count)
            return IngestionResult(status="success", stored_count=storage_res.count)

        except Exception as e:
            self.metrics.record_failure()
            logger.error(f"Pipeline error ingesting quote for {symbol}: {e}")
            return IngestionResult(status="error", errors=[str(e)])

    async def _process_batch_chunk(self, chunk: List[Tuple[str, str]], id_map: dict, provider: MarketDataProvider) -> List[NormalizedQuote]:
        raw_quotes = await self.collector.collect_quotes_batch(chunk, provider)
        valid_quotes = []
        for q in raw_quotes:
            if self.config.enable_validation:
                val_res = self.validator.validate_quote(q)
                if not val_res.is_valid:
                    self.metrics.record_validation_failure()
                    continue
            q.instrument_id = id_map.get(q.symbol, q.instrument_id)
            valid_quotes.append(q)
        return valid_quotes

    async def ingest_quotes_batch(self, symbol_mappings: List[dict], provider: MarketDataProvider) -> List[IngestionResult]:
        self.metrics.record_request()
        symbols_to_collect = [(m['symbol'], m['exchange']) for m in symbol_mappings]
        id_map = {m['symbol']: m['instrument_id'] for m in symbol_mappings}

        # Concurrency limit processing
        chunk_size = max(1, len(symbols_to_collect) // self.config.concurrency_limit)
        chunks = [symbols_to_collect[i:i + chunk_size] for i in range(0, len(symbols_to_collect), chunk_size)]

        tasks = [self._process_batch_chunk(chunk, id_map, provider) for chunk in chunks]
        chunk_results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_quotes = []
        results = []
        for res in chunk_results:
            if isinstance(res, list):
                valid_quotes.extend(res)
            else:
                results.append(IngestionResult(status="error", errors=[str(res)]))

        if valid_quotes:
            try:
                storage_res = await self.storage.store_quotes_batch(valid_quotes)
                self.metrics.record_success()
                self.metrics.record_stored_items(storage_res.count)
                results.append(IngestionResult(status="success", stored_count=storage_res.count))
            except Exception as e:
                self.metrics.record_failure()
                results.append(IngestionResult(status="storage_failed", errors=[str(e)]))

        return results

    async def ingest_historical_ohlcv(self, symbol: str, exchange: str, interval: str, start: datetime, end: datetime, instrument_id: UUID, provider: MarketDataProvider) -> IngestionResult:
        self.metrics.record_request()
        try:
            raw_ohlcv = await self.collector.collect_ohlcv(symbol, exchange, interval, start, end, provider)
            if not raw_ohlcv:
                self.metrics.record_failure()
                return IngestionResult(status="error", errors=["Historical collection empty"])

            valid_data = []
            for o in raw_ohlcv:
                if self.config.enable_validation:
                    val_res = self.validator.validate_ohlcv(o)
                    if not val_res.is_valid:
                        self.metrics.record_validation_failure()
                        continue
                o.instrument_id = instrument_id
                valid_data.append(o)

            if valid_data:
                storage_res = await self.storage.store_ohlcv_batch(valid_data)
                self.metrics.record_success()
                self.metrics.record_stored_items(storage_res.count)
                return IngestionResult(status="success", stored_count=storage_res.count)
            else:
                return IngestionResult(status="validation_failed", errors=["All data points failed validation"])

        except Exception as e:
            self.metrics.record_failure()
            logger.error(f"Pipeline error ingesting historical OHLCV: {e}")
            return IngestionResult(status="error", errors=[str(e)])
