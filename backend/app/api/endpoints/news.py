from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.api.schemas.common import APIResponse, create_response
from app.services.news.news_service import NewsService, get_news_service
from app.services.news.normalized_models import NormalizedNewsArticle

router = APIRouter()

@router.get("/", response_model=APIResponse[List[NormalizedNewsArticle]])
async def get_latest_news(
    limit: int = Query(20, ge=1, le=100),
    service: NewsService = Depends(get_news_service)
):
    """Get latest market news."""
    data = await service.get_latest_news(limit)
    return create_response(data=data)

@router.get("/search", response_model=APIResponse[List[NormalizedNewsArticle]])
async def search_news(
    q: str = Query(..., min_length=2),
    limit: int = Query(20, ge=1, le=100),
    service: NewsService = Depends(get_news_service)
):
    """Search news articles."""
    data = await service.search_news(q, limit)
    return create_response(data=data)

@router.get("/instrument/{instrument_id}", response_model=APIResponse[List[NormalizedNewsArticle]])
async def get_instrument_news(
    instrument_id: str,
    limit: int = Query(20, ge=1, le=100),
    service: NewsService = Depends(get_news_service)
):
    """Get news for a specific instrument."""
    try:
        data = await service.get_news_by_instrument(instrument_id, limit)
        return create_response(data=data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{article_id}", response_model=APIResponse[NormalizedNewsArticle])
async def get_article(
    article_id: str,
    service: NewsService = Depends(get_news_service)
):
    """Get a specific article by ID."""
    try:
        data = await service.get_article(article_id)
        if not data:
            raise HTTPException(status_code=404, detail="Article not found")
        return create_response(data=data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article ID format")
