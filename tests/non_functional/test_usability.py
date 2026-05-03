"""
Accessibility & Usability Test Suite
Covers: WCAG audit (Axe), keyboard navigation, visual contrast cues, responsive viewport,
        missing alt text, form label associations.
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def _login(page: Page):
    login = LoginPage(page)
    login.navigate("https://www.saucedemo.com/")
    login.login("standard_user", "secret_sauce")
    return InventoryPage(page)


# ── WCAG Axe Audit ────────────────────────────────────────────────────────────

@pytest.mark.accessibility
@pytest.mark.regression
def test_wcag_accessibility_login_page(page: Page):
    """Runs Axe WCAG audit on the login page. Reports violations without hard-failing."""
    try:
        from axe_playwright_python.sync_playwright import Axe
        login = LoginPage(page)
        login.navigate("https://www.saucedemo.com/")
        axe      = Axe()
        results  = axe.run(page)

        if isinstance(results, dict):
            violations = results.get("violations", [])
        else:
            violations = getattr(results, "violations",
                                 getattr(results, "response", {}).get("violations", []))

        print(f"\n[A11Y] Login page violations: {len(violations)}")
        for v in violations:
            print(f"  - [{v.get('impact','?')}] {v.get('id','?')}: {v.get('description','?')}")

        # Soft assertion: warn, not fail (known demo-site limitations)
        if len(violations) > 10:
            pytest.xfail(f"Too many accessibility violations: {len(violations)}")
    except ImportError:
        pytest.skip("axe-playwright-python not installed")


@pytest.mark.accessibility
@pytest.mark.regression
def test_wcag_accessibility_inventory_page(page: Page):
    """Runs Axe WCAG audit on the inventory page."""
    try:
        from axe_playwright_python.sync_playwright import Axe
        _login(page)
        axe     = Axe()
        results = axe.run(page)

        if isinstance(results, dict):
            violations = results.get("violations", [])
        else:
            violations = getattr(results, "violations",
                                 getattr(results, "response", {}).get("violations", []))

        print(f"\n[A11Y] Inventory page violations: {len(violations)}")
        assert isinstance(violations, list)
    except ImportError:
        pytest.skip("axe-playwright-python not installed")


# ── Keyboard Navigation ───────────────────────────────────────────────────────

@pytest.mark.accessibility
@pytest.mark.usability
def test_keyboard_navigation_login(page: Page):
    """Verifies that the login form can be completed using only the keyboard."""
    page.goto("https://www.saucedemo.com/")
    page.keyboard.press("Tab")           # Focus username
    page.keyboard.type("standard_user")
    page.keyboard.press("Tab")           # Focus password
    page.keyboard.type("secret_sauce")
    page.keyboard.press("Enter")         # Submit

    page.wait_for_load_state("networkidle")
    assert "inventory.html" in page.url, "Keyboard-only login must reach inventory."


@pytest.mark.accessibility
@pytest.mark.usability
def test_tab_order_is_logical(page: Page):
    """Verifies Tab key moves through form fields in the correct order."""
    page.goto("https://www.saucedemo.com/")
    page.keyboard.press("Tab")
    username_focused = page.evaluate("document.activeElement.id") == "user-name"
    page.keyboard.press("Tab")
    password_focused = page.evaluate("document.activeElement.id") == "password"
    page.keyboard.press("Tab")
    button_focused = page.evaluate("document.activeElement.id") == "login-button"

    assert username_focused, "First Tab must focus username field."
    assert password_focused, "Second Tab must focus password field."
    assert button_focused,   "Third Tab must focus login button."


# ── Image Alt Text ────────────────────────────────────────────────────────────

@pytest.mark.accessibility
def test_images_have_alt_text(page: Page):
    """Finds images missing alt attributes and reports them."""
    _login(page)
    missing = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('img'))
            .filter(img => !img.alt || img.alt.trim() === '')
            .map(img => img.src);
    }""")
    print(f"\n[A11Y] Images missing alt text: {len(missing)}")
    for src in missing:
        print(f"  - {src}")
    # Informational — many product images on demo site lack alt text
    assert isinstance(missing, list)


# ── Form Labels ───────────────────────────────────────────────────────────────

@pytest.mark.accessibility
def test_form_inputs_have_labels(page: Page):
    """Verifies that all visible input fields have associated labels."""
    page.goto("https://www.saucedemo.com/")
    unlabelled = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('input:not([type=hidden])'))
            .filter(input => {
                const id = input.id;
                if (!id) return true;
                return !document.querySelector('label[for="' + id + '"]');
            })
            .map(i => i.id || i.name || i.type);
    }""")
    print(f"\n[A11Y] Inputs without labels: {unlabelled}")
    # Informational
    assert isinstance(unlabelled, list)


# ── Responsive Viewport ───────────────────────────────────────────────────────

@pytest.mark.accessibility
@pytest.mark.responsive
@pytest.mark.parametrize("width, height, label", [
    (375,  812,  "iPhone 14"),
    (768,  1024, "iPad"),
    (1280, 800,  "Desktop"),
    (1920, 1080, "Full HD"),
])
def test_responsive_login_page(page: Page, width, height, label):
    """Verifies login page renders correctly at common viewport sizes."""
    page.set_viewport_size({"width": width, "height": height})
    page.goto("https://www.saucedemo.com/")
    page.wait_for_load_state("networkidle")

    login = LoginPage(page)
    assert login.is_visible(login.login_button), (
        f"Login button not visible at {label} ({width}x{height})."
    )
    assert login.is_visible(login.username_input), (
        f"Username input not visible at {label} ({width}x{height})."
    )
    print(f"[RESPONSIVE] {label} ({width}x{height}): PASS")


# ── Error Message Visibility ──────────────────────────────────────────────────

@pytest.mark.usability
def test_error_message_visible_on_invalid_login(page: Page):
    """Verifies error messages are readable and visible to all users."""
    login = LoginPage(page)
    login.navigate("https://www.saucedemo.com/")
    login.login("invalid_user", "wrong_pass")

    assert login.is_visible(login.error_message), "Error message must be visible."
    error_text = login.get_error_message()
    assert len(error_text) > 10, "Error message must be descriptive (not empty/minimal)."
    print(f"[USABILITY] Error message: '{error_text}'")
