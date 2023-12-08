from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"


class User(BaseModel):
    email: EmailStr
    role: UserRole
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    @field_validator("email", mode="before")
    def email_to_lower(cls, v: str) -> str:
        return v.lower()
