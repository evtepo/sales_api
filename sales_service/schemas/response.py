from datetime import datetime
from uuid import UUID

from schemas.city import CityIdMixin, NameCityMixin
from schemas.product import ProductIdMixin, ProductMixin
from schemas.sales import SaleIdMixin, SaleMixin
from schemas.store import StoreIdMixin, StoreMixin


class BaseResponse:
    class Config:
        from_attributes = True


class CityResponse(BaseResponse, CityIdMixin, NameCityMixin): ...


class StoreResponse(BaseResponse, StoreIdMixin, StoreMixin): ...


class ProductResponse(BaseResponse, ProductIdMixin, ProductMixin):
    sales_id: UUID | None
    created_at: datetime
    updated_at: datetime


class SaleResponse(BaseResponse, SaleIdMixin, SaleMixin):
    amount: int
    price: float
    sale_date: datetime


class SingleCityResponse(CityResponse):
    stores: list[None | StoreResponse]


class SingleProductResponse(ProductResponse):
    sales: SaleResponse | None
    store: StoreResponse


class SingleStoreResponse(StoreResponse):
    city: CityResponse
    products: list[None | ProductResponse]


class SingleSaleResponse(SaleResponse):
    products: list[None | ProductResponse]
