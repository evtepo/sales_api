from uuid import UUID

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from models.location import Store
from models.product import Product
from repository.repository import BaseRepository
from schemas.product import CreateProduct, DeleteProduct, UpdateProduct
from services.base import BaseService


class ProductService(BaseService):
    async def new_product(self, product: CreateProduct, repository: BaseRepository, session: AsyncSession) -> Product | JSONResponse:
        store_id = product.model_dump().get("store_id")
        check_store = await self.check_row(store_id, Store, session)
        if check_store:
            return check_store

        return await self.create_new_row(product, Product, repository, session)

    async def get_single_product(self, product_id: UUID, repository: BaseRepository, session: AsyncSession) -> Product | JSONResponse:
        related_fields = ("sales", "store")
        return await self.get_single_row(product_id, related_fields, Product, repository, session)

    async def get_list_of_products(self, limit: int, offset: int, repository: BaseRepository, session: AsyncSession) -> dict[str, dict | list[Product]]:
        return await self.get_list_rows(offset, limit, Product, repository, session)

    async def update_product_by_id(self, product: UpdateProduct, repository: BaseRepository, session: AsyncSession) -> Product | JSONResponse:
        store_id = product.model_dump().get("store_id")
        check_store = await self.check_row(store_id, Store, session)
        if check_store:
            return check_store

        return await self.update_row_by_id(product, Product, repository, session)

    async def delete_product_by_id(self, product: DeleteProduct, repository: BaseRepository, session: AsyncSession) -> dict[str, str] | JSONResponse:
        return await self.delete_row_by_id(product, Product, repository, session)


product_service = ProductService()


async def get_product_service():
    return product_service
