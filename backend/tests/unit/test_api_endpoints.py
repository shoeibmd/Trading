import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
import json

from app.main import app
from app.api.dependencies import get_db, get_redis

mock_redis = AsyncMock()
mock_db = AsyncMock()

async def override_get_redis():
    return mock_redis

async def override_get_db():
    yield mock_db

app.dependency_overrides[get_redis] = override_get_redis
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_endpoint():
    mock_db.execute.return_value = None
    mock_redis.ping.return_value = True

    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["status"] == "healthy"
    assert data["database"] == "healthy"

def test_instruments_list_endpoint():
    class MockResult:
        def scalar(self): return 1
        def scalars(self):
            mock_obj = MagicMock()
            mock_obj.all = lambda: []
            return mock_obj

    mock_db.execute.return_value = MockResult()

    response = client.get("/api/v1/instruments?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "items" in data
    assert data["total"] == 1

def test_quotes_get_latest():
    from uuid import uuid4
    from datetime import datetime, timezone

    iid = str(uuid4())
    mock_redis.get.return_value = json.dumps({
        "instrument_id": iid,
        "symbol": "AAPL",
        "time": datetime.now(timezone.utc).isoformat(),
        "last_price": 150.0,
        "bid_price": None,
        "ask_price": None,
        "volume": None,
        "bid_size": None,
        "ask_size": None,
        "source": "MOCK"
    })

    response = client.get(f"/api/v1/quotes/{iid}")
    assert response.status_code == 200
    assert response.json()["data"]["last_price"] == "150.0"

def test_error_handling_404():
    class EmptyResult:
        def scalars(self):
            mock_obj = MagicMock()
            mock_obj.first = lambda: None
            return mock_obj

    mock_db.execute.return_value = EmptyResult()

    response = client.get("/api/v1/markets/UNKNOWN")
    assert response.status_code == 404
