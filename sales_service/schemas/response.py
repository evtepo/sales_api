from datetime import datetime

from schemas.city import IdCityMixin, NameCityMixin
from schemas.product import ProductIdMixin, ProductMixin
from schemas.store import StoreIdMixin, StoreMixin


class CityResponse(IdCityMixin, NameCityMixin):
    class Config:
        from_attributes = True


class StoreResponse(StoreIdMixin, StoreMixin):
    class Config:
        from_attributes = True


class ProductResponse(ProductIdMixin, ProductMixin):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SingleCityResponse(CityResponse):
    stores: list[None | StoreResponse]


class SingleProductResponse(ProductResponse):
    # Добавить Sales
    store: StoreResponse


class SingleStoreResponse(StoreResponse):
    city: CityResponse
    products: list[None | ProductResponse]
