from typing import List, Optional
from uuid import UUID
from fastapi import Request
from .normalized_models import NormalizedNewsArticle
from .mock_news_provider import MockNewsProvider
from app.core.redis import RedisManager

class NewsService:
    def __init__(self, request: Request = None):
        self.request = request
        # In a real app we'd inject this, hardcoding mock for phase 13 skeleton
        self.provider = MockNewsProvider()

    async def get_latest_news(self, limit: int = 50) -> List[NormalizedNewsArticle]:
        # Would normally check redis cache here
        return await self.provider.get_latest_news(limit)

    async def get_news_by_instrument(self, instrument_id: str, limit: int = 20) -> List[NormalizedNewsArticle]:
        return await self.provider.get_news_by_instrument(UUID(instrument_id), limit)

    async def search_news(self, query: str, limit: int = 20) -> List[NormalizedNewsArticle]:
        return await self.provider.search_news(query, limit)

    async def get_article(self, article_id: str) -> Optional[NormalizedNewsArticle]:
        return await self.provider.get_article(UUID(article_id))

def get_news_service(request: Request) -> NewsService:
    return NewsService(request)
