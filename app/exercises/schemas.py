from typing import Optional

from pydantic import BaseModel


class ExerciseBody(BaseModel):
    title: str
    description: Optional[str]
    image: Optional[str]


class Exercise(ExerciseBody):
    id: int
    title: str
    description: Optional[str]
    image: Optional[str]
