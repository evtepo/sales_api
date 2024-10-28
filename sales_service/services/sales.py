from datetime import datetime, timedelta, UTC
from uuid import UUID, uuid4

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.product import Product, Sales
from repository.repository import BaseRepository
from schemas.sales import CreateSale, DeleteSale, UpdateSale
from utils.error_handling import error_response


class SalesLogic:
    async def new_sale(self, sale: CreateSale, session: AsyncSession) -> Sales | JSONResponse:
        data = sale.model_dump()
        data["amount"], data["price"], data["id"] = 0, 0, uuid4()
        products = data.get("products")
        del data["products"]
        if not products:
            return error_response("Products cannot be empty.", status.HTTP_400_BAD_REQUEST)

        instance = Sales(**data)
        session.add(instance)

        error = await self.__change_product_sale(instance, "POST", products, session)
        if error:
            return error

        await session.commit()
        await session.refresh(instance)

        return instance

    async def get_single_sale(self, sale_id: UUID, repository: BaseRepository, session: AsyncSession) -> Sales | JSONResponse:
        filters = {"id": sale_id}
        related_fields = ("products",)
        result = await repository.get_single(Sales, session, related_fields, **filters)
        if not result:
            return error_response("Sale with such ID not found.")

        return result

    async def get_list_of_sales(
        self,
        limit: int,
        offset: int,
        city: UUID | None,
        store: UUID | None,
        product: UUID | None,
        days: int | None,
        price: float | None,
        amount: int | None,
        session: AsyncSession,
    ) -> dict[str, dict[str, int] | list[Sales]]:
        query = select(Sales)
        if city:
            query = query.filter(Sales.city_id == city)

        if store:
            query = query.filter(Sales.store_id == store)

        if product:
            query = query.join(Sales.products).filter(Product.id == product)

        if days:
            current_time = datetime.now(UTC) - timedelta(days)
            query = query.filter(Sales.sale_date >= current_time)

        if price:
            if price < 0:
                query = query.filter(Sales.price <= price * -1)
            else:
                query = query.filter(Sales.price >= price)

        if amount:
            if amount < 0:
                query = query.filter(Sales.amount <= amount * -1)
            else:
                query = query.filter(Sales.amount >= amount)

        offset_arg = (offset - 1) * limit
        query = query.limit(limit).offset(offset_arg)
        result = await session.execute(query)
        result = result.scalars().all()

        prev_page = offset - 1 if offset > 1 else None
        next_page = offset + 1 if len(result) == limit else None

        return {
            "links": {
                "prev": prev_page,
                "next": next_page,
            },
            "data": result,
        }

    async def update_sale_by_id(self, sale: UpdateSale, session: AsyncSession) -> Sales | JSONResponse:
        data = sale.model_dump()
        filters = {"id": data.get("id")}
        products = data.get("products")
        del data["products"]
        if not products:
            return error_response("Products cannot be empty.", status.HTTP_400_BAD_REQUEST)

        select_query = select(Sales).filter_by(**filters)
        instance = await session.execute(select_query)
        instance = instance.scalar_one_or_none()
        if not instance:
            return error_response("Can't update a sale with this ID.")

        error = await self.__change_product_sale(instance, "PUT", products, session)
        if error:
            return error

        update_query = update(Sales).values(**data).filter_by(**filters)
        await session.execute(update_query)
        await session.commit()
        await session.refresh(instance)

        return instance

    async def delete_sale_by_id(self, sale: DeleteSale, session: AsyncSession) -> dict[str, str] | JSONResponse:
        data = sale.model_dump()
        filters = {"id": data.get("id")}
        select_query = select(Sales).filter_by(**filters).options(joinedload(Sales.products))
        instance = await session.execute(select_query)
        instance = instance.unique().scalar_one_or_none()
        if not instance:
            return error_response("Can't delete a sale with this ID.")

        products = (product.id for product in instance.products)
        error = await self.__change_product_sale(instance, "DELETE", products, session)
        if error:
            return error

        delete_query = delete(Sales).filter_by(**filters)
        await session.execute(delete_query)
        await session.commit()

        return {"msg": "Successfully deleted."}

    async def __change_product_sale(
        self,
        instance: Sales,
        method: str,
        products: list[UUID],
        session: AsyncSession,
    ) -> None | JSONResponse:
        """
        Метод для удаления или добавления Sales ID в Product.
        """
        price, amount = 0.0, 0
        for product_id in products:
            filters = {"id": product_id}
            query = select(Product).filter_by(**filters)

            product = await session.execute(query)
            product = product.scalar_one_or_none()
            if not product:
                await session.rollback()
                return error_response("Wrong Product ID.", status.HTTP_400_BAD_REQUEST)

            if method in ("POST", "PUT"):
                price += float(product.price)
                amount += 1
                product.sales_id = instance.id
            else:
                product.sales_id = None

        instance.price = price
        instance.amount = amount

        return None


sale_logic = SalesLogic()


async def get_sales_logic():
    return sale_logic
