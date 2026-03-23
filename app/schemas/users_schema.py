import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserLogin(BaseModel):
    """Pydantic model with User values for login"""

    username: str
    password_hash: str

class UserCreate(UserLogin):
    """Pytdantic model for User creation"""

    email: EmailStr
    is_active: bool
    is_admin: bool

class UserDBResponse(BaseModel):
    """Pytdantic model for User response"""

    email: EmailStr
    username: str
    password_hash: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None

    model_config = ConfigDict(from_attributes=True)
