import uuid
from typing import List, Annotated, Optional
from http import HTTPStatus
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from core.db import get_db
from core.http_messages import HTTPMessages

from schemas.authors_schema import AuthorCreate, AuthorUpdate, AuthorDBBasic, AuthorDBFull

from services.authors_service import AuthorService

# Author router
router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

# CREATE #######################################################################

@router.post(
    "",
    summary="Create new author",
    status_code=HTTPStatus.OK,
    response_model=AuthorDBFull,
    response_description="Author created successfully",
    responses={
        HTTPStatus.CONFLICT: {
            "description": "Author name already in use",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.AUTHOR_NAME_ALREADY_EXISTS.format("X")
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
def create_author(
    data: AuthorCreate,
    session: Annotated[Session, Depends(get_db)]
) -> Optional[AuthorDBFull]:
    """
    Create a new Author entity on the database (and returns newly created
    entity), if:

    * The `name` is unique (no other Author entity already registered with it)
    """
    _service = AuthorService(session)
    return _service.create_author(data)

# READ #########################################################################

@router.get(
    "",
    summary="Get all authors",
    status_code=HTTPStatus.OK,
    response_model=List[AuthorDBBasic],
    response_description="List with all authors in the database",
)
def read_all_authors(
    session: Annotated[Session, Depends(get_db)]
) -> List[AuthorDBBasic]:
    """
    Return the list of Author entities registered on the database, or an empty
    list if there are none.
    """
    _service = AuthorService(session)
    return _service.read_all_authors()

# UPDATE #######################################################################

@router.put(
    "/{author_id}",
    summary="Update author",
    status_code=HTTPStatus.OK,
    response_model=AuthorDBFull,
    response_description="Author updated successfully",
    responses={
        HTTPStatus.CONFLICT: {
            "description": "Author name already in use",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.AUTHOR_NAME_ALREADY_EXISTS.format("X")
                    }
                }
            }
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Author/Book not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.AUTHOR_DOES_NOT_EXIST.format("X")
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
def update_author(
    author_id: uuid.UUID,
    data: AuthorUpdate,
    session: Annotated[Session, Depends(get_db)]
) -> Optional[AuthorDBFull]:
    """
    Update the given Author entity with the new provided values, if:

    * The `name` is unique (no other author already registered with it)
    """
    _service = AuthorService(session)
    return _service.update_author(author_id, data)    

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
                        "detail": HTTPMessages.AUTHOR_DOES_NOT_EXIST.format("X")
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
def delete_author(
    author_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db)]
) -> None:
    """
    Delete the given Author.
    """
    _service = AuthorService(session)
    _service.delete_author(author_id)    
