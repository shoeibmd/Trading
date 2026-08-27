import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Workspace(Base, TimestampMixin):
    __tablename__ = "workspaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # The actual db schema links this to the users table
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    layout_config = Column(JSONB, nullable=False, default=dict)
    is_default = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="workspaces")
    panels = relationship("WorkspacePanel", back_populates="workspace", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Workspace {self.name} (id={self.id})>"

class WorkspacePanel(Base, TimestampMixin):
    __tablename__ = "workspace_panels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    panel_type = Column(String(50), nullable=False)
    config = Column(JSONB, nullable=False, default=dict)

    workspace = relationship("Workspace", back_populates="panels")

    def __repr__(self) -> str:
        return f"<WorkspacePanel {self.panel_type} (workspace_id={self.workspace_id})>"
