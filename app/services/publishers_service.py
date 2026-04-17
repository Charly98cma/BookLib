import uuid
from logging import getLogger
from typing import List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.http_messages import HTTPMessages

from schemas.publishers_schema import PublisherCreate, PublisherDBFull

from repositories.publishers_repository import PublisherRepository

from models.publishers_model import Publisher

from services._base_service import BaseService

class PublisherService(BaseService):
    """
    """

    def __init__(self, session: Session):
        self.repository = PublisherRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    def create_publisher(self, data: PublisherCreate) -> PublisherDBFull:
        self.logger.debug("Processing request to create publisher '%s'...", data.name)
        # Check name uniqueness
        self._check_publisher_unique(data.name)
        # Create new ORM object
        publisher_db = Publisher(**data.__dict__)
        self.logger.debug("Adding new publisher to the database")
        self.repository.create_publisher(publisher_db)
        # Return parsed schema of new publisher entity
        return PublisherDBFull.model_validate(publisher_db)

    # READ #####################################################################

    def read_all_publishers(self) -> List[PublisherDBFull]:
        self.logger.debug("Processing request to read all publishers...")
        publisher_db_list = self.repository.read_all_publishers()
        return [PublisherDBFull.model_validate(publisher) for publisher in publisher_db_list]

    # UPDATE ###################################################################

    def update_publisher(self, publisher_id: uuid.UUID, data: PublisherCreate) -> PublisherDBFull:
        self.logger.debug("Processing request to update publisher '%s'...", publisher_id)
        publisher_db = self._read_publisher(publisher_id)
        if (data.name != publisher_db.name):
            self._check_publisher_unique(data.name)
            self.logger.debug("Publisher name changes from '%s' to '%s'", publisher_db.name, data.name)
        # Update publisher values
        self.logger.debug("Updating values of publisher '%d'", publisher_id)
        self.update_orm_object(publisher_db, data.model_dump())
        return PublisherDBFull.model_validate(publisher_db)
        
    # DELETE ###################################################################

    def delete_publisher(self, publisher_id: uuid.UUID) -> None:
        self.logger.debug("Processing request to delete publisher '%s'...", publisher_id)
        # Read ORM object
        publisher_db = self._read_publisher(publisher_id)
        self.logger.debug("Deleting publisher with ID '%s'", publisher_id)
        # Delete ORM object from database
        self.repository.delete_publisher(publisher_db)

    # AUXILIAR FUNCTIONS #######################################################

    def _read_publisher(self, publisher_id: uuid.UUID) -> Publisher:
        publisher_db = self.repository.read_publisher(publisher_id)
        # Check the publisher exists
        if (publisher_db is None):
            self.logger.error("Publisher with ID '%s' does not exists", publisher_id)
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.PUBLISHER_DOES_NOT_EXIST.format(publisher_id)
            )
        self.logger.debug("Publisher with '%s' exists")
        return publisher_db

    def _check_publisher_unique(self, publisher_name: str) -> None:
        publisher_unique = self.repository.is_publisher_unique(publisher_name)
        # Check the name is not already registered to another publisher
        if (not publisher_unique):
            self.logger.error("Publisher name '%s' already in use", publisher_name)
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.PUBLISHER_NAME_ALREADY_EXISTS.format(publisher_name)
            )
        self.logger.debug("Publisher name '%s' is unqiue", publisher_name)

