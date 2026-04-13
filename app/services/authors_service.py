import uuid
from logging import getLogger
from typing import List, Sequence
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.http_messages import HTTPMessages

from schemas.authors_schema import AuthorCreate, AuthorUpdate, AuthorDBResponse

from repositories.books_repository import BooksRepository
from repositories.authors_repository import AuthorRepository

from models.books_models import Book
from models.authors_model import Author

from services._base_service import BaseService

class AuthorService(BaseService):
    """
    """

    def __init__(self, session: Session):
        self.authors_repository = AuthorRepository(session)
        self.books_repository = BooksRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    def create_author(self, data: AuthorCreate) -> AuthorDBResponse:
        # Check uniqueness of fields
        self._check_author_unique(data.name)
        # Create ORM object
        author_db = Author(**data.__dict__)
        # Add author to database    
        self.authors_repository.create_author(author_db)
        return AuthorDBResponse.model_validate(author_db)

    # READ #####################################################################

    def read_all_authors(self) -> List[AuthorDBResponse]:
        author_db_list = self.authors_repository.read_all_authors()
        return [AuthorDBResponse.model_validate(author) for author in author_db_list]

    # UPDATE ###################################################################

    def update_author(self, author_id: uuid.UUID, data: AuthorUpdate) -> AuthorDBResponse:
        author_db = self._read_author(author_id)
        # Update changed values if valid
        if (data.name != author_db.name):
            self._check_author_unique(data.name)
        # Parse special fields to validate format
        books = self._parse_authors(data.authored_books)
        # Clean author data of values in invalid format
        author_data = self._clean_author_values(data)
        # Update values
        self.update_orm_object(author_db, author_data)
        author_db.authored_books = list(books)
        return AuthorDBResponse.model_validate(author_db)
        
    # DELETE ###################################################################

    def delete_author(self, author_id: uuid.UUID) -> None:
        author_db = self._read_author(author_id)
        self.authors_repository.delete_author(author_db)

    # AUXILIAR FUNCTIONS #######################################################

    def _read_author(self, author_id: uuid.UUID) -> Author:
        author_db = self.authors_repository.read_author(author_id)
        # Check the author exists
        if (author_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.AUTHOR_DOES_NOT_EXIST.format(author_id)
            )
        return author_db

    def _check_author_unique(self, author_name: str) -> None:
        author_unique = self.authors_repository.is_author_unique(author_name)
        # Check the name is not already registered to another author
        if (not author_unique):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.AUTHOR_NAME_ALREADY_EXISTS.format(author_name)
            )

    @staticmethod
    def _clean_author_values(book: AuthorUpdate):
        exclude_fields = {"authored_books"}
        return book.model_dump(exclude=exclude_fields)

    # BOOK AUXILIAR FUNCTIONS ##################################################

    def _parse_authors(self, book_id_list: List[uuid.UUID]) -> Sequence[Book]:
        books = self.books_repository.read_books_by_id(book_id_list)
        if (len(books) != len(book_id_list)):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.BOOK_DOES_NOT_EXISTS
            )
        return books
