import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_pages import CheckoutStepOne

@pytest.mark.regression
class TestLoginScenarios:
    
    @pytest.mark.parametrize("username, password, expected_error", [
        ("", "", "Epic sadface: Username is required"),
        ("standard_user", "", "Epic sadface: Password is required"),
        ("", "secret_sauce", "Epic sadface: Username is required"),
        ("invalid_user", "secret_sauce", "Epic sadface: Username and password do not match any user in this service"),
        ("standard_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
    ])
    def test_invalid_login_scenarios(self, page, username, password, expected_error):
        login_page = LoginPage(page)
        login_page.navigate("https://www.saucedemo.com/")
        login_page.login(username, password)
        assert expected_error in login_page.get_error_message()

    @pytest.mark.parametrize("username", [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user"
    ])
    def test_valid_users_login(self, page, username):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        login_page.navigate("https://www.saucedemo.com/")
        login_page.login(username, "secret_sauce")
        assert inventory_page.is_visible(inventory_page.header_title)
        inventory_page.logout()

@pytest.mark.regression
class TestCheckoutFormValidation:
    
    @pytest.mark.parametrize("first, last, zip, expected_error", [
        ("", "Doe", "12345", "Error: First Name is required"),
        ("John", "", "12345", "Error: Last Name is required"),
        ("John", "Doe", "", "Error: Postal Code is required"),
        ("!@#$%^", "Doe", "12345", None), # Special chars in name (should usually pass or have specific validation)
        ("A" * 100, "B" * 100, "123", None), # Long strings
    ])
    def test_checkout_form_validation(self, page, first, last, zip, expected_error):
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
            error_msg = page.inner_text("h3[data-test='error']")
            assert expected_error in error_msg
        else:
            # If no error expected, we should be on step two
            assert "checkout-step-two" in page.url

@pytest.mark.regression
class TestInventoryInteraction:
    
    def test_sort_all_options(self, page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        login_page.navigate("https://www.saucedemo.com/")
        login_page.login("standard_user", "secret_sauce")
        
        sort_options = ["az", "za", "lohi", "hilo"]
        for option in sort_options:
            inventory_page.change_sort(option)
            # Add verification logic for sorting if needed
            
    def test_add_remove_all_items(self, page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        login_page.navigate("https://www.saucedemo.com/")
        login_page.login("standard_user", "secret_sauce")
        
        items = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        
        for item in items:
            inventory_page.add_to_cart(item)
            
        cart_badge = page.inner_text(".shopping_cart_badge")
        assert cart_badge == str(len(items))
        
        for item in items:
            inventory_page.remove_from_cart(item)
            
        assert not inventory_page.is_visible(".shopping_cart_badge")
