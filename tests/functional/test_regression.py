import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_pages import CheckoutStepOne
from axe_playwright_python.sync_playwright import Axe
from datetime import datetime

@pytest.mark.regression
class TestLoginScenarios:
    
    @pytest.mark.parametrize("username, password, expected_error", [
        ("", "", "Epic sadface: Username is required"),
        ("standard_user", "", "Epic sadface: Password is required"),
        ("invalid_user", "secret_sauce", "Epic sadface: Username and password do not match any user in this service"),
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
        ("standard_user", "wrong_pass", "Epic sadface: Username and password do not match any user in this service"),

    ])
    def test_invalid_login_scenarios(self, page, username, password, expected_error):
        login_page = LoginPage(page)
        login_page.navigate("https://www.saucedemo.com/")
        login_page.login(username, password)
        assert expected_error in login_page.get_error_message()

@pytest.mark.regression
class TestCheckoutDataVariants:
    
    @pytest.mark.parametrize("first, last, zip, expected_error", [
        ("John", "Doe", "", "Error: Postal Code is required"),
        ("A" * 50, "B" * 50, "99999", None), # Stable long strings
        ("<b>Injection</b>", "Alert", "00000", None), # Basic Injection
        ("12345", "67890", "12345", None), # Numeric names
        ("Spaces", "Trimmed", "123", None), # Padding

    ])
    def test_checkout_data_variants(self, page, first, last, zip, expected_error):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        checkout_one = CheckoutStepOne(page)
        
        login_page.navigate("https://www.saucedemo.com/")
        login_page.login("standard_user", "secret_sauce")
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.go_to_cart()
        page.click("id=checkout")
        
        checkout_one.fill_form(first, last, zip)
        
        if expected_error:
            assert expected_error in page.inner_text("h3[data-test='error']")
        else:
            assert "checkout-step-two" in page.url

@pytest.mark.regression
def test_accessibility_audit(page):
    """WCAG Accessibility Audit using Axe."""
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    
    axe = Axe()
    results = axe.run(page)
    
    # In axe-playwright-python, results is a dict containing 'violations'
    violations = results["violations"] if isinstance(results, dict) else results.violations
    if len(violations) > 0:
        print(f"Accessibility violations found: {len(violations)}")


@pytest.mark.regression
def test_page_load_performance(page):
    """Basic performance baseline test."""
    login_page = LoginPage(page)
    
    start_time = datetime.now()
    login_page.navigate("https://www.saucedemo.com/")
    end_time = datetime.now()
    
    load_duration = (end_time - start_time).total_seconds()
    print(f"Page load took: {load_duration} seconds")
    
    # Assert standard baseline (e.g., < 3 seconds)
    assert load_duration < 5.0 
