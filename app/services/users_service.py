from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from enums.http_messages import HTTPMessages
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
                status_code=HTTPStatus.BAD_REQUEST,
                detail=HTTPMessages.USERNAME_ALREADY_EXISTS
            )
        if (await self.repository.check_email_exists(user.email)):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=HTTPMessages.EMAIL_ALREADY_EXISTS
            )
        return await self.repository.create(user)

    # READ #####################################################################

    async def read_all(self) -> List[UserDBResponse]:
        return await self.repository.read_all()
    
    # UPDATE ###################################################################

    async def login(self, user: UserLogin):
        user_db = await self.repository.login(user)
        if (user_db is None):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=HTTPMessages.WRONG_CREDENTIALS
            )
        return await self.repository.update_last_login(user.username)

    async def update(self, username: str, user: UserCreate):
        await self.check_username_is_free(username)
        user_db = (await self.repository.update(username, user))
        return user_db

    # DELETE ###################################################################

    async def delete(self, username: str):
        await self.check_username_is_free(username)
        await self.repository.delete(username)

    ############################################################################

    async def check_username_is_free(self, username: str):
        """
        A function that raises a HTTPException with 404 (NOT FOUND) if the
        database does not contain a User with the given username.

        Otherwise, the function does not return any value.
        """
        if (not (await self.repository.check_username_exists(username))):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.USERNAME_DOES_NOT_EXISTS
            )

