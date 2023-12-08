import logging

from ecg_service.ecg.analyzers import analyzers
from ecg_service.ecg.repository import EcgRepository
from ecg_service.ecg.schemas import ECGResponse

logger = logging.getLogger(__name__)


async def analyze(ecg: ECGResponse) -> None:
    logger.info("Analyzing ECG %s", ecg.id)

    ecg_repository = EcgRepository()

    for analyzer in analyzers:
        res = analyzer().analyze(ecg)
        for analysis in res:
            await ecg_repository.add_analysis(ecg.id, analysis)

    logger.info("Finished analyzing ECG %s", ecg.id)
