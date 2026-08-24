from typing import List
from datetime import datetime, timezone
from pydantic import BaseModel
from app.providers.models import NormalizedQuote, NormalizedOHLCV, NormalizedInstrument

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class DataValidator:
    def __init__(self, staleness_threshold_seconds: int = 3600) -> None:
        self.staleness_threshold_seconds = staleness_threshold_seconds

    def validate_quote(self, quote: NormalizedQuote) -> ValidationResult:
        errors = []
        warnings: List[str] = []

        if quote.last_price <= 0:
            errors.append("last_price must be > 0")

        now = datetime.now(timezone.utc)
        if quote.timestamp > now:
            errors.append("timestamp is in the future")

        if (now - quote.timestamp).total_seconds() > self.staleness_threshold_seconds:
            errors.append(f"timestamp is older than {self.staleness_threshold_seconds}s staleness threshold")

        if quote.volume is not None and quote.volume < 0:
            errors.append("volume cannot be negative")

        if quote.bid_price is not None and quote.ask_price is not None:
            if quote.bid_price > quote.ask_price:
                warnings.append("bid_price > ask_price (potential crossed market)")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    def validate_ohlcv(self, ohlcv: NormalizedOHLCV) -> ValidationResult:
        errors = []
        warnings: List[str] = []

        if ohlcv.high < ohlcv.low:
            errors.append("high must be >= low")
        if ohlcv.high < ohlcv.open or ohlcv.high < ohlcv.close:
            errors.append("high must be >= open and close")
        if ohlcv.low > ohlcv.open or ohlcv.low > ohlcv.close:
            errors.append("low must be <= open and close")

        if ohlcv.volume < 0:
            errors.append("volume cannot be negative")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    def validate_instrument(self, instrument: NormalizedInstrument) -> ValidationResult:
        errors = []
        warnings: List[str] = []

        if not instrument.symbol or not instrument.exchange or not instrument.name:
            errors.append("symbol, exchange, and name are required")

        if instrument.lot_size <= 0:
            errors.append("lot_size must be > 0")

        if instrument.tick_size <= 0:
            errors.append("tick_size must be > 0")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)
