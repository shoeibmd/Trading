# Phase 1 - Architecture Conventions

## Backend / Frontend Boundary Rules
- The backend operates exclusively as a REST/WebSocket API provider. No server-side HTML rendering (e.g., Jinja).
- The frontend acts as an independent Single Page Application (SPA).
- Both systems run independently and communicate strictly over well-defined APIs.

## Environment Variable Naming Conventions
- Backend environment variables must be prefixed with `APP_` when read by pydantic-settings in the config file. (e.g. `APP_POSTGRES_DSN`)
- Frontend environment variables exposed to Vite must be prefixed with `VITE_`.
- Sensitive secrets must never be committed to source control and are loaded via `.env` files.

## Logging Format
- Structured JSON logging will be used to ensure seamless ingestion by observability tools.
- A standard Python logger using a custom `JSONFormatter` enforces this behavior. Format includes `level`, `message`, `name`, and `timestamp`.

## API Response Structure Convention
- All API endpoints should return standardized JSON responses using the following envelope structure:
  ```json
  {
    "data": { ... }, // Payload for success responses
    "error": null, // Or an error object detailing issues
    "meta": { ... } // Optional metadata like pagination
  }
  ```

## Testing Conventions
- **Backend:** `pytest` will be the primary testing framework. Tests should reside in a `tests/` directory at the root of the backend folder.
- **Frontend:** `vitest` (or `jest`) combined with React Testing Library will be used for component and logic testing, colocated with components or in a `tests/` folder.
