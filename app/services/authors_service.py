import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from enums.http_messages import HTTPMessages
from schemas.authors_schema import AuthorCreate, AuthorDBResponse
from repositories.authors_repository import AuthorRepository

class AuthorService:
    """
    """

    def __init__(self, session: AsyncSession):
        self.repository = AuthorRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    async def create_author(self, author: AuthorCreate) -> Optional[AuthorDBResponse]:
        await self._check_author_unique(author.name)
        return await self.repository.create_author(author)

    # READ #####################################################################

    async def read_all_authors(self) -> List[AuthorDBResponse]:
        return await self.repository.read_all_authors()

    # UPDATE ###################################################################

    async def update_author(self, author_id: uuid.UUID, author: AuthorCreate) -> AuthorDBResponse:
        author_db = await self._read_author(author_id)
        if (author.name != author_db.name):
            await self._check_author_unique(author.name)
        return await self.repository.update_author(author_id, author)
        
    # DELETE ###################################################################

    async def delete_author(self, author_id: uuid.UUID) -> None:
        await self._read_author(author_id)
        await self.repository.delete_author(author_id)

    # AUXILIAR FUNCTIONS #######################################################

    async def _read_author(self, author_id: uuid.UUID) -> AuthorDBResponse:
        author_db = await self.repository.read_author(author_id)
        # Check the author exists
        if (author_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.AUTHOR_DOES_NOT_EXIST
            )
        return author_db

    async def _check_author_unique(self, author_name: str) -> None:
        author_unique = await self.repository.is_author_unique(author_name)
        # Check the name is not already registered to another author
        if (not author_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.AUTHOR_NAME_ALREADY_EXISTS
            )