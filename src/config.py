from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Telegram OAuth"
    PROJECT_HOST: str = "127.0.0.1"
    PROJECT_PORT: int = 8001
    DEBUG: bool = True

    CONN_URI: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    ACCESS_TOKEN_EXP: int = 900  # 15 minutes
    REFRESH_TOKEN_EXP: int = 86400  # 1 day

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()