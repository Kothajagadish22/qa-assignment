import pytest

from ui_data import USERS


@pytest.mark.ui
@pytest.mark.positive
def test_standard_user_can_login(login_page, inventory_page):
    login_page.goto()
    login_page.login(USERS["standard"]["username"], USERS["standard"]["password"])
    inventory_page.expect_loaded()


@pytest.mark.ui
@pytest.mark.positive
def test_user_can_logout(login_page, inventory_page):
    login_page.goto()
    login_page.login(USERS["standard"]["username"], USERS["standard"]["password"])
    inventory_page.expect_loaded()

    inventory_page.logout()
    login_page.login_button.wait_for()
