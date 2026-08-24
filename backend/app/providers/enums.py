from enum import Enum

class InstrumentType(str, Enum):
    EQUITY = "EQUITY"
    ETF = "ETF"
    INDEX = "INDEX"
    BOND = "BOND"
    DERIVATIVE = "DERIVATIVE"
    CURRENCY = "CURRENCY"

class OHLCVInterval(str, Enum):
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    DAY_1 = "1d"
    WEEK_1 = "1w"
    MONTH_1 = "1mo"

class ProviderType(str, Enum):
    REST_API = "REST_API"
    WEBSOCKET = "WEBSOCKET"
    FILE = "FILE"
    MANUAL = "MANUAL"

class MarketSession(str, Enum):
    PRE_MARKET = "PRE_MARKET"
    REGULAR = "REGULAR"
    POST_MARKET = "POST_MARKET"
    CLOSED = "CLOSED"
