from typing import Optional
from sqlalchemy import Uuid, String, Text, Numeric
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(60))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cost_price: Mapped[float] = mapped_column(Numeric(10, 2))
    sell_price: Mapped[float] = mapped_column(Numeric(10, 2))


