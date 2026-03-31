import uuid
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import EmailStr

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.dialects.postgresql import UUID

from models import aux_tables
from models.base import Base
if TYPE_CHECKING:
    from models.books_models import Book
    from models.userbookprogress_model import UserBookProgress

class User(Base):
    """User database model"""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Auth
    email: Mapped[EmailStr] = mapped_column(
        String(255), nullable=False, unique=True
    )
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    password_hash: Mapped[str] = mapped_column(
        String, nullable=False
    )

    # Profile
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    # Books
    favorite_books: Mapped[List["Book"]] = relationship(
        secondary=aux_tables.user_favorite_books,
        back_populates="favorited_by",
        lazy="selectin",
    )
    reading_progress: Mapped[List["UserBookProgress"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )

    # Audit
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(),
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
