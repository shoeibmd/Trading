import pytest
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from uuid import uuid4
from app.services.ingestion.validator import DataValidator
from app.providers.models import NormalizedQuote, NormalizedOHLCV

def test_quote_validation():
    validator = DataValidator(staleness_threshold_seconds=3600)

    valid_q = NormalizedQuote(
        instrument_id=uuid4(),
        symbol="AAPL",
        timestamp=datetime.now(timezone.utc),
        last_price=Decimal("150.0"),
        source="MOCK"
    )
    assert validator.validate_quote(valid_q).is_valid is True

    stale_q = NormalizedQuote(
        instrument_id=uuid4(),
        symbol="AAPL",
        timestamp=datetime.now(timezone.utc) - timedelta(hours=2),
        last_price=Decimal("150.0"),
        source="MOCK"
    )
    assert validator.validate_quote(stale_q).is_valid is False

    bad_price_q = NormalizedQuote(
        instrument_id=uuid4(),
        symbol="AAPL",
        timestamp=datetime.now(timezone.utc),
        last_price=Decimal("-10.0"),
        source="MOCK"
    )
    assert validator.validate_quote(bad_price_q).is_valid is False

def test_ohlcv_validation():
    validator = DataValidator()

    valid_o = NormalizedOHLCV(
        instrument_id=uuid4(),
        symbol="AAPL",
        timestamp=datetime.now(timezone.utc),
        interval="1d",
        open=Decimal("150"), high=Decimal("155"), low=Decimal("145"), close=Decimal("152"),
        volume=100, source="MOCK"
    )
    assert validator.validate_ohlcv(valid_o).is_valid is True

    bad_o = NormalizedOHLCV(
        instrument_id=uuid4(),
        symbol="AAPL",
        timestamp=datetime.now(timezone.utc),
        interval="1d",
        open=Decimal("150"), high=Decimal("140"), low=Decimal("145"), close=Decimal("152"),
        volume=100, source="MOCK"
    )
    assert validator.validate_ohlcv(bad_o).is_valid is False
