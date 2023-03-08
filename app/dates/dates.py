from fastapi import APIRouter, status, Depends, HTTPException

from app.dates.schemas import DateType, DateBody
from app.dates import crud
from auth_token import get_current_user

router = APIRouter(
    prefix="/dates",
    tags=["dates"],
)


@router.get('/{date}', response_model=DateType)
async def get_date(date: str, user_id: int = Depends(get_current_user)) -> DateType:
    result = await crud.get_date(date, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )

    return DateType(**result, trainingId=result["training_id"])


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_date(body: DateBody, user_id: int = Depends(get_current_user)) -> None:
    if await crud.get_date(body.value, user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This date is already taken",
        )

    await crud.create_date(body, user_id)


@router.delete('/{date_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_date(date_id: int, user_id: int = Depends(get_current_user)) -> None:
    return await crud.delete_date(date_id, user_id)
