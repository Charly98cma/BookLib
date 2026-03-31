import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

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
        # Check if the username or email is already in the database
        username_email_used = \
            await self.repository.is_username_email_used(user.username, user.email)
        # Throw exception if user or email are already used
        if (username_email_used):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.USERNAME_EMAIL_ALREADY_EXISTS
            )
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
        new_username_email_used = \
            await self.repository.is_username_email_used(user.username, user.email)
        user_db = await self.repository.read_user(user_id)
        # Check if the given username is in the database
        if (user_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.USERNAME_DOES_NOT_EXISTS
            )
        # Check the new username or email are not already used
        # (in case they are diferent from the already set ones)
        if (((user_db.username != user.username) and (new_username_email_used)) or
            (user_db.email != user.email) and (new_username_email_used)):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=HTTPMessages.USERNAME_EMAIL_ALREADY_EXISTS
            )
        # Update the user and return the new values of the database
        return await self.repository.update_user(user_id, user)

    # DELETE ###################################################################

    async def delete_user(self, user_id: uuid.UUID) -> None:
        # Check if the username exists and throw exception if does not
        user_db = await self.repository.read_user(user_id)
        if (user_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.USERNAME_DOES_NOT_EXISTS
            )
        # Delete user from database
        await self.repository.delete_user(user_id)

    ############################################################################

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
