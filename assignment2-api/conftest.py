import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import pytest
import requests

BASE_URL = "https://fakestoreapi.com"


class ApiClient:
    """Thin requests wrapper that prefixes the base URL and sets JSON headers."""

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get(self, path: str, **kwargs):
        return self.session.get(self._url(path), timeout=30, **kwargs)

    def post(self, path: str, **kwargs):
        return self.session.post(self._url(path), timeout=30, **kwargs)

    def put(self, path: str, **kwargs):
        return self.session.put(self._url(path), timeout=30, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.session.delete(self._url(path), timeout=30, **kwargs)


@pytest.fixture(scope="session")
def api():
    client = ApiClient()
    yield client
    client.session.close()
