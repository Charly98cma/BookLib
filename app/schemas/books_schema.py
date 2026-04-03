import uuid
from datetime import datetime
from typing import Annotated, Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

_book_example = {
    "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
    "title": "Leviathan Wakes",
    "subtitle": "The Expanse",
    "description": "",
    "num_pages": 592,
    "is_physical": True,
    "isbn_10": "1841499897",
    "isbn_13": "978-1841499895",
    "lang": "en",
    "publishing_date": "2012-05-20",
    "publisher_id": "",
    "hc_book_id": "leviathan-wakes",
    "hc_rating": 4.3,
    "hc_n_ratings": 2296,
    "created_at": "2026-03-24T16:14:21.554Z",
    "updated_at": "2026-03-24T16:14:21.554Z",
}

class BookCreate(BaseModel):
    """
    """

    title: Annotated[str, Field(examples=[_book_example["title"]])]
    subtitle: Annotated[str, Field(examples=[_book_example["subtitle"]])]
    description: Annotated[str, Field(examples=[_book_example["description"]])]
    num_pages: Annotated[int, Field(examples=[_book_example["num_pages"]])]
    is_physical: Annotated[int, Field(examples=[_book_example["is_physical"]])]
    isbn_10: Annotated[str, Field(examples=[_book_example["isbn_10"]])]
    isbn_13: Annotated[str, Field(examples=[_book_example["isbn_13"]])]
    lang: Annotated[str, Field(examples=[_book_example["lang"]])]
    publishing_date: Annotated[datetime, Field(examples=[_book_example["publishing_date"]])]
    # publisher_id: Annotated[uuid.UUID, Field(examples=[_book_example["publisher_id"]])]
    hc_book_id: Annotated[Optional[str], Field(examples=[_book_example["hc_book_id"]])]
    hc_rating: Annotated[Optional[Decimal], Field(examples=[_book_example["hc_rating"]])]
    hc_n_ratings: Annotated[Optional[int], Field(examples=[_book_example["hc_n_ratings"]])]

    # series
    # n_series
    # series_total

    # authors: Annotated[List[Author], Field(examples=[""])]
    # publisher: Annotated[Author, Field(examples=[""])]
    # genres: Annotated[List[Genre], Field(examples=[""])]
    # favorited_by: Annotated[List[User], Field(examples=[""])]
    # read_by: Annotated[List[UserBookProgress], Field(examples=[""])]

class BookDBResponse(BaseModel):
    """
    """

    id: Annotated[uuid.UUID, Field(examples=[_book_example["id"]])]
    title: Annotated[str, Field(examples=[_book_example["title"]])]
    subtitle: Annotated[str, Field(examples=[_book_example["subtitle"]])]
    description: Annotated[str, Field(examples=[_book_example["description"]])]
    num_pages: Annotated[int, Field(examples=[_book_example["num_pages"]])]
    is_physical: Annotated[int, Field(examples=[_book_example["is_physical"]])]
    isbn_10: Annotated[str, Field(examples=[_book_example["isbn_10"]])]
    isbn_13: Annotated[str, Field(examples=[_book_example["isbn_13"]])]
    lang: Annotated[str, Field(examples=[_book_example["lang"]])]
    publishing_date: Annotated[datetime, Field(examples=[_book_example["publishing_date"]])]
    # publisher_id: Annotated[uuid.UUID, Field(examples=[_book_example["publisher_id"]])]
    hc_book_id: Annotated[Optional[str], Field(examples=[_book_example["hc_book_id"]])]
    hc_rating: Annotated[Optional[Decimal], Field(examples=[_book_example["hc_rating"]])]
    hc_n_ratings: Annotated[Optional[int], Field(examples=[_book_example["hc_n_ratings"]])]
    created_at: Annotated[datetime, Field(examples=[_book_example["created_at"]])]
    updated_at: Annotated[datetime, Field(examples=[_book_example["updated_at"]])]

    # authors: Annotated[List[Author], Field(examples=[""])]
    # publisher: Annotated[Author, Field(examples=[""])]
    # genres: Annotated[List[Genre], Field(examples=[""])]
    # favorited_by: Annotated[List[User], Field(examples=[""])]
    # read_by: Annotated[List[UserBookProgress], Field(examples=[""])]

    model_config = ConfigDict(from_attributes=True)
