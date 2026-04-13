import uuid
from logging import getLogger
from typing import List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.http_messages import HTTPMessages

from schemas.genres_schema import GenreCreate, GenreDBResponse

from repositories.genres_repository import GenreRepository

from models.genres_model import Genre

class GenreService:
    """
    """

    def __init__(self, session: Session):
        self.repository = GenreRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    def create_genre(self, data: GenreCreate) -> GenreDBResponse:
        self._check_genre_name_unique(data.name)
        genre = Genre(**data.__dict__)
        self.repository.create_genre(genre)
        return GenreDBResponse.model_validate(genre)

    # READ #####################################################################

    def read_all_genres(self) -> List[GenreDBResponse]:
        genre_db_list = self.repository.read_all_genres()
        return [GenreDBResponse.model_validate(genre) for genre in genre_db_list]

    # UPDATE ###################################################################

    def update_genre(self, genre_id: uuid.UUID, genre: GenreCreate) -> GenreDBResponse:
        genre_db = self._read_genre(genre_id)
        if (genre.name != genre_db.name):
            self._check_genre_name_unique(genre.name)
            genre_db.name = genre.name
        return GenreDBResponse.model_validate(genre_db)
        
    # DELETE ###################################################################

    def delete_genre(self, genre_id: uuid.UUID) -> None:
        genre_db = self._read_genre(genre_id)
        self.repository.delete_genre(genre_db)

    ############################################################################

    def _check_genre_name_unique(self, genre_name: str) -> None:
        genre_unique = self.repository.is_genre_unique(genre_name)
        # Check the name is not already registered to another genre
        if (not genre_unique):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.GENRE_NAME_ALREADY_EXISTS.format(genre_name)
            )
        
    def _read_genre(self, genre_id: uuid.UUID) -> Genre:
        genre_db = self.repository.read_genre(genre_id)
        if (genre_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.GENRE_DOES_NOT_EXIST.format(genre_id)
            )
        return genre_db