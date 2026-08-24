# Real-Time Distribution Architecture

## Overview
The Real-Time data layer bridges the gap between asynchronous batch database processing (Ingestion Pipeline) and UI telemetry natively connecting via WebSockets leveraging Redis Pub/Sub natively mitigating massive scaling issues directly on backend services natively.

## Data Flow
Provider -> MarketDataCollector -> Validator -> DataStorage -> **Redis** -> **RedisWebSocketBridge** -> **WebSocketManager** -> **Client**.

## Components

### 1. Redis Manager (`AsyncRedisManager`)
Handles native `asyncio.redis` execution connecting natively securely mapping configuration constants efficiently bounding `set` mapping commands to `hash` variables locally natively scaling Pub/Sub efficiently without overlapping queues locally securely tracking states. Stored natively utilizing `TTL`.

### 2. WebSocket Manager (`WebSocketManager`)
Aggregates bounded TCP definitions tracking implicit heartbeats monitoring state effectively explicitly isolating backpressure thresholds inherently isolating bad actors seamlessly protecting execution layers efficiently directly avoiding bottlenecks natively.

### 3. Redis WebSocket Bridge (`RedisWebSocketBridge`)
Ties the Native decoupled Pub/Sub architecture securely effectively looping `broadcast_to_channel` cleanly to dynamically aggregated socket scopes dynamically decoupling direct connection links logically distributing telemetry efficiently directly effectively natively natively securely properly.

### 4. WebSocket Endpoint API (`backend/app/api/websocket.py`)
Defines the client structural bounds explicitly:
- `subscribe`
- `unsubscribe`
- `heartbeat`
- `get_snapshot`
