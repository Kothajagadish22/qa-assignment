import re

from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator(".title")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.inventory_items = page.locator(".inventory_item")
        self.item_prices = page.locator(".inventory_item_price")
        self.item_names = page.locator(".inventory_item_name")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"inventory\.html"))
        expect(self.title).to_have_text("Products")

    @staticmethod
    def _to_data_test_id(product_name: str) -> str:
        cleaned = product_name.lower().replace("(", "").replace(")", "")
        return re.sub(r"\s+", "-", cleaned)

    def add_item_to_cart(self, product_name: str) -> None:
        item_id = self._to_data_test_id(product_name)
        self.page.locator(f'[data-test="add-to-cart-{item_id}"]').click()

    def remove_item_from_cart(self, product_name: str) -> None:
        item_id = self._to_data_test_id(product_name)
        self.page.locator(f'[data-test="remove-{item_id}"]').click()

    def get_cart_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()

    def sort_by(self, value: str) -> None:
        """value: 'az' | 'za' | 'lohi' | 'hilo'"""
        self.sort_dropdown.select_option(value)

    def get_prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.item_prices.all_inner_texts()]
