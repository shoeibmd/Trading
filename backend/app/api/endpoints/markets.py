from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.api.schemas.common import APIResponse, create_response
from app.providers.base import FinancialDataProvider
from app.api.deps import get_provider

router = APIRouter()

@router.get("/overview", response_model=APIResponse[Dict[str, Any]])
async def get_market_overview(
    exchange: str = Query("NSE", description="Exchange code"),
    provider: FinancialDataProvider = Depends(get_provider)
):
    if not provider:
        return create_response(data={"error": "Provider not configured"})

    try:
        # Assuming provider has a method for this, otherwise we mock it or compute it
        # For phase 11, if the method doesn't exist, we fallback
        if hasattr(provider, 'get_market_overview'):
            data = await provider.get_market_overview(exchange)
            return create_response(data=data)

        # Fallback simulated overview since base provider doesn't strictly define this yet
        # Real provider implementations should override this
        return create_response(data={
            "indices": [
                {"symbol": "NIFTY 50", "price": 22000.50, "change": 150.25, "percent_change": 0.68},
                {"symbol": "SENSEX", "price": 72500.10, "change": -45.20, "percent_change": -0.06},
                {"symbol": "BANK NIFTY", "price": 46000.00, "change": 210.50, "percent_change": 0.45},
            ]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gainers", response_model=APIResponse[List[Dict[str, Any]]])
async def get_top_gainers(
    limit: int = Query(10, ge=1, le=50),
    exchange: str = Query("NSE"),
    provider: FinancialDataProvider = Depends(get_provider)
):
    if not provider:
        return create_response(data=[])

    if hasattr(provider, 'get_top_gainers'):
        data = await provider.get_top_gainers(limit, exchange)
        return create_response(data=data)

    return create_response(data=[])

@router.get("/losers", response_model=APIResponse[List[Dict[str, Any]]])
async def get_top_losers(
    limit: int = Query(10, ge=1, le=50),
    exchange: str = Query("NSE"),
    provider: FinancialDataProvider = Depends(get_provider)
):
    if not provider:
        return create_response(data=[])

    if hasattr(provider, 'get_top_losers'):
        data = await provider.get_top_losers(limit, exchange)
        return create_response(data=data)

    return create_response(data=[])

@router.get("/most-active", response_model=APIResponse[List[Dict[str, Any]]])
async def get_most_active(
    limit: int = Query(10, ge=1, le=50),
    sort_by: str = Query("volume", regex="^(volume|value)$"),
    exchange: str = Query("NSE"),
    provider: FinancialDataProvider = Depends(get_provider)
):
    if not provider:
        return create_response(data=[])

    if hasattr(provider, 'get_most_active'):
        data = await provider.get_most_active(limit, sort_by, exchange)
        return create_response(data=data)

    return create_response(data=[])

@router.get("/breadth", response_model=APIResponse[Dict[str, Any]])
async def get_market_breadth(
    exchange: str = Query("NSE"),
    provider: FinancialDataProvider = Depends(get_provider)
):
    if not provider:
        return create_response(data={"advances": 0, "declines": 0, "unchanged": 0})

    if hasattr(provider, 'get_market_breadth'):
        data = await provider.get_market_breadth(exchange)
        return create_response(data=data)

    return create_response(data={
        "advances": 1250,
        "declines": 850,
        "unchanged": 120,
        "ratio": 1.47
    })
