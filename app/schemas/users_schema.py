import uuid
from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field

_user_example = {
    "id": "",
    "username": "",
    "plain_password": "PlainPassword",
    "hashed_password": "HashedPassword",
    "email": "user@email.com",
    "is_active": True,
    "is_admin": False,
    "created_at": "2026-03-24T16:14:21.554Z",
    "updated_at": "2026-03-24T16:14:21.554Z",
    "last_login": "2026-03-24T16:14:21.554Z",
}

class UserLogin(BaseModel):
    """
    Pydantic model for User login.
    """

    username: Annotated[str, Field(examples=[_user_example["username"]])]
    password: Annotated[str, Field(examples=[_user_example["plain_password"]])]

class UserCreate(BaseModel):
    """
    Pytdantic model for User creation
    """

    username: Annotated[str, Field(examples=[_user_example["username"]])]
    password: Annotated[str, Field(examples=[_user_example["plain_password"]])]
    email: Annotated[EmailStr, Field(examples=[_user_example["email"]])]
    is_active: Annotated[bool, Field(examples=[_user_example["is_active"]])]
    is_admin: Annotated[bool, Field(examples=[_user_example["is_admin"]])]

class UserDBSecrets(BaseModel):
    """
    Pydantic model for User secrets
    """
    password_hash: Annotated[str, Field(examples=[_user_example["hashed_password"]])]

    model_config = ConfigDict(from_attributes=True)

class UserDBResponse(BaseModel):
    """
    Pytdantic model for User response
    """

    id: Annotated[uuid.UUID, Field(examples=[_user_example["id"]])]
    username: Annotated[str, Field(examples=[_user_example["username"]])]
    email: Annotated[EmailStr, Field(examples=[_user_example["email"]])]
    is_active: Annotated[bool, Field(examples=[_user_example["is_active"]])]
    is_admin: Annotated[bool, Field(examples=[_user_example["is_admin"]])]
    created_at: Annotated[datetime, Field(examples=[_user_example["created_at"]])]
    updated_at: Annotated[datetime, Field(examples=[_user_example["updated_at"]])]
    last_login: Annotated[Optional[datetime], Field(examples=[_user_example["last_login"]])]

    model_config = ConfigDict(from_attributes=True)
