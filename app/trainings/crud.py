from db import database

from app.trainings.schemas import TrainingBody


async def get_all_trainings(user_id: int) -> list:
    print(user_id)
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


async def create_trainings(body: TrainingBody, user_id: int) -> None:
    trainings_query = """
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
    training_id = await database.execute(query=trainings_query, values={
        "title": body.title,
        "user_id": user_id,
    })

    exercises_trainings_query = """
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

    values = []
    for exercise in body.exercises:
        values.append({
            "training_id": training_id,
            "exercise_id": exercise,
            "user_id": user_id,
        })

    await database.execute_many(query=exercises_trainings_query, values=values)
