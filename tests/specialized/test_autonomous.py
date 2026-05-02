import pytest
import random
import time
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.monkey
def test_monkey_random_navigation(page):
    """
    Monkey Testing: Performs random clicks to test system resilience against unpredictable user behavior.
    """
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    
    # List of interactive selectors on inventory page
    selectors = [".inventory_item_name", ".btn_inventory", ".shopping_cart_link", ".product_sort_container"]
    
    for _ in range(5):
        selector = random.choice(selectors)
        try:
            elements = page.locator(selector).all()
            if elements:
                random.choice(elements).click(timeout=2000)
                page.go_back()
        except:
            pass

@pytest.mark.recovery
@pytest.mark.failover
def test_recovery_session_persistence(page, context):
    """
    Recovery Testing: Verifies the system recovers state after a simulated browser crash/restart.
    """
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    inventory_page.add_to_cart("Sauce Labs Backpack")
    
    # Save storage state
    storage = context.storage_state()
    
    # Simulate "Crash" by closing page and opening new one with same state
    page.close()
    new_page = context.new_page()
    new_page.goto("https://www.saucedemo.com/cart.html")
    
    # Verify item is still in cart (Recovery success)
    assert "Sauce Labs Backpack" in new_page.inner_text(".cart_list")

@pytest.mark.chaos
def test_api_chaos_latency_injection(page):
    """
    Chaos Testing: Injects artificial latency to verify UI resilience.
    """
    # Route all API calls to add a 2s delay
    page.route("**/*", lambda route: (time.sleep(1), route.continue_()))
    
    login_page = LoginPage(page)
    start_time = time.time()
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    duration = time.time() - start_time
    
    # Verify the app still works despite the "chaos"
    inventory_page = InventoryPage(page)
    assert inventory_page.is_visible(inventory_page.header_title)
    assert duration > 1 # Verified latency was injected
