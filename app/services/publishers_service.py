import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from enums.http_messages import HTTPMessages
from schemas.publishers_schema import PublisherCreate, PublisherDBResponse
from repositories.publishers_repository import PublisherRepository

class PublisherService:
    """
    """

    def __init__(self, session: AsyncSession):
        self.repository = PublisherRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    async def create_publisher(self, publisher: PublisherCreate) -> Optional[PublisherDBResponse]:
        publisher_unique = await self.repository.is_publisher_unique(publisher.name)
        # Check the name is not already registered to another publisher
        if (not publisher_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.PUBLISHER_NAME_ALREADY_EXISTS
            )
        # Create new Publisher entity
        return await self.repository.create_publisher(publisher)

    # READ #####################################################################

    async def read_all_publishers(self) -> List[PublisherDBResponse]:
        return await self.repository.read_all_publishers()

    # UPDATE ###################################################################

    async def update_publisher(self, publisher_id: uuid.UUID, publisher: PublisherCreate) -> PublisherDBResponse:
        publisher_db = await self.repository.read_publisher(publisher_id)
        publisher_unique = await self.repository.is_publisher_unique(publisher.name)
        # Check the publisher exists
        if (publisher_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.PUBLISHER_DOES_NOT_EXIST
            )
        # Raise exception if new name is not unique
        if ((publisher_db.name != publisher.name) and not publisher_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.PUBLISHER_NAME_ALREADY_EXISTS
            )
        # Update publisher with new values
        return await self.repository.update_publisher(publisher_id, publisher)
        
    # DELETE ###################################################################

    async def delete_publisher(self, publisher_id: uuid.UUID) -> None:
        publisher_db = await self.repository.read_publisher(publisher_id)
        # Check the publisher exists
        if (publisher_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.PUBLISHER_DOES_NOT_EXIST
            )
        # Delete the publisher
        await self.repository.delete_publisher(publisher_id)
