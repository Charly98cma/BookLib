import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base

if TYPE_CHECKING:
    from models.books_models import Book

class Publisher(Base):
    """Publishers database model"""

    __tablename__ = "publishers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )

    published_books: Mapped[List["Book"]] = relationship(
        back_populates="publisher",
        lazy="selectin",
    )