from db import database
from typing import List

from app.exercises.schemas import Exercise, ExerciseBody, UpdateExerciseBody


async def get_single_exercise(exercise_id: int, user_id: int) -> dict:
    query = "SELECT id, title, description, image FROM exercises WHERE user_id = :user_id AND id = :exercise_id"
    return await database.fetch_one(query=query, values={"user_id": user_id, "exercise_id": exercise_id})


async def get_exercises(user_id: int) -> List[Exercise]:
    query = "SELECT id, title, description, image FROM exercises WHERE user_id = :user_id"
    return await database.fetch_all(query=query, values={"user_id": user_id})


async def create_exercises(body: ExerciseBody, user_id: int) -> None:
    query = """
    INSERT INTO exercises (
        title,
        description,
        image,
        user_id
    )
    VALUES (
        :title,
        :description,
        :image,
        :user_id
    )
    """
    values = {
        "title": body.title,
        "description": body.description,
        "image": body.image,
        "user_id": user_id,
    }
    await database.execute(query=query, values=values)


async def delete_exercise(exercise_id: int, user_id: int) -> None:
    query = """
    DELETE FROM exercises 
    WHERE id = :exercise_id AND user_id = :user_id
    """
    await database.execute(query=query, values={
        "exercise_id": exercise_id,
        "user_id": user_id
    })


async def update_exercise(new_data: UpdateExerciseBody, user_id: int) -> None:
    old_model = UpdateExerciseBody(**(await get_single_exercise(new_data.id, user_id)))
    updated_model = old_model.copy(update=new_data.dict(exclude_none=True))

    query = """
    UPDATE exercises
    SET
        title = :title,
        description = :description,
        image = :image
    WHERE user_id = :user_id AND id = :id
    """

    values = {
        "id": new_data.id,
        "title": updated_model.title,
        "description": updated_model.description,
        "image": updated_model.image,
        "user_id": user_id
    }

    await database.execute(query=query, values=values)
