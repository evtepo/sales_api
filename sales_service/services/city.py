from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.location import City
from repository.repository import BaseRepository
from schemas.city import CreateCity, DeleteCity, UpdateCity
from utils.error_handling import error_response


async def new_city(data: CreateCity, repository: BaseRepository, session: AsyncSession):
    data = data.model_dump()
    return await repository.create(data, City, session)


async def get_single_city(city_id: UUID, repository: BaseRepository, session: AsyncSession):
    filters = {"id": city_id}
    related_fields = ("stores",)
    result = await repository.get_single(City, session, related_fields, **filters)
    if not result:
        return error_response("City with such ID not found.")

    return result


async def get_list_of_cities(offset: int, limit: int, repository: BaseRepository, session: AsyncSession):
    offset_arg = (offset - 1) * limit
    result = await repository.get_list(City, session, limit, offset_arg)

    prev_page = offset - 1 if offset > 1 else None
    next_page = offset + 1 if len(result) == limit else None

    return {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
        "data": result,
    }


async def update_city_by_id(data: UpdateCity, repository: BaseRepository, session: AsyncSession):
    data = data.model_dump()
    filters = {"id": data.get("id")}
    result = await repository.update(data, City, session, **filters)
    if not result:
        return error_response("Can't update a city with this ID.")

    return result


async def delete_city_by_id(data: DeleteCity, repository: BaseRepository, session: AsyncSession):
    filters = data.model_dump()
    result = await repository.delete(City, session, **filters)
    if not result:
        return error_response("Can't delete a city with this ID.")

    return result
