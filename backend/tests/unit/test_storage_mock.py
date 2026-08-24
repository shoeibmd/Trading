import pytest
from unittest.mock import AsyncMock, patch
from app.services.ingestion.storage import DataStorage
from app.providers.models import NormalizedOHLCV, NormalizedQuote
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

@pytest.mark.asyncio
async def test_store_ohlcv_batch_mock():
    mock_session = AsyncMock()
    storage = DataStorage(mock_session)

    ohlcv_data = [
        NormalizedOHLCV(
            instrument_id=uuid4(),
            symbol="AAPL",
            timestamp=datetime.now(timezone.utc),
            interval="1d",
            open=Decimal("149.00"),
            high=Decimal("151.00"),
            low=Decimal("148.50"),
            close=Decimal("150.00"),
            volume=1000,
            source="MOCK"
        )
    ]

    result = await storage.store_ohlcv_batch(ohlcv_data)
    assert result.status == "upserted"
    assert result.count == 1
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_store_quotes_batch_mock():
    mock_session = AsyncMock()
    storage = DataStorage(mock_session)

    q_data = [
        NormalizedQuote(
            instrument_id=uuid4(),
            symbol="AAPL",
            timestamp=datetime.now(timezone.utc),
            last_price=Decimal("150.00"),
            source="MOCK"
        )
    ]

    result = await storage.store_quotes_batch(q_data)
    assert result.status == "upserted"
    assert result.count == 1
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()
