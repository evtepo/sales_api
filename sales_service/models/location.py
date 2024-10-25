from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_connect import Base
from models.base import TableMixin


class City(Base, TableMixin):
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    stores: Mapped[list["Store"]] = relationship(back_populates="city")


class Store(Base, TableMixin):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    city_id: Mapped[UUID] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"), nullable=False)

    city: Mapped["City"] = relationship(back_populates="stores")
    products: Mapped[list["Product"]] = relationship(back_populates="store")
