from ecg_service.ecg.schemas import ECGResponse


class BaseAnalyzer:
    name: str = "BaseAnalyzer"

    def analyze(self, ecg: ECGResponse):
        raise NotImplementedError("analyze() not implemented")
