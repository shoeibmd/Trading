from typing import Optional
from typing import Dict, Any
from decimal import Decimal
from datetime import datetime, timezone
from uuid import UUID
from app.providers.models import NormalizedQuote, NormalizedOHLCV, NormalizedInstrument
from app.providers.enums import InstrumentType
from app.providers.utils import normalize_interval, parse_timestamp

class DataNormalizer:

    @staticmethod
    def normalize_quote(raw_data: Dict[str, Any], provider_code: str, instrument_id: UUID) -> NormalizedQuote:
        ts = raw_data.get('timestamp') or raw_data.get('time') or datetime.now(timezone.utc)
        ts_dt = parse_timestamp(ts)

        return NormalizedQuote(
            instrument_id=instrument_id,
            symbol=str(raw_data.get('symbol', '')),
            timestamp=ts_dt,
            bid_price=Decimal(str(raw_data['bid'])) if raw_data.get('bid') is not None else None,
            ask_price=Decimal(str(raw_data['ask'])) if raw_data.get('ask') is not None else None,
            last_price=Decimal(str(raw_data.get('last_price', raw_data.get('price', 0)))),
            volume=int(raw_data['volume']) if raw_data.get('volume') is not None else None,
            bid_size=int(raw_data['bid_size']) if raw_data.get('bid_size') is not None else None,
            ask_size=int(raw_data['ask_size']) if raw_data.get('ask_size') is not None else None,
            source=provider_code
        )

    @staticmethod
    def normalize_ohlcv(raw_data: Dict[str, Any], provider_code: str, instrument_id: UUID) -> NormalizedOHLCV:
        ts = raw_data.get('timestamp') or raw_data.get('time')
        if not ts:
            raise ValueError("OHLCV data must contain a timestamp")

        ts_dt = parse_timestamp(ts)
        interval = normalize_interval(str(raw_data.get('interval', '1d')))

        return NormalizedOHLCV(
            instrument_id=instrument_id,
            symbol=str(raw_data.get('symbol', '')),
            timestamp=ts_dt,
            interval=interval,
            open=Decimal(str(raw_data.get('open', 0))),
            high=Decimal(str(raw_data.get('high', 0))),
            low=Decimal(str(raw_data.get('low', 0))),
            close=Decimal(str(raw_data.get('close', 0))),
            volume=int(raw_data.get('volume', 0)),
            trades_count=int(raw_data['trades_count']) if raw_data.get('trades_count') is not None else None,
            source=provider_code
        )

    @staticmethod
    def normalize_instrument(raw_data: Dict[str, Any], provider_code: str, instrument_id: Optional[UUID] = None) -> NormalizedInstrument:
        i_type_str = str(raw_data.get('instrument_type', 'EQUITY')).upper()
        try:
            i_type = InstrumentType(i_type_str)
        except ValueError:
            i_type = InstrumentType.EQUITY

        return NormalizedInstrument(
            instrument_id=instrument_id,
            symbol=str(raw_data.get('symbol', '')),
            exchange=str(raw_data.get('exchange', '')),
            name=str(raw_data.get('name', '')),
            instrument_type=i_type,
            isin=raw_data.get('isin'),
            sector=raw_data.get('sector'),
            industry=raw_data.get('industry'),
            lot_size=int(raw_data.get('lot_size', 1)),
            tick_size=Decimal(str(raw_data.get('tick_size', 0.01))),
            currency=str(raw_data.get('currency', 'USD')),
            is_active=bool(raw_data.get('is_active', True))
        )
