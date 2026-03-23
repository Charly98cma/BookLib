from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users_schema import UserCreate, UserLogin, UserDBResponse
from repositories.users_repository import UserRepository

class UserService:
    """Service class for handling users"""

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    async def create(self, user: UserCreate) -> Optional[UserDBResponse]:
        if (await self.repository.check_username_exists(user.username)):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists!"
            )
        if (await self.repository.check_email_exists(user.email)):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists!"
            )
        return await self.repository.create(user)

    # READ #####################################################################

    async def read_all(self) -> List[UserDBResponse]:
        return await self.repository.read_all()
    
    # UPDATE ###################################################################

    async def update(self, username: str, user: UserCreate):
        if (not (await self.repository.check_username_exists(username))):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User does not exists!"
            )
        user_db = (await self.repository.update(username, user))
        return user_db

    # DELETE ###################################################################

    async def delete(self, username: str):
        if (not (await self.repository.check_username_exists(username))):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User does not exists!"
            )
        await self.repository.delete(username)

    ############################################################################

    async def login(self, user: UserLogin):
        user_db = await self.repository.login(user)
        if (user_db is None):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Username or password are incorrect!"
            )
        return await self.repository.update_last_login(user.username)

