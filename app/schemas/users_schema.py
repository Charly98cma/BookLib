import uuid
from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserLogin(BaseModel):
    """
    Pydantic model for User login.
    """

    username: Annotated[str, Field(examples=["username"])]
    password: Annotated[str, Field(examples=["plain_password"])]

class UserCreate(BaseModel):
    """
    Pytdantic model for User creation
    """

    username: Annotated[str, Field(examples=["username"])]
    password: Annotated[str, Field(examples=["plain_password"])]
    email: Annotated[EmailStr, Field(examples=["user@example.com"])]
    is_active: Annotated[bool, Field(examples=[True])]
    is_admin: Annotated[bool, Field(examples=[False])]

class UserDBSecrets(BaseModel):
    """
    Pydantic model for User secrets
    """
    password_hash: Annotated[str, Field(examples=["very_secure_hashed_password"])]

    model_config = ConfigDict(from_attributes=True)

class UserDBResponse(BaseModel):
    """
    Pytdantic model for User response
    """

    id: Annotated[uuid.UUID, Field(examples=["52f19e39-20ac-47fd-9df2-53d58c0b3f64"])]
    username: Annotated[str, Field(examples=["username"])]
    email: Annotated[EmailStr, Field(examples=["user@example.com"])]
    is_active: Annotated[bool, Field(examples=[True])]
    is_admin: Annotated[bool, Field(examples=[False])]
    created_at: Annotated[datetime, Field(examples=["2026-03-24T16:14:21.554Z"])]
    updated_at: Annotated[datetime, Field(examples=["2026-03-24T16:14:21.554Z"])]
    last_login: Annotated[Optional[datetime], Field(examples=["2026-03-24T16:14:21.554Z"])]

    model_config = ConfigDict(from_attributes=True)
