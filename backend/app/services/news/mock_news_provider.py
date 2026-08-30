import uuid
import random
from datetime import datetime, timedelta
from typing import List, Optional
from .news_provider import NewsProvider, ProviderHealth
from .normalized_models import NormalizedNewsArticle

class MockNewsProvider(NewsProvider):
    """
    Mock implementation of a NewsProvider for testing.
    """

    def __init__(self):
        self._articles = self._generate_mock_articles(100)

    def _generate_mock_articles(self, count: int) -> List[NormalizedNewsArticle]:
        articles = []
        sources = ["Financial Times", "Reuters", "Bloomberg", "CNBC", "WSJ"]
        authors = ["Alice Smith", "Bob Jones", "Charlie Brown", None]

        now = datetime.utcnow()

        for i in range(count):
            articles.append(NormalizedNewsArticle(
                id=uuid.uuid4(),
                title=f"Mock News Headline {i}: Market Update",
                summary=f"This is a short summary for mock article {i} discussing market trends.",
                content=f"Full detailed content for article {i}. " * 10,
                url=f"https://example.com/news/{i}",
                source=random.choice(sources),
                author=random.choice(authors),
                published_at=now - timedelta(minutes=random.randint(1, 10000)),
                related_instruments=[],
                tags=["stocks", "market", "mock"],
                sentiment=random.uniform(-1.0, 1.0),
                image_url=None
            ))

        # Sort newest first
        articles.sort(key=lambda a: a.published_at, reverse=True)
        return articles

    async def get_latest_news(self, limit: int = 50) -> List[NormalizedNewsArticle]:
        return self._articles[:limit]

    async def get_news_by_instrument(self, instrument_id: uuid.UUID, limit: int = 20) -> List[NormalizedNewsArticle]:
        # For mock, just return random articles
        shuffled = list(self._articles)
        random.shuffle(shuffled)
        return shuffled[:limit]

    async def search_news(self, query: str, limit: int = 20) -> List[NormalizedNewsArticle]:
        results = [a for a in self._articles if query.lower() in a.title.lower() or query.lower() in a.summary.lower()]
        return results[:limit]

    async def get_article(self, article_id: uuid.UUID) -> Optional[NormalizedNewsArticle]:
        for article in self._articles:
            if article.id == article_id:
                return article
        return None

    async def check_health(self) -> ProviderHealth:
        return ProviderHealth(is_healthy=True, latency_ms=10.0)
