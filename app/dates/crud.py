from app.dates.schemas import DateBody, DateType
from db import database


async def get_date(date: str, user_id: int) -> dict:
    query = """
    SELECT 
        id, 
        value, 
        comment,
        training_id
    FROM dates 
    WHERE user_id = :user_id AND value = :value
    """
    return await database.fetch_one(query=query, values={"user_id": user_id, "value": date})


async def create_date(body: DateBody, user_id: int) -> None:
    query = """
    INSERT INTO dates (
        value,
        comment,
        training_id,
        user_id
    )
    VALUES (
        :value,
        :comment,
        :training_id,
        :user_id
    )
    """
    values = {
        "value": body.value,
        "comment": body.comment,
        "training_id": body.trainingId,
        "user_id": user_id,
    }
    await database.execute(query=query, values=values)
