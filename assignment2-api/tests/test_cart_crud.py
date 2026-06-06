"""Cart CRUD happy paths against FakeStoreAPI.

Note: FakeStoreAPI is a mock backend - writes are simulated (not persisted),
but it returns realistic, well-formed responses we can assert against.
"""
import pytest
from jsonschema import validate

from api_data import new_cart_payload
from schemas import CART_SCHEMA, CART_LIST_SCHEMA


@pytest.mark.api
@pytest.mark.positive
def test_get_carts_returns_list(api):
    res = api.get("/carts")
    assert res.status_code == 200

    body = res.json()
    assert isinstance(body, list)
    assert len(body) > 0
    validate(instance=body, schema=CART_LIST_SCHEMA)


@pytest.mark.api
@pytest.mark.positive
def test_get_single_cart(api):
    res = api.get("/carts/1")
    assert res.status_code == 200

    body = res.json()
    assert body["id"] == 1
    validate(instance=body, schema=CART_SCHEMA)


@pytest.mark.api
@pytest.mark.positive
def test_post_creates_cart(api):
    payload = new_cart_payload()
    res = api.post("/carts", json=payload)
    assert res.status_code in (200, 201)

    body = res.json()
    assert "id" in body
    assert body["userId"] == payload["userId"]
    assert body["products"] == payload["products"]


@pytest.mark.api
@pytest.mark.positive
def test_put_updates_cart(api):
    payload = new_cart_payload(userId=3, products=[{"productId": 2, "quantity": 4}])
    res = api.put("/carts/1", json=payload)
    assert res.status_code in (200, 201)

    body = res.json()
    assert body["id"] == 1
    assert body["userId"] == 3
    assert body["products"] == payload["products"]


@pytest.mark.api
@pytest.mark.positive
def test_delete_cart(api):
    res = api.delete("/carts/1")
    assert res.status_code in (200, 201)

    body = res.json()
    assert "id" in body
