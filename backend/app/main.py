from typing import Any
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_db_engine, close_db_engine
from app.core.redis import create_redis_pool, close_redis_pool
from app.api.router import api_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    app.state.db_engine = await create_db_engine()
    app.state.redis_pool = await create_redis_pool()
    yield
    await close_db_engine(app.state.db_engine)
    await close_redis_pool(app.state.redis_pool)

app = FastAPI(title=settings.app_name, lifespan=lifespan)

from app.api.exceptions import APIException, api_exception_handler, generic_exception_handler
from app.api.middleware import RequestLoggingMiddleware
from starlette.middleware.cors import CORSMiddleware

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
