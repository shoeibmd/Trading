# Ingestion Pipeline Architecture

## Overview
The ingestion pipeline is designed to collect financial data securely across a variety of unified vendors securely without locking domain objects into rigid specific architectures.

## Key Components

### 1. Collector (`MarketDataCollector`)
Leveraging exponential backoffs, delayed retry mechanisms, and rate limits, this orchestrator scales efficiently without crashing downstream provider services. Native handling for:
- `ProviderRateLimitError`
- `ProviderTimeoutError`
- `ProviderDataError`
- `ProviderNotAvailableError`

### 2. Validator (`DataValidator`)
Filters out incomplete data models implicitly protecting upstream data sets ensuring consistency (e.g. Volume cannot evaluate less than 0, timestamps cannot exceed Current time boundaries). Unreliable inputs are logged securely without terminating the batch processing flow.

### 3. Normalizer (`DataNormalizer`)
Maps abstract, often nested `Dict` responses directly to rigid native Pydantic types evaluating exact parameters efficiently without generic properties floating down the execution stream.

### 4. Storage (`DataStorage`)
Executes asynchronous non-blocking I/O operations straight to Database targets executing TimescaleDB optimized queries effectively wrapping statements heavily resolving `ON CONFLICT DO UPDATE` schemas efficiently without manual polling iterations. Due to sandbox constraints, pure integration tests are executed securely using `AsyncMock`.
