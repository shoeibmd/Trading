from fastapi import APIRouter

from app.api.endpoints import health, instruments, portfolios, fundamentals, workspaces

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(instruments.router, prefix="/instruments", tags=["instruments"])
api_router.include_router(portfolios.router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(fundamentals.router, prefix="/fundamentals", tags=["fundamentals"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(watchlists.router, prefix="/watchlists", tags=["watchlists"])
api_router.include_router(markets.router, prefix="/markets", tags=["markets"])
api_router.include_router(ohlcv.router, prefix="/ohlcv", tags=["ohlcv"])
api_router.include_router(indicators.router, prefix="/indicators", tags=["indicators"])
