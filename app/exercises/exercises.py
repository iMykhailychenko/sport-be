from typing import List

from fastapi import APIRouter, status, Depends

from app.exercises.schemas import Exercise, ExerciseBody
from app.exercises import crud
from auth_token import get_current_user

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
)


@router.get('', response_model=List[Exercise])
async def get_exercises(user_id: int = Depends(get_current_user)) -> List[Exercise]:
    return await crud.get_exercises(user_id)


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_exercises(body: ExerciseBody, user_id: int = Depends(get_current_user)) -> None:
    return await crud.create_exercises(body, user_id)
