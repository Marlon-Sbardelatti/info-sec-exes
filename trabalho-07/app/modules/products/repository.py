from uuid import UUID
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.db.models.product import Product

class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_products(self) -> Sequence[Product]:
        stmt = select(Product)

        products = self.session.execute(stmt).scalars().all()
        return products

    def get_product_by_id(self, id: UUID) -> Product | None:
        stmt = select(Product).where(Product.id == id)
        product = self.session.execute(stmt).scalar_one_or_none()
        return product

    def create_product(self, product: Product) -> Product:
        self.session.add(product)
        self.session.flush()
        return product

    def update_product(self, product: Product) -> Product:
        self.session.merge(product)
        self.session.flush()
        return product

    def delete_product(self, product: Product) -> None:
        self.session.delete(product)
        self.session.flush()
        return

