from http import HTTPStatus

from fastapi import APIRouter
from app.models.AppStatus import AppStatus
from app.database import users_db

router = APIRouter()


@router.get("/status",  summary='Статус приложения', tags=['Healthcheck'], status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=len(users_db) > 0)