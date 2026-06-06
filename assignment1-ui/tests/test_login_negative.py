import pytest

from ui_data import USERS


@pytest.mark.ui
@pytest.mark.negative
def test_locked_out_user_blocked(login_page):
    login_page.goto()
    login_page.login(USERS["locked_out"]["username"], USERS["locked_out"]["password"])
    login_page.expect_error_contains("Sorry, this user has been locked out")


@pytest.mark.ui
@pytest.mark.negative
def test_invalid_password_rejected(login_page):
    login_page.goto()
    login_page.login(USERS["standard"]["username"], "wrong_password")
    login_page.expect_error_contains("Username and password do not match")


@pytest.mark.ui
@pytest.mark.negative
def test_unknown_username_rejected(login_page):
    login_page.goto()
    login_page.login("ghost_user", USERS["standard"]["password"])
    login_page.expect_error_contains("Username and password do not match")


@pytest.mark.ui
@pytest.mark.negative
def test_empty_username_rejected(login_page):
    login_page.goto()
    login_page.login("", USERS["standard"]["password"])
    login_page.expect_error_contains("Username is required")


@pytest.mark.ui
@pytest.mark.negative
def test_empty_password_rejected(login_page):
    login_page.goto()
    login_page.login(USERS["standard"]["username"], "")
    login_page.expect_error_contains("Password is required")
