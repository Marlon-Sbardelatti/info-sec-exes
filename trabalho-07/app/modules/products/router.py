from uuid import UUID
from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends
from app.modules.products.schemas import ProductRead, ProductCreate, ProductUpdate
from app.modules.products.service import ProductService, get_product_service
from app.core.dependencies.signed_request import signed_request

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductRead], status_code=HTTPStatus.OK)
def get_products(
    products_service: ProductService = Depends(get_product_service),
    api_key: str = Depends(signed_request),
):
    print(f"API KEY={api_key}")
    products = products_service.get_products()
    return products


@router.get("/{id}", response_model=ProductRead, status_code=HTTPStatus.OK)
def get_product_by_id(
    id: UUID,
    products_service: ProductService = Depends(get_product_service),
    api_key: str = Depends(signed_request),
):
    print(f"API KEY={api_key}")
    product = products_service.get_product_by_id(id)
    return product


@router.post("", response_model=ProductRead, status_code=HTTPStatus.CREATED)
def create_product(
    product_create: ProductCreate,
    products_service: ProductService = Depends(get_product_service),
    api_key: str = Depends(signed_request),
):
    print(f"API KEY={api_key}")
    product = products_service.create_product(product_create)
    return product


@router.put("/{id}", response_model=ProductRead, status_code=HTTPStatus.OK)
def update_product(
    id: UUID,
    product_update: ProductUpdate,
    products_service: ProductService = Depends(get_product_service),
    api_key: str = Depends(signed_request),
):
    print(f"API KEY={api_key}")
    product = products_service.update_product(id, product_update)
    return product


@router.delete("/{id}", status_code=HTTPStatus.NO_CONTENT)
def delete_product(
    id: UUID,
    products_service: ProductService = Depends(get_product_service),
    api_key: str = Depends(signed_request),
):
    print(f"API KEY={api_key}")
    products_service.delete_product(id)
    return
