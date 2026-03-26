import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.router import router
from db.init_db import init_tables

logging.basicConfig(level=logging.ERROR)

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_tables()
    yield

app = FastAPI(
    title="BookLib",
    debug=(os.getenv("DEBUG")=="True"),
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
