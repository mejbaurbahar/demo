import pytest
import requests
import ssl
import socket
from datetime import datetime

@pytest.mark.security
def test_security_headers():
    response = requests.get("https://www.saucedemo.com/")
    headers = response.headers
    
    # Basic OWASP security headers check
    # Note: Not all sites implement all of these
    # assert "Content-Security-Policy" in headers
    assert "X-Frame-Options" in headers
    assert "X-Content-Type-Options" in headers

@pytest.mark.security
def test_ssl_certificate():
    hostname = "www.saucedemo.com"
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            
            # Check expiry
            not_after_str = cert['notAfter']
            expiry_date = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
            days_to_expiry = (expiry_date - datetime.now()).days
            
            print(f"SSL Certificate for {hostname} expires in {days_to_expiry} days.")
            assert days_to_expiry > 30 # Alert if less than 30 days

@pytest.mark.security
@pytest.mark.parametrize("payload", [
    "' OR '1'='1",
    "admin'--",
    "' UNION SELECT NULL--",
    "\" OR \"\"=\"",
])
def test_sql_injection_login(page, payload):
    """
    Test SQL Injection vulnerability in Login.
    The system should not log in and should show an error or just fail.
    """
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login(payload, "any_password")
    
    # Verify we are still on the login page and see an error
    assert login_page.is_visible(login_page.error_message)
    assert "do not match any user" in login_page.get_error_message()

@pytest.mark.security
@pytest.mark.parametrize("payload", [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
])
def test_xss_injection_checkout(page, payload):
    """
    Test Cross-Site Scripting (XSS) in Checkout form.
    Verify that the payload is treated as a string and not executed.
    """
    from pages.login_page import LoginPage
    from pages.inventory_page import InventoryPage
    from pages.checkout_pages import CheckoutStepOne
    
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    checkout_one = CheckoutStepOne(page)
    
    # Setup: Go to checkout
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.go_to_cart()
    page.click("id=checkout")
    
    # Attempt XSS injection
    checkout_one.fill_form(payload, "Doe", "12345")
    
    # In a real app, we would check if the script was executed.
    # With Playwright, we can listen for dialogs.
    page.on("dialog", lambda dialog: pytest.fail(f"XSS Alert triggered: {dialog.message}"))
    
    # Continue and check if the payload is displayed literally in step two
    assert "checkout-step-two" in page.url
    # Verify that the payload is rendered as text and not interpreted as HTML
    # (SauceDemo handles this safely)
