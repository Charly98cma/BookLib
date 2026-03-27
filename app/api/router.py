from fastapi import APIRouter

from api import users_router

# Master router of the API
router = APIRouter()

################################################################################

# Router of each model handled by the API

router.include_router(users_router.router)