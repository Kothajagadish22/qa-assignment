"""Response schema validation: every field must exist with the correct type."""
import pytest
from jsonschema import validate

from schemas import CART_SCHEMA, CART_LIST_SCHEMA


@pytest.mark.api
@pytest.mark.schema
def test_single_cart_matches_schema(api):
    res = api.get("/carts/2")
    assert res.status_code == 200
    validate(instance=res.json(), schema=CART_SCHEMA)


@pytest.mark.api
@pytest.mark.schema
def test_cart_list_matches_schema(api):
    res = api.get("/carts")
    assert res.status_code == 200
    validate(instance=res.json(), schema=CART_LIST_SCHEMA)


@pytest.mark.api
@pytest.mark.schema
def test_created_cart_matches_schema(api):
    res = api.post(
        "/carts",
        json={"userId": 1, "date": "2024-05-05", "products": [{"productId": 1, "quantity": 1}]},
    )
    validate(instance=res.json(), schema=CART_SCHEMA)
