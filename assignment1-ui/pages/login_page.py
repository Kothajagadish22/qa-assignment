from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.locator('[data-test="error"]')

    def goto(self) -> None:
        self.page.goto(BASE_URL)

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_error_contains(self, text: str) -> None:
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(text)
