from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from models.location import Store
from repository.repository import BaseRepository
from schemas.store import CreateStore, DeleteStore, UpdateStore


async def new_store(store: CreateStore, model: Store, repository: BaseRepository, session: AsyncSession):
    data = store.model_dump()
    return await repository.create(data, model, session)


async def get_single_store(store_id: UUID, model: Store, repository: BaseRepository, session: AsyncSession):
    filters = {"id": store_id}
    related_fields = ("city", "products")
    result = await repository.get_single(model, session, related_fields, **filters)
    if not result:
        return JSONResponse(
            {"msg": "Store with such ID not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result


async def get_list_of_stores(
    limit: int,
    offset: int,
    model: Store,
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


async def update_store_by_id(store: UpdateStore, model: Store, repository: BaseRepository, session: AsyncSession):
    data = store.model_dump()
    filters = {"id": data.get("id")}
    result = await repository.update(data, model, session, **filters)
    if not result:
        return JSONResponse(
            {"msg": "Can't update a store with this ID."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result


async def delete_store_by_id(store: DeleteStore, model: Store, repository: BaseRepository, session: AsyncSession):
    filters = store.model_dump()
    result = await repository.delete(model, session, **filters)
    if not result:
        return JSONResponse(
            {"msg": "Can't delete a store with this ID."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result
