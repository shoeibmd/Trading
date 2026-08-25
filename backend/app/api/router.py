from fastapi import APIRouter
from .websocket import router as websocket_router
from .endpoints.health import router as health_router
from .endpoints.instruments import router as instruments_router
from .endpoints.quotes import router as quotes_router
from .endpoints.ohlcv import router as ohlcv_router
from .endpoints.markets import router as markets_router
from .endpoints.watchlists import router as watchlists_router
from .endpoints.news import router as news_router
from .endpoints.fundamentals import router as fundamentals_router
from .endpoints.portfolios import router as portfolios_router
from .endpoints.workspaces import router as workspaces_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(instruments_router, tags=["Instruments"])
api_router.include_router(quotes_router, tags=["Quotes"])
api_router.include_router(ohlcv_router, tags=["OHLCV"])
api_router.include_router(markets_router, tags=["Markets"])
api_router.include_router(watchlists_router, tags=["Watchlists"])
api_router.include_router(news_router, tags=["News"])
api_router.include_router(fundamentals_router, tags=["Fundamentals"])
api_router.include_router(portfolios_router, tags=["Portfolios"])
api_router.include_router(workspaces_router, tags=["Workspaces"])
api_router.include_router(websocket_router, tags=["WebSocket"])
