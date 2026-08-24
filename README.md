# Financial Terminal

An open-source Bloomberg-style financial terminal built with modern web technologies.

## Target Stack
- **Frontend:** React + TypeScript + Tailwind + shadcn/ui + Vite
- **Charts:** TradingView Lightweight Charts
- **State:** Zustand
- **Layouts:** React Grid Layout
- **Backend:** Python + FastAPI + WebSockets
- **Jobs:** Celery/RQ
- **Database:** PostgreSQL + TimescaleDB
- **Cache/realtime:** Redis
- **AI:** Provider abstraction (OpenAI, local LLMs/Ollama, RAG)
- **Deployment:** Docker / Docker Compose / Nginx

## Quick Start
```bash
# 1. Setup environment
cp .env.example .env

# 2. Start services
./scripts/start.sh

# 3. View the application
# Frontend will be at http://localhost:5173
# Backend API will be at http://localhost:8000
```

See [docs/development/getting_started.md](docs/development/getting_started.md) for full development setup instructions.
