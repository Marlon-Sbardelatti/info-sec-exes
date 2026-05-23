from http import HTTPStatus
from fastapi import Depends, HTTPException
from app.modules.users.schemas import UserCreate, UserCredentials
from app.modules.users.repository import UserRepository
from app.core.db.session import get_session
from app.core.db.models.user import User
from app.core.security.hashing import Hasher


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def login(self, credentials: UserCredentials) -> User:
        user = self.repo.get_user_by_login(credentials.login)

        if not user or not Hasher.verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return user

    def create(self, user_create: UserCreate) -> User:
        registered = self.repo.get_user_by_login(user_create.login)
        if registered:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Email already in use"
            )

        user_create.password = Hasher.hash_password(user_create.password)
        user = User(**user_create.model_dump())

        user = self.repo.create(user)
        self.repo.session.refresh(user)
        self.repo.session.commit()

        return user


def get_user_service(session=Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)
