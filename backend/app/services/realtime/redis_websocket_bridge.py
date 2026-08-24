import asyncio
import logging
import json
from typing import Dict, Any, Optional

from .redis_manager import AsyncRedisManager
from .websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)

class RedisWebSocketBridge:
    def __init__(self, redis_manager: AsyncRedisManager, ws_manager: WebSocketManager) -> None:
        self.redis_manager = redis_manager
        self.ws_manager = ws_manager
        self.active_channels: set[str] = set()

    def _handle_message(self, message: Dict[str, Any]) -> None:
        """Callback to handle messages from Redis and forward them to WebSocket clients."""
        try:
            channel = message.get("channel", "unknown")
            # The data might be inside 'raw' if parsing failed or direct dict if parsed
            data = message.get("raw") or message

            # Throttle or batch handling could be placed here logically.
            asyncio.create_task(self.ws_manager.broadcast_to_channel(channel, data))
        except Exception as e:
            logger.error(f"Bridge failed to handle message: {e}")

    async def subscribe(self, channel: str) -> None:
        if channel not in self.active_channels:
            await self.redis_manager.subscribe(channel, self._handle_message)
            self.active_channels.add(channel)

    async def unsubscribe(self, channel: str) -> None:
        if channel in self.active_channels:
            await self.redis_manager.unsubscribe(channel)
            self.active_channels.discard(channel)
