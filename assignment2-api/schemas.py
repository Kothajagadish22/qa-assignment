"""JSON Schemas (Draft 2020-12) used for response validation."""

CART_PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "productId": {"type": "number"},
        "quantity": {"type": "number"},
    },
    "required": ["productId", "quantity"],
}

CART_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "userId": {"type": "number"},
        "date": {"type": "string"},
        "products": {"type": "array", "items": CART_PRODUCT_SCHEMA},
        "__v": {"type": "number"},
    },
    "required": ["id", "userId", "date", "products"],
}

CART_LIST_SCHEMA = {"type": "array", "items": CART_SCHEMA}

PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "description": {"type": "string"},
        "category": {"type": "string"},
        "image": {"type": "string"},
        "rating": {
            "type": "object",
            "properties": {
                "rate": {"type": "number"},
                "count": {"type": "number"},
            },
        },
    },
    "required": ["id", "title", "price", "description", "category", "image"],
}

AUTH_TOKEN_SCHEMA = {
    "type": "object",
    "properties": {"token": {"type": "string", "minLength": 1}},
    "required": ["token"],
}
