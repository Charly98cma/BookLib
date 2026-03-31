import uuid
from typing import Optional, List, Sequence
from sqlalchemy import insert
from sqlalchemy.sql.expression import select, update, delete

from models.publishers_model import Publisher
from schemas.publishers_schema import PublisherCreate, PublisherDBResponse

from repositories.base_repository import BaseRepository

class PublisherRepository(BaseRepository):

    # CREATE ###################################################################

    async def create_publisher(self, publisher: PublisherCreate) -> PublisherDBResponse:
        stmt = (
            insert(Publisher)
            .values(**publisher.__dict__)
            .returning(Publisher)
        )
        self.logger.debug("create_publisher() - stmt = ", stmt)
        publisher_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return PublisherDBResponse.model_validate(publisher_db)

    # READ #####################################################################

    async def read_publisher(self, publisher_id: uuid.UUID) -> Optional[PublisherDBResponse]:
        stmt = (
            select(Publisher)
            .where(Publisher.id == publisher_id)
        )
        self.logger.debug("read_publisher() - stmt = ", stmt)
        publisher_db = (await self.db.execute(stmt)).scalar_one_or_none()
        if (publisher_db is None):
            return None
        return PublisherDBResponse.model_validate(publisher_db)

    async def read_all_publishers(self) -> List[PublisherDBResponse]:
        stmt = select(Publisher)
        self.logger.debug("read_all_publishers() - stmt = ", stmt)
        publisher_db_list = (await self.db.execute(stmt)).scalars().all()
        return self._map_publishers_to_schema_list(publisher_db_list)

    # UPDATE ###################################################################

    async def update_publisher(self, publisher_id: uuid.UUID, publisher: PublisherCreate) -> PublisherDBResponse:
        stmt = (
            update(Publisher)
            .where(Publisher.id == publisher_id)
            .values(**publisher.__dict__)
            .returning(Publisher)
        )
        self.logger.debug("update_publisher() - stmt = ", stmt)
        publisher_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return PublisherDBResponse.model_validate(publisher_db)

    # DELETE ###################################################################

    async def delete_publisher(self, publisher_id: uuid.UUID) -> None:
        stmt = (
            delete(Publisher)
            .where(Publisher.id == publisher_id)
        )
        self.logger.debug("delete_publisher() - stmt = ", stmt)
        await self.db.execute(stmt)
        await self.db.commit()

    ############################################################################

    async def is_publisher_unique(self, _publisher_name: str) -> bool:
        stmt = (
            select(Publisher)
            .where(Publisher.name == _publisher_name)
            .limit(1)
        )
        self.logger.debug("is_publisher_unique() - stmt = ", stmt)
        result = (await self.db.execute(stmt)).scalar_one_or_none()
        return (result is None)

    @staticmethod
    def _map_publishers_to_schema_list(publisher_db_list: Sequence[Publisher]) -> List[PublisherDBResponse]:
        return [PublisherDBResponse.model_validate(publisher) for publisher in publisher_db_list]