from typing import List

from db import database

from app.trainings.schemas import TrainingBody, Training


async def get_single_training(training_id: int, user_id: int) -> dict:
    query = "SELECT id, title FROM trainings WHERE user_id = :user_id AND id = :id"
    return await database.fetch_one(query=query, values={"user_id": user_id, "id": training_id})


async def get_all_trainings(user_id: int) -> list:
    query = "SELECT id, title FROM trainings WHERE user_id = :user_id"
    return await database.fetch_all(query=query, values={"user_id": user_id})


async def get_training_exercises(training_id: int, user_id: int) -> list:
    query = """
    SELECT 
        exercises.id, 
        exercises.title, 
        exercises.image,
        exercises.description
    FROM exercises_trainings
    INNER JOIN exercises ON exercises_trainings.exercise_id = exercises.id
    WHERE exercises_trainings.user_id = :user_id AND exercises_trainings.training_id = :training_id
    """
    return await database.fetch_all(query=query, values={"user_id": user_id, "training_id": training_id})


async def create_training(body: TrainingBody, user_id: int) -> int:
    query = """
    INSERT INTO trainings (
        title,
        user_id
    )
    VALUES (
        :title,
        :user_id
    )
    RETURNING id
    """

    values = {
        "title": body.title,
        "user_id": user_id,
    }

    return await database.execute(query=query, values=values)


async def delete_training(training_id: int, user_id: int) -> None:
    values = {"training_id": training_id, "user_id": user_id}

    trainings_query = """
    DELETE FROM trainings 
    WHERE id = :training_id AND user_id = :user_id
    """
    await database.execute(query=trainings_query, values=values)

    exercises_trainings_query = """
    DELETE FROM exercises_trainings 
    WHERE training_id = :training_id AND user_id = :user_id
    """
    await database.execute(query=exercises_trainings_query, values=values)


def get_delete_training_exercise_query():
    return """
    DELETE FROM exercises_trainings 
    WHERE training_id = :training_id AND exercise_id = :exercise_id AND user_id = :user_id
    """


async def delete_training_exercise(training_id: int, exercise_id: int, user_id: int) -> None:
    values = {"training_id": training_id, "exercise_id": exercise_id, "user_id": user_id}
    await database.execute(query=get_delete_training_exercise_query(), values=values)


async def delete_all_training_exercises(training_id: int, exercises: List[int], user_id: int) -> None:
    values = []
    for exercise_id in exercises:
        values.append({
            "training_id": training_id,
            "exercise_id": exercise_id,
            "user_id": user_id
        })

    await database.execute_many(query=get_delete_training_exercise_query(), values=values)


def get_create_exercises_trainings_query() -> str:
    return """
    INSERT INTO exercises_trainings (
        training_id,
        exercise_id,
        user_id
    )
    VALUES (
        :training_id,
        :exercise_id,
        :user_id
    )
    """


async def create_training_exercise(training_id: int, exercise_id: int, user_id: int) -> None:
    values = {
        "training_id": training_id,
        "exercise_id": exercise_id,
        "user_id": user_id,
    }
    await database.execute(query=get_create_exercises_trainings_query(), values=values)


async def create_all_training_exercises(training_id: int, exercises: List[int], user_id: int) -> None:
    values = []
    for exercise in exercises:
        values.append({
            "training_id": training_id,
            "exercise_id": exercise,
            "user_id": user_id,
        })

    await database.execute_many(query=get_create_exercises_trainings_query(), values=values)


async def update_training(body: Training, user_id: int) -> None:
    query = """
    UPDATE trainings
    SET title = :title
    WHERE user_id = :user_id AND id = :id
    """

    values = {
        "id": body.id,
        "title": body.title,
        "user_id": user_id
    }
    await database.execute(query=query, values=values)
