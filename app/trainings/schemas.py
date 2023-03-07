from typing import List

from pydantic import BaseModel


class TrainingBody(BaseModel):
    title: str
    exercises: List[int]


class Training(BaseModel):
    id: int
    title: str
