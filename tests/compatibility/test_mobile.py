import pytest

@pytest.mark.compatibility
@pytest.mark.responsive
@pytest.mark.mobile
def test_mobile_responsive_layout(page):
    """
    Responsive/Mobile Testing: Verifies UI layout on mobile viewports.
    """
    # Set viewport to iPhone 12
    page.set_viewport_size({"width": 390, "height": 844})
    
    page.goto("https://www.saucedemo.com/")
    
    # Verify login container is visible and properly sized
    login_container = page.locator(".login_wrapper")
    assert login_container.is_visible()
    
    # Check if elements are stacked vertically (responsive check)
    box = login_container.bounding_box()
    assert box['width'] <= 390

@pytest.mark.cross_browser
def test_cross_browser_support(browser_name, page):
    """
    Cross-Browser Testing: Playwright automatically runs this on multiple browsers if configured.
    """
    page.goto("https://www.saucedemo.com/")
    assert "Swag Labs" in page.title()
    print(f"Running on {browser_name}")
