from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME = "app"
    BACKEND_CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost",
    ]
    API_PREFIX = "/api"
    HOST = "localhost"
    PORT = 5000
    BASE_URL = "{}:{}/".format(HOST, str(PORT))
    MODELS = [
        "app.models.users",
    ]

    class Config:
        case_sensitive: bool = True


@lru_cache
def get_setting():
    return Settings()
