import asyncio
import logging
from typing import Dict, Set, Optional, Any
from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from fastapi import WebSocket

from .config import RealtimeConfig

logger = logging.getLogger(__name__)

class WebSocketConnection(BaseModel):
    model_config = dict(arbitrary_types_allowed=True)

    connection_id: UUID = Field(default_factory=uuid4)
    websocket: Any # Type erased for generic FastAPI testing
    subscriptions: Set[str] = Field(default_factory=set)
    user_id: Optional[UUID] = None
    connected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    client_info: Dict[str, Any] = Field(default_factory=dict)
    messages_sent: int = 0
    message_timestamps: list[float] = Field(default_factory=list) # used for sliding window rate limiting

class WebSocketManager:
    def __init__(self, config: RealtimeConfig) -> None:
        self.config = config
        self.active_connections: Dict[UUID, WebSocketConnection] = {}
        self.channel_subscriptions: Dict[str, Set[UUID]] = {}
        self._cleanup_task: Optional[asyncio.Task[Any]] = None

    def start_cleanup_task(self) -> None:
        if not self._cleanup_task:
            self._cleanup_task = asyncio.create_task(self._cleanup_stale_connections())

    async def connect(self, websocket: Any, user_id: Optional[UUID] = None, client_info: Optional[Dict[str, Any]] = None) -> UUID:
        await websocket.accept()
        connection = WebSocketConnection(
            websocket=websocket,
            user_id=user_id,
            client_info=client_info or {}
        )
        self.active_connections[connection.connection_id] = connection
        logger.info(f"WebSocket connected: {connection.connection_id}")
        return connection.connection_id

    async def disconnect(self, connection_id: UUID) -> None:
        connection = self.active_connections.pop(connection_id, None)
        if connection:
            for channel in connection.subscriptions:
                if channel in self.channel_subscriptions:
                    self.channel_subscriptions[channel].discard(connection_id)
                    if not self.channel_subscriptions[channel]:
                        del self.channel_subscriptions[channel]
            try:
                await connection.websocket.close()
            except Exception:
                pass
            logger.info(f"WebSocket disconnected: {connection_id}")

    async def heartbeat(self, connection_id: UUID) -> None:
        if connection_id in self.active_connections:
            self.active_connections[connection_id].last_heartbeat = datetime.now(timezone.utc)

    async def subscribe(self, connection_id: UUID, channel: str) -> None:
        if connection_id in self.active_connections:
            connection = self.active_connections[connection_id]
            if channel not in connection.subscriptions:
                connection.subscriptions.add(channel)
                if channel not in self.channel_subscriptions:
                    self.channel_subscriptions[channel] = set()
                self.channel_subscriptions[channel].add(connection_id)

    async def unsubscribe(self, connection_id: UUID, channel: str) -> None:
        if connection_id in self.active_connections:
            connection = self.active_connections[connection_id]
            if channel in connection.subscriptions:
                connection.subscriptions.remove(channel)
            if channel in self.channel_subscriptions:
                self.channel_subscriptions[channel].discard(connection_id)
                if not self.channel_subscriptions[channel]:
                    del self.channel_subscriptions[channel]

    async def get_subscriptions(self, connection_id: UUID) -> Set[str]:
        if connection_id in self.active_connections:
            return self.active_connections[connection_id].subscriptions
        return set()

    def _format_message(self, msg_type: str, channel: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": msg_type,
            "channel": channel,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sequence": 0 # Handled externally or implicitly by client tracking if necessary
        }

    def _is_rate_limited(self, connection: WebSocketConnection) -> bool:
        """Evaluate messages per second threshold natively via sliding window."""
        now = asyncio.get_event_loop().time()

        # Clean timestamps older than 1 second
        connection.message_timestamps = [t for t in connection.message_timestamps if now - t <= 1.0]

        if len(connection.message_timestamps) >= self.config.throttle_messages_per_second:
            return True

        connection.message_timestamps.append(now)
        return False

    async def send_to_connection(self, connection_id: UUID, message: Dict[str, Any]) -> None:
        if connection_id in self.active_connections:
            conn = self.active_connections[connection_id]

            # Backpressure / Throttling explicit implementation
            if self._is_rate_limited(conn):
                logger.warning(f"Connection {connection_id} exceeded throttle limit. Dropping message.")
                # Send warning message natively once implicitly handled gracefully bypassing bounds cleanly.
                try:
                    await conn.websocket.send_json({"type": "error", "data": {"message": "Throttle limit exceeded."}})
                except Exception:
                    pass
                return

            try:
                await conn.websocket.send_json(message)
                conn.messages_sent += 1
            except Exception as e:
                logger.warning(f"Failed to send message to {connection_id}: {e}")
                await self.disconnect(connection_id)

    async def broadcast_to_channel(self, channel: str, message: Dict[str, Any]) -> None:
        if channel in self.channel_subscriptions:
            formatted_msg = self._format_message("data", channel, message)
            subscriber_ids = list(self.channel_subscriptions[channel])
            # Send concurrently
            tasks = [self.send_to_connection(cid, formatted_msg) for cid in subscriber_ids]
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def _cleanup_stale_connections(self) -> None:
        timeout = self.config.websocket_stale_connection_timeout_seconds
        while True:
            await asyncio.sleep(timeout / 2)
            now = datetime.now(timezone.utc)
            stale_cids = []
            for cid, conn in self.active_connections.items():
                if (now - conn.last_heartbeat).total_seconds() > timeout:
                    stale_cids.append(cid)

            for cid in stale_cids:
                logger.warning(f"Disconnecting stale connection: {cid}")
                await self.disconnect(cid)
