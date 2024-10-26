from uuid import UUID

from pydantic import BaseModel


class NameCityMixin(BaseModel):
    name: str


class CityIdMixin(BaseModel):
    id: UUID


class CreateCity(NameCityMixin): ...


class UpdateCity(CityIdMixin, NameCityMixin): ...


class DeleteCity(CityIdMixin): ...
