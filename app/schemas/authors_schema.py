import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

_author_example = {
    "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
    "name": "Robert S.A. Corey",
    "biography": "So much text, oh my god",
    "photo_path": "/path/to/photo.png",
}

class AuthorCreate(BaseModel):
    """
    Pydantic model for Author creation
    """

    name: Annotated[str, Field(examples=[_author_example["name"]])]
    biography: Annotated[str, Field(examples=[_author_example["biography"]])]
    photo_path: Annotated[str, Field(examples=[_author_example["photo_path"]])]

class AuthorDBResponse(BaseModel):
    """
    Pydantic model for Author response
    """

    id: Annotated[uuid.UUID, Field(examples=[_author_example["id"]])]
    name: Annotated[str, Field(examples=[_author_example["name"]])]
    biography: Annotated[str, Field(examples=[_author_example["biography"]])]
    photo_path: Annotated[str, Field(examples=[_author_example["photo_path"]])]
    
    model_config = ConfigDict(from_attributes=True)
