# Provider Abstraction Architecture

## Overview
The Market Data Provider abstraction isolates the core financial terminal domain from vendor-specific logic.

## Interface Contracts
All market data integrations must inherit from the `MarketDataProvider` abstract base class located in `backend/app/providers/base.py`. This ensures:
1. **Normalized Data returned:** (E.g., `NormalizedInstrument`, `NormalizedQuote`).
2. **Unified Error handling:** (Raising subclasses of `ProviderError`).
3. **Async Evaluation:** Native `asyncio` for non-blocking I/O.
4. **Strong Typing:** Leveraging Pydantic validations heavily.

## Mock Provider
A native `MockProvider` exists returning synthetic deterministic data to streamline local UI/UX testing independent of rate-limits and network faults.

## Adding a New Provider
1. Inherit from `MarketDataProvider`.
2. Map vendor specific endpoints via generic config classes (`RESTProviderConfig`, `WebSocketProviderConfig`).
3. Map vendor data fields accurately matching Pydantic typing bounds (especially transforming float fields to standard `Decimal`).
4. Register the provider with the system via `ProviderRegistry`.
