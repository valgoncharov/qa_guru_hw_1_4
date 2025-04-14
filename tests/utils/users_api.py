from typing import Optional, Dict, Any

from .base_api import BaseApi


class UsersApi(BaseApi):
    def __init__(self, env: str):
        super().__init__(env)
        self.base_path = "/users"

    def get_all_users(self) -> dict:
        response = self._get(self.base_path)
        return response.json()

    def get_user_by_id(self, user_id: int) -> dict:
        response = self._get(f"{self.base_path}/{user_id}")
        return response.json()

    def create_user(self, user_data: Dict[str, Any]) -> dict:
        response = self._post(self.base_path + "/", json=user_data)
        return response.json()

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> dict:
        response = self._patch(f"{self.base_path}/{user_id}", json=user_data)
        return response.json()

    def delete_user(self, user_id: int) -> None:
        self._delete(f"{self.base_path}/{user_id}")
