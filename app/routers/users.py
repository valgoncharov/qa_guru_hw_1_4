from http import HTTPStatus
import logging
from app.database import get_users
from fastapi import APIRouter, HTTPException
from fastapi_pagination import paginate, Page
from pydantic import BaseModel

from app.models.User import User

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


@router.get("/", summary='Просмотр данных всех пользователей', tags=['Admin'], status_code=HTTPStatus.OK)
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
