import uuid
from typing import Optional, List, Sequence
from sqlalchemy.sql.expression import select

from models.authors_model import Author
from models.books_models import Book

from repositories._base_repository import BaseRepository

class BooksRepository(BaseRepository):

    # CREATE ###################################################################

    def create_book(self, book: Book) -> Book:
        self.db.add(book)
        self.db.flush()
        return book

    # READ #####################################################################

    def read_book(self, book_id: uuid.UUID) -> Optional[Book]:
        return self.db.get(Book, book_id)

    def read_books_by_id(self, book_id_list: List[uuid.UUID]) -> Sequence[Book]:
        stmt = select(Book).where(Book.id.in_(book_id_list))
        return self.db.scalars(stmt).all()

    def read_all_books(self) -> Sequence[Book]:
        stmt = select(Book)
        return self.db.scalars(stmt).all()

    def read_books_by_author_id(self, author_id: uuid.UUID) -> Sequence[Book]:
        stmt = select(Book).where(Book.authors.any(Author.id == author_id))
        return self.db.scalars(stmt).all()

    def is_isbn_10_unique(self, book_isbn_10: str) -> bool:
        stmt = select(Book).where(Book.isbn_10 == book_isbn_10)
        book_db = self.db.scalar(stmt)
        return (book_db == None)

    def is_isbn_13_unique(self, book_isbn_13: str) -> bool:
        stmt = select(Book).where(Book.isbn_13 == book_isbn_13)
        book_db = self.db.scalar(stmt)
        return (book_db == None)

    def is_hc_book_id_unique(self, hc_book_id: str) -> bool:
        stmt = select(Book).where(Book.hc_book_id == hc_book_id)
        book_db = self.db.scalar(stmt)
        return (book_db == None)

    # UPDATE ###################################################################



    # DELETE ###################################################################

    def delete_book(self, book: Book) -> None:
        self.db.delete(book)
        