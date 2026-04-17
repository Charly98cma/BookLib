import uuid
from datetime import datetime
from typing import Annotated, Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

from schemas.authors_schema import AuthorDBBasic
from schemas.publishers_schema import PublisherDBFull
from schemas.genres_schema import GenreDBFull

################################################################################

_book_example : Dict[str, Any] = {
    "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
    "cover_path": "/path/to/cover",
    "title": "Leviathan Wakes",
    "subtitle": "The Expanse",
    "description": "",
    "num_pages": 592,
    "is_physical": True,
    "isbn_10": "1841499897",
    "isbn_13": "9781841499895",
    "lang": "en",
    "publishing_date": "2012-05-20",
    "hc_book_id": "leviathan-wakes",
    "hc_rating": Decimal('4.3'),
    "hc_n_ratings": 2296,
    "created_at": "2026-03-24T16:14:21.554Z",
    "updated_at": "2026-03-24T16:14:21.554Z",
    "authors": [
        {
            "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
            "name": "Robert S.A. Corey"
        }
    ],
    "publisher": {
        "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
        "name": "Orbit Books"
    },
    "genres": [
        {
            "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
            "name": "Sci-Fi"
        }
    ]
}

################################################################################

class BookCreate(BaseModel):
    """
    Pydantic schema for Book creation
    """
    title: Annotated[
        str,
        Field(
            description="Title of the book",
            examples=[_book_example["title"]],
            max_length=255
        )
    ]
    subtitle: Annotated[
        str,
        Field(
            default="",
            description="Subtitle of the book",
            examples=[_book_example["subtitle"]],
            max_length=255
        )
    ] = ""
    description: Annotated[
        str,
        Field(
            default="",
            description="Synopsis of the book",
            examples=[_book_example["description"]]
        )
    ] = ""
    num_pages: Annotated[
        Optional[int],
        Field(
            default=None,
            description="Number of pages of the book",
            examples=[_book_example["num_pages"]],
            gt=0,
            allow_inf_nan=False
        )
    ] = None
    is_physical: Annotated[
        bool,
        Field(
            default=False,
            description="Physical (True) or digital (False) book",
            examples=[_book_example["is_physical"]]
        )
    ] = False
    cover_path: Annotated[
        str,
        Field(
            default="",
            description="Local path to book cover image",
            examples=[_book_example["cover_path"]],
            pattern="^(\\/[^\\/ ]*)+\\/?$|^\\.(\\/[^\\/ ]*)+\\/?$|^\\.\\.\\/([^\\/ ]*\\/)*[^\\/ ]*$",
            max_length=255)
    ] = ""
    isbn_10: Annotated[
        str,
        Field(
            description="ISBN-10 (9 digits followed by letter X, or 10 digits)",
            examples=[_book_example["isbn_10"]],
            pattern="^(?:\\d{9}X|\\d{10})$",
            max_length=10
        )
    ]
    isbn_13: Annotated[
        str,
        Field(
            description="ISBN-13 (97, followed by either a 8 or 9, followed by 10 digits)",
            examples=[_book_example["isbn_13"]],
            pattern="^97[89]\\d{10}$",
            max_length=13
        )
    ]
    lang: Annotated[
        str,
        Field(
            default="",
            description="Book language in ISO-639-1 code (2 characters)",
            examples=[_book_example["lang"]],
            pattern="^[a-z]{2}$"
        )
    ] = ""
    publishing_date: Annotated[
        datetime,
        Field(
            description="Date of publication",
            examples=[_book_example["publishing_date"]]
        )
    ]
    hc_book_id: Annotated[
        str,
        Field(
            default="",
            description="Hardcover book ID",
            examples=[_book_example["hc_book_id"]],
            max_length=255
        )
    ] = ""
    hc_rating: Annotated[
        Decimal,
        Field(
            default=Decimal(0.0),
            description="Hardcover mean user rating",
            examples=[_book_example["hc_rating"]],
            ge=Decimal(0.0),
            le=Decimal(5.0),
            decimal_places=2,
            allow_inf_nan=False
        )
    ] = Decimal(0.0)
    hc_n_ratings: Annotated[
        int,
        Field(
            default=0,
            description="Number of user ratings in Hardcover",
            examples=[_book_example["hc_n_ratings"]],
            ge=0,
            allow_inf_nan=False
        )
    ] = 0
    authors: Annotated[
        List["AuthorDBBasic"],
        Field(
            default=[],
            description="List of authors of the book",
            examples=[_book_example["authors"]]
        )
    ] = []
    publisher: Annotated[
        Optional["PublisherDBFull"],
        Field(
            default=None,
            description="Publisher of the book",
            examples=[_book_example["publisher"]]
        )
    ] = None
    genres: Annotated[
        List["GenreDBFull"],
        Field(
            default=[],
            description="List of genres of the book",
            examples=[_book_example["genres"]]
        )
    ] = []

################################################################################

class BookDBBasic(BaseModel):
    """
    Pydantic schema with basic information of Book entity
    """
    id: Annotated[
        uuid.UUID,
        Field(
            description="Book UUID",
            examples=[_book_example["id"]])
    ]
    title: Annotated[
        str,
        Field(
            description="Title of the book",
            examples=[_book_example["title"]],
            max_length=255
        )
    ]
    cover_path: Annotated[
        str,
        Field(
            description="Local path to book cover image",
            examples=[_book_example["cover_path"]],
            pattern="^(\\/[^\\/ ]*)+\\/?$|^\\.(\\/[^\\/ ]*)+\\/?$|^\\.\\.\\/([^\\/ ]*\\/)*[^\\/ ]*$",
            max_length=255)
    ]
    model_config = ConfigDict(from_attributes=True)

class BookDBFull(BookDBBasic):
    """
    Pydantic schema with all values of Book entity
    """
    subtitle: Annotated[
        str,
        Field(
            description="Subtitle of the book",
            examples=[_book_example["subtitle"]],
            max_length=255
        )
    ]
    description: Annotated[
        str,
        Field(
            description="Synopsis of the book",
            examples=[_book_example["description"]]
        )
    ]
    num_pages: Annotated[
        int,
        Field(
            description="Number of pages of the book",
            examples=[_book_example["num_pages"]],
            gt=0,
            allow_inf_nan=False
        )
    ]
    is_physical: Annotated[
        bool,
        Field(
            description="Physical (True) or digital (False) book",
            examples=[_book_example["is_physical"]]
        )
    ]
    isbn_10: Annotated[
        str,
        Field(
            description="ISBN-10 (9 digits followed by letter X, or 10 digits)",
            examples=[_book_example["isbn_10"]],
            pattern="^(?:\\d{9}X|\\d{10})$",
            max_length=10
        )
    ]
    isbn_13: Annotated[
        str,
        Field(
            description="ISBN-13 (97, followed by either a 8 or 9, followed by 10 digits)",
            examples=[_book_example["isbn_13"]],
            pattern="^97[89]\\d{10}$",
            max_length=13
        )
    ]
    lang: Annotated[
        str,
        Field(
            description="Book language in ISO-639-1 code (2 characters)",
            examples=[_book_example["lang"]],
            pattern="^[a-z]{2}$"
        )
    ]
    publishing_date: Annotated[
        datetime,
        Field(
            description="Date of publication",
            examples=[_book_example["publishing_date"]]
        )
    ]
    hc_book_id: Annotated[
        str,
        Field(
            description="Hardcover book ID",
            examples=[_book_example["hc_book_id"]],
            max_length=255
        )
    ]
    hc_rating: Annotated[
        Decimal,
        Field(
            description="Hardcover mean user rating",
            examples=[_book_example["hc_rating"]],
            ge=Decimal(0.0),
            le=Decimal(5.0),
            allow_inf_nan=False,
            decimal_places=2
        )
    ]
    hc_n_ratings: Annotated[
        int,
        Field(
            description="Number of user ratings in Hardcover",
            examples=[_book_example["hc_n_ratings"]],
            ge=0,
            allow_inf_nan=False
        )
    ]
    created_at: Annotated[
        datetime,
        Field(
            description="Timestamp of the book creation",
            examples=[_book_example["created_at"]]
        )
    ]
    updated_at: Annotated[
        datetime,
        Field(
            description="Timestamp of the last update",
            examples=[_book_example["updated_at"]]
        )
    ]
    authors: Annotated[
        List["AuthorDBBasic"],
        Field(
            description="List of authors of the book"
        )
    ] 
    publisher: Annotated[
        Optional["PublisherDBFull"],
        Field(
            description="Publisher of the book"
        )
    ]
    genres: Annotated[
        List["GenreDBFull"],
        Field(
            description="List of genres of the book"
        )
    ]
    # favorited_by: Annotated[List[User], Field(examples=[""])]
    # read_by: Annotated[List[UserBookProgress], Field(examples=[""])]
    model_config = ConfigDict(from_attributes=True)
