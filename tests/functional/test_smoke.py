import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.smoke
@pytest.mark.sanity
def test_basic_login_smoke(page):
    """
    Smoke/Sanity Test: Verifies the most critical path (Login) is working.
    """
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    inventory_page = InventoryPage(page)
    assert inventory_page.is_visible(inventory_page.header_title)
    assert inventory_page.get_text(inventory_page.header_title) == "Products"

@pytest.mark.retesting
def test_login_error_message_retest(page):
    """
    Retesting: Verifies a previously reported bug (e.g., missing error message) is fixed.
    """
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("locked_out_user", "secret_sauce")
    assert login_page.is_visible(login_page.error_message)
    assert "Epic sadface: Sorry, this user has been locked out." in login_page.get_text(login_page.error_message)

@pytest.mark.integration
def test_login_to_inventory_integration(page):
    """
    Integration Test: Verifies the transition between Login and Inventory components.
    """
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    
    # Check if inventory items are loaded
    assert inventory_page.is_visible(inventory_page.inventory_list)
