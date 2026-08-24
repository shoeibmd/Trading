import logging
from typing import List
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.models.core import Quote, OHLCV, Instrument, ProviderSymbol
from app.providers.models import NormalizedQuote, NormalizedOHLCV, NormalizedInstrument
from .exceptions import StorageError

logger = logging.getLogger(__name__)

class StorageResult(BaseModel):
    status: str
    count: int

class DataStorage:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def store_quote(self, quote: NormalizedQuote) -> StorageResult:
        try:
            stmt = pg_insert(Quote).values(
                time=quote.timestamp,
                instrument_id=quote.instrument_id,
                bid_price=quote.bid_price,
                ask_price=quote.ask_price,
                last_price=quote.last_price,
                volume=quote.volume,
                bid_size=quote.bid_size,
                ask_size=quote.ask_size,
                source=quote.source
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=['time', 'instrument_id'],
                set_={
                    'bid_price': stmt.excluded.bid_price,
                    'ask_price': stmt.excluded.ask_price,
                    'last_price': stmt.excluded.last_price,
                    'volume': stmt.excluded.volume,
                    'bid_size': stmt.excluded.bid_size,
                    'ask_size': stmt.excluded.ask_size,
                    'source': stmt.excluded.source
                }
            )
            await self.session.execute(stmt)

            # Update last_price on the instrument
            update_stmt = update(Instrument).where(Instrument.id == quote.instrument_id).values(
                tick_size=quote.last_price  # Implicit simplified mapping assuming latest tick matches tick_size representation or last evaluation
            )
            await self.session.execute(update_stmt)

            await self.session.commit()
            return StorageResult(status="upserted", count=1)
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Failed to store quote: {e}")
            raise StorageError(f"Database error: {e}")

    async def store_quotes_batch(self, quotes: List[NormalizedQuote]) -> StorageResult:
        if not quotes:
            return StorageResult(status="skipped", count=0)

        try:
            values = [{
                'time': q.timestamp,
                'instrument_id': q.instrument_id,
                'bid_price': q.bid_price,
                'ask_price': q.ask_price,
                'last_price': q.last_price,
                'volume': q.volume,
                'bid_size': q.bid_size,
                'ask_size': q.ask_size,
                'source': q.source
            } for q in quotes]

            stmt = pg_insert(Quote).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=['time', 'instrument_id'],
                set_={
                    'bid_price': stmt.excluded.bid_price,
                    'ask_price': stmt.excluded.ask_price,
                    'last_price': stmt.excluded.last_price,
                    'volume': stmt.excluded.volume,
                    'bid_size': stmt.excluded.bid_size,
                    'ask_size': stmt.excluded.ask_size,
                    'source': stmt.excluded.source
                }
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return StorageResult(status="upserted", count=len(quotes))
        except Exception as e:
            await self.session.rollback()
            raise StorageError(f"Batch storage failed: {e}")

    async def store_ohlcv_batch(self, ohlcv_data: List[NormalizedOHLCV]) -> StorageResult:
        if not ohlcv_data:
            return StorageResult(status="skipped", count=0)

        try:
            values = [{
                'time': o.timestamp,
                'instrument_id': o.instrument_id,
                'interval': o.interval,
                'open': o.open,
                'high': o.high,
                'low': o.low,
                'close': o.close,
                'volume': o.volume,
                'trades_count': o.trades_count,
                'source': o.source
            } for o in ohlcv_data]

            stmt = pg_insert(OHLCV).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=['time', 'instrument_id', 'interval'],
                set_={
                    'open': stmt.excluded.open,
                    'high': stmt.excluded.high,
                    'low': stmt.excluded.low,
                    'close': stmt.excluded.close,
                    'volume': stmt.excluded.volume,
                    'trades_count': stmt.excluded.trades_count,
                    'source': stmt.excluded.source
                }
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return StorageResult(status="upserted", count=len(ohlcv_data))
        except Exception as e:
            await self.session.rollback()
            raise StorageError(f"Batch OHLCV storage failed: {e}")

    async def store_instrument(self, instrument: NormalizedInstrument, provider_id: UUID) -> UUID:
        try:
            from uuid import uuid4
            target_id = instrument.instrument_id or uuid4()

            if instrument.instrument_id:
                stmt = update(Instrument).where(Instrument.id == instrument.instrument_id).values(
                    symbol=instrument.symbol,
                    name=instrument.name,
                    instrument_type=instrument.instrument_type,
                    isin=instrument.isin,
                    sector=instrument.sector,
                    industry=instrument.industry,
                    lot_size=instrument.lot_size,
                    tick_size=instrument.tick_size,
                    is_active=instrument.is_active
                )
                await self.session.execute(stmt)
            else:
                stmt_insert = insert(Instrument).values(
                    id=target_id,
                    symbol=instrument.symbol,
                    name=instrument.name,
                    instrument_type=instrument.instrument_type,
                    exchange_id=uuid4(), # Note: requires real matching upstream for production
                    tick_size=instrument.tick_size
                )
                await self.session.execute(stmt_insert)

            # Create provider_symbols mapping
            ps_stmt = pg_insert(ProviderSymbol).values(
                id=uuid4(),
                provider_id=provider_id,
                instrument_id=target_id,
                provider_symbol=instrument.symbol,
                is_primary=True
            )
            ps_stmt = ps_stmt.on_conflict_do_nothing(
                index_elements=['provider_id', 'instrument_id']
            )
            await self.session.execute(ps_stmt)

            await self.session.commit()
            return target_id
        except Exception as e:
            await self.session.rollback()
            raise StorageError(f"Instrument storage failed: {e}")
