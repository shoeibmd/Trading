from typing import Any
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.api.dependencies import get_db
from app.api.schemas.common import APIResponse, PaginatedResponse
from app.api.schemas.entity import NewsArticleResponse
from app.models.core import NewsArticle

router = APIRouter()

@router.get("/news", response_model=APIResponse[PaginatedResponse[NewsArticleResponse]])
async def list_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    source: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> Any:
    query = select(NewsArticle).order_by(NewsArticle.published_at.desc())
    if source:
        query = query.where(NewsArticle.source == source)

    total_res = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_res.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return APIResponse(
        data=PaginatedResponse(
            items=[NewsArticleResponse.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total,
            has_previous=page > 1
        )
    )

@router.get("/news/search", response_model=APIResponse[PaginatedResponse[NewsArticleResponse]])
async def search_news(
    q: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
) -> Any:
    query = select(NewsArticle).where(
        or_(
            NewsArticle.title.ilike(f"%{q}%"),
            NewsArticle.content.ilike(f"%{q}%")
        )
    ).order_by(NewsArticle.published_at.desc())

    total_res = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_res.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return APIResponse(
        data=PaginatedResponse(
            items=[NewsArticleResponse.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total,
            has_previous=page > 1
        )
    )

@router.get("/news/{article_id}", response_model=APIResponse[NewsArticleResponse])
async def get_article(article_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(NewsArticle).where(NewsArticle.id == article_id))
    article = result.scalars().first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return APIResponse(data=NewsArticleResponse.model_validate(article))

@router.get("/news/instrument/{instrument_id}", response_model=APIResponse[PaginatedResponse[NewsArticleResponse]])
async def get_instrument_news(
    instrument_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
) -> Any:
    return APIResponse(
        data=PaginatedResponse(
            items=[],
            total=0,
            page=page,
            page_size=page_size,
            has_next=False,
            has_previous=False
        )
    )
