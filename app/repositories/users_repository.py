from logging import getLogger
from typing import Optional, List, Sequence
from sqlalchemy import insert
from sqlalchemy.sql.expression import select, exists, update, delete
from sqlalchemy.sql.functions import func

from models.users import User
from schemas.users_schema import UserLogin, UserCreate, UserDBResponse, UserDBSecrets
from repositories.base_repository import BaseRepository

logger = getLogger(__name__)

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
        user_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return UserDBResponse.model_validate(user_db)

    # READ #####################################################################

    async def read_user(self, _username: str) -> Optional[UserDBResponse]:
        stmt = (
            select(User)
            .filter_by(username = _username)
            .limit(1)
        )
        user_db = (await self.db.execute(stmt)).scalar_one_or_none()
        if (user_db is None):
            return None
        return UserDBResponse.model_validate(user_db)

    async def read_password(self, _username: str) -> Optional[UserDBSecrets]:
        stmt = (
            select(User.password_hash)
            .filter_by(username=_username, is_active=True)
            .limit(1)
        )
        user_db = (await self.db.execute(stmt)).scalar_one_or_none()
        if (user_db is None):
            return None
        return UserDBSecrets.model_validate(user_db)

    async def read_all_users(self) -> List[UserDBResponse]:
        stmt = select(User)
        user_db_list = (await self.db.execute(stmt)).scalars().all()
        return self._map_users_to_schema_list(user_db_list)

    async def is_username_used(self, _username: str) -> bool:
        stmt = (
            select(
                exists()
                .where(User.username == _username)
            )
        )
        result = (await self.db.execute(stmt)).scalar()
        return bool(result)

    async def is_email_used(self, _email: str) -> bool:
        stmt = (
            select(
                exists()
                .where(User.email == _email)
            )
        )
        result = (await self.db.execute(stmt)).scalar()
        return bool(result)

    # UPDATE ###################################################################

    async def update_user(self, _username: str, _user: UserCreate) -> UserDBResponse:
        stmt = (
            update(User)
            .where(User.username==_username)
            .values(**_user.__dict__)
            .values(updated_at=func.now())
            .returning(User)
        )
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
        user_db = (await self.db.execute(stmt)).scalar_one()
        await self.db.commit()
        return UserDBResponse.model_validate(user_db)

    # DELETE ###################################################################
    
    async def delete_user(self, _username: str) -> None:
        stmt = (
            delete(User)
            .where(User.username==_username)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    ############################################################################

    @staticmethod
    def _map_users_to_schema_list(users: Sequence[User]) -> List[UserDBResponse]:
        return [UserDBResponse.model_validate(user) for user in users]
