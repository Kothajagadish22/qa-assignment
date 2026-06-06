import pytest

from ui_data import USERS, PRODUCTS, CHECKOUT_INFO
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.ui
@pytest.mark.e2e
def test_full_purchase_flow(page, logged_in_inventory):
    inventory = logged_in_inventory
    cart = CartPage(page)
    checkout = CheckoutPage(page)

    inventory.add_item_to_cart(PRODUCTS["backpack"])
    inventory.add_item_to_cart(PRODUCTS["bolt_tshirt"])
    assert inventory.get_cart_count() == 2

    inventory.open_cart()
    cart.expect_loaded()
    assert cart.get_item_count() == 2
    cart.checkout()

    checkout.fill_information(
        CHECKOUT_INFO["first_name"],
        CHECKOUT_INFO["last_name"],
        CHECKOUT_INFO["postal_code"],
    )
    checkout.continue_()
    checkout.expect_overview_loaded()

    checkout.finish()
    checkout.expect_order_complete()


@pytest.mark.ui
@pytest.mark.negative
def test_checkout_blocked_without_postal_code(page, login_page):
    from pages.inventory_page import InventoryPage

    login_page.goto()
    login_page.login(USERS["standard"]["username"], USERS["standard"]["password"])

    inventory = InventoryPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

    inventory.add_item_to_cart(PRODUCTS["backpack"])
    inventory.open_cart()
    cart.checkout()

    checkout.fill_information(
        CHECKOUT_INFO["first_name"], CHECKOUT_INFO["last_name"], ""
    )
    checkout.continue_()
    checkout.expect_error_contains("Postal Code is required")
