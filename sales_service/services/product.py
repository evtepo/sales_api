from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from repository.repository import BaseRepository
from schemas.product import CreateProduct, DeleteProduct, UpdateProduct
from utils.error_handling import error_response


async def new_product(product: CreateProduct, repository: BaseRepository, session: AsyncSession):
    data = product.model_dump()
    return await repository.create(data, Product, session)


async def get_single_product(product_id: UUID, repository: BaseRepository, session: AsyncSession):
    filters = {"id": product_id}
    related_fields = ("sales", "store")
    result = await repository.get_single(Product, session, related_fields, **filters)
    if not result:
        return error_response("Product with such ID not found.")

    return result


async def get_list_of_products(limit: int, offset: int, repository: BaseRepository, session: AsyncSession):
    offset_arg = (offset - 1) * limit
    result = await repository.get_list(Product, session, limit, offset_arg)

    prev_page = offset - 1 if offset > 1 else None
    next_page = offset + 1 if len(result) == limit else None

    return {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
        "data": result,
    }


async def update_product_by_id(product: UpdateProduct, repository: BaseRepository, session: AsyncSession):
    data = product.model_dump()
    filters = {"id": data.get("id")}
    result = await repository.update(data, Product, session, **filters)
    if not result:
        return error_response("Can't update a product with this ID.")

    return result


async def delete_product_by_id(product: DeleteProduct, repository: BaseRepository, session: AsyncSession):
    filters = product.model_dump()
    result = await repository.delete(Product, session, **filters)
    if not result:
        return error_response("Can't delete a product with this ID.")

    return result
