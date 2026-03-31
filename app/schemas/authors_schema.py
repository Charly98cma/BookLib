import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

class AuthorCreate(BaseModel):
    """
    Pydantic model for Author creation
    """

    name: Annotated[str, Field(examples=["Robert S.A. Corey"])]
    biography: Annotated[str, Field(examples=["So much text, oh my god"])]
    photo_path: Annotated[str, Field(examples=["/path/to/photo.png"])]

class AuthorDBResponse(BaseModel):
    """
    Pydantic model for Author response
    """

    id: Annotated[uuid.UUID, Field(examples=["52f19e39-20ac-47fd-9df2-53d58c0b3f64"])]
    name: Annotated[str, Field(examples=["Robert S.A. Corey"])]
    biography: Annotated[str, Field(examples=["So much text, oh my god"])]
    photo_path: Annotated[str, Field(examples=["/path/to/photo.png"])]
    
    model_config = ConfigDict(from_attributes=True)
