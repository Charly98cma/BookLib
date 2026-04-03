import uuid 
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Text,
    Date,
    ForeignKey,
    Numeric,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.dialects.postgresql import UUID

from models import aux_tables
from models.base import Base
if TYPE_CHECKING:
    from models.userbookprogress_model import UserBookProgress
    from models.authors_model import Author
    from models.publishers_model import Publisher
    from models.genres_model import Genre
    from models.users_model import User

class Book(Base):
    """Books database model"""

    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Basic info
    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    subtitle: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text
    )
    num_pages: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    is_physical: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    
    # ISBNs
    isbn_10: Mapped[Optional[str]] = mapped_column(
        String(10), unique=True
    )
    isbn_13: Mapped[Optional[str]] = mapped_column(
        String(14), unique=True
    )

    # Language (ISO 639-1)
    lang: Mapped[Optional[str]] = mapped_column(
        String(2)
    )

    # Publishing info
    publishing_date: Mapped[Optional[date]] = mapped_column(
        Date
    )
    publisher_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("publishers.id")
    )

    # Hardcover
    hc_book_id: Mapped[Optional[str]] = mapped_column(
        String(50), unique=True
    )
    hc_rating: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(3,2)
    )
    hc_n_ratings: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    # Audit
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    
    # Relationships

    authors: Mapped[List["Author"]] = relationship(
        secondary=aux_tables.book_authors,
        back_populates="authored_books",
        lazy="selectin",
    )
    
    publisher: Mapped[Optional["Publisher"]] = relationship(
        back_populates="published_books",
        lazy="selectin",
    )

    genres: Mapped[List["Genre"]] = relationship(
        secondary=aux_tables.book_genres,
        back_populates="genre_books",
        lazy="selectin",
    )

    favorited_by: Mapped[List["User"]] = relationship(
        secondary=aux_tables.user_favorite_books,
        back_populates="favorite_books",
        lazy="selectin",
    )

    read_by: Mapped[List["UserBookProgress"]] = relationship(
        back_populates="book",
        lazy="selectin",
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("num_pages > 0", name="pages_positive"),
        CheckConstraint("hc_n_ratings >= 0", name="hc_n_rating_positive"),
        CheckConstraint("hc_rating > 0.0", name="hc_rating_positive"),
        CheckConstraint("hc_rating <= 5.0", name="hc_rating_in_range")
    )