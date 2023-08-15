"""Configuration module."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class."""

    VIDEO_PATH: str = "./video_data"
    DATE_INPUT_FORMAT: str = "%d/%m/%Y %H%p"

    POSTGRES_DB: str = "satlink_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    PG_HOST: str = "localhost"
    PG_PORT: str = "5432"
    PG_VIDEO_TABLE_NAME: str = "video"

    class Config:
        """Config class."""

        case_sensitive = True
        env_file = "./.env"
        env_file_encoding = "utf-8"


settings = Settings()
