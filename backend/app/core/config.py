import os
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Template"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/app_db"
    allowed_origins: str = "http://localhost:3000"
    log_level: str = "INFO"
    openai_api_key: str | None = None

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v: str) -> str:
        return v

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

if settings.openai_api_key:
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
