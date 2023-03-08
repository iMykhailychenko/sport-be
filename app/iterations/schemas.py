from pydantic import BaseModel


class IterationBody(BaseModel):
    time: int
    weight: int
    repeat: int
    date_id: int
    exercise_id: int


class Iteration(BaseModel):
    id: int
    time: int
    weight: int
    repeat: int
    date_id: int
    exercise_id: int
