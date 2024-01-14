from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Telegram OAuth"
    PROJECT_URL: str = "http://127.0.0.1:8081"
    PROJECT_HOST: str = "127.0.0.1"
    PROJECT_PORT: int = 8001
    DEBUG: bool = True

    CONN_URI: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    ACCESS_TOKEN_EXP: int = 900  # 15 minutes
    REFRESH_TOKEN_EXP: int = 86400  # 1 day

    CORS_ORIGINS: List[str] = ["*"]

    BOT_TOKEN: str
    BOT_USERNAME: str
    BOT_API_ID: int
    BOT_API_HASH: str
    BOT_MANAGER_IDS: List[int]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
