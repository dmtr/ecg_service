from datetime import datetime
from typing import List, Optional

from ecg_service.models import EcgBaseModel
from pydantic import Field, validator
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class LeadInput(EcgBaseModel):
    name: str
    number_of_samples: Optional[int] = Field(None, alias="number of samples")
    signal: List[int]

    @validator("number_of_samples", always=True, pre=True)
    def calculate_number_of_samples(cls, v, values):
        if "signal" in values and v is None:
            return len(values["signal"])
        return v


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
