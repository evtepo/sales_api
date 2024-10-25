from uuid import UUID

from fastapi import APIRouter, Query, status

from models.location import City
from schemas.response import CityResponse, SingleCityResponse
from schemas.city import CreateCity, DeleteCity, UpdateCity
from services.city import (
    delete_city_by_id,
    get_list_of_cities,
    get_single_city,
    new_city,
    update_city_by_id
)
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/city", tags=["City"])


@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(city: CreateCity, repository: repository_dependency, session: db_dependency):
    return await new_city(city, City, repository, session)


@router.get("/{city_id}", response_model=SingleCityResponse, status_code=status.HTTP_200_OK)
async def get_city(city_id: UUID, repository: repository_dependency, session: db_dependency):
    return await get_single_city(city_id, City, repository, session)


@router.get(
    "/",
    response_model=dict[str, dict[str, int | None] | list[CityResponse | None]],
    status_code=status.HTTP_200_OK,
)
async def get_cities(
    repository: repository_dependency,
    session: db_dependency,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    return await get_list_of_cities(page, size, City, repository, session)


@router.put("/", response_model=CityResponse, status_code=status.HTTP_200_OK)
async def update_city(city: UpdateCity, repository: repository_dependency, session: db_dependency):
    return await update_city_by_id(city, City, repository, session)


@router.delete("/", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_city(city: DeleteCity, repository: repository_dependency, session: db_dependency):
    return await delete_city_by_id(city, City, repository, session)
