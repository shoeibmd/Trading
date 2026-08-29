import uuid
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .entity import InstrumentResponse

class WatchlistItemCreate(BaseModel):
    instrument_id: str

class WatchlistItemResponse(BaseModel):
    id: str
    watchlist_id: str
    instrument_id: str
    order: int
    instrument: Optional[InstrumentResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WatchlistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class WatchlistResponse(WatchlistBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    items: List[WatchlistItemResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

class WatchlistItemReorder(BaseModel):
    item_ids: List[str] = Field(..., description="Ordered list of watchlist item IDs")
