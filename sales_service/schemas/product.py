from uuid import UUID

from pydantic import BaseModel, field_validator


class ProductIdMixin(BaseModel):
    id: UUID


class ProductMixin(BaseModel):
    name: str
    description: str | None
    price: float
    store_id: UUID

    @field_validator("price")
    def validate_price(cls, price: float) -> float:
        if price < 0:
            raise ValueError("Price must be greater than or equal to 0.")

        return price


class CreateProduct(ProductMixin): ...


class UpdateProduct(ProductIdMixin, ProductMixin): ...


class DeleteProduct(ProductIdMixin): ...
