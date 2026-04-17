import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.http_messages import HTTPMessages

from schemas.books_schema import BookCreate, BookDBBasic, BookDBFull
from schemas.authors_schema import AuthorDBBasic
from schemas.genres_schema import GenreDBFull

from repositories.books_repository import BooksRepository
from repositories.authors_repository import AuthorRepository
from repositories.publishers_repository import PublisherRepository
from repositories.genres_repository import GenreRepository

from models.books_models import Book
from models.authors_model import Author
from models.publishers_model import Publisher
from models.genres_model import Genre

from services._base_service import BaseService

class BooksService(BaseService):
    """
    """

    def __init__(self, session: Session):
        self.books_repository = BooksRepository(session)
        self.authors_repository = AuthorRepository(session)
        self.publisher_repository = PublisherRepository(session)
        self.genre_repository = GenreRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    def create_book(self, data: BookCreate) -> BookDBFull:
        # Check unique values
        self._check_isbn_10_unique(data.isbn_10)
        self._check_isbn_13_unique(data.isbn_13)
        self._check_hc_book_id_unique(data.hc_book_id)
        # Clear special values for ORM
        book_data = self._clean_book_values(data)
        # Create ORM object and add all parameters
        book_db = Book(**book_data)
        # Add authors list (get Author entities from their ID)
        book_db.authors = self._read_authors_by_id(data.authors)
        if (data.publisher is not None):
            book_db.publisher = self._read_publisher_by_id(data.publisher.id)
        book_db.genres = self._read_genres_by_id(data.genres)
        # Insert object into database and return 
        self.books_repository.create_book(book_db)
        return BookDBFull.model_validate(book_db)

    # READ #####################################################################

    def read_book(self, book_id: uuid.UUID) -> BookDBFull:
        book_db = self._read_book(book_id)
        return BookDBFull.model_validate(book_db)
    
    def read_books_by_id(self, book_list: List[uuid.UUID]) -> List[BookDBBasic]:
        return [BookDBBasic.model_validate(self._read_book(book_id)) for book_id in book_list]

    def read_all_books(self) -> List[BookDBBasic]:
        book_db_list = self.books_repository.read_all_books()
        return [BookDBBasic.model_validate(book) for book in book_db_list]
    
    def read_books_by_author_id(self, author_id: uuid.UUID) -> List[BookDBBasic]:
        book_db_list = self.books_repository.read_books_by_author_id(author_id)
        return [BookDBBasic.model_validate(book) for book in book_db_list]

    # UPDATE ###################################################################

    def update_book(self, book_id: uuid.UUID, data: BookCreate) -> BookDBFull:
        book_db = self._read_book(book_id)
        # Check new values uniqueness
        if (data.isbn_10 != book_db.isbn_10):
            self._check_isbn_10_unique(data.isbn_10)
        if (data.isbn_13 != book_db.isbn_13):
            self._check_isbn_13_unique(data.isbn_13)
        if (data.hc_book_id != book_db.hc_book_id):
            self._check_hc_book_id_unique(data.hc_book_id)
        # Clear special values for ORM
        book_data = self._clean_book_values(data)
        # Update all values and return
        self.update_orm_object(book_db, book_data)
        # Update authors list
        book_db.authors = self._read_authors_by_id(data.authors)
        # Update publisher
        if (data.publisher is not None):
            book_db.publisher = self._read_publisher_by_id(data.publisher.id)
        else:
            book_db.publisher = None
        # Update genres list
        book_db.genres = self._read_genres_by_id(data.genres)
        return BookDBFull.model_validate(book_db)

    # DELETE ###################################################################

    def delete_book(self, book_id: uuid.UUID) -> None:
        # Search for Book and delete ORM object
        book = self._read_book(book_id)
        self.books_repository.delete_book(book)

    # AUXILIAR FUNCTIONS #######################################################

    def _check_isbn_10_unique(self, isbn_10: str) -> None:
        isbn_10_unique = self.books_repository.is_isbn_10_unique(isbn_10)
        if (not isbn_10_unique):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.BOOK_ISBN10_NOT_UNIQUE.format(isbn_10)
            )

    def _check_isbn_13_unique(self, isbn_13: str) -> None:
        isbn_13_unique = self.books_repository.is_isbn_13_unique(isbn_13)
        if (not isbn_13_unique):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.BOOK_ISBN13_NOT_UNIQUE.format(isbn_13)
            )

    def _check_hc_book_id_unique(self, hc_book_id: Optional[str]) -> None:
        if (hc_book_id is not None):
            hc_book_id_unique = self.books_repository.is_hc_book_id_unique(hc_book_id)
            if (not hc_book_id_unique):
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=HTTPMessages.BOOK_HC_ID_NOT_UNIQUE.format(hc_book_id)
                )

    def _read_book(self, book_id: uuid.UUID) -> Book:
        book_db = self.books_repository.read_book(book_id)
        if (book_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.BOOK_DOES_NOT_EXISTS.format(book_id)
            )
        return book_db

    @staticmethod
    def _clean_book_values(book: BookCreate):
        exclude_fields = {"authors", "publisher", "genres"}
        return book.model_dump(exclude=exclude_fields)

    # AUTHOR AUXILIAR FUNCTIONS ################################################

    def _read_authors_by_id(self, author_list: List[AuthorDBBasic]) -> List[Author]:
        author_db_list : List[Author] = []
        if (len(author_list) != 0):
            for author_id in [author.id for author in author_list]:
                author_db = self.authors_repository.read_author(author_id)
                if (author_db is None):
                    raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND,
                        detail=HTTPMessages.AUTHOR_DOES_NOT_EXIST.format(author_id)
                    )
                author_db_list.append(author_db)
        return author_db_list

    # PUBLISHER AUXILIAR FUNCTIONS #############################################

    def _read_publisher_by_id(self, publisher_id: uuid.UUID) -> Publisher:
        publisher_db = self.publisher_repository.read_publisher(publisher_id)
        if (publisher_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.PUBLISHER_DOES_NOT_EXIST.format(publisher_id)
            )
        return publisher_db

    # GENRES AUXILIAR FUNCTIONS ################################################

    def _read_genres_by_id(self, genre_list: List[GenreDBFull]) -> List[Genre]:
        genre_db_list : List[Genre] = []
        if (len(genre_list) != 0):
            for genre_id in [genre.id for genre in genre_list]:
                genre_db = self.genre_repository.read_genre(genre_id)
                if (genre_db is None):
                    raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND,
                        detail=HTTPMessages.GENRE_DOES_NOT_EXIST.format(genre_id)
                    )
                genre_db_list.append(genre_db)
        return genre_db_list
