import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.api.schemas.watchlist import (
    WatchlistCreate, WatchlistUpdate, WatchlistResponse,
    WatchlistItemCreate, WatchlistItemResponse, WatchlistItemReorder
)
from app.api.schemas.common import APIResponse, create_response
from app.models.watchlist import Watchlist, WatchlistItem
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

@router.get("/", response_model=APIResponse[List[WatchlistResponse]])
async def list_watchlists(db: AsyncSession = Depends(get_db)):
    user = await get_default_user(db)
    result = await db.execute(
        select(Watchlist)
        .options(selectinload(Watchlist.items).selectinload(WatchlistItem.instrument))
        .where(Watchlist.user_id == user.id)
    )
    watchlists = result.scalars().all()
    for w in watchlists:
        w.id = str(w.id)
        w.user_id = str(w.user_id)
        for i in w.items:
            i.id = str(i.id)
            i.watchlist_id = str(i.watchlist_id)
            i.instrument_id = str(i.instrument_id)
            if i.instrument:
                i.instrument.id = str(i.instrument.id)
    return create_response(data=watchlists)

@router.post("/", response_model=APIResponse[WatchlistResponse])
async def create_watchlist(watchlist: WatchlistCreate, db: AsyncSession = Depends(get_db)):
    user = await get_default_user(db)
    new_watchlist = Watchlist(user_id=user.id, name=watchlist.name)
    db.add(new_watchlist)
    await db.commit()
    await db.refresh(new_workspace)
    new_watchlist.id = str(new_watchlist.id)
    new_watchlist.user_id = str(new_watchlist.user_id)
    return create_response(data=new_watchlist)

@router.get("/{watchlist_id}", response_model=APIResponse[WatchlistResponse])
async def get_watchlist(watchlist_id: str, db: AsyncSession = Depends(get_db)):
    try:
        wl_uuid = uuid.UUID(watchlist_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(
        select(Watchlist)
        .options(selectinload(Watchlist.items).selectinload(WatchlistItem.instrument))
        .where(Watchlist.id == wl_uuid, Watchlist.user_id == user.id)
    )
    watchlist = result.scalar_one_or_none()

    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")

    watchlist.id = str(watchlist.id)
    watchlist.user_id = str(watchlist.user_id)
    for i in watchlist.items:
        i.id = str(i.id)
        i.watchlist_id = str(i.watchlist_id)
        i.instrument_id = str(i.instrument_id)
        if i.instrument:
            i.instrument.id = str(i.instrument.id)

    return create_response(data=watchlist)

@router.patch("/{watchlist_id}", response_model=APIResponse[WatchlistResponse])
async def update_watchlist(watchlist_id: str, updates: WatchlistUpdate, db: AsyncSession = Depends(get_db)):
    try:
        wl_uuid = uuid.UUID(watchlist_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Watchlist).where(Watchlist.id == wl_uuid, Watchlist.user_id == user.id))
    watchlist = result.scalar_one_or_none()

    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")

    if updates.name is not None:
        watchlist.name = updates.name

    await db.commit()
    await db.refresh(watchlist)

    watchlist.id = str(watchlist.id)
    watchlist.user_id = str(watchlist.user_id)
    return create_response(data=watchlist)

@router.delete("/{watchlist_id}")
async def delete_watchlist(watchlist_id: str, db: AsyncSession = Depends(get_db)):
    try:
        wl_uuid = uuid.UUID(watchlist_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Watchlist).where(Watchlist.id == wl_uuid, Watchlist.user_id == user.id))
    watchlist = result.scalar_one_or_none()

    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")

    await db.delete(watchlist)
    await db.commit()
    return create_response(data={"message": "Watchlist deleted successfully"})

@router.post("/{watchlist_id}/items", response_model=APIResponse[WatchlistItemResponse])
async def add_watchlist_item(watchlist_id: str, item: WatchlistItemCreate, db: AsyncSession = Depends(get_db)):
    try:
        wl_uuid = uuid.UUID(watchlist_id)
        inst_uuid = uuid.UUID(item.instrument_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Watchlist).where(Watchlist.id == wl_uuid, Watchlist.user_id == user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Watchlist not found")

    # Get max order
    from sqlalchemy import func
    max_order_result = await db.execute(
        select(func.max(WatchlistItem.order)).where(WatchlistItem.watchlist_id == wl_uuid)
    )
    max_order = max_order_result.scalar() or 0

    new_item = WatchlistItem(
        watchlist_id=wl_uuid,
        instrument_id=inst_uuid,
        order=max_order + 1
    )
    db.add(new_item)
    await db.commit()

    # Reload with instrument
    result = await db.execute(
        select(WatchlistItem)
        .options(selectinload(WatchlistItem.instrument))
        .where(WatchlistItem.id == new_item.id)
    )
    loaded_item = result.scalar_one()
    loaded_item.id = str(loaded_item.id)
    loaded_item.watchlist_id = str(loaded_item.watchlist_id)
    loaded_item.instrument_id = str(loaded_item.instrument_id)
    if loaded_item.instrument:
        loaded_item.instrument.id = str(loaded_item.instrument.id)

    return create_response(data=loaded_item)

@router.delete("/{watchlist_id}/items/{item_id}")
async def remove_watchlist_item(watchlist_id: str, item_id: str, db: AsyncSession = Depends(get_db)):
    try:
        wl_uuid = uuid.UUID(watchlist_id)
        item_uuid = uuid.UUID(item_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(
        select(WatchlistItem)
        .join(Watchlist)
        .where(WatchlistItem.id == item_uuid, WatchlistItem.watchlist_id == wl_uuid, Watchlist.user_id == user.id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Watchlist item not found")

    await db.delete(item)
    await db.commit()
    return create_response(data={"message": "Watchlist item deleted successfully"})

@router.put("/{watchlist_id}/reorder", response_model=APIResponse[dict])
async def reorder_watchlist_items(watchlist_id: str, reorder: WatchlistItemReorder, db: AsyncSession = Depends(get_db)):
    try:
        wl_uuid = uuid.UUID(watchlist_id)
        item_uuids = [uuid.UUID(i) for i in reorder.item_ids]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_default_user(db)
    result = await db.execute(select(Watchlist).where(Watchlist.id == wl_uuid, Watchlist.user_id == user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Watchlist not found")

    # Batch update orders
    for index, item_uuid in enumerate(item_uuids):
        result = await db.execute(select(WatchlistItem).where(WatchlistItem.id == item_uuid, WatchlistItem.watchlist_id == wl_uuid))
        item = result.scalar_one_or_none()
        if item:
            item.order = index

    await db.commit()
    return create_response(data={"message": "Watchlist reordered successfully"})
