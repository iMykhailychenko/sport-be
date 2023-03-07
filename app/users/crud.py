from typing import Mapping

from pydantic import EmailStr

from app.users.schemas import UserPartialUpdate
from db import database


async def user_exist(email: EmailStr) -> bool:
    query = "SELECT TRUE FROM users WHERE email = :email"
    return bool(await database.fetch_one(query=query, values={"email": email}))


async def create_user(
        email: str,
        name: str,
        hashed_password: str,
) -> None:
    query = """
    INSERT INTO users (
        password,
        name,
        email
    )
    VALUES (
        :password,
        :name,
        :email
    )
    """
    values = {
        "password": hashed_password,
        "name": name,
        "email": email,
    }
    await database.execute(query=query, values=values)


async def get_user_by_id(user_id: int) -> dict:
    query = """
    SELECT email, name, id
    FROM users
    WHERE id = :id
    """
    return await database.fetch_one(query=query, values={"id": user_id})


async def get_user_by_email(email: str) -> dict:
    query = """
        SELECT email, name, id, password
        FROM users
        WHERE email = :email
        """
    return await database.fetch_one(query=query, values={"email": email})


async def partial_update_user(
        user_id: int,
        update_user_data: UserPartialUpdate,
        stored_user_data: Mapping,
) -> None:
    stored_user_model = UserPartialUpdate(**stored_user_data)
    update_data = update_user_data.dict(exclude_unset=True)
    updated_user = stored_user_model.copy(update=update_data)

    query = """
    UPDATE users
    SET
        name = :last_name,
        avatar = :avatar
    WHERE id = :user_id
    """
    values = {
        "name": updated_user.name,
        "avatar": updated_user.avatar,
        "user_id": user_id
    }
    await database.execute(query=query, values=values)
