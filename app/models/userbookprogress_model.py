import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base

if TYPE_CHECKING:
    from models.users_model import User
    from models.books_models import Book

class UserBookProgress(Base):
    """"""
    
    __tablename__ = "user_book_progress"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.id"), primary_key=True
    )

    status: Mapped[str] = mapped_column(
        String(20), default="not_started"
    )
    progress: Mapped[float] = mapped_column(
        Float, default=0.0
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime
    )

    user: Mapped["User"] = relationship(
        back_populates="reading_progress",
        lazy="selectin",
    )
    book: Mapped["Book"] = relationship(
        back_populates="read_by",
        lazy="selectin",
    )