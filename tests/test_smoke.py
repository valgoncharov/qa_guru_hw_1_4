import requests
from http import HTTPStatus


class TestSmoke:
    def test_app_status(self, app_url: str):
        response = requests.get(f"{app_url}/status")
        assert response.status_code == HTTPStatus.OK

    def test_smoke_users(self, app_url: str):
        response = requests.get(f"{app_url}/users/")
        assert response.status_code == HTTPStatus.OK
