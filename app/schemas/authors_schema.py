import uuid
from typing import Annotated, List, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator

from models.books_models import Book

################################################################################

_author_example : Dict[str, str | List[str]] = {
    "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
    "name": "Robert S.A. Corey",
    "biography": "So much text, oh my god",
    "photo_path": "/path/to/photo.png",
    "authored_books": [
        "52f19e39-20ac-47fd-9df2-53d58c0b8j51",
    ],
}

################################################################################

class AuthorCreate(BaseModel):
    """
    Pydantic model for Author creation
    """

    name: Annotated[
        str,
        Field(
            description="Author's name",
            examples=[_author_example["name"]],
            min_length=0,
            max_length=255)
    ]
    biography: Annotated[
        str,
        Field(
            default="",
            description="Author biography",
            examples=[_author_example["biography"]])
    ] = ""
    photo_path: Annotated[
        str,
        Field(
            default="",
            description="Local path to author image/portrait",
            examples=[_author_example["photo_path"]],
            pattern="^(\\/[^\\/ ]*)+\\/?$|^\\.(\\/[^\\/ ]*)+\\/?$|^\\.\\.\\/([^\\/ ]*\\/)*[^\\/ ]*$")
    ] = ""

class AuthorUpdate(AuthorCreate):
    """
    Pydantic schema for Author update endpoint
    """

    authored_books: Annotated[
        List[uuid.UUID],
        Field(
            default=[],
            description="List of Book UUIDs",
            examples=[_author_example["authored_books"]])
    ]

################################################################################

class AuthorDBBasic(BaseModel):
    """
    Pydantic schema with basic values of Author entity
    """

    id: Annotated[
        uuid.UUID,
        Field(
            description="Author UUID",
            examples=[_author_example["id"]])
    ]
    name: Annotated[
        str,
        Field(
            description="Author's name",
            examples=[_author_example["name"]],
            min_length=0,
            max_length=255)
    ]
    photo_path: Annotated[
        str,
        Field(
            default="",
            description="Local path to Author image/portrait",
            examples=[_author_example["photo_path"]],
            pattern="^(\\/[^\\/ ]*)+\\/?$|^\\.(\\/[^\\/ ]*)+\\/?$|^\\.\\.\\/([^\\/ ]*\\/)*[^\\/ ]*$")
    ]
    model_config = ConfigDict(from_attributes=True)

class AuthorDBFull(AuthorDBBasic):
    """
    Pydantic schema with all values of Author entity
    """

    biography: Annotated[
        str,
        Field(
            default="",
            description="Author biography",
            examples=[_author_example["biography"]])
    ]
    authored_books: Annotated[
        List[uuid.UUID],
        Field(
            default=[],
            description="List of Book UUID authored",
            examples=[_author_example["authored_books"]])
    ]
    model_config = ConfigDict(from_attributes=True)

    @field_validator("authored_books", mode="before")
    def extract_book_ids(cls, book_list: List[Book]) -> List[uuid.UUID]:
        return [book.id for book in book_list]
