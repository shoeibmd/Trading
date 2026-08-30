from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .normalized_models import NormalizedNewsArticle

class ProviderHealth:
    def __init__(self, is_healthy: bool, latency_ms: float = 0.0, error_message: str = None):
        self.is_healthy = is_healthy
        self.latency_ms = latency_ms
        self.error_message = error_message

class NewsProvider(ABC):
    @abstractmethod
    async def get_latest_news(self, limit: int = 50) -> List[NormalizedNewsArticle]:
        pass

    @abstractmethod
    async def get_news_by_instrument(self, instrument_id: UUID, limit: int = 20) -> List[NormalizedNewsArticle]:
        pass

    @abstractmethod
    async def search_news(self, query: str, limit: int = 20) -> List[NormalizedNewsArticle]:
        pass

    @abstractmethod
    async def get_article(self, article_id: UUID) -> Optional[NormalizedNewsArticle]:
        pass

    @abstractmethod
    async def check_health(self) -> ProviderHealth:
        pass
