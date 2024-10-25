from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from repository.repository import BaseRepository
from schemas.product import CreateProduct, DeleteProduct, UpdateProduct


async def new_product(
    product: CreateProduct,
    model: Product,
    repository: BaseRepository,
    session: AsyncSession,
):
    data = product.model_dump()
    return await repository.create(data, model, session)


async def get_single_product(
    product_id: UUID,
    model: Product,
    repository: BaseRepository,
    session: AsyncSession,
):
    filters = {"id": product_id}
    related_fields = ("sales", "store")
    result = await repository.get_single(model, session, related_fields, **filters)
    if not result:
        return JSONResponse(
            {"msg": "Product with such ID not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result


async def get_list_of_products(
    limit: int,
    offset: int,
    model: Product,
    repository: BaseRepository,
    session: AsyncSession,
):
    offset_arg = (offset - 1) * limit
    result = await repository.get_list(model, session, limit, offset_arg)

    prev_page = offset - 1 if offset > 1 else None
    next_page = offset + 1 if len(result) == limit else None

    return {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
        "data": result,
    }


async def update_product_by_id(
    product: UpdateProduct,
    model: Product,
    repository: BaseRepository,
    session: AsyncSession,
):
    data = product.model_dump()
    filters = {"id": data.get("id")}
    result = await repository.update(data, model, session, **filters)
    if not result:
        return JSONResponse(
            {"msg": "Can't update a product with this ID."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result


async def delete_product_by_id(
    product: DeleteProduct,
    model: Product,
    repository: BaseRepository,
    session: AsyncSession,
):
    filters = product.model_dump()
    result = await repository.delete(model, session, **filters)
    if not result:
        return JSONResponse(
            {"msg": "Can't delete a product with this ID."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result