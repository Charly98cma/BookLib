import uuid
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from models import aux_tables
from models.base import Base
if TYPE_CHECKING:
    from models.books_models import Book

class Author(Base):
    """Auhors database model"""

    __tablename__ = "authors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Basic information
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    biography: Mapped[Optional[str]] = mapped_column(
        String
    )
    photo_path: Mapped[Optional[str]] = mapped_column(
        String
    )

    # Books
    authored_books: Mapped[List["Book"]] = relationship(
        secondary=aux_tables.book_authors,
        back_populates="authors",
        lazy="selectin",
    )