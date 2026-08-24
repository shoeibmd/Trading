from pydantic import BaseModel
import os

class RealtimeConfig(BaseModel):
    redis_url: str = os.getenv("APP_REDIS_URL", "redis://localhost:6379/0")
    redis_pool_size: int = 10
    websocket_max_connections: int = 1000
    websocket_heartbeat_interval_seconds: int = 30
    websocket_stale_connection_timeout_seconds: int = 60
    throttle_messages_per_second: int = 100
    batch_interval_ms: int = 100
    quote_ttl_seconds: int = 3600
