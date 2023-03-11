from app.iterations.schemas import IterationBody, UpdateIterationBody
from db import database


async def get_single_iteration(iteration_id: int, user_id: int) -> dict:
    query = "SELECT * FROM iterations WHERE id = :iteration_id AND user_id = :user_id"
    values = {"iteration_id": iteration_id, "user_id": user_id}
    return await database.fetch_one(query=query, values=values)


async def get_exercise_iterations(exercise_id: int, user_id: int) -> list:
    query = """
    SELECT
        iterations.id,
        iterations.time,
        iterations.weight,
        iterations.repeat,
        iterations.exercise_id,
        dates.date
    FROM iterations
    INNER JOIN dates ON iterations.date_id = dates.id
    WHERE iterations.exercise_id = :exercise_id AND iterations.user_id = :user_id
    ORDER BY iterations.id DESC
    """
    values = {
        "exercise_id": exercise_id,
        "user_id": user_id,
    }
    return await database.fetch_all(query=query, values=values)


async def get_date_iterations(date_id: int, exercise_id: int, user_id: int) -> list:
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


async def delete_iteration(iteration_id: int, user_id: int) -> None:
    query = """
    DELETE FROM iterations 
    WHERE id = :iteration_id AND user_id = :user_id
    """
    await database.execute(query=query, values={
        "iteration_id": iteration_id,
        "user_id": user_id
    })


async def update_iteration(new_data: UpdateIterationBody, user_id: int) -> None:
    old_model = UpdateIterationBody(**(await get_single_iteration(new_data.id, user_id)))
    updated_model = old_model.copy(update=new_data.dict(exclude_none=True))

    query = """
    UPDATE iterations
    SET
        time = :time,
        weight = :weight,
        repeat = :repeat
    WHERE user_id = :user_id AND id = :id
    """

    values = {
        "id": new_data.id,
        "time": updated_model.time,
        "weight": updated_model.weight,
        "repeat": updated_model.repeat,
        "user_id": user_id
    }

    await database.execute(query=query, values=values)
