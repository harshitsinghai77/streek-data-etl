from functools import lru_cache
from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    APP_NAME = "app"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    API_PREFIX = "/api"
    HOST = "localhost"
    PORT = 8000
    BASE_URL = "{}:{}/".format(HOST, str(PORT))
    MODELS = [
        "app.models.users",
    ]

    class Config:
        case_sensitive: bool = True


@lru_cache
def get_setting():
    return Settings()
