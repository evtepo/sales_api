from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from models.location import City
from repository.repository import BaseRepository
from schemas.city import CreateCity, DeleteCity, UpdateCity


async def new_city(data: CreateCity, model: City, repository: BaseRepository, session: AsyncSession):
    data = data.model_dump()
    return await repository.create(data, model, session)


async def get_single_city(city_id: UUID, model: City, repository: BaseRepository, session: AsyncSession):
    filters = {"id": city_id}
    related_fields = ("stores",)
    result = await repository.get_single(model, session, related_fields, **filters)
    if not result:
        return JSONResponse(
            {"msg": "City with such ID not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result


async def get_list_of_cities(
    offset: int,
    limit: int,
    model: City,
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


async def update_city_by_id(data: UpdateCity, model: City, repository: BaseRepository, session: AsyncSession):
    data = data.model_dump()
    filters = {"id": data.get("id")}
    result = await repository.update(data, model, session, **filters)
    if not result:
        return JSONResponse(
            {"msg": "Can't update a city with this ID."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result


async def delete_city_by_id(data: DeleteCity, model: City, repository: BaseRepository, session: AsyncSession):
    filters = data.model_dump()
    result = await repository.delete(model, session, **filters)
    if not result:
        return JSONResponse(
            {"msg": "Can't delete a city with this ID."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result
