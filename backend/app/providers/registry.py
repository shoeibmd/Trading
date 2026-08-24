from typing import Dict, List, Optional
from .base import MarketDataProvider
from .models import ProviderHealth
import logging

logger = logging.getLogger(__name__)

class ProviderRegistry:
    """Registry pattern to manage multiple initialized MarketDataProviders."""

    def __init__(self) -> None:
        self._providers: Dict[str, MarketDataProvider] = {}

    def register_provider(self, code: str, provider: MarketDataProvider) -> None:
        if code in self._providers:
            logger.warning(f"Provider {code} is already registered. Overwriting.")
        self._providers[code] = provider

    def get_provider(self, code: str) -> MarketDataProvider:
        provider = self._providers.get(code)
        if not provider:
            raise KeyError(f"Provider '{code}' is not registered.")
        return provider

    def list_providers(self) -> List[str]:
        return list(self._providers.keys())

    def get_active_providers(self) -> List[MarketDataProvider]:
        return [p for p in self._providers.values() if p.config.is_active]

    async def check_all_health(self) -> List[ProviderHealth]:
        health_statuses = []
        for code, provider in self._providers.items():
            if provider.config.is_active:
                try:
                    health = await provider.check_health()
                    health_statuses.append(health)
                except Exception as e:
                    from datetime import datetime, timezone
                    logger.error(f"Error checking health for {code}: {e}")
                    health_statuses.append(
                        ProviderHealth(
                            provider_code=code,
                            is_healthy=False,
                            last_check=datetime.now(timezone.utc),
                            error_message=str(e)
                        )
                    )
        return health_statuses
