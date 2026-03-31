import uuid
from fastapi import APIRouter, Depends
from typing import List, Annotated, Optional
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from enums.http_messages import HTTPMessages
from schemas.publishers_schema import PublisherCreate, PublisherDBResponse
from services.publishers_service import PublisherService

# Publisher router
router = APIRouter(
    prefix="/publishers",
    tags=["publishers"]
)

# CREATE #######################################################################

@router.post(
    "",
    summary="Create publisher",
    status_code=HTTPStatus.OK,
    response_model=PublisherDBResponse,
    response_description="Publisher created successfully",
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Invalid format",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.PUBLISHER_NAME_ALREADY_EXISTS
                    }
                }
            }
        }
    }
)
async def create_publisher(
    data: PublisherCreate,
    session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[PublisherDBResponse]:
    """
    Inserts a new publisher and returns the created database entity, if:

    * The *name* is unique (no other publisher already registered with it)
    """
    _service = PublisherService(session)
    return await _service.create_publisher(data)

# READ #########################################################################

@router.get(
    "",
    summary="Get all publishers",
    status_code=HTTPStatus.OK,
    response_model=List[PublisherDBResponse],
    response_description="List with all publishers in the database",
)
async def read_all_publishers(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> List[PublisherDBResponse]:
    """
    Returns a list with all publishers in the database,
    or an empty list if there are none.
    """
    _service = PublisherService(session)
    return await _service.read_all_publishers()

# UPDATE #######################################################################

@router.put(
    "/{publisher_id}",
    summary="Update publisher",
    status_code=HTTPStatus.OK,
    response_model=PublisherDBResponse,
    response_description="Publisher updated successfully",
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Publisher name already used",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.PUBLISHER_NAME_ALREADY_EXISTS
                    }
                }
            }
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Publisher not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.PUBLISHER_DOES_NOT_EXIST
                    }
                }
            }
        }
    }
)
async def update_publisher(
    publisher_id: uuid.UUID,
    data: PublisherCreate,
    session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[PublisherDBResponse]:
    """
    Update the publisher information with the new values if:

    * The *name* is unique (no other publisher already registered with it)
    """    
    _service = PublisherService(session)
    return await _service.update_publisher(publisher_id, data)    

# DELETE #######################################################################

@router.delete(
    "/{publisher_id}",
    summary="Delete publisher",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Publisher not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.PUBLISHER_DOES_NOT_EXIST
                    }
                }
            }
        }
    }
)
async def delete_publisher(
    publisher_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_db)]
):
    _service = PublisherService(session)
    await _service.delete_publisher(publisher_id)    
