from typing import Mapping

from fastapi import APIRouter, HTTPException, Response, status, Depends

from app.users import crud
from app.users.crud import get_user_by_email
from app.users.schemas import UserCreateRequest, User, Token, LoginRequest, UserPartialUpdate
from app.users.utils import get_password_hash, verify_password
from auth_token import get_current_user, create_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(body: UserCreateRequest) -> Response:
    """ Create new user """
    if await crud.user_exist(email=body.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )

    await crud.create_user(
        email=body.email,
        name=body.name,
        hashed_password=get_password_hash(body.password),
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/login", response_model=Token)
async def login_user(body: LoginRequest) -> dict:
    """ OAuth2 compatible token login, get an access token for future requests """
    user = await get_user_by_email(email=body.email)

    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    return {
        "accessToken": create_access_token(
            subject=body.email, user_id=user["id"]
        ),
        "tokenType": "Bearer",
    }


@router.get("/profile", response_model=User)
async def logged_in_user_details(user_id: int = Depends(get_current_user)) -> Mapping:
    """ Get logged-in user details """
    user = await crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    return user


@router.put("/profile", response_model=User)
async def update_user(
        update_user_data: UserPartialUpdate,
        user_id: int = Depends(get_current_user),
) -> User:
    stored_user_data = await crud.get_user_by_id(user_id)

    if not stored_user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    await crud.partial_update_user(
        user_id=user_id,
        update_user_data=update_user_data,
        stored_user_data=stored_user_data,
    )

    user = await crud.get_user_by_id(user_id)

    return User(**user)
