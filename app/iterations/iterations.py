from typing import List

from fastapi import APIRouter, status, Depends

from app.iterations.schemas import Iteration, IterationBody, UpdateIterationBody
from app.iterations import crud
from auth_token import get_current_user

router = APIRouter(
    prefix="/iterations",
    tags=["iterations"],
)


@router.get('/{date_id}/{exercise_id}', response_model=List[Iteration])
async def get_iterations(date_id: int, exercise_id: int, user_id: int = Depends(get_current_user)) -> List[Iteration]:
    return await crud.get_iterations(date_id, exercise_id, user_id)


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_iteration(body: IterationBody, user_id: int = Depends(get_current_user)) -> None:
    await crud.create_iteration(body, user_id)


@router.delete('/{iteration_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_iteration(iteration_id: int, user_id: int = Depends(get_current_user)) -> None:
    await crud.delete_iteration(iteration_id, user_id)


@router.put('', status_code=status.HTTP_204_NO_CONTENT)
async def update_iteration(body: UpdateIterationBody, user_id: int = Depends(get_current_user)) -> None:
    await crud.update_iteration(body, user_id)
