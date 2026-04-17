import uuid
from logging import getLogger
from typing import List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.http_messages import HTTPMessages

from schemas.authors_schema import AuthorCreate, AuthorUpdate, AuthorDBBasic, AuthorDBFull

from repositories.books_repository import BooksRepository
from repositories.authors_repository import AuthorRepository

from models.books_models import Book
from models.authors_model import Author

from services._base_service import BaseService

class AuthorService(BaseService):

    def __init__(self, session: Session):
        self.authors_repository = AuthorRepository(session)
        self.books_repository = BooksRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    def create_author(self, data: AuthorCreate) -> AuthorDBFull:
        self.logger.debug("Processing request to create author '%s'...", data.name)
        # Check name uniqueness
        self._check_author_unique(data.name)
        # Create ORM object
        author_db = Author(**data.__dict__)
        # Add author to database
        self.logger.debug("Adding new author to tbe database")
        self.authors_repository.create_author(author_db)
        # Return parsed schema of new author entity
        return AuthorDBFull.model_validate(author_db)

    # READ #####################################################################

    def read_all_authors(self) -> List[AuthorDBBasic]:
        self.logger.debug("Processing request to read all authors...")
        author_db_list = self.authors_repository.read_all_authors()
        return [AuthorDBBasic.model_validate(author) for author in author_db_list]
    
    # UPDATE ###################################################################

    def update_author(self, author_id: uuid.UUID, data: AuthorUpdate) -> AuthorDBFull:
        self.logger.debug("Processing request to update author '%s'...", author_id)
        # Read ORM object
        author_db = self._read_author(author_id)
        # Check if values have changed
        if (data.name != author_db.name):
            self._check_author_unique(data.name)
            self.logger.debug("Author name changes from '%s' to '%s'", author_db.name, data.name)
        # Parse special fields to validate format
        books = self._parse_book_id_list(data.authored_books)
        # Clean author data of values in invalid format
        author_data = self._clean_author_values(data)
        # Update author values
        self.logger.debug("Updating values of author '%d'", author_id)
        self.update_orm_object(author_db, author_data)
        author_db.authored_books = books
        return AuthorDBFull.model_validate(author_db)
        
    # DELETE ###################################################################

    def delete_author(self, author_id: uuid.UUID) -> None:
        self.logger.debug("Processing request to delete author '%s'...", author_id)
        # Read ORM object
        author_db = self._read_author(author_id)
        self.logger.debug("Deleting author with ID '%s'", author_id)
        # Delete ORM object from database
        self.authors_repository.delete_author(author_db)

    # AUXILIAR FUNCTIONS #######################################################

    def _read_author(self, author_id: uuid.UUID) -> Author:
        author_db = self.authors_repository.read_author(author_id)
        # Check the author exists
        if (author_db is None):
            self.logger.error("Author with ID '%s' does not exists", author_id)
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.AUTHOR_DOES_NOT_EXIST.format(author_id)
            )
        self.logger.debug("Author with ID '%s' exists", author_id)
        return author_db 

    def _check_author_unique(self, author_name: str) -> None:
        author_unique = self.authors_repository.is_author_unique(author_name)
        # Check the name is not already registered to another author
        if (not author_unique):
            self.logger.error("Author name '%s' is already in use", author_name)
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.AUTHOR_NAME_ALREADY_EXISTS.format(author_name)
            )
        self.logger.debug("Author name '%s' is unique", author_name)

    def _clean_author_values(self, author: AuthorUpdate):
        exclude_fields = {"authored_books"}
        self.logger.debug("Cleaning author of fields '%s'", exclude_fields)
        return author.model_dump(exclude=exclude_fields)

    # BOOK AUXILIAR FUNCTIONS ##################################################

    def _parse_book_id_list(self, book_id_list: List[uuid.UUID]) -> List[Book]:
        book_db_list : List[Book] = []
        if (len(book_id_list) != 0):
            for book_id in book_id_list:
                book_db = self.books_repository.read_book(book_id)
                if (book_db is None):
                    self.logger.error("Book with ID '%s' not found", book_id)
                    raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND,
                        detail=HTTPMessages.BOOK_DOES_NOT_EXISTS.format(book_id)
                    )
                self.logger.debug("Adding book '%s' to authored_books", book_id)
                book_db_list.append(book_db)
        return book_db_list
