import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

import pytest
import requests

from mock_responses import register_mocks

BASE_URL = "https://fakestoreapi.com"


class ApiClient:
    """Thin requests wrapper that prefixes the base URL and sets JSON headers."""

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "qa-assignment-tests/1.0",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, **kwargs):
        """Retry transient network / 5xx errors (common from CI runners)."""
        last_response = None
        for attempt in range(3):
            response = self.session.request(
                method, self._url(path), timeout=30, **kwargs
            )
            last_response = response
            if response.status_code < 500:
                return response
            time.sleep(1 + attempt)
        return last_response

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request("DELETE", path, **kwargs)


@pytest.fixture(scope="session")
def api():
    """Use mocked API responses in CI (GitHub runners often cannot reach fakestoreapi.com)."""
    use_mocks = os.getenv("CI", "").lower() == "true" or os.getenv("USE_API_MOCKS") == "1"
    if use_mocks:
        mock = register_mocks()
        mock.start()
        client = ApiClient()
        yield client
        client.session.close()
        mock.stop()
        mock.reset()
    else:
        client = ApiClient()
        yield client
        client.session.close()
