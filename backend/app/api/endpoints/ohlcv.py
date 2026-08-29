from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from app.api.schemas.common import APIResponse, create_response
from app.providers.base import FinancialDataProvider
from app.api.deps import get_provider
from datetime import datetime

router = APIRouter()

@router.get("/{instrument_id}", response_model=APIResponse[List[Dict[str, Any]]])
async def get_ohlcv(
    instrument_id: str,
    interval: str = Query("1d", description="Time interval (e.g., 1m, 5m, 1d)"),
    limit: int = Query(100, description="Number of candles"),
    provider: FinancialDataProvider = Depends(get_provider)
):
    """
    Get OHLCV (Open, High, Low, Close, Volume) data for an instrument.
    For Phase 12, this leverages the configured financial data provider.
    """
    if not provider:
        # Fallback simulated OHLCV data for testing the UI
        # Generate some dummy candles ending at current time
        import time, random
        now = int(time.time())
        candles = []
        base_price = 150.0

        # 86400 seconds in a day
        interval_seconds = 86400 if interval == '1d' else 3600

        for i in range(limit, 0, -1):
            timestamp = (now - (i * interval_seconds)) * 1000

            open_p = base_price + random.uniform(-2, 2)
            high_p = open_p + random.uniform(0, 5)
            low_p = open_p - random.uniform(0, 5)
            close_p = random.uniform(low_p, high_p)

            candles.append({
                "timestamp": datetime.fromtimestamp(timestamp/1000).isoformat(),
                "open": open_p,
                "high": high_p,
                "low": low_p,
                "close": close_p,
                "volume": int(random.uniform(1000, 50000))
            })
            base_price = close_p

        return create_response(data=candles)

    try:
        # If the provider has historical support
        if hasattr(provider, 'get_historical_ohlcv'):
            data = await provider.get_historical_ohlcv(instrument_id, interval, limit=limit)
            return create_response(data=data)

        return create_response(data=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
