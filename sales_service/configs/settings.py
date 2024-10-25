from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = Field("Sales service", alias="SERVICE_NAME")
    service_host: str = Field("localhost", alias="SERVICE_HOST")
    service_port: int = Field(8000, alias="SERVICE_PORT")

    pg_name: str = Field("sales", alias="POSTGRES_DB")
    pg_user: str = Field("postgres", alias="POSTGRES_USER")
    pg_password: str = Field("postgres", alias="POSTGRES_PASSWORD")
    pg_host: str = Field("localhost", alias="POSTGRES_HOST")
    pg_port: int = Field(5432, alias="POSTGRES_PORT")


settings = Settings()

database_dsn = f"postgresql+asyncpg://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}:{settings.pg_port}/{settings.pg_name}"
