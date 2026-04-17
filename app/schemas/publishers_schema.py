import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

################################################################################

_publisher_example = {
    "id": "52f19e39-20ac-47fd-9df2-53d58c0b3f64",
    "name": "Orbit Books",
}

################################################################################

class PublisherCreate(BaseModel):
    """
    Pydantic schema for Publisher creation
    """
    name: Annotated[
        str,
        Field(
            description="Name of the publisher",
            examples=[_publisher_example["name"]],
            max_length=255
        )
    ]

################################################################################

class PublisherDBFull(BaseModel):
    """
    Pydantic schema of Publisher entity
    """
    id: Annotated[
        uuid.UUID,
        Field(
            description="Publisher UUID",
            examples=[_publisher_example["id"]]
        )
    ]
    name: Annotated[
        str,
        Field(
            description="Name of the publisher",
            examples=[_publisher_example["name"]],
            max_length=255
        )
    ]
    model_config = ConfigDict(from_attributes=True)
