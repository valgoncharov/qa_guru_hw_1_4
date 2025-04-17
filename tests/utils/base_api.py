from typing import Optional

import requests
from requests import Session
from .config import Server


class BaseSession(Session):
    def __init__(self, **kwargs):
        super().__init__()
        self.base_url = kwargs.get('base_url', None)
        self.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def request(self, method, url, **kwargs):
        if self.base_url and not url.startswith(('http://', 'https://')):
            url = f"{self.base_url}{url}"
        return super().request(method, url, **kwargs)


class BaseApi:
    def __init__(self, env: str):
        # Пробрасываем из конфига
        self.base_url = Server(env).app
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
