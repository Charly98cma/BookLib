import uuid
from typing import Optional, List, Sequence
from sqlalchemy import insert
from sqlalchemy.sql.expression import select, exists, update, delete
from sqlalchemy.sql.functions import func

from models.authors_model import Author
from schemas.authors_schema import AuthorCreate, AuthorDBResponse

from repositories.base_repository import BaseRepository

class AuthorRepository(BaseRepository):

    # CREATE ###################################################################

    async def create_author(self, author: AuthorCreate) -> AuthorDBResponse:
        stmt = (
            insert(Author)
            .values(**author.__dict__)
            .returning(Author)
        )
        self.logger.debug("create_author() - stmt = ", stmt)
        author_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return AuthorDBResponse.model_validate(author_db)

    # READ #####################################################################

    async def read_author(self, author_id: uuid.UUID) -> Optional[AuthorDBResponse]:
        stmt = (
            select(Author)
            .where(Author.id == author_id)
        )
        self.logger.debug("read_author() - stmt = ", stmt)
        author_db = (await self.db.execute(stmt)).scalar_one_or_none()
        if (author_db is None):
            return None
        return AuthorDBResponse.model_validate(author_db)

    async def read_all_authors(self) -> List[AuthorDBResponse]:
        stmt = select(Author)
        self.logger.debug("read_all_authors() - stmt = ", stmt)
        author_db_list = (await self.db.execute(stmt)).scalars().all()
        return self._map_authors_to_schema_list(author_db_list)

    # UPDATE ###################################################################

    async def update_author(self, author_id: uuid.UUID, author: AuthorCreate) -> AuthorDBResponse:
        stmt = (
            update(Author)
            .where(Author.id == author_id)
            .values(**author.__dict__)
            .returning(Author)
        )
        self.logger.debug("update_author() - stmt = ", stmt)
        author_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return AuthorDBResponse.model_validate(author_db)

    # DELETE ###################################################################

    async def delete_author(self, author_id: uuid.UUID) -> None:
        stmt = (
            delete(Author)
            .where(Author.id == author_id)
        )
        self.logger.debug("delete_author() - stmt = ", stmt)
        await self.db.execute(stmt)
        await self.db.commit()

    ############################################################################

    async def is_author_unique(self, _author_name: str) -> bool:
        stmt = (
            select(Author)
            .where(Author.name == _author_name)
            .limit(1)
        )
        self.logger.debug("is_author_unique() - stmt = ", stmt)
        result = (await self.db.execute(stmt)).scalar_one_or_none()
        return (result is None)

    @staticmethod
    def _map_authors_to_schema_list(author_db_list: Sequence[Author]) -> List[AuthorDBResponse]:
        return [AuthorDBResponse.model_validate(author) for author in author_db_list]