from uuid import UUID

from fastapi import APIRouter, Query, status

from models.location import Store
from schemas.response import SingleStoreResponse, StoreResponse
from schemas.store import CreateStore, DeleteStore, UpdateStore
from services.store import (
    delete_store_by_id,
    get_list_of_stores,
    get_single_store,
    new_store,
    update_store_by_id
)
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/store", tags=["Store"])


@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(store: CreateStore, repository: repository_dependency, session: db_dependency):
    return await new_store(store, Store, repository, session)


@router.get("/{store_id}", response_model=SingleStoreResponse, status_code=status.HTTP_200_OK)
async def get_store(store_id: UUID, repository: repository_dependency, session: db_dependency):
    return await get_single_store(store_id, Store, repository, session)


@router.get(
    "/",
    response_model=dict[str, dict[str, int | None] | list[StoreResponse | None]],
    status_code=status.HTTP_200_OK,
)
async def get_stores(
    repository: repository_dependency,
    session: db_dependency,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    return await get_list_of_stores(size, page, Store, repository, session)


@router.put("/", response_model=StoreResponse, status_code=status.HTTP_200_OK)
async def update_store(store: UpdateStore, repository: repository_dependency, session: db_dependency):
    return await update_store_by_id(store, Store, repository, session)


@router.delete("/", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_store(store: DeleteStore, repository: repository_dependency, session: db_dependency):
    return await delete_store_by_id(store, Store, repository, session)
