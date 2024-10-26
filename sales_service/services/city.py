from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.location import City
from repository.repository import BaseRepository
from schemas.city import CreateCity, DeleteCity, UpdateCity
from services.base import BaseService


class CityService(BaseService):
    async def new_city(self, data: CreateCity, repository: BaseRepository, session: AsyncSession):
        return await self.create_new_row(data, City, repository, session)

    async def get_single_city(self, city_id: UUID, repository: BaseRepository, session: AsyncSession):
        related_fields = ("stores",)
        return await self.get_single_row(city_id, related_fields, City, repository, session)

    async def get_list_of_cities(self, offset: int, limit: int, repository: BaseRepository, session: AsyncSession):
        return await self.get_list_rows(offset, limit, City, repository, session)

    async def update_city_by_id(self, data: UpdateCity, repository: BaseRepository, session: AsyncSession):
        return await self.update_row_by_id(data, City, repository, session)

    async def delete_city_by_id(self, data: DeleteCity, repository: BaseRepository, session: AsyncSession):
        return await self.delete_row_by_id(data, City, repository, session)


city_service = CityService()


async def get_city_service():
    return city_service
