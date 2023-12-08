from typing import AsyncGenerator

import pytest
import pytest_asyncio
from ecg_service.database import get_database
from ecg_service.user.repository import UserRepository

pytestmark = pytest.mark.asyncio(scope="session")


class TestUserRepository:
    @pytest_asyncio.fixture(scope="session", autouse=True)
    async def db(self) -> AsyncGenerator:
        db = get_database()

        await db.user.create_index("email", unique=True)

        yield

        await db.drop_collection("user")

    @pytest.fixture
    def repository(self):
        return UserRepository()

    async def test_create_admin(self, repository):
        email = "test@t1.com"
        user_id = await repository.create_admin(email=email, password="test")
        assert user_id
        user = await repository.get_user_by_email(email=email)
        assert user
        assert user.email == email
        assert user.role == "ADMIN"
        user = await repository.get_user_by_id(user_id)
        assert user
        assert user.email == email
        assert user.role == "ADMIN"

    async def test_create_customer(self, repository):
        email = "test@t2.com"
        user_id = await repository.create_customer(email=email, password="test")
        assert user_id
        user = await repository.get_user_by_email(email=email)
        assert user
        assert user.email == email
        assert user.role == "CUSTOMER"
