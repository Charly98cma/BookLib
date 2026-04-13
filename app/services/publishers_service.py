import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.http_messages import HTTPMessages

from schemas.publishers_schema import PublisherCreate, PublisherDBResponse

from repositories.publishers_repository import PublisherRepository

from models.publishers_model import Publisher

class PublisherService:
    """
    """

    def __init__(self, session: Session):
        self.repository = PublisherRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    def create_publisher(self, data: PublisherCreate) -> PublisherDBResponse:
        self._check_publisher_unique(data.name)
        publisher_db = Publisher(**data.__dict__)
        self.repository.create_publisher(publisher_db)
        return PublisherDBResponse.model_validate(publisher_db)

    # READ #####################################################################

    def read_all_publishers(self) -> List[PublisherDBResponse]:
        publisher_db_list = self.repository.read_all_publishers()
        return [PublisherDBResponse.model_validate(publisher) for publisher in publisher_db_list]

    # UPDATE ###################################################################

    def update_publisher(self, publisher_id: uuid.UUID, publisher: PublisherCreate) -> PublisherDBResponse:
        publisher_db = self._read_publisher(publisher_id)
        if (publisher.name != publisher_db.name):
            self._check_publisher_unique(publisher.name)
            publisher_db.name = publisher.name
        return PublisherDBResponse.model_validate(publisher_db)
        
    # DELETE ###################################################################

    def delete_publisher(self, publisher_id: uuid.UUID) -> None:
        publisher_db = self._read_publisher(publisher_id)
        self.repository.delete_publisher(publisher_db)

    # AUXILIAR FUNCTIONS #######################################################

    def _read_publisher(self, publisher_id: uuid.UUID) -> Publisher:
        publisher_db = self.repository.read_publisher(publisher_id)
        # Check the publisher exists
        if (publisher_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.PUBLISHER_DOES_NOT_EXIST.format(publisher_id)
            )
        return publisher_db

    def _check_publisher_unique(self, publisher_name: str) -> None:
        publisher_unique = self.repository.is_publisher_unique(publisher_name)
        # Check the name is not already registered to another publisher
        if (not publisher_unique):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.PUBLISHER_NAME_ALREADY_EXISTS.format(publisher_name)
            )