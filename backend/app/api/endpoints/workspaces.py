from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.dependencies import get_db, get_current_user
from app.api.schemas.common import APIResponse
from app.api.schemas.entity import WorkspaceResponse, WorkspacePanelResponse
from app.models.core import Workspace, WorkspacePanel

router = APIRouter()

@router.get("/workspaces", response_model=APIResponse[List[WorkspaceResponse]])
async def list_workspaces(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user)
) -> Any:
    query = select(Workspace).options(joinedload(Workspace.panels)).where(Workspace.user_id == user_id)
    result = await db.execute(query)
    items = result.unique().scalars().all()
    return APIResponse(data=[WorkspaceResponse.model_validate(i) for i in items])

@router.post("/workspaces", response_model=APIResponse[dict])
async def create_workspace() -> Any:
    return APIResponse(data={"status": "not implemented"})

@router.get("/workspaces/{workspace_id}", response_model=APIResponse[WorkspaceResponse])
async def get_workspace(workspace_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    query = select(Workspace).options(joinedload(Workspace.panels)).where(Workspace.id == workspace_id)
    result = await db.execute(query)
    item = result.unique().scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return APIResponse(data=WorkspaceResponse.model_validate(item))

@router.put("/workspaces/{workspace_id}", response_model=APIResponse[dict])
async def update_workspace(workspace_id: UUID) -> Any:
    return APIResponse(data={"status": "updated"})

@router.delete("/workspaces/{workspace_id}", response_model=APIResponse[dict])
async def delete_workspace(workspace_id: UUID) -> Any:
    return APIResponse(data={"status": "deleted"})

@router.get("/workspaces/{workspace_id}/panels", response_model=APIResponse[List[WorkspacePanelResponse]])
async def get_panels(workspace_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(WorkspacePanel).where(WorkspacePanel.workspace_id == workspace_id))
    items = result.scalars().all()
    return APIResponse(data=[WorkspacePanelResponse.model_validate(i) for i in items])

@router.post("/workspaces/{workspace_id}/panels", response_model=APIResponse[dict])
async def add_panel(workspace_id: UUID) -> Any:
    return APIResponse(data={"status": "panel added"})

@router.put("/workspaces/{workspace_id}/panels/{panel_id}", response_model=APIResponse[dict])
async def update_panel(workspace_id: UUID, panel_id: UUID) -> Any:
    return APIResponse(data={"status": "panel updated"})

@router.delete("/workspaces/{workspace_id}/panels/{panel_id}", response_model=APIResponse[dict])
async def delete_panel(workspace_id: UUID, panel_id: UUID) -> Any:
    return APIResponse(data={"status": "panel deleted"})
