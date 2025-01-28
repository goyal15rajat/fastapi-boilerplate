from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from core.settings import app_configs
from core.utils.loggers.app_logger import app_logger

class MongoConnectionSingleton:
    _instance = None
    _client: Optional[AsyncIOMotorClient] = None
    _database_name = app_configs.MONGO_DBNAME

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnectionSingleton, cls).__new__(cls)
        return cls._instance

    async def connect(self):
        if self._client is None:
            try:
                self._client = AsyncIOMotorClient(f"mongodb://{app_configs.MONGO_HOST}:{app_configs.MONGO_PORT}/")
                database = self._client[MongoConnectionSingleton._database_name]
                # Initialize Beanie (replace with your own models)
                await init_beanie(database, document_models=[])
                app_logger.info("MongoDB connection established")
            except Exception as e:
                app_logger.exception(f"Failed to connect to MongoDB: {e}")
                raise
        return self._client

    async def close(self):
        if self._client:
            self._client.close()
            self._client = None
            app_logger.info("MongoDB connection closed")