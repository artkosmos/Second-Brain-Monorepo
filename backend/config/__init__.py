import os
from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.supabase" if os.getenv("DB_TARGET") == "supabase" else ".env",
        extra="ignore",
    )

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_sslmode: str | None = None
    jwt_secret: str
    jwt_algorithm: str
    jwt_access_expiration_time: int
    jwt_refresh_expiration_time: int
    jwt_cookie_name: str
    jwt_refresh_cookie_name: str
    jwt_cookie_secure: bool = False

    app_name: str = "Notes API"
    environment: str = "dev"

    @property
    def database_url(self) -> str:
        user = quote_plus(self.postgres_user)
        password = quote_plus(self.postgres_password)
        url = (
            f"postgresql+psycopg://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

        if self.postgres_sslmode:
            return f"{url}?sslmode={self.postgres_sslmode}"

        return url


@lru_cache
def get_settings() -> Settings:
    return Settings.model_validate({})
