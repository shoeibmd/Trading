from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)

class APIException(Exception):
    def __init__(self, code: str, message: str, status_code: int, details: Optional[dict] = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

async def api_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=getattr(exc, "status_code", 500),
        content={
            "data": None,
            "error": getattr(exc, "message", str(exc)),
            "meta": {"code": getattr(exc, "code", "UNKNOWN_ERROR"), "details": getattr(exc, "details", None)}
        }
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "data": None,
            "error": "Internal server error",
            "meta": {"code": "INTERNAL_ERROR"}
        }
    )
