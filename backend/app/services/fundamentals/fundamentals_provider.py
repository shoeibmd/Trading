from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .normalized_models import (
    NormalizedCompanyProfile,
    NormalizedFinancialStatement,
    NormalizedFinancialRatios,
    NormalizedHistoricalFundamental
)

class ProviderHealth:
    def __init__(self, is_healthy: bool, latency_ms: float = 0.0, error_message: str = None):
        self.is_healthy = is_healthy
        self.latency_ms = latency_ms
        self.error_message = error_message

class FundamentalsProvider(ABC):
    @abstractmethod
    async def get_company_profile(self, instrument_id: UUID) -> Optional[NormalizedCompanyProfile]:
        pass

    @abstractmethod
    async def get_financial_statements(self, instrument_id: UUID, statement_type: str, period: str, limit: int = 10) -> List[NormalizedFinancialStatement]:
        pass

    @abstractmethod
    async def get_financial_ratios(self, instrument_id: UUID, period: str, limit: int = 10) -> List[NormalizedFinancialRatios]:
        pass

    @abstractmethod
    async def get_historical_fundamentals(self, instrument_id: UUID, metric: str, period: str, limit: int = 20) -> List[NormalizedHistoricalFundamental]:
        pass

    @abstractmethod
    async def check_health(self) -> ProviderHealth:
        pass
