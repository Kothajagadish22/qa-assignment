import pytest
from jsonschema import validate

from api_data import AUTH
from schemas import AUTH_TOKEN_SCHEMA


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.positive
def test_valid_credentials_return_token(api):
    res = api.post("/auth/login", json=AUTH["valid"])
    assert res.status_code in (200, 201), res.text

    body = res.json()
    validate(instance=body, schema=AUTH_TOKEN_SCHEMA)
    assert body.get("token")


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.negative
def test_invalid_credentials_no_valid_token(api):
    res = api.post("/auth/login", json=AUTH["invalid"])
    assert res.status_code in (400, 401, 403), res.text
    try:
        body = res.json()
    except ValueError:
        return
    assert "token" not in body or not body.get("token")


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.negative
def test_missing_credentials_rejected(api):
    res = api.post("/auth/login", json={})
    assert res.status_code >= 400


@pytest.mark.api
@pytest.mark.auth
def test_authenticated_request_with_bearer(api):
    login = api.post("/auth/login", json=AUTH["valid"])
    token = login.json()["token"]

    res = api.get("/carts/1", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code in (200, 201)
