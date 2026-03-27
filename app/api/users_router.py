from fastapi import APIRouter, Depends
from typing import Optional, List, Annotated
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from enums.http_messages import HTTPMessages
from db.database import get_db
from schemas.users_schema import UserCreate, UserLogin, UserDBResponse
from services.users_service import UserService

# User router
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# CREATE #######################################################################

@router.post(
    "",
    summary="Create new user",
    status_code=HTTPStatus.OK,
    response_model=UserDBResponse,
    response_description="User created and returned successfully",
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Username or email not unique, or email in incorrect format",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "< reason for failure >"
                    }
                }
            }
        },
    }
)
async def create_user(
    data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Inserts a new user, and returns the created database entity, if the values
    follow the next criteria:

    * The *username* and *email* are unique (no other user uses them already)
    * The *email* is in email format
    * The *password* length is less than or equals to 72 Bytes. 
    """
    _service = UserService(session)
    return await _service.create_user(data)

# READ #########################################################################

@router.get(
    "",
    summary="Get a list with all registered users",
    status_code=HTTPStatus.OK,
    response_model=List[Optional[UserDBResponse]],
    response_description="List with all registered users on the database",
)
async def get_all(
    session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Returns a list with all registered users on the database, or en empty list
    if there are none.    
    """
    _service = UserService(session)
    return await _service.read_all_users()

# UPDATE #######################################################################

@router.put(
    "/login",
    summary="User login",
    status_code=HTTPStatus.OK,
    response_model=UserDBResponse,
    response_description="User logged in successfully",
    responses={
        HTTPStatus.UNAUTHORIZED: {
            "description": "Wrong credentials",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.WRONG_CREDENTIALS
                    }
                }
            }
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Invalid format",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid format of username and/or password"
                    }
                }
            }
        }
    }
)
async def login(
        data: UserLogin,
        session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Login user with username and password.
    """
    _service = UserService(session)
    return await _service.login(data)

@router.put(
    "/{username}",
    summary="Update user",
    status_code=HTTPStatus.OK,
    response_model=UserDBResponse,
    response_description="User with updated information",
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.USERNAME_DOES_NOT_EXISTS
                    }
                }
            }
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "New user or email already registered",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.USERNAME_EMAIL_ALREADY_EXISTS
                    }
                }
            }
        }
    }
)
async def update_user(
    data: UserCreate,
    username: str,
    session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Updates the user information if the new values follow the next criteria:

    * The *username* and *email* are unique (no other user uses them already)
    * The *email* is in email format
    * The *password* length is less than or equals to 72 Bytes.
    """
    _service = UserService(session)
    return await _service.update_user(username, data)

# DELETE #######################################################################

@router.delete(
    "/{username}",
    summary="Delete user",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": HTTPMessages.USERNAME_DOES_NOT_EXISTS
                    }
                }
            }
        },
    }
)
async def delete_user(
    username: str,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Delete user with the given username
    """
    _service = UserService(session)
    await _service.delete_user(username)
