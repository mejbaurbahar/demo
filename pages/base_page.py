from playwright.sync_api import Page
from components.ai_service import AIService

import time

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.ai = AIService()

    def navigate(self, url: str):
        self.page.goto(url)

    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")

    def click(self, selector: str):
        try:
            self.page.click(selector, timeout=5000)
        except Exception as e:
            print(f"⚠️ Locator failed: {selector}. Attempting AI Self-Healing...")
            self._heal_and_retry("click", selector, str(e))

    def fill(self, selector: str, text: str):
        try:
            self.page.fill(selector, text, timeout=5000)
        except Exception as e:
            print(f"⚠️ Locator failed: {selector}. Attempting AI Self-Healing...")
            self._heal_and_retry("fill", selector, str(e), text)

    def _heal_and_retry(self, action, old_selector, error, text=None):
        """Self-healing logic: Captures HTML, gets AI suggestion, and retries."""
        try:
            # Only attempt healing if it looks like a locator issue
            if "timeout" in str(error).lower() or "not found" in str(error).lower() or "selector" in str(error).lower():
                html = self.page.content()
                new_selector = self.ai.suggest_new_locator(html, f"Element intended for {action} with selector {old_selector}", error)
                
                if new_selector and new_selector != old_selector and new_selector != "FAILED":
                    print(f"✅ AI Found New Locator: {new_selector}. Retrying...")
                    if action == "click":
                        self.page.click(new_selector, timeout=5000)
                    elif action == "fill":
                        self.page.fill(new_selector, text, timeout=5000)
                    return
        except Exception:
            pass
        
        # If healing fails or isn't applicable, raise the original error properly
        raise Exception(f"Action '{action}' failed for selector '{old_selector}'. {error}")



    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)

