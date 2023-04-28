from typing import List

from app.dates.schemas import DateExerciseBody, DateTrainingBody
from app.trainings.crud import get_training_exercises
from db import database


async def get_calendar(date: str, user_id: int) -> List[str]:
    query = """
        SELECT dates.date FROM dates
        WHERE dates.user_id = :user_id AND dates.date ILIKE :date
        """
    result = await database.fetch_all(query=query, values={"user_id": user_id, "date": f"%{date}%"})

    return list(set(map(lambda x: x.date, result)))


async def is_exercise_exist(date: str, exercise_id: int, user_id: int) -> bool:
    query = """
    SELECT TRUE FROM dates
    INNER JOIN exercises ON dates.exercise_id = exercises.id
    WHERE dates.user_id = :user_id AND dates.date = :date AND dates.exercise_id = :exercise_id
    """
    return bool(
        await database.fetch_one(query=query, values={"user_id": user_id, "date": date, "exercise_id": exercise_id}))


async def get_date_exercises(date: str, user_id: int) -> list:
    query = """
    SELECT 
        dates.id,
        dates.date,
        dates.comment,
        dates.exercise_id, 
        exercises.title, 
        exercises.image,
        exercises.description
    FROM dates
    INNER JOIN exercises ON dates.exercise_id = exercises.id
    WHERE dates.user_id = :user_id AND dates.date = :date
    """
    return await database.fetch_all(query=query, values={"user_id": user_id, "date": date})


def get_insert_exercise_query() -> str:
    return """
    INSERT INTO dates (
        date,
        comment,
        exercise_id,
        user_id
    )
    VALUES (
        :date,
        :comment,
        :exercise_id,
        :user_id
    )
    """


async def add_exercise(body: DateExerciseBody, user_id: int) -> None:
    if await is_exercise_exist(body.date, body.exercise_id, user_id):
        return None

    values = {
        "date": body.date,
        "comment": body.comment,
        "exercise_id": body.exercise_id,
        "user_id": user_id,
    }
    await database.execute(query=get_insert_exercise_query(), values=values)


async def add_training(body: DateTrainingBody, user_id: int) -> None:
    exercises = await get_training_exercises(body.training_id, user_id)

    values = []
    for ex in exercises:
        if await is_exercise_exist(body.date, ex.id, user_id):
            continue
        values.append({
            "date": body.date,
            "comment": body.comment,
            "exercise_id": ex.id,
            "user_id": user_id,
        })

    await database.execute_many(query=get_insert_exercise_query(), values=values)


async def delete_exercise(date_id: int, exercise_id: int, user_id: int) -> None:
    query = """
    DELETE FROM dates 
    WHERE id = :date_id AND exercise_id = :exercise_id AND user_id = :user_id
    """
    values = {"date_id": date_id, "exercise_id": exercise_id, "user_id": user_id}
    await database.execute(query=query, values=values)
