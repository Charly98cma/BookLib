from fastapi import APIRouter, Depends
from typing import Optional, List, Annotated
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.users_schema import UserCreate, UserLogin, UserDBResponse
from services.users_service import UserService

# User router
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# CREATE #######################################################################

@router.post("",
             status_code=HTTPStatus.OK,
             response_model=UserDBResponse)
async def create_user(
    data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_db)]
):
    _service = UserService(session)
    return await _service.create(data)

# READ #########################################################################

@router.get("",
            status_code=HTTPStatus.OK,
            response_model=List[Optional[UserDBResponse]])
async def get_all(
    session: Annotated[AsyncSession, Depends(get_db)]
):
    _service = UserService(session)
    return await _service.read_all()

# UPDATE #######################################################################

@router.put("/login",
             status_code=HTTPStatus.OK,
             response_model=UserDBResponse)
async def login(
        data: UserLogin,
        session: Annotated[AsyncSession, Depends(get_db)]
):
    _service = UserService(session)
    return await _service.login(data)

@router.put("/{username}",
            status_code=HTTPStatus.OK,
            response_model=UserDBResponse)
async def update_user(
    data: UserCreate,
    username: str,
    session: Annotated[AsyncSession, Depends(get_db)]
):
    _service = UserService(session)
    return await _service.update(username, data)

# DELETE #######################################################################

@router.delete("/{username}",
               status_code=HTTPStatus.NO_CONTENT)
async def delete_user(
    username: str,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    _service = UserService(session)
    await _service.delete(username)
