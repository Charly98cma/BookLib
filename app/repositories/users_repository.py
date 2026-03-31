import uuid
from typing import Optional, List, Sequence
from sqlalchemy import insert
from sqlalchemy.sql.expression import select, exists, update, delete, or_
from sqlalchemy.sql.functions import func
from pydantic import EmailStr

from models.users_model import User
from schemas.users_schema import UserCreate, UserDBResponse, UserDBSecrets
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):

    # CREATE ###################################################################

    async def create_user(self, user: UserCreate, password_hash: str) -> UserDBResponse:
        stmt = (
            insert(User)
            .values(
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                is_admin=user.is_admin,
            )
            .values(
                password_hash=password_hash
            )
            .returning(User)
        )
        self.logger.debug("create_user() - stmt = ", stmt)
        user_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return UserDBResponse.model_validate(user_db)

    # READ #####################################################################

    async def read_user(self, _user_id: uuid.UUID) -> Optional[UserDBResponse]:
        stmt = (
            select(User)
            .where(User.id == _user_id)
        )
        self.logger.debug("read_user() - stmt = ", stmt)
        user_db = (await self.db.execute(stmt)).scalar_one_or_none()
        if (user_db is None):
            return None
        return UserDBResponse.model_validate(user_db)

    async def read_password(self, _username: str) -> Optional[UserDBSecrets]:
        stmt = (
            select(User.password_hash)
            .where(
                User.username==_username,
                User.is_active==True
            )
        )
        self.logger.debug("read_password() - stmt = ", stmt)
        user_db = (await self.db.execute(stmt)).scalar_one_or_none()
        if (user_db is None):
            return None
        return UserDBSecrets.model_validate(user_db)

    async def read_all_users(self) -> List[UserDBResponse]:
        stmt = select(User)
        self.logger.debug("read_all_users() - stmt = ", stmt)
        user_db_list = (await self.db.execute(stmt)).scalars().all()
        return self._map_users_to_schema_list(user_db_list)

    async def is_username_email_used(self, _username: str, _email: EmailStr) -> bool:
        stmt = (
            select(
                exists()
                .where(
                    or_(
                        User.username == _username,
                        User.email == _email
                    )
                )
            )
        )
        self.logger.debug("is_username_email_used() - stmt = ", stmt)
        result = (await self.db.execute(stmt)).scalar()
        return bool(result)

    # UPDATE ###################################################################

    async def update_user(self, _user_id: uuid.UUID, _user: UserCreate) -> UserDBResponse:
        stmt = (
            update(User)
            .where(User.id==_user_id)
            .values(**_user.__dict__)
            .values(updated_at=func.now())
            .returning(User)
        )
        self.logger.debug("update_user() - stmt = ", stmt)
        user_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return UserDBResponse.model_validate(user_db)

    async def update_last_login(self, _username: str) -> UserDBResponse:
        stmt = (
            update(User)
            .where(User.username==_username)
            .values(last_login=func.now())
            .returning(User)
        )
        self.logger.debug("update_last_login() - stmt = ", stmt)
        user_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return UserDBResponse.model_validate(user_db)

    # DELETE ###################################################################
    
    async def delete_user(self, user_id: uuid.UUID) -> None:
        stmt = (
            delete(User)
            .where(User.id==user_id)
        )
        self.logger.debug("delete_user() - stmt = ", stmt)
        await self.db.execute(stmt)
        await self.db.commit()

    ############################################################################

    @staticmethod
    def _map_users_to_schema_list(users_db_list: Sequence[User]) -> List[UserDBResponse]:
        return [UserDBResponse.model_validate(user) for user in users_db_list]
