from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.db.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        return user

    def get_user_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        return self.session.execute(stmt).scalar_one_or_none()
