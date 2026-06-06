import pytest

from ui_data import PRODUCTS
from pages.cart_page import CartPage


@pytest.mark.ui
@pytest.mark.positive
def test_add_item_updates_badge(logged_in_inventory):
    inventory = logged_in_inventory
    assert inventory.get_cart_count() == 0

    inventory.add_item_to_cart(PRODUCTS["backpack"])
    assert inventory.get_cart_count() == 1


@pytest.mark.ui
@pytest.mark.positive
def test_multiple_items_appear_in_cart(page, logged_in_inventory):
    inventory = logged_in_inventory
    cart = CartPage(page)

    inventory.add_item_to_cart(PRODUCTS["backpack"])
    inventory.add_item_to_cart(PRODUCTS["bike_light"])
    assert inventory.get_cart_count() == 2

    inventory.open_cart()
    cart.expect_loaded()
    assert cart.get_item_count() == 2
    cart.expect_item_present(PRODUCTS["backpack"])
    cart.expect_item_present(PRODUCTS["bike_light"])


@pytest.mark.ui
@pytest.mark.positive
def test_remove_item_decrements_badge(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.add_item_to_cart(PRODUCTS["backpack"])
    inventory.add_item_to_cart(PRODUCTS["bike_light"])
    assert inventory.get_cart_count() == 2

    inventory.remove_item_from_cart(PRODUCTS["backpack"])
    assert inventory.get_cart_count() == 1


@pytest.mark.ui
@pytest.mark.positive
def test_sort_price_low_to_high(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.sort_by("lohi")

    prices = inventory.get_prices()
    assert prices == sorted(prices)


@pytest.mark.ui
@pytest.mark.positive
def test_sort_price_high_to_low(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.sort_by("hilo")

    prices = inventory.get_prices()
    assert prices == sorted(prices, reverse=True)
