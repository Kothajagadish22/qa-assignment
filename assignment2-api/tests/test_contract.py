"""Senior bonus - contract / snapshot test.

We derive a structural "shape" of the response (keys mapped to their JSON
types, recursively) and snapshot it to disk. Future responses must match the
committed snapshot, so any breaking change to the response contract
(added/removed field, changed type) fails the build.

Re-baseline intentionally by setting the env var before running:
    UPDATE_SNAPSHOTS=1 pytest assignment2-api/tests/test_contract.py
"""
import json
import os

import pytest

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "__snapshots__")


def derive_shape(value):
    if isinstance(value, list):
        return [derive_shape(value[0])] if value else ["unknown"]
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return {key: derive_shape(value[key]) for key in sorted(value)}
    if isinstance(value, (int, float)):
        return "number"
    return "string"


def assert_matches_snapshot(name: str, shape) -> None:
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    path = os.path.join(SNAPSHOT_DIR, f"{name}.json")
    actual = json.dumps(shape, indent=2, sort_keys=True)

    if os.environ.get("UPDATE_SNAPSHOTS") == "1" or not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(actual)
        return

    with open(path, "r", encoding="utf-8") as fh:
        expected = fh.read()
    assert actual == expected, (
        f"Contract drift for '{name}'.\nExpected:\n{expected}\nActual:\n{actual}"
    )


@pytest.mark.api
@pytest.mark.contract
def test_cart_contract(api):
    res = api.get("/carts/1")
    assert res.status_code == 200
    assert_matches_snapshot("cart-contract", derive_shape(res.json()))


@pytest.mark.api
@pytest.mark.contract
def test_product_contract(api):
    res = api.get("/products/1")
    assert res.status_code == 200
    assert_matches_snapshot("product-contract", derive_shape(res.json()))
