from typing import TypeVar
from uuid import UUID

from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product, Sales
from models.location import City, Store
from repository.repository import BaseRepository
from schemas.city import CreateCity, DeleteCity, UpdateCity
from schemas.product import CreateProduct, DeleteProduct, UpdateProduct
from schemas.sales import CreateSale, DeleteSale, UpdateSale
from schemas.store import CreateStore, DeleteStore, UpdateStore
from utils.error_handling import error_response


Model = TypeVar("Model", City, Product, Sales, Store)

SchemaCreate = TypeVar("SchemaCreate", CreateCity, CreateProduct, CreateSale, CreateStore)
SchemaDelete = TypeVar("SchemaDelete", DeleteCity, DeleteProduct, DeleteSale, DeleteStore)
SchemaUpdate = TypeVar("SchemaUpdate", UpdateCity, UpdateProduct, UpdateSale, UpdateStore)


class BaseService:
    async def create_new_row(
        self,
        data: SchemaCreate,
        model: Model,
        repository: BaseRepository,
        session: AsyncSession,
    ):
        data = data.model_dump()
        return await repository.create(data, model, session)

    async def get_single_row(
        self,
        row_id: UUID,
        related_fields: tuple[str],
        model: Model,
        repository: BaseRepository,
        session: AsyncSession,
    ):
        filters = {"id": row_id}
        result = await repository.get_single(model, session, related_fields, **filters)
        if not result:
            return error_response("Data with such ID not found.")

        return result

    async def get_list_rows(
        self,
        offset: int,
        limit: int,
        model: Model,
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

    async def update_row_by_id(
        self,
        product: SchemaUpdate,
        model: Model,
        repository: BaseRepository,
        session: AsyncSession,
    ):
        data = product.model_dump()
        filters = {"id": data.get("id")}
        result = await repository.update(data, model, session, **filters)
        if not result:
            return error_response("Can't update data with this ID.")

        return result

    async def delete_row_by_id(
        self,
        product: SchemaDelete,
        model: Model,
        repository: BaseRepository,
        session: AsyncSession,
    ):
        filters = product.model_dump()
        result = await repository.delete(model, session, **filters)
        if not result:
            return error_response("Can't delete data with this ID.")

        return result

    async def check_row(self, row_id: UUID, model: Model, session: AsyncSession):
        check_query = select(model).filter(model.id == row_id)

        result = await session.execute(check_query)
        result = result.scalar_one_or_none()
        if not result:
            return error_response("Wrong ID.", status.HTTP_400_BAD_REQUEST)

        return None
