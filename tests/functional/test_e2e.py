import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_pages import CartPage, CheckoutStepOne, CheckoutStepTwo, CheckoutComplete

@pytest.mark.smoke
def test_saucedemo_full_flow(page):
    # Setup Pages
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_step_one = CheckoutStepOne(page)
    checkout_step_two = CheckoutStepTwo(page)
    checkout_complete = CheckoutComplete(page)

    # 1. Login
    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.get_text(inventory_page.header_title) == "Products"

    # 2. Add to cart (Sauce Labs Backpack)
    inventory_page.add_to_cart("Sauce Labs Backpack")
    
    # 3. Remove from cart
    inventory_page.remove_from_cart("Sauce Labs Backpack")

    # 4. Check filter (Price High to Low)
    inventory_page.change_sort("hilo")

    # 5. Add another product (Sauce Labs Bolt T-Shirt)
    inventory_page.add_to_cart("Sauce Labs Bolt T-Shirt")

    # 6. Go to cart page
    inventory_page.go_to_cart()

    # 7. Checkout
    cart_page.click_checkout()

    # 8. Fillup checkout form
    checkout_step_one.fill_form("John", "Doe", "12345")

    # 9. Continue & Finish purchase
    checkout_step_two.click_finish()

    # 10. Verify success
    assert "Thank you for your order!" in checkout_complete.get_success_message()

    # 11. Logout
    inventory_page.logout()
    assert login_page.is_visible(login_page.login_button)
@pytest.mark.functional
def test_multi_item_complex_checkout(page):
    """
    Complex Functional Test: Multiple items, cart modification, and total price verification.
    """
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_one = CheckoutStepOne(page)
    checkout_two = CheckoutStepTwo(page)

    login_page.navigate("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    # Add 3 items
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.add_to_cart("Sauce Labs Bike Light")
    inventory_page.add_to_cart("Sauce Labs Bolt T-Shirt")

    # Go to cart and verify count
    inventory_page.go_to_cart()
    assert "3" in page.inner_text(".shopping_cart_link")

    # Remove one item in cart
    page.click("id=remove-sauce-labs-bike-light")
    assert "2" in page.inner_text(".shopping_cart_link")

    # Checkout
    cart_page.click_checkout()
    checkout_one.fill_form("Agent", "AI", "9999")
    
    # Verify subtotal (Backpack 29.99 + T-Shirt 15.99 = 45.98)
    subtotal_text = checkout_two.get_text(checkout_two.subtotal_label)
    assert "45.98" in subtotal_text
    
    checkout_two.click_finish()
    assert "Thank you" in page.inner_text(".complete-header")
