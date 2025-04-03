from http import HTTPStatus

import pytest
import requests
from app.models.User import User, UserCreate
from random import randint
from fastapi_pagination import Page
from faker import Faker

fake = Faker()


@pytest.fixture
def users(app_url: str):
    response = requests.get(f"{app_url}/users")
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]


@pytest.fixture
def fake_user_data():
    return {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "job_title": fake.job(),
        "avatar": fake.image_url()
    }


@pytest.fixture
def created_user(app_url: str, fake_user_data):
    response = requests.post(f"{app_url}/users/", json=fake_user_data)
    assert response.status_code == HTTPStatus.CREATED
    user = response.json()
    return user["id"]


@pytest.fixture
def updated_user_data():
    return {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "job_title": fake.job(),
        "avatar": fake.image_url()
    }


@pytest.fixture
def empty_user_data():
    return {
        "email": "",
        "first_name": "",
        "last_name": "",
        "job_title": "",
        "avatar": ""
    }


class TestUserData:
    @pytest.mark.parametrize("user_id", [1, 6, 14])
    def test_get_user_by_id(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)

    def test_get_all_users(self, app_url: str):
        response = requests.get(f"{app_url}/users")
        assert response.status_code == HTTPStatus.OK
        users_data = response.json()
        Page[User].model_validate(users_data)

    def test_users_no_duplicates(self, users):
        users_id = [user["id"] for user in users]
        assert len(users_id) == len(set(users_id))

    @pytest.mark.parametrize("user_id", [15, 111])
    def test_nonexistent_user(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", ["str", 0, -1, 1.1, " "])
    def test_user_invalid_id_type(self, app_url: str, user_id):
        response = requests.get(f"{app_url}/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_random_user(self, app_url: str):
        user_id = randint(1, 13)
        response = requests.get(f"{app_url}/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


class TestCRUD:
    def test_post_create_user(self, app_url: str, fake_user_data):
        response = requests.post(f"{app_url}/users/", json=fake_user_data)
        assert response.status_code == HTTPStatus.CREATED
        created_user = response.json()

        assert created_user["email"] == fake_user_data["email"]
        assert created_user["first_name"] == fake_user_data["first_name"]
        assert created_user["last_name"] == fake_user_data["last_name"]
        assert created_user["job_title"] == fake_user_data["job_title"]
        assert created_user["avatar"] == fake_user_data["avatar"]
        assert "id" in created_user
        assert created_user["id"] is not None

    def test_post_create_user_not_valid(self, app_url: str):
        invalid_users = [
            {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "job_title": fake.job(),
                "avatar": fake.image_url()
            }
        ]

        for invalid_user in invalid_users:
            response = requests.post(f"{app_url}/users/", json=invalid_user)
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, \
                f"Expected 422 for invalid user data: {invalid_user}"

    def test_update_user(self, app_url, created_user, updated_user_data):
        response = requests.patch(
            f"{app_url}/users/{created_user}", json=updated_user_data)

        assert response.status_code == HTTPStatus.OK
        updated_user = response.json()

        assert updated_user["id"] == created_user
        assert updated_user["email"] == updated_user_data["email"]
        assert updated_user["first_name"] == updated_user_data["first_name"]
        assert updated_user["last_name"] == updated_user_data["last_name"]
        assert updated_user["job_title"] == updated_user_data["job_title"]
        assert updated_user["avatar"] == updated_user_data["avatar"]

    def test_update_not_exsist_user(self, app_url, updated_user_data):
        non_existent_id = 99999
        response = requests.patch(
            f"{app_url}/users/{non_existent_id}", json=updated_user_data)

        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f"Пользователь 404 не найден: {non_existent_id}"

    def test_update_empty_data(self, app_url: str, created_user, empty_user_data):
        response = requests.patch(
            f"{app_url}/users/{created_user}", json=empty_user_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, \
            "Expected 422 for empty fields in update data"

    def test_delete_user(self, app_url: str, created_user):
        response = requests.delete(f"{app_url}/users/{created_user}")
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            f"Ожидаем 204 успешное удаление, статус {response.status_code}"

        get_response = requests.get(f"{app_url}/users/{created_user}")
        assert get_response.status_code == HTTPStatus.NOT_FOUND, \
            "Проверяем, что пользователя нет"

    def test_delete_deleted_user(self, app_url: str, created_user):
        delete_response = requests.delete(f"{app_url}/users/{created_user}")
        assert delete_response.status_code == HTTPStatus.NO_CONTENT, \
            "Удалили первый раз"

        second_delete_response = requests.delete(
            f"{app_url}/users/{created_user}")
        assert second_delete_response.status_code == HTTPStatus.NOT_FOUND, \
            "Повторное удаление получаем 404"

    @pytest.mark.parametrize("invalid_id,description", [
        (-1, "Negative ID"),
        (0, "Zero ID"),
        ("abc", "String ID"),
        (1.5, "Float ID"),
        (" ", "Space string"),
        (None, "None value"),
        (-999999, "Large negative number")
    ])
    def test_delete_not_valid_user(self, app_url: str, invalid_id, description: str):
        response = requests.delete(f"{app_url}/users/{invalid_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, \
            f"Expected 422 for {description} ({invalid_id}), got {response.status_code}"

# - Тест на post: создание. Предусловия: подготовленные тестовые данные (fake)

# - Тест на delete: удаление. Предусловия: созданный пользователь

# - Тест на patch: изменение. Предусловия: созданный пользователь
