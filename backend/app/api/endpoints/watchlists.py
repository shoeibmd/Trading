from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.dependencies import get_db, get_current_user
from app.api.schemas.common import APIResponse
from app.api.schemas.entity import WatchlistResponse
from app.models.core import Watchlist

router = APIRouter()

@router.get("/watchlists", response_model=APIResponse[List[WatchlistResponse]])
async def list_watchlists(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user)
) -> Any:
    query = select(Watchlist).options(joinedload(Watchlist.items)).where(Watchlist.user_id == user_id)
    result = await db.execute(query)
    watchlists = result.unique().scalars().all()

    return APIResponse(data=[WatchlistResponse.model_validate(w) for w in watchlists])

@router.post("/watchlists", response_model=APIResponse[dict])
async def create_watchlist() -> Any:
    return APIResponse(data={"status": "not implemented"})

@router.get("/watchlists/{watchlist_id}", response_model=APIResponse[dict])
async def get_watchlist(watchlist_id: UUID) -> Any:
    return APIResponse(data={"id": str(watchlist_id)})

@router.put("/watchlists/{watchlist_id}", response_model=APIResponse[dict])
async def update_watchlist(watchlist_id: UUID) -> Any:
    return APIResponse(data={"status": "updated"})

@router.delete("/watchlists/{watchlist_id}", response_model=APIResponse[dict])
async def delete_watchlist(watchlist_id: UUID) -> Any:
    return APIResponse(data={"status": "deleted"})

@router.post("/watchlists/{watchlist_id}/items", response_model=APIResponse[dict])
async def add_watchlist_item(watchlist_id: UUID) -> Any:
    return APIResponse(data={"status": "item added"})

@router.delete("/watchlists/{watchlist_id}/items/{item_id}", response_model=APIResponse[dict])
async def remove_watchlist_item(watchlist_id: UUID, item_id: UUID) -> Any:
    return APIResponse(data={"status": "item removed"})

@router.put("/watchlists/{watchlist_id}/items/reorder", response_model=APIResponse[dict])
async def reorder_watchlist_items(watchlist_id: UUID) -> Any:
    return APIResponse(data={"status": "items reordered"})
