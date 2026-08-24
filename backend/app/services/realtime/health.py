from typing import Dict, Any
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class RealtimeHealth:
    def __init__(self, redis_manager: Any, ws_manager: Any) -> None:
        self.redis_manager = redis_manager
        self.ws_manager = ws_manager
        self.last_check_time = datetime.now(timezone.utc)

    async def check_health(self) -> Dict[str, Any]:
        """Aggregate health metrics across the distribution system."""
        self.last_check_time = datetime.now(timezone.utc)

        # Redis Health
        redis_healthy = False
        try:
            redis_healthy = await self.redis_manager.check_health()
        except Exception as e:
            logger.error(f"Health check failed for Redis: {e}")

        # WebSocket Metrics
        active_connections = len(self.ws_manager.active_connections)

        # Estimate global subscription count roughly
        total_subscriptions = sum(len(conn.subscriptions) for conn in self.ws_manager.active_connections.values())

        return {
            "status": "healthy" if redis_healthy else "unhealthy",
            "redis_connected": redis_healthy,
            "active_ws_connections": active_connections,
            "total_subscriptions": total_subscriptions,
            "timestamp": self.last_check_time.isoformat()
        }
