import os

import pythonjsonlogger
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Initialize templates
templates = Jinja2Templates(directory="templates")


class Settings(BaseSettings):
    APP_NAME: str = "boilerplate"
    DEBUG: bool = False
    ENV: str = "prod"
    CUSTOMER_CODE: str = "internal"
    MONGO_HOST: str = "127.0.0.1"
    MONGO_PORT: str = "27017"
    MONGO_DBNAME: str = "boilerplate"
    REDOC_URL: str = "/redoc"
    DOCS_URL: str = "/doc"
    LOGGING_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": "DEBUG"},
        },
    }
    REDIS_KEY_PREFIX: str = "boilerplate"
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: str = "6379"
    REDIS_DBNAME: int = 2
    PING_TIMEOUT: int = 10
    PING_INTERVAL: int = 60

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()


class DevSettings(Settings):
    DEBUG: bool = True
    REDOC_URL: str = "/redoc"
    DOCS_URL: str = "/doc"


class ProductionSettings(Settings):
    DEBUG: bool = False


class TestingSettings(Settings):
    DEBUG: bool = False


if settings.ENV == "prod":
    app_configs = ProductionSettings()
elif settings.ENV == "test":
    app_configs = TestingSettings()
elif settings.ENV == "dev":
    app_configs = DevSettings()
else:
    app_configs = Settings()
