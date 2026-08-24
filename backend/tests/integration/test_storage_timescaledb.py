import pytest

@pytest.mark.integration
@pytest.mark.timescaledb
@pytest.mark.skip(reason="Requires real PostgreSQL/TimescaleDB container")
@pytest.mark.asyncio
async def test_store_ohlcv_hypertable():
    pass
