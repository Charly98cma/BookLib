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

    async def create_genre(self, genre: GenreCreate) -> Optional[GenreDBResponse]:
        genre_unique = await self.repository.is_genre_unique(genre.name)
        # Check the name is not already registered to another genre
        if (not genre_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.GENRE_NAME_ALREADY_EXISTS
            )
        # Create new Genre entity
        return await self.repository.create_genre(genre)

    # READ #####################################################################

    async def read_all_genres(self) -> List[GenreDBResponse]:
        return await self.repository.read_all_genres()

    # UPDATE ###################################################################

    async def update_genre(self, genre_id: uuid.UUID, genre: GenreCreate) -> GenreDBResponse:
        genre_db = await self.repository.read_genre(genre_id)
        genre_unique = await self.repository.is_genre_unique(genre.name)
        # Check the genre exists
        if (genre_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.GENRE_DOES_NOT_EXIST
            )
        # Raise exception if new name is not unique
        if ((genre_db.name != genre.name) and not genre_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.GENRE_NAME_ALREADY_EXISTS
            )
        # Update genre with new values
        return await self.repository.update_genre(genre_id, genre)
        
    # DELETE ###################################################################

    async def delete_genre(self, genre_id: uuid.UUID) -> None:
        genre_db = await self.repository.read_genre(genre_id)
        # Check the genre exists
        if (genre_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.GENRE_DOES_NOT_EXIST
            )
        # Delete the genre
        await self.repository.delete_genre(genre_id)
