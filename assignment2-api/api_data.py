AUTH = {
    "valid": {"username": "mor_2314", "password": "83r5^_"},
    "invalid": {"username": "mor_2314", "password": "totally_wrong"},
}

# Product IDs reused by the data-driven cart test.
PRODUCT_IDS = [1, 2, 3, 5]


def new_cart_payload(**overrides):
    payload = {
        "userId": 5,
        "date": "2024-01-01",
        "products": [
            {"productId": 1, "quantity": 2},
            {"productId": 5, "quantity": 1},
        ],
    }
    payload.update(overrides)
    return payload
