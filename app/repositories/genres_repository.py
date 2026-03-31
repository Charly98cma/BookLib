import uuid
from typing import Optional, List, Sequence
from sqlalchemy import insert
from sqlalchemy.sql.expression import select, update, delete

from models.genres_model import Genre
from schemas.genres_schema import GenreCreate, GenreDBResponse

from repositories.base_repository import BaseRepository

class GenreRepository(BaseRepository):

    # CREATE ###################################################################

    async def create_genre(self, genre: GenreCreate) -> GenreDBResponse:
        stmt = (
            insert(Genre)
            .values(**genre.__dict__)
            .returning(Genre)
        )
        self.logger.debug("create_genre() - stmt = ", stmt)
        genre_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return GenreDBResponse.model_validate(genre_db)

    # READ #####################################################################

    async def read_genre(self, genre_id: uuid.UUID) -> Optional[GenreDBResponse]:
        stmt = (
            select(Genre)
            .where(Genre.id == genre_id)
        )
        self.logger.debug("read_genre() - stmt = ", stmt)
        genre_db = (await self.db.execute(stmt)).scalar_one_or_none()
        if (genre_db is None):
            return None
        return GenreDBResponse.model_validate(genre_db)

    async def read_all_genres(self) -> List[GenreDBResponse]:
        stmt = select(Genre)
        self.logger.debug("read_all_genres() - stmt = ", stmt)
        genre_db_list = (await self.db.execute(stmt)).scalars().all()
        return self._map_genres_to_schema_list(genre_db_list)

    # UPDATE ###################################################################

    async def update_genre(self, genre_id: uuid.UUID, genre: GenreCreate) -> GenreDBResponse:
        stmt = (
            update(Genre)
            .where(Genre.id == genre_id)
            .values(**genre.__dict__)
            .returning(Genre)
        )
        self.logger.debug("update_genre() - stmt = ", stmt)
        genre_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return GenreDBResponse.model_validate(genre_db)

    # DELETE ###################################################################

    async def delete_genre(self, genre_id: uuid.UUID) -> None:
        stmt = (
            delete(Genre)
            .where(Genre.id == genre_id)
        )
        self.logger.debug("delete_genre() - stmt = ", stmt)
        await self.db.execute(stmt)
        await self.db.commit()

    ############################################################################

    async def is_genre_unique(self, _genre_name: str) -> bool:
        stmt = (
            select(Genre)
            .where(Genre.name == _genre_name)
            .limit(1)
        )
        self.logger.debug("is_genre_unique() - stmt = ", stmt)
        result = (await self.db.execute(stmt)).scalar_one_or_none()
        return (result is None)

    @staticmethod
    def _map_genres_to_schema_list(genre_db_list: Sequence[Genre]) -> List[GenreDBResponse]:
        return [GenreDBResponse.model_validate(genre) for genre in genre_db_list]