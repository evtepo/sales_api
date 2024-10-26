from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SaleIdMixin(BaseModel):
    id: UUID


class SaleMixin(BaseModel):
    store_id: UUID
    city_id: UUID


class CreateSale(SaleMixin):
    products: list[UUID]


class UpdateSale(SaleIdMixin, CreateSale): ...


class DeleteSale(SaleIdMixin): ...
