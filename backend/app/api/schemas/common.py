from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional, Dict, Any

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    data: T
    meta: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool
