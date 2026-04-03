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
        await self._check_publisher_unique(publisher.name)
        return await self.repository.create_publisher(publisher)

    # READ #####################################################################

    async def read_all_publishers(self) -> List[PublisherDBResponse]:
        return await self.repository.read_all_publishers()

    # UPDATE ###################################################################

    async def update_publisher(self, publisher_id: uuid.UUID, publisher: PublisherCreate) -> PublisherDBResponse:
        publisher_db = await self._read_publisher(publisher_id)
        if (publisher.name != publisher_db.name):
            await self._check_publisher_unique(publisher.name)
        return await self.repository.update_publisher(publisher_id, publisher)
        
    # DELETE ###################################################################

    async def delete_publisher(self, publisher_id: uuid.UUID) -> None:
        await self._read_publisher(publisher_id)
        await self.repository.delete_publisher(publisher_id)

    # AUXILIAR FUNCTIONS #######################################################

    async def _read_publisher(self, publisher_id: uuid.UUID) -> PublisherDBResponse:
        publisher_db = await self.repository.read_publisher(publisher_id)
        # Check the publisher exists
        if (publisher_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.PUBLISHER_DOES_NOT_EXIST
            )
        return publisher_db

    async def _check_publisher_unique(self, publisher_name: str) -> None:
        publisher_unique = await self.repository.is_publisher_unique(publisher_name)
        # Check the name is not already registered to another publisher
        if (not publisher_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.PUBLISHER_NAME_ALREADY_EXISTS
            )