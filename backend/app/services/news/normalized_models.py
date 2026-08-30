from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class NormalizedNewsArticle(BaseModel):
    id: UUID
    title: str
    summary: str
    content: str
    url: str
    source: str
    author: Optional[str] = None
    published_at: datetime
    related_instruments: List[UUID] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    sentiment: Optional[float] = None  # -1.0 to 1.0
    image_url: Optional[str] = None
