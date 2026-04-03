from fastapi import APIRouter

from api import (
    authors_router,
    books_router,
    genres_router,
    publishers_router,
    users_router,
)

# Master router of the API
router = APIRouter()

################################################################################

# Router of each model handled by the API

router.include_router(users_router.router)
router.include_router(books_router.router)
router.include_router(authors_router.router)
router.include_router(genres_router.router)
router.include_router(publishers_router.router)
