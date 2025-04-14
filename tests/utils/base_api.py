from typing import Optional

import requests


class BaseApi:
    def __init__(self, env: str):
        self.base_url = {
            "prod": "https://api.prod.example.com",
            "stage": "https://api.stage.example.com",
            "dev": "https://api.dev.example.com"
        }.get(env, "https://api.dev.example.com")  # по умолчанию dev
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _get(self, path: str, params: Optional[dict] = None) -> requests.Response:
        return self.session.get(f"{self.base_url}{path}", params=params)

    def _post(self, path: str, json: Optional[dict] = None) -> requests.Response:
        return self.session.post(f"{self.base_url}{path}", json=json)

    def _put(self, path: str, json: Optional[dict] = None) -> requests.Response:
        return self.session.put(f"{self.base_url}{path}", json=json)

    def _delete(self, path: str) -> requests.Response:
        return self.session.delete(f"{self.base_url}{path}")
