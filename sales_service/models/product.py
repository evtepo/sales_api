from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, func, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_connect import Base
from models.base import TableMixin
from models.location import Store


class Sales(Base, TableMixin):
    store_id: Mapped[UUID] = mapped_column(ForeignKey("store.id", ondelete="CASCADE"), nullable=False)
    city_id: Mapped[UUID] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(precision=9, scale=2), nullable=False)
    sale_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    products: Mapped[list["Product"]] = relationship(back_populates="sales")


class Product(Base, TableMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(precision=9, scale=2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    store_id: Mapped[UUID] = mapped_column(ForeignKey("store.id", ondelete="CASCADE"), nullable=False)
    sales_id: Mapped[UUID | None] = mapped_column(ForeignKey("sales.id", ondelete="CASCADE"))

    sales: Mapped["Sales"] = relationship(back_populates="products")
    store: Mapped["Store"] = relationship(back_populates="products")
