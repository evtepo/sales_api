from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.location import Store
from repository.repository import BaseRepository
from schemas.store import CreateStore, DeleteStore, UpdateStore
from utils.error_handling import error_response


async def new_store(store: CreateStore, repository: BaseRepository, session: AsyncSession):
    data = store.model_dump()
    return await repository.create(data, Store, session)


async def get_single_store(store_id: UUID, repository: BaseRepository, session: AsyncSession):
    filters = {"id": store_id}
    related_fields = ("city", "products")
    result = await repository.get_single(Store, session, related_fields, **filters)
    if not result:
        return error_response("Store with such ID not found.")

    return result


async def get_list_of_stores(limit: int, offset: int, repository: BaseRepository, session: AsyncSession):
    offset_arg = (offset - 1) * limit
    result = await repository.get_list(Store, session, limit, offset_arg)

    prev_page = offset - 1 if offset > 1 else None
    next_page = offset + 1 if len(result) == limit else None

    return {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
        "data": result,
    }


async def update_store_by_id(store: UpdateStore, repository: BaseRepository, session: AsyncSession):
    data = store.model_dump()
    filters = {"id": data.get("id")}
    result = await repository.update(data, Store, session, **filters)
    if not result:
        return error_response("Can't update a store with this ID.")

    return result


async def delete_store_by_id(store: DeleteStore, repository: BaseRepository, session: AsyncSession):
    filters = store.model_dump()
    result = await repository.delete(Store, session, **filters)
    if not result:
        return error_response("Can't delete a store with this ID.")

    return result
