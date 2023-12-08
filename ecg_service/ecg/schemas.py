from datetime import datetime
from typing import List, Optional

from ecg_service.models import EcgBaseModel
from pydantic import Field, model_validator
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class LeadInput(EcgBaseModel):
    name: str
    number_of_samples: Optional[int] = Field(None)
    signal: List[int]

    @model_validator(mode="after")
    def calculate_number_of_samples(self):
        if self.number_of_samples is None:
            self.number_of_samples = len(self.signal)
        return self


class ECGInput(EcgBaseModel):
    id: str
    date: datetime
    leads: List[LeadInput]


class AnalysisResult(EcgBaseModel):
    lead: str
    value: float


class Analysis(EcgBaseModel):
    analysis: str
    result: AnalysisResult


class ECGResponse(ECGInput):
    analysis: List[Analysis] = []
    created_at: datetime
    updated_at: datetime
