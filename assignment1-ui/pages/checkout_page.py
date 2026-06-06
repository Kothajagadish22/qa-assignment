import re

from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.error_message = page.locator('[data-test="error"]')
        self.summary_total = page.locator(".summary_total_label")
        self.complete_header = page.locator(".complete-header")

    def fill_information(self, first: str, last: str, postal: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def continue_(self) -> None:
        self.continue_button.click()

    def finish(self) -> None:
        self.finish_button.click()

    def expect_overview_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"checkout-step-two\.html"))
        expect(self.summary_total).to_be_visible()

    def expect_order_complete(self) -> None:
        expect(self.page).to_have_url(re.compile(r"checkout-complete\.html"))
        expect(self.complete_header).to_have_text("Thank you for your order!")

    def expect_error_contains(self, text: str) -> None:
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(text)
