"""
Workflow Healer
Detects and recovers broken application state automatically.
Handles: session expiry, unexpected popups, wrong page, cart loss, modal overlays.
"""
from playwright.sync_api import Page
from utils.thinking_engine import ThinkingEngine


class WorkflowHealer:
    """
    Autonomous Workflow State Recovery Engine.
    Diagnoses what went wrong with the application state and restores it.
    """

    BASE_URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page, thinking: ThinkingEngine = None):
        self.page = page
        self.thinking = thinking or ThinkingEngine()

    def diagnose_and_heal(self) -> str:
        """
        Runs a full state diagnosis and attempts recovery.
        Returns a string describing the recovery action taken.
        """
        self.thinking.think("[HEALER] Running workflow state diagnosis...")

        # 1. Detect session expiry (redirect to login)
        if self._is_on_login_page() and "inventory" not in self.page.url:
            return self._recover_session()

        # 2. Detect unexpected modal/alert
        if self._has_open_dialog():
            return self._close_dialog()

        # 3. Detect error banner
        if self._has_error_banner():
            return self._dismiss_error_banner()

        # 4. Detect wrong page (not on expected workflow step)
        current_url = self.page.url
        self.thinking.think(f"[HEALER] Current URL: {current_url} — state appears valid.")
        return "NO_RECOVERY_NEEDED"

    def _is_on_login_page(self) -> bool:
        return "saucedemo.com" in self.page.url and self.page.is_visible("id=login-button")

    def _has_open_dialog(self) -> bool:
        # Playwright auto-dismisses dialogs; this checks for visible overlay divs
        return self.page.is_visible(".bm-overlay") or False

    def _has_error_banner(self) -> bool:
        return self.page.is_visible("h3[data-test='error']")

    def _recover_session(self) -> str:
        """Re-authenticates with standard credentials."""
        self.thinking.think("[HEALER] Session expired — re-logging in as standard_user...", level="WARNING")
        self.page.fill("id=user-name", "standard_user")
        self.page.fill("id=password",  "secret_sauce")
        self.page.click("id=login-button")
        self.page.wait_for_load_state("networkidle")
        self.thinking.think("[HEALER] Session restored successfully.")
        return "SESSION_RESTORED"

    def _close_dialog(self) -> str:
        """Closes any open overlay/sidebar."""
        self.thinking.think("[HEALER] Unexpected overlay detected — closing...", level="WARNING")
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)
        except Exception:
            pass
        return "OVERLAY_CLOSED"

    def _dismiss_error_banner(self) -> str:
        """Dismisses the error banner if present."""
        self.thinking.think("[HEALER] Error banner detected — dismissing...", level="WARNING")
        try:
            self.page.click(".error-button")
        except Exception:
            pass
        return "ERROR_BANNER_DISMISSED"

    def restore_cart(self, product_name: str) -> str:
        """Ensures a product is in the cart; adds it if missing."""
        self.thinking.think(f"[HEALER] Checking cart state for '{product_name}'...")
        cart_badge = self.page.locator(".shopping_cart_badge")
        if not cart_badge.is_visible():
            self.thinking.think("[HEALER] Cart is empty — re-adding product...", level="WARNING")
            selector = f"id=add-to-cart-{product_name.lower().replace(' ', '-')}"
            try:
                self.page.click(selector, timeout=4000)
                return "CART_RESTORED"
            except Exception as e:
                self.thinking.think(f"[HEALER] Could not restore cart: {e}", level="ERROR")
                return "CART_RESTORE_FAILED"
        return "CART_OK"

    def navigate_to_checkpoint(self, url: str) -> str:
        """Hard-navigates to a known-good URL checkpoint."""
        self.thinking.think(f"[HEALER] Navigating to checkpoint: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        return f"NAVIGATED_TO:{url}"
