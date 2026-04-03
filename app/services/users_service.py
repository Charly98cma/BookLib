import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

import tools.password_manager as passwd_mngr
from enums.http_messages import HTTPMessages
from schemas.users_schema import UserCreate, UserLogin, UserDBResponse
from repositories.users_repository import UserRepository

DUMMY_PASSWORD_HASH = passwd_mngr.hash_password("dummypassword")

class UserService:
    """Class to handle all services provided for the User endpoints"""

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    async def create_user(self, user: UserCreate) -> UserDBResponse:
        # Verify uniqueness of username and email
        await self._check_username_unique(user.username)
        await self._check_email_unique(user.email)
        # Verify password length
        self._verify_password_length(user.password)
        # If all OK, then hash user password and create the new user
        password_hash = passwd_mngr.hash_password(user.password)
        return await self.repository.create_user(user, password_hash)

    # READ #####################################################################

    async def read_all_users(self) -> List[UserDBResponse]:
        return await self.repository.read_all_users()
    
    # UPDATE ###################################################################

    async def login(self, user: UserLogin) -> Optional[UserDBResponse]:
        user_db = await self.repository.read_password(user.username)
        # Check againts dummy password to avoid timming attacks
        if (user_db is None):
            self._verify_password(user.password, DUMMY_PASSWORD_HASH)
        else:
            self._verify_password(user.password, user_db.password_hash)
        # If user exists and passwords match, update login and return user
        return await self.repository.update_last_login(user.username)

    async def update_user(self, user_id: uuid.UUID, user: UserCreate) -> Optional[UserDBResponse]:
        user_db = await self._read_user(user_id)
        if (user.username != user_db.username):
            await self._check_username_unique(user_db.username)
        if (user.email != user_db.email):
            await self._check_email_unique(user_db.email)
        # Update the user and return the new values of the database
        return await self.repository.update_user(user_id, user)

    # DELETE ###################################################################

    async def delete_user(self, user_id: uuid.UUID) -> None:
        await self._read_user(user_id)
        await self.repository.delete_user(user_id)

    # AUXILIAR FUNCTIONS #######################################################

    async def _read_user(self, user_id: uuid.UUID) -> UserDBResponse:
        user_db = await self.repository.read_user(user_id)
        if (user_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.USERNAME_DOES_NOT_EXISTS
            )
        return user_db
    
    async def _check_username_unique(self, username: str) -> None:
        username_unique = await self.repository.is_username_unique(username)
        if (not username_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.USERNAME_ALREADY_EXISTS
            )

    async def _check_email_unique(self, email: EmailStr) -> None:
        email_unique = await self.repository.is_email_unique(email)
        if (not email_unique):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.EMAIL_ALREADY_EXISTS
            )

    @staticmethod
    def _verify_password_length(password: str):
        """Check the validity of the password length
        
        Raises HTTPException 422 if password longer than 72 Bytes
        """
        # Raise exception if password longer that 72 Bytes (bcrypt limitations)
        if (len(password) > 72):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.INVALID_PASSWORD_LENGTH
            )

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str):
        """Check a plain password againts a hashed one
        
        Uses 'bcrypt' to compare a plain password introduced by the user and
        the hashed password from the database.

        Raises HTTPException 401 if passwords do not match.
        """
        if (not passwd_mngr.verify_password(plain_password, hashed_password)):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=HTTPMessages.WRONG_CREDENTIALS
            )
