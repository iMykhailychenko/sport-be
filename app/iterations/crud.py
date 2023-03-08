from app.iterations.schemas import IterationBody
from db import database


async def create_iteration(body: IterationBody, user_id: int) -> None:
    query = """
    INSERT INTO iterations (
        time,
        weight,
        repeat,
        date_id,
        user_id,
        training_id
    )
    VALUES (
        :time,
        :weight,
        :repeat,
        :date_id,
        :user_id,
        :training_id
    )
    """
    values = {
        "time": body.time,
        "weight": body.weight,
        "repeat": body.repeat,
        "date_id": body.date_id,
        "user_id": user_id,
        "training_id": body.training_id
    }
    await database.execute(query=query, values=values)


async def get_iterations(date_id: str, training_id: int, user_id: int) -> list:
    query = """
    SELECT
        time,
        weight,
        repeat,
        date_id,
        training_id
    FROM iterations
    WHERE training_id = :training_id AND date_id = :date_id AND user_id = :user_id
    """
    values = {
        "date_id": date_id,
        "user_id": user_id,
        "training_id": training_id
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
