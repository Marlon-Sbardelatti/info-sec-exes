from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ProductRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    cost_price: float
    sell_price: float


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cost_price: float
    sell_price: float


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cost_price: Optional[float] = None
    sell_price: Optional[float] = None
