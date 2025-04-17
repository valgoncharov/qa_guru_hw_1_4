from http import HTTPStatus


class TestSmoke:
    def test_app_status(self, users_api):
        response = users_api.session.get("/status")
        assert response.status_code == HTTPStatus.OK

    def test_smoke_users(self, users_api):
        response = users_api.get_users()
        assert response.status_code == HTTPStatus.OK
