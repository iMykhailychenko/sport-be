from typing import List

from fastapi import APIRouter, status, Depends, HTTPException

from app.exercises.schemas import Exercise, ExerciseBody, UpdateExerciseBody
from app.exercises import crud
from auth_token import get_current_user

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
)


@router.get('', response_model=List[Exercise])
async def get_exercises(user_id: int = Depends(get_current_user)) -> List[Exercise]:
    return await crud.get_exercises(user_id)


@router.get('/{exercise_id}', response_model=Exercise)
async def get_exercises(exercise_id: int, user_id: int = Depends(get_current_user)) -> Exercise:
    result = await crud.get_single_exercise(exercise_id, user_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Exercise(**result)


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_exercises(body: ExerciseBody, user_id: int = Depends(get_current_user)) -> None:
    return await crud.create_exercises(body, user_id)


@router.delete('/{exercise_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(exercise_id: int, user_id: int = Depends(get_current_user)) -> None:
    return await crud.delete_exercise(exercise_id, user_id)


@router.put('', status_code=status.HTTP_204_NO_CONTENT)
async def update_exercise(body: UpdateExerciseBody, user_id: int = Depends(get_current_user)) -> None:
    await crud.update_exercise(body, user_id)
