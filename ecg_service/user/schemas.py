from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr
    role: UserRole
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    ecgs: list[str] = []

    @field_validator("email", mode="before")
    def email_to_lower(cls, v: str) -> str:
        return v.lower()

    @property
    def database_id(self) -> Optional[ObjectId]:
        if self.id is not None:
            return ObjectId(self.id)


class UserResponse(BaseModel):
    email: EmailStr
    role: UserRole

    @classmethod
    def from_user(cls, user: User) -> "UserResponse":
        return cls(
            email=user.email,
            role=user.role,
        )
