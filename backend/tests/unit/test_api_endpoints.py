import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_get_workspace(async_client: AsyncClient, override_get_db):
    workspace_data = {
        "name": "My Workspace",
        "is_default": True,
        "layout_config": {"workspaceId": "test", "panels": []}
    }

    response = await async_client.post("/api/v1/workspaces/", json=workspace_data)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "My Workspace"
    assert "id" in data["data"]
    assert data["data"]["is_default"] is True

    workspace_id = data["data"]["id"]

    get_response = await async_client.get(f"/api/v1/workspaces/{workspace_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["data"]["id"] == workspace_id
    assert get_data["data"]["name"] == "My Workspace"

@pytest.mark.asyncio
async def test_update_and_delete_workspace(async_client: AsyncClient, override_get_db):
    workspace_data = {
        "name": "To Update",
        "layout_config": {"workspaceId": "test", "panels": []}
    }
    create_response = await async_client.post("/api/v1/workspaces/", json=workspace_data)
    workspace_id = create_response.json()["data"]["id"]

    update_data = {"name": "Updated Name", "is_default": False}
    update_response = await async_client.patch(f"/api/v1/workspaces/{workspace_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["data"]["name"] == "Updated Name"

    delete_response = await async_client.delete(f"/api/v1/workspaces/{workspace_id}")
    assert delete_response.status_code == 200

    get_response = await async_client.get(f"/api/v1/workspaces/{workspace_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_get_market_aggregations(async_client: AsyncClient, override_get_db):
    response = await async_client.get("/api/v1/markets/overview")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "indices" in data["data"]

    response = await async_client.get("/api/v1/markets/gainers")
    assert response.status_code == 200

    response = await async_client.get("/api/v1/markets/losers")
    assert response.status_code == 200

    response = await async_client.get("/api/v1/markets/most-active")
    assert response.status_code == 200

    response = await async_client.get("/api/v1/markets/breadth")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_watchlist_endpoints(async_client: AsyncClient, override_get_db):
    wl_data = {
        "name": "Tech Stocks"
    }

    # Create
    create_resp = await async_client.post("/api/v1/watchlists/", json=wl_data)
    assert create_resp.status_code == 200
    wl_id = create_resp.json()["data"]["id"]

    # Get
    get_resp = await async_client.get(f"/api/v1/watchlists/{wl_id}")
    assert get_resp.status_code == 200

    # Update
    update_resp = await async_client.patch(f"/api/v1/watchlists/{wl_id}", json={"name": "New Name"})
    assert update_resp.status_code == 200
    assert update_resp.json()["data"]["name"] == "New Name"

    # Delete
    del_resp = await async_client.delete(f"/api/v1/watchlists/{wl_id}")
    assert del_resp.status_code == 200

@pytest.mark.asyncio
async def test_ohlcv_and_indicators(async_client: AsyncClient, override_get_db):
    response = await async_client.get("/api/v1/ohlcv/AAPL?interval=1d&limit=50")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 50
    assert "open" in data["data"][0]

    response = await async_client.get("/api/v1/indicators/AAPL?indicator=rsi&interval=1d&period=14")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 100
    assert "close" in data["data"][0]

@pytest.mark.asyncio
async def test_news_endpoints(async_client: AsyncClient):
    # Test GET /api/v1/news/
    response = await async_client.get("/api/v1/news/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 5
    assert "id" in data["data"][0]

    # Test GET /api/v1/news/search
    search_res = await async_client.get("/api/v1/news/search?q=Mock&limit=5")
    assert search_res.status_code == 200
    assert len(search_res.json()["data"]) > 0

    # Test GET /api/v1/news/{article_id}
    article_id = data["data"][0]["id"]
    detail_res = await async_client.get(f"/api/v1/news/{article_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["data"]["id"] == article_id

@pytest.mark.asyncio
async def test_fundamentals_endpoints(async_client: AsyncClient):
    # Test GET /api/v1/fundamentals/{id}/profile
    res = await async_client.get("/api/v1/fundamentals/123e4567-e89b-12d3-a456-426614174000/profile")
    assert res.status_code == 200

    # Test GET statements
    res = await async_client.get("/api/v1/fundamentals/123e4567-e89b-12d3-a456-426614174000/statements/income")
    assert res.status_code == 200

    # Test GET ratios
    res = await async_client.get("/api/v1/fundamentals/123e4567-e89b-12d3-a456-426614174000/ratios")
    assert res.status_code == 200

    # Test GET historical
    res = await async_client.get("/api/v1/fundamentals/123e4567-e89b-12d3-a456-426614174000/historical?metric=revenue")
    assert res.status_code == 200

@pytest.mark.asyncio

@pytest.mark.asyncio
async def test_portfolio_endpoints(async_client: AsyncClient, override_get_db):
    port_data = {
        "name": "My Portfolio",
        "currency": "USD",
        "is_default": True
    }
    create_resp = await async_client.post("/api/v1/portfolios/", json=port_data)
    assert create_resp.status_code == 200
    portfolio_id = create_resp.json()["data"]["id"]

    get_resp = await async_client.get(f"/api/v1/portfolios/{portfolio_id}")
    assert get_resp.status_code == 200

    list_resp = await async_client.get("/api/v1/portfolios/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()["data"]) >= 1

    sum_resp = await async_client.get(f"/api/v1/portfolios/{portfolio_id}/summary")
    assert sum_resp.status_code == 200
