from http import HTTPStatus
import logging
from app.database import users
from app.database.users import get_users, get_user, create_user, update_user, delete_user
from fastapi import APIRouter, HTTPException
from fastapi_pagination import paginate, Page
from pydantic import BaseModel

from app.models.User import User, UserCreate, UserUpdate

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


class UsersList(BaseModel):
    data: list[User]


@router.get("/users_all", summary='Просмотр данных всех пользователей', tags=['Admin'], status_code=HTTPStatus.OK)
def get_all_users() -> UsersList:
    users = get_users()
    logger.debug(f"Retrieved {len(users)} users from database")
    try:
        response = UsersList(data=users)
        logger.debug("Successfully created UsersList response")
        return response
    except Exception as e:
        logger.error(f"Error creating UsersList: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f"Error processing users data: {str(e)}"
        )


@router.get("/", summary='Просмотр данных пользователей постранично', tags=['Admin'], status_code=HTTPStatus.OK)
def get_paginated_users() -> Page[User]:
    return paginate(get_users())


@router.get("/{user_id}", summary='Просмотр данных пользователя', tags=['Admin'], status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")

    users = get_users()
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    return user


@router.post("/", summary='Создание пользователя', tags=['Admin'], status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate) -> User:
    # Convert UserCreate to User model
    user_data = user.model_dump()
    new_user = User(**user_data)
    return users.create_user(new_user)


@router.patch("/{user_id}", summary='Обновление пользователя', tags=['Admin'], status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserUpdate) -> User:
    # Convert UserUpdate to User model
    user_data = user.model_dump(exclude_unset=True)
    updated_user = User(**user_data)
    return users.update_user(user_id, updated_user)


@router.delete("/{user_id}", summary='Удаление пользователя', tags=['Admin'], status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int) -> None:
    if user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")

    # Check if user exists before deletion
    users_list = get_users()
    user = next((user for user in users_list if user.id == user_id), None)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"User with id {user_id} not found or already deleted"
        )

    # If user exists, proceed with deletion
    users.delete_user(user_id)
    return {"message": "User deleted successfully"}
