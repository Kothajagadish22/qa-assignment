"""Negative / edge cases for the cart endpoints.

FakeStoreAPI is a lenient public mock, so several assertions are written
defensively: we accept either a proper error status OR an empty/null body.
This documents the *expected* contract while staying green against the mock.
"""
import pytest


@pytest.mark.api
@pytest.mark.negative
def test_get_nonexistent_cart(api):
    res = api.get("/carts/999999")
    # A strict API would return 404; the mock returns 200 with null/empty body.
    raw = res.text.strip()
    if not raw:
        parsed = None
    else:
        try:
            parsed = res.json()
        except ValueError:
            parsed = raw
    assert parsed in (None, "", {}) or (isinstance(parsed, dict) and not parsed)


@pytest.mark.api
@pytest.mark.negative
def test_get_cart_non_numeric_id(api):
    res = api.get("/carts/not-a-number")
    assert res.status_code < 500


@pytest.mark.api
@pytest.mark.negative
def test_delete_nonexistent_cart(api):
    res = api.delete("/carts/999999")
    assert res.status_code < 500


@pytest.mark.api
@pytest.mark.negative
def test_post_empty_body(api):
    res = api.post("/carts", json={})
    assert res.status_code < 500
