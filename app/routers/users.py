from http import HTTPStatus
from app.database import users_db
from fastapi import APIRouter, HTTPException
from fastapi_pagination import paginate, Page

from app.models.User import User

router = APIRouter(prefix="/users")


@router.get("/{user_id}", summary='Просмотр данных пользователя', tags=['Admin'], status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")

    user = next((user for user in users_db if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    return user


@router.get("/", summary='Просмотр данных всех пользователей', tags=['Admin'], status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users_db)


@router.get("/users_all", summary='Просмотр данных всех пользователей', tags=['Admin'], status_code=HTTPStatus.OK)
def get_all_users() -> list[User]:
    return users_db