import uuid
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class WorkspacePanelBase(BaseModel):
    panel_type: str = Field(..., max_length=50)
    config: Dict[str, Any] = Field(default_factory=dict)

class WorkspacePanelCreate(WorkspacePanelBase):
    pass

class WorkspacePanelResponse(WorkspacePanelBase):
    id: str
    workspace_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    layout_config: Dict[str, Any] = Field(default_factory=dict)
    is_default: bool = False

class WorkspaceCreate(WorkspaceBase):
    pass

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    layout_config: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None

class WorkspaceResponse(WorkspaceBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    panels: List[WorkspacePanelResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
