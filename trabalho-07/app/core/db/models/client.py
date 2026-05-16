from sqlalchemy import Uuid, String, DateTime, func
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db.base import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    api_key: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    hmac_secret: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
