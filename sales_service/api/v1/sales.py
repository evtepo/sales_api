from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from services.sales import SalesLogic, get_sales_logic
from schemas.response import SaleResponse, SingleSaleResponse
from schemas.sales import CreateSale, DeleteSale, UpdateSale
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/sales", tags=["Sales"])

sale_dependency = Annotated[SalesLogic, Depends(get_sales_logic)]


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(sale: CreateSale, sale_logic: sale_dependency, session: db_dependency):
    return await sale_logic.new_sale(sale, session)


@router.get("/{sale_id}", response_model=SingleSaleResponse, status_code=status.HTTP_200_OK)
async def get_sale(
    sale_id: UUID,
    sale_logic: sale_dependency,
    repository: repository_dependency,
    session: db_dependency,
):
    return await sale_logic.get_single_sale(sale_id, repository, session)


@router.get(
    "/",
    response_model=dict[str, dict[str, int | None] | list[SaleResponse | None]],
    status_code=status.HTTP_200_OK,
)
async def get_sales(
    sale_logic: sale_dependency,
    session: db_dependency,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
    city: UUID | None = Query(None, description="City ID"),
    store: UUID | None = Query(None, description="Store ID"),
    product: UUID | None = Query(None, description="Product ID"),
    days: int | None = Query(None),
    price: float | None = Query(
        None,
        description="Usage: 5000 for >= or -5000 for <=",
    ),
    amount: int | None = Query(
        None,
        description="Usage: 5 for >= or -5 for <=",
    ),
):
    return await sale_logic.get_list_of_sales(size, page, city, store, product, days, price, amount, session)


@router.put("/", response_model=SaleResponse, status_code=status.HTTP_200_OK)
async def update_sale(sale: UpdateSale, sale_logic: sale_dependency, session: db_dependency):
    return await sale_logic.update_sale_by_id(sale, session)


@router.delete("/", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_sale(sale: DeleteSale, sale_logic: sale_dependency, session: db_dependency):
    return await sale_logic.delete_sale_by_id(sale, session)
