from typing import Optional

from pydantic import BaseModel


class ExerciseBody(BaseModel):
    title: str
    description: Optional[str]
    image: Optional[str]


class UpdateExerciseBody(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    image: Optional[str]


class Exercise(ExerciseBody):
    id: int
