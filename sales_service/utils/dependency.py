from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connect import get_session
from repository.repository import BaseRepository, get_repository
from services.sales import get_sales_logic, SalesLogic


db_dependency = Annotated[AsyncSession, Depends(get_session)]
repository_dependency = Annotated[BaseRepository, Depends(get_repository)]

sale_dependency = Annotated[SalesLogic, Depends(get_sales_logic)]
