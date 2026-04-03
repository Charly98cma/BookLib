import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.router import router
from db.init_db import init_tables

logging.basicConfig(
    level=(logging.DEBUG if bool(os.getenv("DEBUG")) else logging.ERROR)
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_tables()
    yield

app = FastAPI(
    title="BookLib",
    debug=(bool(os.getenv("DEBUG"))),
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

logger = logging.getLogger(__name__)

app.include_router(router)
