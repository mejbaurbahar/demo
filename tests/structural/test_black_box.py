import pytest
from pages.login_page import LoginPage

@pytest.mark.black_box
@pytest.mark.boundary
def test_password_length_boundary(page):
    """
    Boundary Value Analysis: Testing password field limits (hypothetical).
    """
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    
    # Testing with 'secret_sauce' (Standard)
    login_page.login("standard_user", "secret_sauce")
    assert "inventory.html" in page.url

@pytest.mark.equivalence
def test_user_type_equivalence_partitioning(page):
    """
    Equivalence Partitioning: Testing different classes of users.
    """
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    
    # Partition 1: Standard User
    login_page.login("standard_user", "secret_sauce")
    assert "inventory.html" in page.url
    
    # Partition 2: Problem User
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("problem_user", "secret_sauce")
    assert "inventory.html" in page.url

@pytest.mark.negative
def test_invalid_login_negative(page):
    """
    Negative Testing: Providing invalid input to ensure system handles it gracefully.
    """
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("invalid_user", "invalid_pass")
    assert login_page.is_visible(login_page.error_message)
    assert "Username and password do not match" in login_page.get_text(login_page.error_message)

@pytest.mark.positive
def test_valid_login_positive(page):
    """
    Positive Testing: Providing valid input to ensure system works as expected.
    """
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    assert "inventory.html" in page.url
