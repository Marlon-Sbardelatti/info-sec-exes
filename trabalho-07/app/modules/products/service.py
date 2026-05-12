from uuid import UUID
from typing import List
from fastapi import Depends, HTTPException
from app.modules.products.repository import ProductRepository
from app.core.db.session import get_session
from app.core.db.models.product import Product
from app.modules.products.schemas import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def get_products(self) -> List[Product]:
        products = self.repo.get_products()
        return list(products)

    def get_product_by_id(self, id: UUID) -> Product:
        product = self.repo.get_product_by_id(id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")

        return product

    def create_product(self, product_create: ProductCreate) -> Product:
        product = Product(**product_create.model_dump())
        self.repo.create_product(product)
        self.repo.session.refresh(product)
        self.repo.session.commit()
        return product

    def update_product(self, id: UUID, product_update: ProductUpdate) -> Product:
        product = self.get_product_by_id(id)
        update_data = product_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        self.repo.update_product(product)
        self.repo.session.refresh(product)
        self.repo.session.commit()
        return product

    def delete_product(self, id: UUID) -> None:
        product = self.get_product_by_id(id)
        self.repo.delete_product(product)
        self.repo.session.commit()
        return


def get_product_service(session=Depends(get_session)) -> ProductService:
    repo = ProductRepository(session)
    return ProductService(repo)
