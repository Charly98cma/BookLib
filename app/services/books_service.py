import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from enums.http_messages import HTTPMessages
from schemas.books_schema import BookCreate, BookDBResponse
from repositories.books_repository import BooksRepository

class BooksService:
    """
    """

    def __init__(self, session: AsyncSession):
        self.repository = BooksRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    async def create_book(self, book: BookCreate) -> BookDBResponse:
        await self._check_isbn_10_unique(book.isbn_10)
        await self._check_isbn_13_unique(book.isbn_13)
        await self._check_hc_book_id_unique(book.hc_book_id)
        return await self.repository.create_book(book)

    # READ #####################################################################

    async def read_all_books(self) -> List[BookDBResponse]:
        return await self.repository.read_all_books()

    # UPDATE ###################################################################

    async def update_book(self, book_id: uuid.UUID, book: BookCreate) -> BookDBResponse:
        book_db = await self._read_book(book_id)
        if (book.isbn_10 != book_db.isbn_10):
            await self._check_isbn_10_unique(book.isbn_10)
        if (book.isbn_13 != book_db.isbn_13):
            await self._check_isbn_13_unique(book.isbn_13)
        if (book.hc_book_id != book_db.hc_book_id):
            await self._check_hc_book_id_unique(book.hc_book_id)
        return await self.repository.update_book(book_id, book)

    # DELETE ###################################################################

    async def delete_book(self, book_id: uuid.UUID) -> None:
        await self._read_book(book_id)
        await self.repository.delete_book(book_id)

    # AUXILIAR FUNCTIONS #######################################################

    async def _check_isbn_10_unique(self, isbn_10: str) -> None:
        isbn_10_unique = await self.repository.is_isbn_10_unique(isbn_10)
        if (not isbn_10_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.BOOK_ISBN10_NOT_UNIQUE
            )

    async def _check_isbn_13_unique(self, isbn_13: str) -> None:
        isbn_13_unique = await self.repository.is_isbn_13_unique(isbn_13)
        if (not isbn_13_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.BOOK_ISBN13_NOT_UNIQUE
            )

    async def _check_hc_book_id_unique(self, hc_book_id: Optional[str]) -> None:
        if (hc_book_id is not None):
            hc_book_id_unique = await self.repository.is_hc_book_id_unique(hc_book_id)
            if (not hc_book_id_unique):
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=HTTPMessages.BOOK_HC_ID_NOT_UNIQUE
                )
            
    async def _read_book(self, book_id: uuid.UUID) -> BookDBResponse:
        book_db = await self.repository.read_book(book_id)
        if (book_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.BOOK_DOES_NOT_EXISTS
            )
        return book_db
