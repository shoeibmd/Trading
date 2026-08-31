import uuid
import random
from datetime import date, datetime, timedelta
from typing import List, Optional
from decimal import Decimal
from .fundamentals_provider import FundamentalsProvider, ProviderHealth
from .normalized_models import (
    NormalizedCompanyProfile,
    NormalizedFinancialStatement,
    NormalizedFinancialRatios,
    NormalizedHistoricalFundamental
)

class MockFundamentalsProvider(FundamentalsProvider):
    """
    Mock implementation of a FundamentalsProvider for development testing.
    Generates coherent, realistic financial data to ensure charts and tables render correctly.
    """

    def __init__(self):
        # We don't pre-generate everything because of the parameter matrix,
        # instead we use seeded generation per instrument to maintain consistency
        pass

    def _get_seeded_random(self, instrument_id: uuid.UUID):
        # Use a stable seed per instrument so data remains consistent across requests
        seed_val = hash(str(instrument_id)) % (2**32)
        r = random.Random(seed_val)
        return r

    async def get_company_profile(self, instrument_id: uuid.UUID) -> Optional[NormalizedCompanyProfile]:
        r = self._get_seeded_random(instrument_id)
        return NormalizedCompanyProfile(
            instrument_id=str(instrument_id),
            company_name=f"Mock Corp {str(instrument_id)[:4].upper()}",
            description="A leading provider of mock data and test infrastructure for financial systems globally.",
            sector=r.choice(["Technology", "Finance", "Healthcare", "Energy"]),
            industry=r.choice(["Software", "Banking", "Biotech", "Oil & Gas"]),
            founded_year=r.randint(1950, 2015),
            employees=r.randint(500, 50000),
            website="https://example.com",
            headquarters="New York, NY",
            ceo="Jane Doe",
            market_cap=Decimal(str(r.randint(1_000_000_000, 100_000_000_000))),
            shares_outstanding=r.randint(50_000_000, 5_000_000_000)
        )

    async def get_financial_statements(self, instrument_id: uuid.UUID, statement_type: str, period: str, limit: int = 10) -> List[NormalizedFinancialStatement]:
        r = self._get_seeded_random(instrument_id)
        statements = []

        # Base values for Q8 (oldest)
        base_revenue = Decimal(str(r.randint(100_000_000, 5_000_000_000)))
        base_assets = base_revenue * Decimal('1.5')

        current_date = date.today()
        current_year = current_date.year
        current_quarter = (current_date.month - 1) // 3 + 1

        for i in range(limit):
            # Calculate dates working backwards
            if period == 'quarterly':
                q = current_quarter - i
                y = current_year
                while q <= 0:
                    q += 4
                    y -= 1
                period_end = date(y, q * 3, 28) # rough end of quarter
            else:
                y = current_year - i - 1
                q = 4
                period_end = date(y, 12, 31)

            # Apply growth factor 2-5% per quarter to work backwards from now (meaning divide to get past values)
            growth = Decimal(str(1 + r.uniform(-0.02, 0.08)))

            revenue = base_revenue * (growth ** (limit - i))
            cogs = revenue * Decimal(str(r.uniform(0.4, 0.6)))
            gross_profit = revenue - cogs
            opex = revenue * Decimal(str(r.uniform(0.15, 0.25)))
            net_income = gross_profit - opex

            items = {}
            if statement_type == 'income':
                items = {
                    'totalRevenue': revenue,
                    'costOfRevenue': cogs,
                    'grossProfit': gross_profit,
                    'operatingExpenses': opex,
                    'netIncome': net_income
                }
            elif statement_type == 'balance':
                assets = base_assets * (growth ** (limit - i))
                liabilities = assets * Decimal(str(r.uniform(0.3, 0.7)))
                equity = assets - liabilities
                items = {
                    'totalAssets': assets,
                    'totalLiabilities': liabilities,
                    'totalStockholderEquity': equity
                }
            elif statement_type == 'cashflow':
                items = {
                    'operatingCashflow': net_income * Decimal('1.2'),
                    'investingCashflow': net_income * Decimal('-0.5'),
                    'financingCashflow': net_income * Decimal('-0.3')
                }

            statements.append(NormalizedFinancialStatement(
                instrument_id=str(instrument_id),
                statement_type=statement_type,
                period_type=period,
                period_end_date=period_end,
                fiscal_year=y,
                fiscal_quarter=q if period == 'quarterly' else None,
                items=items,
                currency="USD",
                reported_at=datetime.combine(period_end, datetime.min.time()) + timedelta(days=30)
            ))

        return statements

    async def get_financial_ratios(self, instrument_id: uuid.UUID, period: str, limit: int = 10) -> List[NormalizedFinancialRatios]:
        r = self._get_seeded_random(instrument_id)
        ratios = []

        current_date = date.today()
        current_year = current_date.year
        current_quarter = (current_date.month - 1) // 3 + 1

        # Base realistic ratios
        pe_base = Decimal(str(r.uniform(10, 40)))
        roe_base = Decimal(str(r.uniform(0.05, 0.25)))

        for i in range(limit):
            if period == 'quarterly':
                q = current_quarter - i
                y = current_year
                while q <= 0:
                    q += 4
                    y -= 1
                period_end = date(y, q * 3, 28)
            else:
                y = current_year - i - 1
                period_end = date(y, 12, 31)

            variance = Decimal(str(1 + r.uniform(-0.1, 0.1)))

            ratios.append(NormalizedFinancialRatios(
                instrument_id=str(instrument_id),
                period_type=period,
                period_end_date=period_end,
                pe_ratio=pe_base * variance,
                pb_ratio=pe_base * Decimal('0.2') * variance,
                ps_ratio=pe_base * Decimal('0.1') * variance,
                roe=roe_base * variance,
                roa=roe_base * Decimal('0.4') * variance,
                debt_to_equity=Decimal(str(r.uniform(0.2, 2.0))),
                current_ratio=Decimal(str(r.uniform(1.1, 3.0))),
                quick_ratio=Decimal(str(r.uniform(0.8, 2.0))),
                gross_margin=Decimal(str(r.uniform(0.3, 0.8))),
                operating_margin=Decimal(str(r.uniform(0.1, 0.3))),
                net_margin=Decimal(str(r.uniform(0.05, 0.2))),
                dividend_yield=Decimal(str(r.uniform(0.01, 0.05))),
                eps=Decimal(str(r.uniform(1.0, 10.0)))
            ))

        return ratios

    async def get_historical_fundamentals(self, instrument_id: uuid.UUID, metric: str, period: str, limit: int = 20) -> List[NormalizedHistoricalFundamental]:
        # Reuse statement logic to ensure consistency
        stmts = await self.get_financial_statements(instrument_id, 'income', period, limit)
        hist = []
        for s in stmts:
            # Map metric name to statement key
            key_map = {'revenue': 'totalRevenue', 'net_income': 'netIncome'}
            item_key = key_map.get(metric, 'totalRevenue')

            val = s.items.get(item_key, Decimal('0'))
            hist.append(NormalizedHistoricalFundamental(
                instrument_id=str(instrument_id),
                metric=metric,
                period_type=period,
                period_end_date=s.period_end_date,
                value=val
            ))
        return hist

    async def check_health(self) -> ProviderHealth:
        return ProviderHealth(is_healthy=True, latency_ms=5.0)
