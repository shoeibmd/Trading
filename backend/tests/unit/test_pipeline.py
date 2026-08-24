import pytest
from unittest.mock import AsyncMock, patch
from app.services.ingestion.pipeline import IngestionPipeline
from app.services.ingestion.config import IngestionConfig
from app.services.ingestion.metrics import IngestionMetrics
from app.services.ingestion.validator import DataValidator
from app.services.ingestion.storage import DataStorage
from app.services.ingestion.collector import MarketDataCollector
from app.providers.mock import MockProvider
from app.providers.models import RESTProviderConfig
from app.providers.enums import ProviderType
from uuid import uuid4

@pytest.mark.asyncio
async def test_pipeline_ingest_quote():
    config = IngestionConfig()
    metrics = IngestionMetrics()
    collector = MarketDataCollector()
    validator = DataValidator()

    mock_session = AsyncMock()
    storage = DataStorage(mock_session)

    pipeline = IngestionPipeline(config, metrics, collector, validator, storage)

    provider_config = RESTProviderConfig(
        code="MOCK_TEST",
        name="Mock Provider",
        provider_type=ProviderType.REST_API,
        base_url="http://mock.local"
    )
    provider = MockProvider(provider_config)

    inst_id = uuid4()
    result = await pipeline.ingest_quote("AAPL", "NASDAQ", inst_id, provider)

    assert result.status == "success"
    assert result.stored_count == 1
    assert mock_session.execute.call_count == 2
    mock_session.commit.assert_called_once()
    assert metrics.success_count == 1
