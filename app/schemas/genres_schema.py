import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

class GenreCreate(BaseModel):
    """
    Pydantic schema for Genre creation
    """

    name: Annotated[str, Field(examples=["Sci-fi"])]

class GenreDBResponse(BaseModel):

    id: Annotated[uuid.UUID, Field(examples=["52f19e39-20ac-47fd-9df2-53d58c0b3f64"])]
    name: Annotated[str, Field(examples=["Sci-fi"])]

    model_config = ConfigDict(from_attributes=True)
