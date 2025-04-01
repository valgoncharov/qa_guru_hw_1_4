from http import HTTPStatus

from fastapi import APIRouter
from app.models.AppStatus import AppStatus
from app.database import get_users

router = APIRouter()


@router.get("/status",  summary='Статус приложения', tags=['Healthcheck'], status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=len(get_users()) > 0)
