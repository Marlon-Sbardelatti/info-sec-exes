from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
