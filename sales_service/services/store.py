from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.location import Store
from repository.repository import BaseRepository
from schemas.store import CreateStore, DeleteStore, UpdateStore
from services.base import BaseService


class StoreService(BaseService):
    async def new_store(self, store: CreateStore, repository: BaseRepository, session: AsyncSession):
        return await self.create_new_row(store, Store, repository, session)

    async def get_single_store(self, store_id: UUID, repository: BaseRepository, session: AsyncSession):
        related_fields = ("city", "products")
        return await self.get_single_row(store_id, related_fields, Store, repository, session)

    async def get_list_of_stores(self, limit: int, offset: int, repository: BaseRepository, session: AsyncSession):
        return await self.get_list_rows(offset, limit, Store, repository, session)

    async def update_store_by_id(self, store: UpdateStore, repository: BaseRepository, session: AsyncSession):
        return await self.update_row_by_id(store, Store, repository, session)

    async def delete_store_by_id(self, store: DeleteStore, repository: BaseRepository, session: AsyncSession):
        return await self.delete_row_by_id(store, Store, repository, session)


store_service = StoreService()


async def get_store_service():
    return store_service
