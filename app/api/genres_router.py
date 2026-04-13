import uuid
from fastapi import APIRouter, Depends
from typing import List, Annotated, Optional
from http import HTTPStatus

from sqlalchemy.orm import Session

from core.db import get_db
from core.http_messages import HTTPMessages

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
    summary="Create new genre",
    status_code=HTTPStatus.OK,
    response_model=GenreDBResponse,
    response_description="Genre created successfully",
    responses={
        HTTPStatus.CONFLICT: {
            "description": "Genre name already in use",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.GENRE_NAME_ALREADY_EXISTS.format("X")
                    }
                }
            }
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Invalid fields",
            "content": {
                "text/plain": {
                    "example": HTTPMessages.VALIDATION_ERROR
                }
            }
        }
    }
)
def create_genre(
    data: GenreCreate,
    session: Annotated[Session, Depends(get_db)]
) -> Optional[GenreDBResponse]:
    """
    Create a new Genre entity on the database (and returns newly created
    entity), if:

    * The `name` is unique (no other Genre already registered with it)
    """
    _service = GenreService(session)
    return _service.create_genre(data)

# READ #########################################################################

@router.get(
    "",
    summary="Get all genres",
    status_code=HTTPStatus.OK,
    response_model=List[GenreDBResponse],
    response_description="List with all genres in the database",
)
def read_all_genres(
    session: Annotated[Session, Depends(get_db)]
) -> List[GenreDBResponse]:
    """
    Return the list of Genre entities registered on the database, or an empty
    list if there are none.
    """
    _service = GenreService(session)
    return _service.read_all_genres()

# UPDATE #######################################################################

@router.put(
    "/{genre_id}",
    summary="Update genre",
    status_code=HTTPStatus.OK,
    response_model=GenreDBResponse,
    response_description="Genre updated successfully",
    responses={
        HTTPStatus.CONFLICT: {
            "description": "Genre name already used",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.GENRE_NAME_ALREADY_EXISTS.format("X")
                    }
                }
            }
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Genre not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.GENRE_DOES_NOT_EXIST.format("X")
                    }
                }
            }
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Invalid fields",
            "content": {
                "text/plain": {
                    "example": HTTPMessages.VALIDATION_ERROR
                }
            }
        }
    }
)
def update_genre(
    genre_id: uuid.UUID,
    data: GenreCreate,
    session: Annotated[Session, Depends(get_db)]
) -> Optional[GenreDBResponse]:
    """
    Update the given Author entity with the new provided values, if:

    * The `name` is unique (no other Genre already registered with it)
    """    
    _service = GenreService(session)
    return _service.update_genre(genre_id, data)    

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
                        "detail": HTTPMessages.GENRE_DOES_NOT_EXIST.format("X")
                    }
                }
            }
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Invalid fields",
            "content": {
                "text/plain": {
                    "example": HTTPMessages.VALIDATION_ERROR
                }
            }
        }
    }
)
def delete_genre(
    genre_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db)]
) -> None:
    """
    Delete the given Genre.
    """
    _service = GenreService(session)
    _service.delete_genre(genre_id)    
