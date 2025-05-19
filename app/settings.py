from pydantic.v1.env_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    API_KEY: str = config("API_KEY", cast=str)
    DATABASE_URL: str = config("DATABASE_URL", cast=str)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
