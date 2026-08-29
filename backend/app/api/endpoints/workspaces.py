import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.api.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse
from app.api.schemas.common import APIResponse, create_response
from app.models.workspace import Workspace
from app.models.core import User
from app.api.deps import get_db

router = APIRouter()

async def get_default_user(db: AsyncSession) -> User:
    result = await db.execute(select(User).limit(1))
    user = result.scalar_one_or_none()
    if not user:
        user = User(
            email="test@test.com",
            hashed_password="pw",
            is_active=True,
            is_superuser=False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

@router.get("/", response_model=APIResponse[List[WorkspaceResponse]])
async def list_workspaces(db: AsyncSession = Depends(get_db)):
    """List all workspaces for the current user."""
    user = await get_default_user(db)
    result = await db.execute(select(Workspace).where(Workspace.user_id == user.id))
    workspaces = result.scalars().all()
    for w in workspaces:
        w.id = str(w.id)
        w.user_id = str(w.user_id)
    return create_response(data=workspaces)

@router.post("/", response_model=APIResponse[WorkspaceResponse])
async def create_workspace(workspace: WorkspaceCreate, db: AsyncSession = Depends(get_db)):
    """Create a new workspace."""
    user = await get_default_user(db)

    if workspace.is_default:
        result = await db.execute(select(Workspace).where(Workspace.user_id == user.id, Workspace.is_default == True))
        for existing in result.scalars().all():
            existing.is_default = False

    new_workspace = Workspace(
        user_id=user.id,
        name=workspace.name,
        is_default=workspace.is_default,
        layout_config=workspace.layout_config
    )

    db.add(new_workspace)
    await db.commit()
    await db.refresh(new_workspace)

    new_workspace.id = str(new_workspace.id)
    new_workspace.user_id = str(new_workspace.user_id)
    return create_response(data=new_workspace)

@router.get("/{workspace_id}", response_model=APIResponse[WorkspaceResponse])
async def get_workspace(workspace_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific workspace by ID."""
    try:
        ws_uuid = uuid.UUID(workspace_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Workspace).where(Workspace.id == ws_uuid, Workspace.user_id == user.id))
    workspace = result.scalar_one_or_none()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    workspace.id = str(workspace.id)
    workspace.user_id = str(workspace.user_id)
    return create_response(data=workspace)

@router.patch("/{workspace_id}", response_model=APIResponse[WorkspaceResponse])
async def update_workspace(workspace_id: str, updates: WorkspaceUpdate, db: AsyncSession = Depends(get_db)):
    """Update a workspace (name, layout_config)."""
    try:
        ws_uuid = uuid.UUID(workspace_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Workspace).where(Workspace.id == ws_uuid, Workspace.user_id == user.id))
    workspace = result.scalar_one_or_none()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    update_data = updates.model_dump(exclude_unset=True)

    if update_data.get("is_default") is True:
        others_result = await db.execute(select(Workspace).where(Workspace.user_id == user.id, Workspace.id != ws_uuid, Workspace.is_default == True))
        for existing in others_result.scalars().all():
            existing.is_default = False

    for key, value in update_data.items():
        setattr(workspace, key, value)

    await db.commit()
    await db.refresh(workspace)

    workspace.id = str(workspace.id)
    workspace.user_id = str(workspace.user_id)
    return create_response(data=workspace)

@router.delete("/{workspace_id}")
async def delete_workspace(workspace_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a workspace."""
    try:
        ws_uuid = uuid.UUID(workspace_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Workspace).where(Workspace.id == ws_uuid, Workspace.user_id == user.id))
    workspace = result.scalar_one_or_none()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    if workspace.is_default:
        raise HTTPException(status_code=400, detail="Cannot delete the default workspace")

    await db.delete(workspace)
    await db.commit()

    return create_response(data={"message": "Workspace deleted successfully"})
