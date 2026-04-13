import uuid
from fastapi import APIRouter, Depends
from typing import List, Annotated, Optional
from http import HTTPStatus

from sqlalchemy.orm import Session

from core.db import get_db
from core.http_messages import HTTPMessages

from schemas.books_schema import BookCreate, BookDBResponse

from services.books_service import BooksService

# Books router
router = APIRouter(
    prefix="/books",
    tags=["books"]
)

# CREATE #######################################################################

@router.post(
    "",
    summary="Create new book",
    status_code=HTTPStatus.OK,
    response_model=BookDBResponse,
    response_description="Book created and returned successfully",
    responses={
        HTTPStatus.CONFLICT: {
            "description": "ISBN 10 / ISBN 13 / Hardcover ID already being used (must be unique)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.BOOK_ISBN10_NOT_UNIQUE.format("X")
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
def create_book(
    data: BookCreate,
    session: Annotated[Session, Depends(get_db)]
) -> Optional[BookDBResponse]:
    """
    Creates a new book in the database, and returns the newly created entity, if:

    * The value of `isbn_10` is not already used by another book
    * The value of `isbn_13` is not already used by another book
    * If present, the value of `hc_book_id` is not already used by another book
    """
    _service = BooksService(session)
    return _service.create_book(data)

# READ #########################################################################

@router.get(
    "/{book_id}",
    summary="Get book with the given ID",
    status_code=HTTPStatus.OK,
    response_model=BookDBResponse,
    response_description="Book with the given ID",
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Book not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.BOOK_DOES_NOT_EXISTS.format("X")
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
def read_book(
    book_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db)]
) -> BookDBResponse:
    """
    """
    _service = BooksService(session)
    return _service.read_book(book_id)

@router.get(
    "",
    summary="Get all books",
    status_code=HTTPStatus.OK,
    response_model=List[BookDBResponse],
    response_description="List with all books on the database"
)
def read_all_books(
    session: Annotated[Session, Depends(get_db)]
) -> List[BookDBResponse]:
    """
    Yields a list with all the books in the database, or an empty list if there
    are none.
    """
    _service = BooksService(session)
    return _service.read_all_books()

# UPDATE #######################################################################

@router.put(
    "/{book_id}",
    summary="Update book",
    status_code=HTTPStatus.OK,
    response_model=BookDBResponse,
    response_description="Book with updated values",
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Book not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.BOOK_DOES_NOT_EXISTS.format("X")
                    }
                }
            }
        },
        HTTPStatus.CONFLICT: {
            "description": "ISBN 10 / ISBN 13 / Hardcover ID already being used (must be unique)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.BOOK_ISBN10_NOT_UNIQUE.format("X")
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
def update_book(
    book_id: uuid.UUID,
    data: BookCreate,
    session: Annotated[Session, Depends(get_db)]
) -> Optional[BookDBResponse]:
    """
    Updates a book of the database, and returns the entity with its updated
    values if:

    * The value of `isbn_10` is not already used by another book
    * The value of `isbn_13` is not already used by another book
    * If present, the value of `hc_book_id` is not already used by another book
    """
    _service = BooksService(session)
    return _service.update_book(book_id, data)

# DELETE #######################################################################

@router.delete(
    "/{book_id}",
    summary="Delete book",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Book not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.BOOK_DOES_NOT_EXISTS.format("X")
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
def delete_book(
    book_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db)]
) -> None:
    """
    Deletes the given book
    """
    _service = BooksService(session)
    _service.delete_book(book_id)
