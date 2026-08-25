import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.main import app
from app.api.dependencies import get_db, get_redis

mock_redis = AsyncMock()
mock_db = AsyncMock()

async def override_get_redis(): return mock_redis
async def override_get_db(): yield mock_db

app.dependency_overrides[get_redis] = override_get_redis
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_openapi_json_schema_valid():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
    assert "/api/v1/health" in schema["paths"]
    assert "/api/v1/instruments" in schema["paths"]
