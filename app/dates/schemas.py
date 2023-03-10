from typing import Optional

from pydantic import BaseModel

from app.exercises.schemas import Exercise


class DateType(Exercise):
    date: str
    exercise_id: int
    comment: Optional[str]


class DateExerciseBody(BaseModel):
    date: str
    exercise_id: int
    comment: Optional[str]


class DateTrainingBody(BaseModel):
    date: str
    training_id: int
    comment: Optional[str]
