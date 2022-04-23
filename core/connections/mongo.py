from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from ..settings import app_configs


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


def connect_to_mongo():
    client = AsyncIOMotorClient(f"mongodb://{app_configs.MONGO_HOST}:{app_configs.MONGO_PORT}/")
    db.client = AIOEngine(motor_client=client, database=app_configs.MONGO_DBNAME)


async def close_mongo_connection():
    db.client.close()
