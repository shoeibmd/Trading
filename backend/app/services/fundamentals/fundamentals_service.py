from typing import List, Optional
from uuid import UUID
from fastapi import Request
from .normalized_models import (
    NormalizedCompanyProfile,
    NormalizedFinancialStatement,
    NormalizedFinancialRatios,
    NormalizedHistoricalFundamental
)
from .mock_fundamentals_provider import MockFundamentalsProvider

class FundamentalsService:
    def __init__(self, request: Request = None):
        self.request = request
        # Mock provider used for initial phase 14 frontend skeleton
        self.provider = MockFundamentalsProvider()

    async def get_company_profile(self, instrument_id: str) -> Optional[NormalizedCompanyProfile]:
        return await self.provider.get_company_profile(UUID(instrument_id))

    async def get_financial_statements(self, instrument_id: str, statement_type: str, period: str, limit: int = 10) -> List[NormalizedFinancialStatement]:
        # Validate inputs
        if statement_type not in ['income', 'balance', 'cashflow']:
            statement_type = 'income'
        if period not in ['quarterly', 'annual']:
            period = 'annual'

        return await self.provider.get_financial_statements(UUID(instrument_id), statement_type, period, limit)

    async def get_financial_ratios(self, instrument_id: str, period: str, limit: int = 10) -> List[NormalizedFinancialRatios]:
        if period not in ['quarterly', 'annual']:
            period = 'annual'
        return await self.provider.get_financial_ratios(UUID(instrument_id), period, limit)

    async def get_historical_fundamentals(self, instrument_id: str, metric: str, period: str, limit: int = 20) -> List[NormalizedHistoricalFundamental]:
        if period not in ['quarterly', 'annual']:
            period = 'annual'
        return await self.provider.get_historical_fundamentals(UUID(instrument_id), metric, period, limit)

def get_fundamentals_service(request: Request) -> FundamentalsService:
    return FundamentalsService(request)
