from typing import Optional

from pydantic import BaseModel


class DateBody(BaseModel):
    value: str
    trainingId: int
    comment: Optional[str]


class DateType(BaseModel):
    id: int
    value: str
    trainingId: int
    comment: Optional[str]
