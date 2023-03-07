from typing import List

from fastapi import APIRouter, Depends, status

from app.trainings.schemas import TrainingBody, Training
from app.trainings import crud
from auth_token import get_current_user

router = APIRouter(
    prefix="/trainings",
    tags=["trainings"],
)


@router.get('', response_model=List[Training])
async def get_all_trainings(user_id: int = Depends(get_current_user)) -> List[Training]:
    return await crud.get_all_trainings(user_id)


@router.get('/{training_id}', response_model=List[Training])
async def get_all_trainings(training_id: int, user_id: int = Depends(get_current_user)) -> List[Training]:
    return await crud.get_training_exercises(training_id, user_id)


@router.delete('/{training_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_training(training_id: int, user_id: int = Depends(get_current_user)) -> None:
    return await crud.delete_training(training_id, user_id)


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_trainings(body: TrainingBody, user_id: int = Depends(get_current_user)) -> None:
    await crud.create_trainings(body, user_id)
