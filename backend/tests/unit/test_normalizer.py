from app.services.ingestion.normalizer import DataNormalizer
from decimal import Decimal
from uuid import uuid4

def test_quote_normalization():
    raw_data = {
        "symbol": "AAPL",
        "price": "150.50",
        "volume": 1000
    }
    iid = uuid4()
    q = DataNormalizer.normalize_quote(raw_data, "MOCK", iid)

    assert q.symbol == "AAPL"
    assert q.last_price == Decimal("150.50")
    assert q.volume == 1000
    assert q.source == "MOCK"
