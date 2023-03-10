from typing import List

from pydantic import BaseModel


class TrainingBody(BaseModel):
    title: str
    exercises: List[int]


class UpdateTrainingBody(TrainingBody):
    id: int


class Training(BaseModel):
    id: int
    title: str
