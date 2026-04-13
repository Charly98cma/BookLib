from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, ForeignKey

from models.base import Base

"""
Mid tables for relationships between tables

* book_genres: Many-to-Many between Books and Genres
* book_authors: Many-to-Many between Authors and Books
* user_favorite_books: Many-to-Many User and Books
"""

book_genres = Table(
    "book_genres",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("books.id"), primary_key=True),
    Column("genre_id", UUID(as_uuid=True), ForeignKey("genres.id"), primary_key=True),
)

book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("books.id"), primary_key=True),
    Column("author_id", UUID(as_uuid=True), ForeignKey("authors.id"), primary_key=True),
)

user_favorite_books = Table(
    "user_favorite_books",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("book_id", UUID(as_uuid=True), ForeignKey("books.id"), primary_key=True),
)