import datetime

from bson import ObjectId
from ecg_service.database import get_database
from ecg_service.ecg.schemas import ECGInput, ECGResponse


class EcgRepository:
    def __init__(self, db: "motor.motor_asyncio.AsyncIOMotorDatabase" = get_database()):
        self.db = db

    async def create_ecg(self, ecg_input: ECGInput) -> ObjectId:
        ecg = ECGResponse(
            **ecg_input.model_dump(),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        res = await self.db.ecg.insert_one(ecg.model_dump())
        return res.inserted_id

    async def get_ecg_by_id(self, ecg_id: str) -> ECGResponse:
        ecg = await self.db.ecg.find_one({"id": ecg_id})
        if ecg:
            return ECGResponse(**ecg)
