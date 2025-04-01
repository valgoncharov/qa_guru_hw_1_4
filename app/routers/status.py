from http import HTTPStatus

from fastapi import APIRouter
from app.models.AppStatus import AppStatus
from app.database.engins import get_database_status

router = APIRouter()


@router.get("/status",  summary='Статус приложения', tags=['Healthcheck'], status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=get_database_status())
