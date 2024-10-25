from uuid import UUID, uuid4

from sqlalchemy.orm import declared_attr, Mapped, mapped_column


class TableMixin:
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
