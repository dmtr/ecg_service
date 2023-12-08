from typing import Annotated

from ecg_service.ecg.analyze import analyze
from ecg_service.ecg.repository import EcgRepository
from ecg_service.ecg.schemas import ECGInput, ECGResponse
from ecg_service.user.repository import UserRepository
from ecg_service.user.routes import get_current_user
from fastapi import (APIRouter, BackgroundTasks, Body, Depends, HTTPException,
                     status)

router = APIRouter()


@router.post("/ecgs", status_code=status.HTTP_201_CREATED, response_model=ECGResponse)
async def create_ecg(
    current_user: Annotated[UserRepository, Depends(get_current_user)],
    background_tasks: BackgroundTasks,
    ecg_input: ECGInput = Body(...),
):
    if current_user.role != "CUSTOMER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can create ECGs",
        )

    ecg_repository = EcgRepository()
    await ecg_repository.create_ecg(ecg_input)
    user_repository = UserRepository()
    if not await user_repository.add_ecg(current_user.database_id, ecg_input.id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add ECG to user",
        )
    ecg = await ecg_repository.get_ecg_by_id(ecg_input.id)
    background_tasks.add_task(analyze, ecg)
    return ecg


@router.get("/ecgs/{id}", response_model=ECGResponse)
async def get_ecg_by_id(
    id: str, current_user: Annotated[UserRepository, Depends(get_current_user)]
):
    if current_user.role != "CUSTOMER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can get ECGs",
        )

    if id not in current_user.ecgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ECG not found"
        )

    ecg_repository = EcgRepository()
    ecg = await ecg_repository.get_ecg_by_id(id)
    if not ecg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ECG not found"
        )
    return ecg
