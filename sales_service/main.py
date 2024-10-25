import uvicorn
from fastapi import FastAPI

from api.v1.city import router as city_router
from api.v1.product import router as product_router
from api.v1.store import router as store_router
from configs.settings import settings


app = FastAPI(title=settings.service_name)

app.include_router(city_router)
app.include_router(product_router)
app.include_router(store_router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.service_host,
        port=settings.service_port,
    )
