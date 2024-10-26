from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from schemas.response import SingleStoreResponse, StoreResponse
from schemas.store import CreateStore, DeleteStore, UpdateStore
from services.store import get_store_service, StoreService
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/store", tags=["Store"])

store_dependency = Annotated[StoreService, Depends(get_store_service)]


@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store: CreateStore,
    repository: repository_dependency,
    session: db_dependency,
    store_service: store_dependency,
):
    return await store_service.new_store(store, repository, session)


@router.get("/{store_id}", response_model=SingleStoreResponse, status_code=status.HTTP_200_OK)
async def get_store(
    store_id: UUID,
    repository: repository_dependency,
    session: db_dependency,
    store_service: store_dependency,
):
    return await store_service.get_single_store(store_id, repository, session)


@router.get(
    "/",
    response_model=dict[str, dict[str, int | None] | list[StoreResponse | None]],
    status_code=status.HTTP_200_OK,
)
async def get_stores(
    repository: repository_dependency,
    session: db_dependency,
    store_service: store_dependency,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    return await store_service.get_list_of_stores(size, page, repository, session)


@router.put("/", response_model=StoreResponse, status_code=status.HTTP_200_OK)
async def update_store(
    store: UpdateStore,
    repository: repository_dependency,
    session: db_dependency,
    store_service: store_dependency,
):
    return await store_service.update_store_by_id(store, repository, session)


@router.delete("/", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_store(
    store: DeleteStore,
    repository: repository_dependency,
    session: db_dependency,
    store_service: store_dependency,
):
    return await store_service.delete_store_by_id(store, repository, session)
