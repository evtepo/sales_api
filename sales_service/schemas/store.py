from uuid import UUID

from pydantic import BaseModel


class StoreIdMixin(BaseModel):
    id: UUID


class StoreMixin(BaseModel):
    name: str
    city_id: UUID


class CreateStore(StoreMixin): ...


class UpdateStore(StoreIdMixin, StoreMixin): ...


class DeleteStore(StoreIdMixin): ...
