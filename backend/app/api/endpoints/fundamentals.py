from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.api.schemas.common import APIResponse, create_response
from app.services.fundamentals.fundamentals_service import FundamentalsService, get_fundamentals_service
from app.services.fundamentals.normalized_models import (
    NormalizedCompanyProfile,
    NormalizedFinancialStatement,
    NormalizedFinancialRatios,
    NormalizedHistoricalFundamental
)

router = APIRouter()

@router.get("/{instrument_id}/profile", response_model=APIResponse[NormalizedCompanyProfile])
async def get_company_profile(
    instrument_id: str,
    service: FundamentalsService = Depends(get_fundamentals_service)
):
    try:
        data = await service.get_company_profile(instrument_id)
        if not data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return create_response(data=data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid instrument ID format")

@router.get("/{instrument_id}/statements", response_model=APIResponse[List[NormalizedFinancialStatement]])
async def get_all_statements(
    instrument_id: str,
    period_type: str = Query("annual", regex="^(quarterly|annual)$"),
    limit: int = Query(4, ge=1, le=20),
    service: FundamentalsService = Depends(get_fundamentals_service)
):
    try:
        # Defaults to income statement if not specified,
        # but in a real API you might aggregate them.
        # We will use the specific /statements/{type} endpoint below instead.
        data = await service.get_financial_statements(instrument_id, "income", period_type, limit)
        return create_response(data=data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid instrument ID format")

@router.get("/{instrument_id}/statements/{statement_type}", response_model=APIResponse[List[NormalizedFinancialStatement]])
async def get_specific_statements(
    instrument_id: str,
    statement_type: str,
    period_type: str = Query("annual", regex="^(quarterly|annual)$"),
    limit: int = Query(4, ge=1, le=20),
    service: FundamentalsService = Depends(get_fundamentals_service)
):
    try:
        data = await service.get_financial_statements(instrument_id, statement_type, period_type, limit)
        return create_response(data=data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid instrument ID format")

@router.get("/{instrument_id}/ratios", response_model=APIResponse[List[NormalizedFinancialRatios]])
async def get_financial_ratios(
    instrument_id: str,
    period_type: str = Query("annual", regex="^(quarterly|annual)$"),
    limit: int = Query(4, ge=1, le=20),
    service: FundamentalsService = Depends(get_fundamentals_service)
):
    try:
        data = await service.get_financial_ratios(instrument_id, period_type, limit)
        return create_response(data=data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid instrument ID format")

@router.get("/{instrument_id}/historical", response_model=APIResponse[List[NormalizedHistoricalFundamental]])
async def get_historical_fundamentals(
    instrument_id: str,
    metric: str = Query(..., description="Metric to chart (e.g. revenue, net_income)"),
    period_type: str = Query("annual", regex="^(quarterly|annual)$"),
    limit: int = Query(20, ge=1, le=50),
    service: FundamentalsService = Depends(get_fundamentals_service)
):
    try:
        data = await service.get_historical_fundamentals(instrument_id, metric, period_type, limit)
        return create_response(data=data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid instrument ID format")
