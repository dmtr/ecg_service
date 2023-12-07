from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict


class EcgBaseModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: lambda d: d.isoformat(), ObjectId: lambda d: str(d)},
        populate_by_name=True,
    )
