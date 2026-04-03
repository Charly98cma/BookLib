import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

_publisher_example = {
    "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
    "name": "Orbit Books",
}

class PublisherCreate(BaseModel):
    """
    Pydantic schema for Publisher creation
    """

    name: Annotated[str, Field(examples=[_publisher_example["name"]])]

class PublisherDBResponse(BaseModel):

    id: Annotated[uuid.UUID, Field(examples=[_publisher_example["id"]])]
    name: Annotated[str, Field(examples=[_publisher_example["name"]])]

    model_config = ConfigDict(from_attributes=True)
