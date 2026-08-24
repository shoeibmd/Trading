import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from datetime import datetime, timezone
from app.services.realtime.config import RealtimeConfig
from app.services.realtime.websocket_manager import WebSocketManager
from app.services.realtime.redis_manager import AsyncRedisManager

@pytest.mark.asyncio
async def test_websocket_lifecycle():
    config = RealtimeConfig()
    manager = WebSocketManager(config)
    mock_ws = AsyncMock()

    cid = await manager.connect(mock_ws)
    assert cid in manager.active_connections

    await manager.subscribe(cid, "quotes:AAPL")
    subs = await manager.get_subscriptions(cid)
    assert "quotes:AAPL" in subs

    await manager.unsubscribe(cid, "quotes:AAPL")
    subs = await manager.get_subscriptions(cid)
    assert "quotes:AAPL" not in subs

    await manager.disconnect(cid)
    assert cid not in manager.active_connections

@pytest.mark.asyncio
async def test_redis_pubsub_manager():
    config = RealtimeConfig()
    with patch("app.services.realtime.redis_manager.redis") as mock_redis:
        mock_client = MagicMock() # Needs to be a MagicMock because pubsub is not awaited in connect
        mock_redis.Redis.return_value = mock_client

        rm = AsyncRedisManager(config)
        rm.client = mock_client
        mock_pubsub = MagicMock()
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.psubscribe = AsyncMock()

        async def mock_listen():
            yield {"type": "message", "channel": "quotes:AAPL", "data": '{"test": 1}'}

        mock_pubsub.listen = mock_listen
        mock_client.pubsub.return_value = mock_pubsub

        await rm.subscribe("quotes:AAPL", lambda x: None)
        assert "quotes:AAPL" in rm._callbacks

@pytest.mark.asyncio
async def test_backpressure_drop():
    config = RealtimeConfig()
    manager = WebSocketManager(config)
    mock_ws = AsyncMock()
    mock_ws.send_json.side_effect = Exception("Slow client")

    cid = await manager.connect(mock_ws)
    # Simulate a broadcast causing an error that triggers disconnect
    await manager.send_to_connection(cid, {"msg": "test"})
    assert cid not in manager.active_connections
