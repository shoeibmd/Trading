import pytest
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from app.providers.models import (
    NormalizedInstrument, NormalizedQuote, NormalizedOHLCV,
    RESTProviderConfig
)
from app.providers.enums import InstrumentType, ProviderType
from app.providers.exceptions import ProviderDataError
from app.providers.mock import MockProvider
from app.providers.registry import ProviderRegistry
from app.providers.utils import validate_symbol_format, normalize_interval, parse_timestamp, calculate_rate_limit_delay


# --- Models Test ---
def test_normalized_instrument():
    inst = NormalizedInstrument(
        symbol="AAPL",
        exchange="NASDAQ",
        name="Apple Inc.",
        instrument_type=InstrumentType.EQUITY,
        tick_size=Decimal("0.01"),
        currency="USD"
    )
    assert inst.symbol == "AAPL"
    assert inst.is_active is True

# --- Mock Provider Tests ---
@pytest.mark.asyncio
async def test_mock_provider():
    config = RESTProviderConfig(
        code="MOCK_REST",
        name="Mock REST Provider",
        provider_type=ProviderType.REST_API,
        base_url="http://mock.local"
    )
    provider = MockProvider(config)

    # Test Instrument Fetch
    inst = await provider.get_instrument("TEST", "MOCKEX")
    assert inst is not None
    assert inst.symbol == "TEST"
    assert inst.tick_size == Decimal("0.01")

    # Test Quote Fetch
    quote = await provider.get_quote("TEST", "MOCKEX")
    assert quote is not None
    assert quote.last_price == Decimal("150.00")

    # Test Health Check
    health = await provider.check_health()
    assert health.is_healthy is True

@pytest.mark.asyncio
async def test_mock_provider_failure():
    config = RESTProviderConfig(
        code="MOCK_REST",
        name="Mock REST Provider",
        provider_type=ProviderType.REST_API,
        base_url="http://mock.local"
    )
    provider = MockProvider(config)
    provider.force_error = True

    with pytest.raises(ProviderDataError):
        await provider.get_quote("TEST", "MOCKEX")

# --- Registry Tests ---
@pytest.mark.asyncio
async def test_provider_registry():
    config = RESTProviderConfig(
        code="MOCK_REST",
        name="Mock REST Provider",
        provider_type=ProviderType.REST_API,
        base_url="http://mock.local"
    )
    provider = MockProvider(config)
    registry = ProviderRegistry()

    registry.register_provider(config.code, provider)
    retrieved = registry.get_provider(config.code)

    assert retrieved is provider
    assert len(registry.list_providers()) == 1

    with pytest.raises(KeyError):
        registry.get_provider("NONEXISTENT")

# --- Utilities Tests ---
def test_validate_symbol():
    assert validate_symbol_format("AAPL", "NASDAQ") is True
    assert validate_symbol_format("BRK.A", "NYSE") is True
    assert validate_symbol_format("TCS*", "NSE") is False

def test_normalize_interval():
    assert normalize_interval("1") == "1m"
    assert normalize_interval("1D") == "1d"
    assert normalize_interval("1w") == "1w"

def test_parse_timestamp():
    # Unix timestamp
    dt = parse_timestamp(1609459200)
    assert dt.year == 2021
    assert dt.tzinfo == timezone.utc

    # String iso format
    dt = parse_timestamp("2021-01-01T00:00:00Z")
    assert dt.year == 2021
    assert dt.tzinfo == timezone.utc

def test_calculate_delay():
    # 60 requests per minute
    delay = calculate_rate_limit_delay(60, 60)
    assert delay == 1.0
