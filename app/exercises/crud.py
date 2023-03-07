from db import database
from typing import List

from app.exercises.schemas import Exercise, ExerciseBody


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
