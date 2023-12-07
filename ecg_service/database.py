import motor.motor_asyncio

from ecg_service.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(str(settings.MONGODB_URL))


def get_database() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return client.ecg_service
