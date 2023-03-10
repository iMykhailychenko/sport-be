from typing import List

from fastapi import APIRouter, Depends, status

from app.dates.schemas import DateType, DateExerciseBody, DateTrainingBody
from app.dates import crud
from auth_token import get_current_user

router = APIRouter(
    prefix="/dates",
    tags=["dates"],
)


@router.get('/{date}', response_model=List[DateType])
async def get_date_exercises(date: str, user_id: int = Depends(get_current_user)) -> List[DateType]:
    return await crud.get_date_exercises(date, user_id)


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def add_exercise(body: DateExerciseBody, user_id: int = Depends(get_current_user)) -> None:
    return await crud.add_exercise(body, user_id)


@router.post('/training', status_code=status.HTTP_204_NO_CONTENT)
async def add_exercise(body: DateTrainingBody, user_id: int = Depends(get_current_user)) -> None:
    return await crud.add_training(body, user_id)


@router.delete('/{date_id}/{exercise_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(date_id: int, exercise_id: int, user_id: int = Depends(get_current_user)) -> None:
    await crud.delete_exercise(date_id, exercise_id, user_id)
