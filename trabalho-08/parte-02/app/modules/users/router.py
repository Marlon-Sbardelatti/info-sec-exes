from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.modules.users.schemas import UserRead, UserCreate, UserCredentials
from app.modules.users.service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserRead, status_code=HTTPStatus.CREATED)
async def create(
    user_create: UserCreate, user_service: UserService = Depends(get_user_service)
) -> UserRead:
    user = user_service.create(user_create)
    return user


@router.post("/login", status_code=HTTPStatus.OK)
async def login(
    credentials: UserCredentials, user_service: UserService = Depends(get_user_service)
) -> dict:
    user_service.login(credentials)
    return {"status": "success!"}
