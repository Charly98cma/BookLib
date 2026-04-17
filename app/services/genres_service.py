import uuid
from logging import getLogger
from typing import List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.http_messages import HTTPMessages

from schemas.genres_schema import GenreCreate, GenreDBFull

from repositories.genres_repository import GenreRepository

from models.genres_model import Genre

from services._base_service import BaseService

class GenreService(BaseService):

    def __init__(self, session: Session):
        self.repository = GenreRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    def create_genre(self, data: GenreCreate) -> GenreDBFull:
        self.logger.debug("Processing request to create genre '%s'...", data.name)
        # Check name uniqueness
        self._check_genre_name_unique(data.name)
        # Create new ORM object
        genre = Genre(**data.__dict__)
        self.repository.create_genre(genre)
        self.logger.debug("Adding new genre to the database")
        # Return parsed schema of new genre entity
        return GenreDBFull.model_validate(genre)

    # READ #####################################################################

    def read_all_genres(self) -> List[GenreDBFull]:
        self.logger.debug("Processing request to read all genres...")
        genre_db_list = self.repository.read_all_genres()
        return [GenreDBFull.model_validate(genre) for genre in genre_db_list]

    # UPDATE ###################################################################

    def update_genre(self, genre_id: uuid.UUID, data: GenreCreate) -> GenreDBFull:
        self.logger.debug("Processing request to update genre '%s'...", genre_id)
        # Read ORM object
        genre_db = self._read_genre(genre_id)
        # Check if values have changed
        if (data.name != genre_db.name):
            self._check_genre_name_unique(data.name)
            self.logger.debug("Genre name changes from '%s' to '%s'", genre_db.name, data.name)
        # Update genre values
        self.logger.debug("Updating values of genre '%d'", genre_id)
        self.update_orm_object(genre_db, data.model_dump())
        return GenreDBFull.model_validate(genre_db)
        
    # DELETE ###################################################################

    def delete_genre(self, genre_id: uuid.UUID) -> None:
        self.logger.debug("Processing request to delete genre '%s'...", genre_id)
        # Read ORM object
        genre_db = self._read_genre(genre_id)
        self.logger.debug("Deleting genre with ID '%s'", genre_id)
        # Delete ORM object from database
        self.repository.delete_genre(genre_db)

    ############################################################################

    def _read_genre(self, genre_id: uuid.UUID) -> Genre:
        genre_db = self.repository.read_genre(genre_id)
        # Check the genre exists
        if (genre_db is None):
            self.logger.error("Genre with ID '%s' does not exists", genre_id)
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.GENRE_DOES_NOT_EXIST.format(genre_id)
            )
        self.logger.debug("Genre with '%s' exists")
        return genre_db

    def _check_genre_name_unique(self, genre_name: str) -> None:
        genre_unique = self.repository.is_genre_unique(genre_name)
        # Check the name is not already registered to another genre
        if (not genre_unique):
            self.logger.error("Genre name '%s' already in use", genre_name)
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.GENRE_NAME_ALREADY_EXISTS.format(genre_name)
            )
        self.logger.debug("Genre name '%s' is unqiue", genre_name)
