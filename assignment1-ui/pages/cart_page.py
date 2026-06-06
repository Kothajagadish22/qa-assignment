import re

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator(".title")
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"cart\.html"))
        expect(self.title).to_have_text("Your Cart")

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def expect_item_present(self, product_name: str) -> None:
        expect(self.cart_items.filter(has_text=product_name)).to_have_count(1)

    def checkout(self) -> None:
        self.checkout_button.click()
