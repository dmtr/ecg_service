import datetime

from bson import ObjectId
from ecg_service.database import get_database
from ecg_service.user.auth import get_password_hash
from ecg_service.user.schemas import User, UserRole


class UserRepository:
    def __init__(self, db: "motor.motor_asyncio.AsyncIOMotorDatabase" = get_database()):
        self.db = db

    async def _create_user(self, email: str, password: str, role: UserRole) -> ObjectId:
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            role=role,
            hashed_password=hashed_password,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        res = await self.db.user.insert_one(user.model_dump())
        return res.inserted_id

    async def create_customer(self, email: str, password: str) -> ObjectId:
        return await self._create_user(email, password, UserRole.CUSTOMER)

    async def create_admin(self, email: str, password: str) -> ObjectId:
        return await self._create_user(email, password, UserRole.ADMIN)

    async def get_user_by_email(self, email: str) -> User:
        user = await self.db.user.find_one({"email": email})
        if user:
            return User(**user)

    async def get_user_by_id(self, user_id: ObjectId) -> User:
        user = await self.db.user.find_one({"_id": user_id})
        if user:
            return User(**user)
