import logging
import uuid
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from core import setup_logging, request_id_var
from config import get_settings
from api.health import router as health_router
from starlette.middleware.base import BaseHTTPMiddleware



logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load settings on startup
    settings = get_settings()
    setup_logging(environment=settings.environment, debug=settings.debug)
    logger.info(f"Starting {settings.app_name} version {settings.app_version} in {settings.environment} environment")
    yield
    # Perform any necessary cleanup on shutdown
    logger.info("Shutting down application")

settings = get_settings()
app = FastAPI(lifespan=lifespan, title=settings.app_name, version=settings.app_version)

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_var.set(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestIDMiddleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "request_id": request_id_var.get(),
            "error": str(exc)
        }
    )

app.include_router(health_router, prefix="/api/v1")
