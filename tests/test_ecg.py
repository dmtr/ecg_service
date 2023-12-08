from typing import AsyncGenerator

import pytest
import pytest_asyncio
from ecg_service import ecg
from ecg_service.database import get_database
from ecg_service.ecg.repository import EcgRepository
from ecg_service.ecg.schemas import ECGInput, ECGResponse

pytestmark = pytest.mark.asyncio(scope="module")


class TestEcgRepository:
    @pytest_asyncio.fixture(scope="module", autouse=True)
    async def db(self) -> AsyncGenerator:
        db = get_database()

        await db.ecg.create_index("id", unique=True)

        yield

        await db.drop_collection("ecg")

    @pytest.fixture
    def repository(self):
        return EcgRepository()

    async def test_create_ecg(self, repository):
        ecg_input = ECGInput(
            **{
                "id": "ecg_id",
                "date": "2023-12-08T15:57:29.700000",
                "leads": [
                    {"name": "aVL", "number of samples": 3, "signal": [0, 1, -1]}
                ],
            }
        )
        res = await repository.create_ecg(ecg_input)
        assert res
