from uuid import UUID

from pydantic import BaseModel


class NameCityMixin(BaseModel):
    name: str


class IdCityMixin(BaseModel):
    id: UUID


class CreateCity(NameCityMixin): ...


class UpdateCity(IdCityMixin, NameCityMixin): ...


class DeleteCity(IdCityMixin): ...