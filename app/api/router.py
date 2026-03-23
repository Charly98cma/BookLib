from fastapi import APIRouter

from api import users_router

router = APIRouter()

router.include_router(users_router.router)