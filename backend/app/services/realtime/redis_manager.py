import asyncio
import json
import logging
from typing import Dict, List, Optional, Callable, Any
from uuid import UUID

import redis.asyncio as redis
from redis.asyncio.client import PubSub

from app.providers.models import NormalizedQuote, NormalizedOHLCV
from .config import RealtimeConfig

logger = logging.getLogger(__name__)

class AsyncRedisManager:
    def __init__(self, config: RealtimeConfig) -> None:
        self.config = config
        self.pool: Any = redis.ConnectionPool.from_url(
            self.config.redis_url,
            max_connections=self.config.redis_pool_size,
            decode_responses=True
        )
        self.client = redis.Redis(connection_pool=self.pool)
        self.pubsub: Optional[PubSub] = None
        self._pubsub_task: Optional[asyncio.Task[Any]] = None
        self._callbacks: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    async def connect(self) -> None:
        """Establish base pub/sub connection."""
        self.pubsub = self.client.pubsub(ignore_subscribe_messages=True)
        self._pubsub_task = asyncio.create_task(self._listen_to_pubsub())

    async def close(self) -> None:
        """Graceful shutdown of Redis connections."""
        if self._pubsub_task:
            self._pubsub_task.cancel()
        if self.pubsub:
            await self.pubsub.close()
        await self.client.close()
        await self.pool.disconnect()

    async def check_health(self) -> bool:
        try:
            return await self.client.ping()
        except Exception:
            return False

    # --- State Management ---
    async def set_quote(self, instrument_id: UUID, quote: NormalizedQuote) -> None:
        key = f"quotes:{instrument_id}"
        data = quote.model_dump_json()
        await self.client.set(key, data, ex=self.config.quote_ttl_seconds)

    async def get_quote(self, instrument_id: UUID) -> Optional[NormalizedQuote]:
        key = f"quotes:{instrument_id}"
        data = await self.client.get(key)
        if data:
            return NormalizedQuote.model_validate_json(data)
        return None

    async def set_quotes_batch(self, quotes: Dict[UUID, NormalizedQuote]) -> None:
        if not quotes:
            return
        async with self.client.pipeline(transaction=False) as pipe:
            for instrument_id, quote in quotes.items():
                key = f"quotes:{instrument_id}"
                data = quote.model_dump_json()
                pipe.set(key, data, ex=self.config.quote_ttl_seconds)
            await pipe.execute()

    async def get_quotes_batch(self, instrument_ids: List[UUID]) -> Dict[UUID, NormalizedQuote]:
        if not instrument_ids:
            return {}
        keys = [f"quotes:{iid}" for iid in instrument_ids]
        results = await self.client.mget(keys)

        quotes = {}
        for iid, data in zip(instrument_ids, results):
            if data:
                quotes[iid] = NormalizedQuote.model_validate_json(data)
        return quotes

    # --- Pub/Sub Implementation ---
    async def publish_quote(self, quote: NormalizedQuote) -> None:
        channel = f"quotes:{quote.instrument_id}"
        data = quote.model_dump_json()
        await self.client.publish(channel, data)

    async def publish_ohlcv(self, ohlcv: NormalizedOHLCV) -> None:
        channel = f"ohlcv:{ohlcv.instrument_id}:{ohlcv.interval}"
        data = ohlcv.model_dump_json()
        await self.client.publish(channel, data)

    # --- Subscription Management ---
    async def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        if self.pubsub is None:
            await self.connect()

        assert self.pubsub is not None
        if channel not in self._callbacks:
            self._callbacks[channel] = []
            await self.pubsub.psubscribe(channel) if "*" in channel else await self.pubsub.subscribe(channel)

        self._callbacks[channel].append(callback)

    async def unsubscribe(self, channel: str) -> None:
        if channel in self._callbacks:
            del self._callbacks[channel]
            if self.pubsub:
                await self.pubsub.punsubscribe(channel) if "*" in channel else await self.pubsub.unsubscribe(channel)

    async def _listen_to_pubsub(self) -> None:
        assert self.pubsub is not None
        try:
            async for message in self.pubsub.listen():
                if message and message['type'] in ('message', 'pmessage'):
                    channel = message['channel']
                    if message['type'] == 'pmessage':
                        # Pattern matching handling if needed
                        pass

                    data = message['data']
                    try:
                        parsed_data = json.loads(data)
                    except Exception:
                        parsed_data = {"raw": data}

                    callbacks = self._callbacks.get(channel, [])
                    for cb in callbacks:
                        try:
                            # Evaluate callback synchronously or asynchronously based on type if needed
                            # Assuming simple synchronous callback wrapping for now as requested
                            cb(parsed_data)
                        except Exception as e:
                            logger.error(f"Error in pubsub callback for channel {channel}: {e}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Redis pubsub listener failed: {e}")
            # Real reconnection logic would backoff and restart the task here
