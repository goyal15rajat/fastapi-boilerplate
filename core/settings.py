from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "boilerplate"
    DEBUG: bool = False
    ENV: str = "prod"
    CUSTOMER_CODE: str = "internal"
    ENV_CODE: str = "pd"
    MONGO_HOST: str = "127.0.0.1"
    MONGO_PORT: str = "27017"
    MONGO_DBNAME: str = "innote-vision"
    REDOC_URL: str = None
    DOCS_URL: str = None

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
