from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from app.exercises.schemas import Exercise
from app.trainings.schemas import TrainingBody, Training, UpdateTrainingBody
from app.trainings import crud
from auth_token import get_current_user

router = APIRouter(
    prefix="/trainings",
    tags=["trainings"],
)


@router.get('', response_model=List[Training])
async def get_all_trainings(user_id: int = Depends(get_current_user)) -> List[Training]:
    return await crud.get_all_trainings(user_id)


@router.get('/{training_id}', response_model=Training)
async def get_single_training(training_id: int, user_id: int = Depends(get_current_user)) -> Training:
    result = await crud.get_single_training(training_id, user_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Training(**result)


@router.get('/{training_id}/exercises', response_model=List[Exercise])
async def get_training_exercises(training_id: int, user_id: int = Depends(get_current_user)) -> List[Exercise]:
    return await crud.get_training_exercises(training_id, user_id)


@router.delete('/{training_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_training(training_id: int, user_id: int = Depends(get_current_user)) -> None:
    await crud.delete_training(training_id, user_id)


@router.delete('/{training_id}/{exercise_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_training_exercise(training_id: int, exercise_id: int,
                                   user_id: int = Depends(get_current_user)) -> None:
    await crud.delete_training_exercise(training_id, exercise_id, user_id)


@router.post('/{training_id}/{exercise_id}', status_code=status.HTTP_204_NO_CONTENT)
async def create_training_exercise(training_id: int, exercise_id: int,
                                   user_id: int = Depends(get_current_user)) -> None:
    await crud.create_training_exercise(training_id, exercise_id, user_id)


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_all_training_exercises(body: TrainingBody, user_id: int = Depends(get_current_user)) -> None:
    training_id = await crud.create_training(body, user_id)
    await crud.create_all_training_exercises(training_id, body.exercises, user_id)


@router.put('', status_code=status.HTTP_204_NO_CONTENT)
async def update_training(body: Training, user_id: int = Depends(get_current_user)) -> None:
    await crud.update_training(body, user_id)


@router.put('/all', status_code=status.HTTP_204_NO_CONTENT)
async def update_all_training(body: UpdateTrainingBody, user_id: int = Depends(get_current_user)) -> None:
    training = Training(id=body.id, title=body.title)
    await crud.update_training(training, user_id)

    old_exercises = list(map(lambda i: i["id"], await crud.get_training_exercises(body.id, user_id)))

    new_exercises = list(set(body.exercises) - (set(old_exercises)))
    deleted_exercises = list(set(old_exercises) - (set(body.exercises)))

    if len(deleted_exercises):
        await crud.delete_all_training_exercises(body.id, deleted_exercises, user_id)

    if len(new_exercises):
        await crud.create_all_training_exercises(body.id, new_exercises, user_id)
