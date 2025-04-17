import os

import dotenv
import pytest
from .utils.users_api import UsersApi
from .utils.config import Server


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev",
                    help="Окружение на котором запущены тесты (dev/stage/prod)")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url(env) -> str:
    # Используем из конфига
    return Server(env).app


@pytest.fixture(scope='function')
def users_api(env: str):
    return UsersApi(env)
