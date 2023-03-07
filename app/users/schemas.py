from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    id: int
    name: str
    avatar: Optional[HttpUrl]
    email: EmailStr


class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserPartialUpdate(BaseModel):
    name: Optional[str]
    avatar: Optional[HttpUrl]


class Token(BaseModel):
    accessToken: str
    tokenType: str
