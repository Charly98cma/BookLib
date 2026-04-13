import uuid
from logging import getLogger
from typing import Optional, List
from http import HTTPStatus
from fastapi import HTTPException
#from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func
from pydantic import EmailStr

from core import oauth2
from core.http_messages import HTTPMessages

from schemas.users_schema import UserCreate, UserLogin, UserDBResponse

from repositories.users_repository import UserRepository

from models.users_model import User

DUMMY_PASSWORD_HASH = oauth2.hash_password("dummypassword")

class UserService:
    """Class to handle all services provided for the User endpoints"""

    def __init__(self, session: Session):
        self.repository = UserRepository(session)
        self.logger = getLogger(__name__)

    # CREATE ###################################################################

    def create_user(self, user: UserCreate) -> UserDBResponse:
        # Check values uniqueness
        self._check_username_unique(user.username)
        self._check_email_unique(user.email)
        # Check password is not longer than 72 Bytes
        self._verify_password_length(user.password)
        # Hash password for database storage
        password_hash = oauth2.hash_password(user.password)
        # Create User ORM object
        user_db = User(**(user.model_dump(exclude={"password"})))
        user_db.password_hash = password_hash
        # Add new User to database
        self.repository.create_user(user_db)
        return UserDBResponse.model_validate(user_db)

    # READ #####################################################################

    def read_all_users(self) -> List[UserDBResponse]:
        user_db_list = self.repository.read_all_users()
        return [UserDBResponse.model_validate(user) for user in user_db_list]

    # UPDATE ###################################################################

    def login(self, user: UserLogin) -> Optional[UserDBResponse]:
        user_db = self.repository.read_user_by_username(user.username)
        # Check provided password
        if (user_db is None):
            # Check againts dummy password to avoid timing attacks
            self._verify_password(user.password, DUMMY_PASSWORD_HASH)
        else:
            self._verify_password(user.password, user_db.password_hash)
            # If user exists and passwords match, update login and return user
            user_db.last_login = func.now()
            return UserDBResponse.model_validate(user_db)

    def update_user(self, user_id: uuid.UUID, data: UserCreate) -> Optional[UserDBResponse]:
        user_db = self._read_user(user_id)
        # Check uniqueness of values (if they changed)
        if (data.username != user_db.username):
            self._check_username_unique(user_db.username)
        if (data.email != user_db.email):
            self._check_email_unique(user_db.email)
        # Update values
        for field, value in (data.__dict__).items():
            setattr(user_db, field, value)
        # Update the user and return the new values of the database
        return UserDBResponse.model_validate(user_db)

    # DELETE ###################################################################

    def delete_user(self, user_id: uuid.UUID) -> None:
        user_db = self._read_user(user_id)
        self.repository.delete_user(user_db)

    # AUXILIAR FUNCTIONS #######################################################

    def _read_user(self, user_id: uuid.UUID) -> User:
        user_db = self.repository.read_user(user_id)
        if (user_db is None):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=HTTPMessages.USERNAME_DOES_NOT_EXISTS.format(user_id)
            )
        return user_db
    
    def _check_username_unique(self, username: str) -> None:
        username_unique = self.repository.is_username_unique(username)
        if (not username_unique):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.USERNAME_ALREADY_EXISTS.format(username)
            )

    def _check_email_unique(self, email: EmailStr) -> None:
        email_unique = self.repository.is_email_unique(email)
        if (not email_unique):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=HTTPMessages.EMAIL_ALREADY_EXISTS.format(email)
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
        if (not oauth2.verify_password(plain_password, hashed_password)):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=HTTPMessages.WRONG_CREDENTIALS
            )
