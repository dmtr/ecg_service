import numpy as np
from ecg_service.ecg.analyzers.base import BaseAnalyzer
from ecg_service.ecg.schemas import Analysis, AnalysisResult, ECGResponse


class ZeroCrossingsAnalyzer(BaseAnalyzer):
    name = "ZeroCrossingsAnalyzer"

    @staticmethod
    def count_zero_crossings(data: list[int]) -> int:
        data_array = np.array(data)
        non_zero_data = data_array[data_array != 0]
        sign_changes = np.diff(np.sign(non_zero_data)) != 0
        return np.sum(sign_changes)

    def analyze(self, ecg: ECGResponse) -> list[Analysis]:
        res = []
        for lead in ecg.leads:
            result = AnalysisResult(
                lead=lead.name,
                value=self.count_zero_crossings(lead.signal),
            )
            res.append(Analysis(analysis=self.name, result=result))
        return res
