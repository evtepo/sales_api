from uuid import UUID

from pydantic import BaseModel


class ProductIdMixin(BaseModel):
    id: UUID


class ProductMixin(BaseModel):
    name: str
    description: str | None
    price: float
    store_id: UUID
    sales_id: UUID | None


class CreateProduct(ProductMixin): ...


class UpdateProduct(ProductIdMixin, ProductMixin): ...


class DeleteProduct(ProductIdMixin): ...
