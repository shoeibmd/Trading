# Getting Started

## Prerequisites
- Docker
- Docker Compose v2 (usually included with Docker Desktop)

## Initial Setup
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Start the local development environment:
   ```bash
   ./scripts/start.sh
   ```

## Services Overview
- **Frontend:** [http://localhost:5173](http://localhost:5173) (React + Vite)
- **Backend API:** [http://localhost:8000](http://localhost:8000) (FastAPI)
- **PostgreSQL/TimescaleDB:** `localhost:5432`
- **Redis:** `localhost:6379`
- **Worker:** Celery background worker (runs automatically in background)

## Managing the Environment
- **Start Services:** `./scripts/start.sh`
- **Stop Services:** `./scripts/stop.sh`
- **View All Logs:** `./scripts/logs.sh`
- **View Specific Logs:** `./scripts/logs.sh [service_name]` (e.g. `./scripts/logs.sh backend`)
- **Reset Environment (Destructive!):** `./scripts/reset.sh`

## Troubleshooting
- If changes to Python packages or Node dependencies don't reflect, you may need to force a rebuild:
  ```bash
  docker compose build
  docker compose up -d
  ```
