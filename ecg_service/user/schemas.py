from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


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


class UserResponse(BaseModel):
    email: EmailStr
    role: UserRole

    @classmethod
    def from_user(cls, user: User) -> "UserResponse":
        return cls(
            email=user.email,
            role=user.role,
        )
