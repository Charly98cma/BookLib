import uuid
from fastapi import APIRouter, Depends
from typing import List, Annotated, Optional
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from enums.http_messages import HTTPMessages
from schemas.authors_schema import AuthorCreate, AuthorDBResponse
from services.authors_service import AuthorService

# Author router
router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

# CREATE #######################################################################

@router.post(
    "",
    summary="Create author",
    status_code=HTTPStatus.OK,
    response_model=AuthorDBResponse,
    response_description="Author created successfully",
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Invalid format",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.AUTHOR_NAME_ALREADY_EXISTS
                    }
                }
            }
        }
    }
)
async def create_author(
    data: AuthorCreate,
    session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[AuthorDBResponse]:
    """
    Inserts a new author and returns the created database entity, if:

    * The *name* is unique (no other author already registered with it)
    """
    _service = AuthorService(session)
    return await _service.create_author(data)

# READ #########################################################################

@router.get(
    "",
    summary="Get all authors",
    status_code=HTTPStatus.OK,
    response_model=List[AuthorDBResponse],
    response_description="List with all authors in the database",
)
async def read_all_authors(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> List[AuthorDBResponse]:
    """
    Returns a list with all authors in the database, or an empty list if there
    are none.
    """
    _service=AuthorService(session)
    return await _service.read_all_authors()

# UPDATE #######################################################################

@router.put(
    "/{author_id}",
    summary="Update author",
    status_code=HTTPStatus.OK,
    response_model=AuthorDBResponse,
    response_description="Author updated successfully",
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Invalid format",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.AUTHOR_NAME_ALREADY_EXISTS
                    }
                }
            }
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Author not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.AUTHOR_DOES_NOT_EXIST
                    }
                }
            }
        }
    }
)
async def update_author(
    author_id: uuid.UUID,
    data: AuthorCreate,
    session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[AuthorDBResponse]:
    """
    Update the author information with the new values if:

    * The *name* is unique (no other author already registered with it)
    """
    _service=AuthorService(session)
    return await _service.update_author(author_id, data)    

# DELETE #######################################################################

@router.delete(
    "/{author_id}",
    summary="Delete author",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Author not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.AUTHOR_DOES_NOT_EXIST
                    }
                }
            }
        }
    }
)
async def delete_author(
    author_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    """
    Delete the given author
    """
    _service=AuthorService(session)
    await _service.delete_author(author_id)    
