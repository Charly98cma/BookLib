import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from http import HTTPStatus

from core.db import init_tables
from core.config import settings

from api.router import router

# Logging ######################################################################

logging.basicConfig(
    level=(logging.DEBUG if settings.DEBUG else logging.ERROR)
)

logger = logging.getLogger(__name__)

# FastAPI ######################################################################

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create all tables (no effect if they already exists)
    init_tables()
    yield

# Create API instance
app = FastAPI(
    title="BookLib",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Add basic middleware security measures
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include all defined routers
app.include_router(router)

# Custom exception handler for ValidationError exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=message
    )
