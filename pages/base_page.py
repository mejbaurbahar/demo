from playwright.sync_api import Page
from components.ai_service import AIService
import time


class BasePage:
    """
    BasePage with full AI Self-Healing and Smart Interaction Engine.
    - smart_click / smart_fill: full reasoning + healing
    - click / fill: backward-compatible aliases
    """

    def __init__(self, page: Page):
        self.page = page
        self.ai = AIService()

    def navigate(self, url: str):
        self.page.goto(url)

    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")

    # ── Smart Methods (Full AI Reasoning + Healing) ────────────────────────────

    def smart_click(self, selector: str, reason: str = "Standard Interaction"):
        """Clicks an element with AI reasoning, failure prediction, and auto-healing."""
        self.ai.thinking.think(f"Intent: Click '{selector}' | Reason: {reason}")
        self.ai.thinking.think("Pre-check: Verifying element is not hidden or stale...")
        try:
            self.page.wait_for_selector(selector, timeout=4000)
            self.page.click(selector, timeout=5000)
            self.ai.thinking.think(f"Action Verified: Successfully clicked '{selector}'")
        except Exception as e:
            self.ai.thinking.think(f"Failure Detected on '{selector}': {str(e)[:80]}", level="ERROR")
            self._heal_and_retry("click", selector, str(e))

    def smart_fill(self, selector: str, text: str, reason: str = "Standard Input"):
        """Fills a field with AI reasoning and context-aware data validation."""
        self.ai.thinking.think(f"Intent: Fill '{selector}' | Reason: {reason}")
        try:
            self.page.wait_for_selector(selector, timeout=4000)
            self.page.fill(selector, text, timeout=5000)
            self.ai.thinking.think(f"Action Verified: Filled '{selector}' successfully")
        except Exception as e:
            self.ai.thinking.think(f"Fill Failure on '{selector}': {str(e)[:80]}", level="ERROR")
            self._heal_and_retry("fill", selector, str(e), text)

    # ── Backward-Compatible Aliases (used by all existing Page Objects) ─────────

    def click(self, selector: str):
        """Backward-compatible click with embedded self-healing."""
        try:
            self.page.click(selector, timeout=5000)
        except Exception as e:
            self.ai.thinking.think(f"Locator failure on '{selector}' — triggering Self-Healing...", level="WARNING")
            self._heal_and_retry("click", selector, str(e))

    def fill(self, selector: str, text: str):
        """Backward-compatible fill with embedded self-healing."""
        try:
            self.page.fill(selector, text, timeout=5000)
        except Exception as e:
            self.ai.thinking.think(f"Fill failure on '{selector}' — triggering Self-Healing...", level="WARNING")
            self._heal_and_retry("fill", selector, str(e), text)

    # ── Self-Healing Core Engine ───────────────────────────────────────────────

    def _heal_and_retry(self, action: str, old_selector: str, error: str, text: str = None):
        """
        Self-Healing Engine:
        1. Captures current DOM
        2. Queries AI HEALER agent for alternative locator
        3. Retries with new locator
        4. Logs healed mapping to AI memory for future runs
        """
        self.ai.thinking.think(
            f"[SELF-HEAL] Initiating recovery for '{old_selector}' — action: {action}", level="WARNING"
        )
        try:
            html = self.page.content()
            new_selector = self.ai.suggest_new_locator(html, old_selector, error)

            is_valid = (
                new_selector
                and new_selector != old_selector
                and "FAILED" not in new_selector
                and "FALLBACK" not in new_selector
                and len(new_selector) > 2
            )

            if is_valid:
                self.ai.thinking.think(
                    f"[SELF-HEAL] AI resolved new locator: '{new_selector}' — retrying..."
                )
                if action == "click":
                    self.page.click(new_selector, timeout=5000)
                elif action == "fill":
                    self.page.fill(new_selector, text, timeout=5000)

                # Persist to long-term memory
                self.ai._update_memory("healed_elements", {old_selector: new_selector})
                self.ai.thinking.think(
                    f"[SELF-HEAL] Recovery SUCCESS. Mapping saved: '{old_selector}' -> '{new_selector}'"
                )
                return
            else:
                self.ai.thinking.think(
                    f"[SELF-HEAL] AI could not produce a valid alternative locator.", level="CRITICAL"
                )
        except Exception as heal_error:
            self.ai.thinking.think(
                f"[SELF-HEAL] Recovery exception: {str(heal_error)[:80]}", level="CRITICAL"
            )

        raise Exception(f"[ACTION FAILED] '{action}' on selector '{old_selector}'. Original: {error}")

    # ── State Recovery ─────────────────────────────────────────────────────────

    def recover_to_url(self, url: str, reason: str = "State Recovery"):
        """Navigates back to a safe URL checkpoint."""
        self.ai.thinking.think(f"[RECOVERY] Navigating back to: {url} | Reason: {reason}")
        self.page.goto(url)
        self.wait_for_load()

    # ── Common Assertions ──────────────────────────────────────────────────────

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)

    def get_current_url(self) -> str:
        return self.page.url
