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
