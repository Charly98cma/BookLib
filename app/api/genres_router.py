import uuid
from fastapi import APIRouter, Depends
from typing import List, Annotated, Optional
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from enums.http_messages import HTTPMessages
from schemas.genres_schema import GenreCreate, GenreDBResponse
from services.genres_service import GenreService

# Genre router
router = APIRouter(
    prefix="/genres",
    tags=["genres"]
)

# CREATE #######################################################################

@router.post(
    "",
    summary="Create genre",
    status_code=HTTPStatus.OK,
    response_model=GenreDBResponse,
    response_description="Genre created successfully",
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Invalid format",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.GENRE_NAME_ALREADY_EXISTS
                    }
                }
            }
        }
    }
)
async def create_genre(
    data: GenreCreate,
    session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[GenreDBResponse]:
    """
    Inserts a new genre and returns the created database entity, if:

    * The *name* is unique (no other genre already registered with it)
    """
    _service = GenreService(session)
    return await _service.create_genre(data)

# READ #########################################################################

@router.get(
    "",
    summary="Get all genres",
    status_code=HTTPStatus.OK,
    response_model=List[GenreDBResponse],
    response_description="List with all genres in the database",
)
async def read_all_genres(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> List[GenreDBResponse]:
    """
    Returns a list with all genres in the database,
    or an empty list if there are none.
    """
    _service = GenreService(session)
    return await _service.read_all_genres()

# UPDATE #######################################################################

@router.put(
    "/{genre_id}",
    summary="Update genre",
    status_code=HTTPStatus.OK,
    response_model=GenreDBResponse,
    response_description="Genre updated successfully",
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Genre name already used",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.GENRE_NAME_ALREADY_EXISTS
                    }
                }
            }
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Genre not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.GENRE_DOES_NOT_EXIST
                    }
                }
            }
        }
    }
)
async def update_genre(
    genre_id: uuid.UUID,
    data: GenreCreate,
    session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[GenreDBResponse]:
    """
    Update the genre information with the new values if:

    * The *name* is unique (no other genre already registered with it)
    """    
    _service = GenreService(session)
    return await _service.update_genre(genre_id, data)    

# DELETE #######################################################################

@router.delete(
    "/{genre_id}",
    summary="Delete genre",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Genre not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.GENRE_DOES_NOT_EXIST
                    }
                }
            }
        }
    }
)
async def delete_genre(
    genre_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    _service = GenreService(session)
    await _service.delete_genre(genre_id)    
