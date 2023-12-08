from typing import AsyncGenerator

import pytest
import pytest_asyncio
from ecg_service.database import get_database
from ecg_service.ecg.repository import EcgRepository
from ecg_service.ecg.schemas import Analysis, ECGInput

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

    @pytest.fixture
    def ecg_input(self):
        return ECGInput(
            **{
                "id": "ecg_id",
                "date": "2023-12-08T15:57:29.700000",
                "leads": [
                    {"name": "aVL", "number of samples": 3, "signal": [0, 1, -1]}
                ],
            }
        )

    async def test_create_ecg(self, repository, ecg_input):
        res = await repository.create_ecg(ecg_input)
        assert res
        res = await repository.get_ecg_by_id(ecg_input.id)
        assert res.id == "ecg_id"

    async def test_add_analysis(self, repository, ecg_input):
        ecg_input.id = "ecg_id2"
        await repository.create_ecg(ecg_input)
        analysis = Analysis(
            analysis="ZeroCrossingsAnalyzer", result={"lead": "aVL", "value": 2}
        )
        res = await repository.add_analysis(ecg_input.id, analysis)
        assert res
        res = await repository.get_ecg_by_id(ecg_input.id)
        assert res.analysis[0].analysis == "ZeroCrossingsAnalyzer"
        assert res.analysis[0].result.model_dump() == {"lead": "aVL", "value": 2}
