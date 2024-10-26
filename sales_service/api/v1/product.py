from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from schemas.response import ProductResponse, SingleProductResponse
from schemas.product import CreateProduct, DeleteProduct, UpdateProduct
from services.product import get_product_service, ProductService
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/product", tags=["Product"])

product_dependency = Annotated[ProductService, Depends(get_product_service)]


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: CreateProduct,
    repository: repository_dependency,
    session: db_dependency,
    product_service: product_dependency,
):
    return await product_service.new_product(product, repository, session)


@router.get("/{product_id}", response_model=SingleProductResponse, status_code=status.HTTP_200_OK)
async def get_product(
    product_id: UUID,
    repository: repository_dependency,
    session: db_dependency,
    product_service: product_dependency,
):
    return await product_service.get_single_product(product_id, repository, session)


@router.get(
    "/",
    response_model=dict[str, dict[str, int | None] | list[ProductResponse | None]],
    status_code=status.HTTP_200_OK,
)
async def get_products(
    repository: repository_dependency,
    session: db_dependency,
    product_service: product_dependency,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    return await product_service.get_list_of_products(size, page, repository, session)


@router.put("/", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(
    product: UpdateProduct,
    repository: repository_dependency,
    session: db_dependency,
    product_service: product_dependency,
):
    return await product_service.update_product_by_id(product, repository, session)


@router.delete("/", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_product(
    product: DeleteProduct,
    repository: repository_dependency,
    session: db_dependency,
    product_service: product_dependency,
):
    return await product_service.delete_product_by_id(product, repository, session)
