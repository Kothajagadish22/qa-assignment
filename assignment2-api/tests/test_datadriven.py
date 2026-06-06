"""Data-driven: the SAME scenario runs across 3+ product IDs.

Scenario = "fetch product -> put it in a cart -> validate both responses".
"""
import pytest
from jsonschema import validate

from api_data import PRODUCT_IDS
from schemas import PRODUCT_SCHEMA, CART_SCHEMA


@pytest.mark.api
@pytest.mark.datadriven
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_can_be_added_to_cart(api, product_id):
    product_res = api.get(f"/products/{product_id}")
    assert product_res.status_code == 200

    product = product_res.json()
    validate(instance=product, schema=PRODUCT_SCHEMA)
    assert product["id"] == product_id

    cart_res = api.post(
        "/carts",
        json={
            "userId": 1,
            "date": "2024-01-01",
            "products": [{"productId": product_id, "quantity": 2}],
        },
    )
    assert cart_res.status_code in (200, 201)

    cart = cart_res.json()
    validate(instance=cart, schema=CART_SCHEMA)
    assert cart["products"][0]["productId"] == product_id
    assert cart["products"][0]["quantity"] == 2
