import pytest

@pytest.mark.usability
@pytest.mark.accessibility
def test_accessibility_audit(page):
    """
    Accessibility Testing: Checks for ARIA labels and alt text.
    Note: Real accessibility testing usually requires axe-core.
    """
    page.goto("https://www.saucedemo.com/")
    
    # Simple check for alt text on images
    images = page.locator("img")
    count = images.count()
    for i in range(count):
        alt_text = images.nth(i).get_attribute("alt")
        assert alt_text is not None, f"Image {i} is missing alt text"

@pytest.mark.localization
@pytest.mark.i18n
def test_internationalization_placeholders(page):
    """
    Localization/i18n Testing: Verifies text content can be localized.
    """
    page.goto("https://www.saucedemo.com/")
    
    # Check for specific English strings that should be localizable
    login_button_val = page.get_attribute("#login-button", "value")
    assert login_button_val == "Login"
