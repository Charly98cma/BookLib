import uuid
from typing import Annotated, List, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator

from models.books_models import Book

_author_example : Dict[str, str | List[str]] = {
    "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
    "name": "Robert S.A. Corey",
    "biography": "So much text, oh my god",
    "photo_path": "/path/to/photo.png",
    "authored_books": [
        "52f19e39-20ac-47fd-9df2-53d58c0b8j51",
    ],
}

class AuthorCreate(BaseModel):
    """
    Pydantic model for Author creation
    """

    name: Annotated[str, Field(examples=[_author_example["name"]])]
    biography: Annotated[str, Field(examples=[_author_example["biography"]])]
    photo_path: Annotated[str, Field(examples=[_author_example["photo_path"]])]

class AuthorUpdate(AuthorCreate):
    """
    Python model for Author update
    """

    authored_books: Annotated[List[uuid.UUID], Field(examples=[_author_example["authored_books"]])]

class AuthorDBResponse(BaseModel):
    """
    Pydantic model for Author response
    """

    id: Annotated[uuid.UUID, Field(examples=[_author_example["id"]])]
    name: Annotated[str, Field(examples=[_author_example["name"]])]
    biography: Annotated[str, Field(examples=[_author_example["biography"]])]
    photo_path: Annotated[str, Field(examples=[_author_example["photo_path"]])]

    authored_books: Annotated[List[uuid.UUID], Field(examples=[_author_example["authored_books"]])]
    @field_validator("authored_books", mode="before")
    def extract_book_ids(cls, book_list: List[Book]) -> List[uuid.UUID]:
        return [book.id for book in book_list]
    
    model_config = ConfigDict(from_attributes=True)
