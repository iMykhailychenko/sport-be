from app.iterations.schemas import IterationBody
from db import database


async def create_iteration(body: IterationBody, user_id: int) -> None:
    query = """
    INSERT INTO iterations (
        time,
        weight,
        repeat,
        date_id,
        exercise_id,
        user_id
    )
    VALUES (
        :time,
        :weight,
        :repeat,
        :date_id,
        :exercise_id,
        :user_id
    )
    """
    values = {
        "time": body.time,
        "weight": body.weight,
        "repeat": body.repeat,
        "date_id": body.date_id,
        "exercise_id": body.exercise_id,
        "user_id": user_id
    }
    await database.execute(query=query, values=values)


async def get_iterations(date_id: int, exercise_id: int, user_id: int) -> list:
    query = """
    SELECT
        id,
        time,
        weight,
        repeat,
        date_id,
        exercise_id
    FROM iterations
    WHERE date_id = :date_id AND exercise_id = :exercise_id AND user_id = :user_id
    """
    values = {
        "date_id": date_id,
        "exercise_id": exercise_id,
        "user_id": user_id,
    }
    return await database.fetch_all(query=query, values=values)


async def delete_iteration(iteration_id: int, user_id: int) -> None:
    query = """
    DELETE FROM iterations 
    WHERE id = :iteration_id AND user_id = :user_id
    """
    await database.execute(query=query, values={
        "iteration_id": iteration_id,
        "user_id": user_id
    })
