import logging
from typing import Annotated

from ecg_service.user.auth import (create_access_token, decode_token,
                                   verify_password)
from ecg_service.user.repository import UserRepository
from ecg_service.user.schemas import Token, User, UserResponse
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


async def authenticate_user(username: str, password: str) -> User:
    user_repository = UserRepository()
    user = await user_repository.get_user_by_email(email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = decode_token(token)
    if username is None:
        raise credentials_exception

    user_repository = UserRepository()
    user = await user_repository.get_user_by_email(email=username)
    if user is None:
        raise credentials_exception
    logger.info("Current user: %s", user.id)
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token(user)


@router.get("/users/me/", response_model=UserResponse)
async def get_me(current_user: Annotated[UserRepository, Depends(get_current_user)]):
    return UserResponse.from_user(current_user)


@router.post(
    "/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def create_customer(
    current_user: Annotated[UserRepository, Depends(get_current_user)],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repository = UserRepository()
    if not user_repository.get_user_by_email(email=email):
        user_id = await user_repository.create_customer(email=email, password=password)
        user = await user_repository.get_user_by_id(user_id)
        return UserResponse.from_user(user)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User with this email already exists",
    )
