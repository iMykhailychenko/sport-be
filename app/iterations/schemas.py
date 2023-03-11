from typing import Optional

from pydantic import BaseModel


class IterationBody(BaseModel):
    time: int
    weight: int
    repeat: int
    date_id: int
    exercise_id: int


class UpdateIterationBody(BaseModel):
    id: int
    time: Optional[int]
    weight: Optional[int]
    repeat: Optional[int]


class Iteration(BaseModel):
    id: int
    time: int
    weight: int
    repeat: int
    date_id: int
    exercise_id: int


class ExerciseIterations(BaseModel):
    id: int
    time: int
    weight: int
    repeat: int
    exercise_id: int
    date: str
