"""Mock FakeStoreAPI responses for CI when the live API is unreachable from GitHub runners."""
import json
import re

import responses

BASE = "https://fakestoreapi.com"

CART_1 = {
    "id": 1,
    "userId": 1,
    "date": "2020-03-02T00:00:00.000Z",
    "products": [
        {"productId": 1, "quantity": 4},
        {"productId": 2, "quantity": 1},
        {"productId": 3, "quantity": 6},
    ],
    "__v": 0,
}

CART_2 = {
    "id": 2,
    "userId": 3,
    "date": "2019-12-02T00:00:00.000Z",
    "products": [{"productId": 1, "quantity": 4}],
    "__v": 0,
}

CARTS_LIST = [
    CART_1,
    CART_2,
    {
        "id": 3,
        "userId": 2,
        "date": "2019-12-01T00:00:00.000Z",
        "products": [{"productId": 1, "quantity": 4}],
        "__v": 0,
    },
]

PRODUCTS = {
    1: {
        "id": 1,
        "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
        "price": 109.95,
        "description": "Your perfect pack for everyday use",
        "category": "men's clothing",
        "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
        "rating": {"rate": 3.9, "count": 120},
    },
    2: {
        "id": 2,
        "title": "Mens Casual Premium Slim Fit T-Shirts",
        "price": 22.3,
        "description": "Slim-fitting style",
        "category": "men's clothing",
        "image": "https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg",
        "rating": {"rate": 4.1, "count": 259},
    },
    3: {
        "id": 3,
        "title": "Mens Cotton Jacket",
        "price": 55.99,
        "description": "Great outerwear jackets",
        "category": "men's clothing",
        "image": "https://fakestoreapi.com/img/71li7pjIGL._AC_UL640_QL65_ML3_.jpg",
        "rating": {"rate": 4.7, "count": 500},
    },
    5: {
        "id": 5,
        "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet",
        "price": 695,
        "description": "From our Legends Collection",
        "category": "jewelery",
        "image": "https://fakestoreapi.com/img/71pWzhdJNwL._AC_UL640_QL65_ML3_.jpg",
        "rating": {"rate": 4.6, "count": 400},
    },
}

VALID_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Im1vcl8yMzE0IiwiaWF0IjoxNTE2MjM5MDIyfQ."
    "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
)


def _post_cart_callback(request):
    payload = json.loads(request.body or "{}")
    response = {
        "id": 11,
        "userId": payload.get("userId", 1),
        "date": payload.get("date", "2024-01-01"),
        "products": payload.get("products", []),
        "__v": 0,
    }
    return 201, {}, json.dumps(response)


def _put_cart_callback(request):
    payload = json.loads(request.body or "{}")
    cart_id = int(request.url.rstrip("/").split("/")[-1])
    response = {
        "id": cart_id,
        "userId": payload.get("userId", 1),
        "date": payload.get("date", "2024-01-01"),
        "products": payload.get("products", []),
        "__v": 0,
    }
    return 200, {}, json.dumps(response)


def register_mocks() -> responses.RequestsMock:
    """Register all FakeStoreAPI endpoints used by the test suite."""
    mock = responses.RequestsMock(assert_all_requests_are_fired=False)

    mock.add(
        responses.POST,
        f"{BASE}/auth/login",
        body="username and password are not provided in JSON format",
        status=400,
        content_type="text/plain",
        match=[responses.matchers.json_params_matcher({})],
    )
    mock.add(
        responses.POST,
        f"{BASE}/auth/login",
        body="username or password is incorrect",
        status=401,
        content_type="text/plain",
        match=[
            responses.matchers.json_params_matcher(
                {"username": "mor_2314", "password": "totally_wrong"}
            )
        ],
    )
    mock.add(
        responses.POST,
        f"{BASE}/auth/login",
        json={"token": VALID_TOKEN},
        status=200,
        match=[
            responses.matchers.json_params_matcher(
                {"username": "mor_2314", "password": "83r5^_"}
            )
        ],
    )

    mock.add(responses.GET, f"{BASE}/carts", json=CARTS_LIST, status=200)
    mock.add(responses.GET, f"{BASE}/carts/1", json=CART_1, status=200)
    mock.add(responses.GET, f"{BASE}/carts/2", json=CART_2, status=200)
    mock.add(responses.GET, f"{BASE}/carts/999999", body="null", status=200, content_type="application/json")
    mock.add(responses.GET, re.compile(rf"{BASE}/carts/not-a-number"), json={"error": "bad id"}, status=404)

    mock.add_callback(responses.POST, f"{BASE}/carts", callback=_post_cart_callback, content_type="application/json")
    mock.add_callback(
        responses.PUT,
        re.compile(rf"{BASE}/carts/\d+"),
        callback=_put_cart_callback,
        content_type="application/json",
    )
    mock.add(responses.DELETE, f"{BASE}/carts/1", json=CART_1, status=200)
    mock.add(responses.DELETE, f"{BASE}/carts/999999", body="", status=200)

    for product_id, product in PRODUCTS.items():
        mock.add(responses.GET, f"{BASE}/products/{product_id}", json=product, status=200)

    return mock
