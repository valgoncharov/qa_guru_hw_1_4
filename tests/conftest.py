import os

import dotenv
import pytest


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
    env_urls = {
        "prod": "https://api.prod.example.com",
        "stage": "https://api.stage.example.com",
        "dev": "https://api.dev.example.com"
    }
    return env_urls.get(env, env_urls["dev"])
