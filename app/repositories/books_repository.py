import uuid
from typing import Optional, List, Sequence
from sqlalchemy import insert
from sqlalchemy.sql.expression import select, update, delete

from models.books_models import Book
from schemas.books_schema import BookCreate, BookDBResponse

from repositories.base_repository import BaseRepository

class BooksRepository(BaseRepository):

    # CREATE ###################################################################

    async def create_book(self, book: BookCreate) -> BookDBResponse:
        stmt = (
            insert(Book)
            .values(**book.__dict__)
            .returning(Book)
        )
        book_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return BookDBResponse.model_validate(book_db)

    # READ #####################################################################

    async def read_book(self, book_id: uuid.UUID) -> Optional[BookDBResponse]:
        stmt = (
            select(Book)
            .where(Book.id == book_id)
        )
        book_db = (await self.db.execute(stmt)).scalar_one_or_none()
        if (book_db is None):
            return None
        return BookDBResponse.model_validate(book_db)
    
    async def read_all_books(self) -> List[BookDBResponse]:
        stmt = select(Book)
        book_db_list = (await self.db.execute(stmt)).scalars().all()
        return self._map_books_to_schema_list(book_db_list)

    async def is_isbn_10_unique(self, book_isbn_10: str) -> bool:
        stmt = (
            select(Book)
            .where(Book.isbn_10 == book_isbn_10)
        )
        book_db = (await self.db.execute(stmt)).scalar_one_or_none()
        return (book_db == None)

    async def is_isbn_13_unique(self, book_isbn_13: str) -> bool:
        stmt = (
            select(Book)
            .where(Book.isbn_13 == book_isbn_13)
        )
        book_db = (await self.db.execute(stmt)).scalar_one_or_none()
        return (book_db == None)

    async def is_hc_book_id_unique(self, hc_book_id: str) -> bool:
        stmt = (
            select(Book)
            .where(Book.hc_book_id == hc_book_id)
        )
        book_db = (await self.db.execute(stmt)).scalar_one_or_none()
        return (book_db == None)

    # UPDATE ###################################################################

    async def update_book(self, book_id: uuid.UUID, book: BookCreate) -> BookDBResponse:
        stmt = (
            update(Book)
            .where(Book.id == book_id)
            .values(**book.__dict__)
            .returning(Book)
        )
        book_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return BookDBResponse.model_validate(book_db)

    # DELETE ###################################################################

    async def delete_book(self, book_id: uuid.UUID) -> None:
        stmt = (
            delete(Book)
            .where(Book.id == book_id)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    ############################################################################

    @staticmethod
    def _map_books_to_schema_list(book_db_list: Sequence[Book]) -> List[BookDBResponse]:
        return [BookDBResponse.model_validate(book) for book in book_db_list]