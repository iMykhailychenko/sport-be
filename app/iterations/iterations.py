from typing import List

from fastapi import APIRouter, status, Depends

from app.iterations.schemas import Iteration, IterationBody
from app.iterations import crud
from auth_token import get_current_user

router = APIRouter(
    prefix="/iterations",
    tags=["iterations"],
)


@router.get('/{date_id}/{training_id}', response_model=List[Iteration])
async def get_iterations(date_id: str, training_id: int, user_id: Depends(get_current_user)) -> List[Iteration]:
    return await crud.get_iterations(date_id, training_id, user_id)


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def get_iterations(body: IterationBody, user_id: Depends(get_current_user)) -> None:
    await crud.create_iteration(body, user_id)


@router.delete('/{iteration_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_iteration(iteration_id: int, user_id: Depends(get_current_user)) -> None:
    await crud.delete_iteration(iteration_id, user_id)
