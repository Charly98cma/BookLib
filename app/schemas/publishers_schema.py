import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

class PublisherCreate(BaseModel):
    """
    Pydantic schema for Publisher creation
    """

    name: Annotated[str, Field(examples=["Orbit Books"])]

class PublisherDBResponse(BaseModel):

    id: Annotated[uuid.UUID, Field(examples=["52f19e39-20ac-47fd-9df2-53d58c0b3f64"])]
    name: Annotated[str, Field(examples=["Orbit Books"])]

    model_config = ConfigDict(from_attributes=True)
