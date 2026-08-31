from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal

class NormalizedCompanyProfile(BaseModel):
    instrument_id: str
    company_name: str
    description: str
    sector: str
    industry: str
    founded_year: Optional[int] = None
    employees: Optional[int] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    ceo: Optional[str] = None
    market_cap: Optional[Decimal] = None
    shares_outstanding: Optional[int] = None

    @field_serializer('market_cap', when_used='json')
    def serialize_decimal(self, value: Optional[Decimal]) -> Optional[str]:
        return str(value) if value is not None else None


class NormalizedFinancialStatement(BaseModel):
    instrument_id: str
    statement_type: str  # 'income', 'balance', 'cashflow'
    period_type: str  # 'quarterly', 'annual'
    period_end_date: date
    fiscal_year: int
    fiscal_quarter: Optional[int] = None
    items: Dict[str, Decimal]
    currency: str
    reported_at: datetime

    @field_serializer('items', when_used='json')
    def serialize_items(self, value: Dict[str, Decimal]) -> Dict[str, str]:
        return {k: str(v) for k, v in value.items()}


class NormalizedFinancialRatios(BaseModel):
    instrument_id: str
    period_type: str
    period_end_date: date
    pe_ratio: Optional[Decimal] = None
    pb_ratio: Optional[Decimal] = None
    ps_ratio: Optional[Decimal] = None
    roe: Optional[Decimal] = None
    roa: Optional[Decimal] = None
    debt_to_equity: Optional[Decimal] = None
    current_ratio: Optional[Decimal] = None
    quick_ratio: Optional[Decimal] = None
    gross_margin: Optional[Decimal] = None
    operating_margin: Optional[Decimal] = None
    net_margin: Optional[Decimal] = None
    dividend_yield: Optional[Decimal] = None
    eps: Optional[Decimal] = None

    @field_serializer(
        'pe_ratio', 'pb_ratio', 'ps_ratio', 'roe', 'roa', 'debt_to_equity',
        'current_ratio', 'quick_ratio', 'gross_margin', 'operating_margin',
        'net_margin', 'dividend_yield', 'eps',
        when_used='json'
    )
    def serialize_decimal(self, value: Optional[Decimal]) -> Optional[str]:
        return str(value) if value is not None else None


class NormalizedHistoricalFundamental(BaseModel):
    instrument_id: str
    metric: str
    period_type: str
    period_end_date: date
    value: Decimal

    @field_serializer('value', when_used='json')
    def serialize_decimal(self, value: Decimal) -> str:
        return str(value)
