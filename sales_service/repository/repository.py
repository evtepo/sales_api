from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.location import City, Store
from models.product import Product, Sales


Model = TypeVar("Model", City, Product, Sales, Store)


class BaseRepository(ABC):
    @abstractmethod
    async def get_single(
        self,
        model: Model,
        session: AsyncSession,
        related_fields: tuple[str] | None = None,
        **filters,
    ) -> Model: ...

    @abstractmethod
    async def get_list(self, model: Model, session: AsyncSession, limit: int, offset: int, **filters) -> list[Model | None]: ...

    @abstractmethod
    async def create(self, data: dict, model: Model, session: AsyncSession) -> Model: ...

    @abstractmethod
    async def update(self, data: dict, model: Model, session: AsyncSession, **filters) -> Model: ...

    @abstractmethod
    async def delete(self, model: Model, session: AsyncSession, **filters) -> dict[str, str] | None: ...


class PostgresRepository(BaseRepository):
    async def get_single(
        self,
        model: Model,
        session: AsyncSession,
        related_fields: tuple[str] | None = None,
        **filters,
    ) -> Model | None:
        query = select(model).filter_by(**filters)
        if related_fields:
            query = query.options(*(joinedload(getattr(model, field)) for field in related_fields))

        data = await session.execute(query)

        return data.unique().scalar_one_or_none()

    async def get_list(self, model: Model, session: AsyncSession, limit: int, offset: int, **filters) -> list[Model | None]:
        query = select(model).filter_by(**filters).limit(limit).offset(offset)
        result = await session.execute(query)

        return result.scalars().all()

    async def create(self, data: dict, model: Model, session: AsyncSession) -> Model:
        instance = model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)

        return instance

    async def update(self, data: dict, model: Model, session: AsyncSession, **filters) -> Model:
        update_query = update(model).values(**data).filter_by(**filters)
        await session.execute(update_query)
        await session.commit()

        select_query = select(model).filter_by(**filters)
        instance = await session.execute(select_query)

        return instance.scalar_one_or_none()

    async def delete(self, model: Model, session: AsyncSession, **filters) -> dict[str, str] | None:
        select_query = select(model).filter_by(**filters)
        instance = await session.execute(select_query)
        if not instance.scalar_one_or_none():
            return None

        delete_query = delete(model).filter_by(**filters)
        await session.execute(delete_query)
        await session.commit()

        return {"msg": "Successfully deleted."}


repository: BaseRepository | None = PostgresRepository()


async def get_repository():
    return repository
