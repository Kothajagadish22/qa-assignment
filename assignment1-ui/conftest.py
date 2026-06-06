import os
import sys

# Make the page objects and test data importable from the tests.
sys.path.insert(0, os.path.dirname(__file__))

import pytest

from ui_data import USERS
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def logged_in_inventory(page):
    """Logs in as the standard user and returns a ready InventoryPage."""
    login = LoginPage(page)
    login.goto()
    login.login(USERS["standard"]["username"], USERS["standard"]["password"])
    inventory = InventoryPage(page)
    inventory.expect_loaded()
    return inventory
