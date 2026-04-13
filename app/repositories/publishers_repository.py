import uuid
from typing import Optional, List, Sequence
from sqlalchemy import insert
from sqlalchemy.sql.expression import select, update, delete

from models.publishers_model import Publisher

from repositories._base_repository import BaseRepository

class PublisherRepository(BaseRepository):

    # CREATE ###################################################################

    def create_publisher(self, publisher: Publisher) -> Publisher:
        self.db.add(publisher)
        self.db.flush()
        return publisher

    # READ #####################################################################

    def read_publisher(self, publisher_id: uuid.UUID) -> Optional[Publisher]:
        return self.db.get(Publisher, publisher_id)

    def read_all_publishers(self) -> Sequence[Publisher]:
        stmt = select(Publisher)
        return self.db.scalars(stmt).all()

    # UPDATE ###################################################################



    # DELETE ###################################################################

    def delete_publisher(self, publisher: Publisher) -> None:
        self.db.delete(publisher)

    ############################################################################

    def is_publisher_unique(self, _publisher_name: str) -> bool:
        stmt = select(Publisher).where(Publisher.name == _publisher_name)
        result = self.db.scalar(stmt)
        return (result is None)
