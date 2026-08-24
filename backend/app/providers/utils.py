import re
from datetime import datetime, timezone
from typing import Any

def validate_symbol_format(symbol: str, exchange: str) -> bool:
    """Validate a given symbol and exchange pattern broadly."""
    if not symbol or not exchange:
        return False
    # Only allow alphanumerics and some standard separators
    if not re.match(r"^[A-Z0-9.\-_]+$", symbol.upper()):
        return False
    if not re.match(r"^[A-Z0-9_]+$", exchange.upper()):
        return False
    return True

def normalize_interval(interval: str) -> str:
    """Normalize common interval strings into the standard internal format."""
    interval_map = {
        "1": "1m",
        "5": "5m",
        "15": "15m",
        "30": "30m",
        "60": "1h",
        "1H": "1h",
        "D": "1d",
        "1D": "1d",
        "W": "1w",
        "1W": "1w",
        "M": "1mo",
        "1M": "1mo",
    }
    return interval_map.get(interval.upper(), interval.lower())

def parse_timestamp(timestamp: Any) -> datetime:
    """Parse common timestamp types to a timezone-aware UTC datetime."""
    if isinstance(timestamp, datetime):
        if timestamp.tzinfo is None:
            return timestamp.replace(tzinfo=timezone.utc)
        return timestamp.astimezone(timezone.utc)

    if isinstance(timestamp, (int, float)):
        # Check if it's ms or s based on length
        if timestamp > 10**11:
            timestamp = timestamp / 1000.0
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    if isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            raise ValueError(f"Unable to parse string timestamp: {timestamp}")

    raise TypeError(f"Unsupported timestamp type: {type(timestamp)}")

def calculate_rate_limit_delay(limit: int, window: int) -> float:
    """Calculate the minimal sleep delay to obey a rate limit window (window in seconds)."""
    if limit <= 0:
        return 0.0
    return float(window) / float(limit)
