from typing import Optional

from pydantic import BaseModel


class DateBody(BaseModel):
    value: str
    training_id: int
    comment: Optional[str]


class DateType(BaseModel):
    id: int
    value: str
    training_id: int
    comment: Optional[str]
