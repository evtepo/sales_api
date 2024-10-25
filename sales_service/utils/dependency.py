from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connect import get_session
from repository.repository import BaseRepository, get_repository


db_dependency = Annotated[AsyncSession, Depends(get_session)]
repository_dependency = Annotated[BaseRepository, Depends(get_repository)]
