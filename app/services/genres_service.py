import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from enums.http_messages import HTTPMessages
from schemas.genres_schema import GenreCreate, GenreDBResponse
from repositories.genres_repository import GenreRepository

class GenreService:
    """
    """

    def __init__(self, session: AsyncSession):
        self.repository = GenreRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    async def create_genre(self, genre: GenreCreate) -> GenreDBResponse:
        await self._check_genre_name_unique(genre.name)
        return await self.repository.create_genre(genre)

    # READ #####################################################################

    async def read_all_genres(self) -> List[GenreDBResponse]:
        return await self.repository.read_all_genres()

    # UPDATE ###################################################################

    async def update_genre(self, genre_id: uuid.UUID, genre: GenreCreate) -> GenreDBResponse:
        genre_db = await self._read_genre(genre_id)
        if (genre.name != genre_db.name):
            await self._check_genre_name_unique(genre.name)
        return await self.repository.update_genre(genre_id, genre)
        
    # DELETE ###################################################################

    async def delete_genre(self, genre_id: uuid.UUID) -> None:
        await self._read_genre(genre_id)
        await self.repository.delete_genre(genre_id)

    ############################################################################

    async def _check_genre_name_unique(self, name: str) -> None:
        genre_unique = await self.repository.is_genre_unique(name)
        # Check the name is not already registered to another genre
        if (not genre_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.GENRE_NAME_ALREADY_EXISTS
            )
        
    async def _read_genre(self, genre_id: uuid.UUID) -> GenreDBResponse:
        genre_db = await self.repository.read_genre(genre_id)
        if (genre_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.GENRE_DOES_NOT_EXIST
            )
        return genre_db