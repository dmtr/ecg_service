from pydantic import BaseModel, ConfigDict


class EcgBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
