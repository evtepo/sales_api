from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from schemas.response import CityResponse, SingleCityResponse
from schemas.city import CreateCity, DeleteCity, UpdateCity
from services.city import CityService, get_city_service
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/city", tags=["City"])

city_dependency = Annotated[CityService, Depends(get_city_service)]


@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(
    city: CreateCity,
    repository: repository_dependency,
    session: db_dependency,
    city_service: city_dependency,
):
    return await city_service.new_city(city, repository, session)


@router.get("/{city_id}", response_model=SingleCityResponse, status_code=status.HTTP_200_OK)
async def get_city(
    city_id: UUID,
    repository: repository_dependency,
    session: db_dependency,
    city_service: city_dependency,
):
    return await city_service.get_single_city(city_id, repository, session)


@router.get(
    "/",
    response_model=dict[str, dict[str, int | None] | list[CityResponse | None]],
    status_code=status.HTTP_200_OK,
)
async def get_cities(
    repository: repository_dependency,
    session: db_dependency,
    city_service: city_dependency,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    return await city_service.get_list_of_cities(page, size, repository, session)


@router.put("/", response_model=CityResponse, status_code=status.HTTP_200_OK)
async def update_city(
    city: UpdateCity,
    repository: repository_dependency,
    session: db_dependency,
    city_service: city_dependency,
):
    return await city_service.update_city_by_id(city, repository, session)


@router.delete("/", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_city(
    city: DeleteCity,
    repository: repository_dependency,
    session: db_dependency,
    city_service: city_dependency,
):
    return await city_service.delete_city_by_id(city, repository, session)
