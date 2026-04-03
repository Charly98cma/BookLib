import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

_genre_example = {
    "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
    "name": "Sci-Fi",
}

class GenreCreate(BaseModel):
    """
    Pydantic schema for Genre creation
    """

    name: Annotated[str, Field(examples=[_genre_example["name"]])]

class GenreDBResponse(BaseModel):

    id: Annotated[uuid.UUID, Field(examples=[_genre_example["id"]])]
    name: Annotated[str, Field(examples=[_genre_example["name"]])]

    model_config = ConfigDict(from_attributes=True)
