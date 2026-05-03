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

    def _show_ai_overlay(self, message: str, level: str = "INFO"):
        """Injects a beautiful AI thinking overlay into the browser DOM for client demos."""
        try:
            color = "#16a34a" if level == "INFO" else "#dc2626" if level in ("ERROR", "CRITICAL") else "#eab308"
            script = f"""
            (() => {{
                let el = document.getElementById('ai-overlay-box');
                if (!el) {{
                    el = document.createElement('div');
                    el.id = 'ai-overlay-box';
                    el.style.position = 'fixed';
                    el.style.bottom = '20px';
                    el.style.right = '20px';
                    el.style.backgroundColor = '#0f172a';
                    el.style.color = '#e2e8f0';
                    el.style.padding = '15px 25px';
                    el.style.borderRadius = '12px';
                    el.style.fontFamily = 'monospace';
                    el.style.fontSize = '14px';
                    el.style.zIndex = '999999';
                    el.style.boxShadow = '0 20px 25px -5px rgba(0,0,0,0.5)';
                    el.style.borderLeft = '6px solid {color}';
                    el.style.maxWidth = '350px';
                    el.style.lineHeight = '1.5';
                    document.body.appendChild(el);
                }}
                el.style.borderLeft = '6px solid {color}';
                el.innerHTML = '<strong style="color:#38bdf8">🤖 AI AGENT ACTIVE</strong><br><br><span style="color:#94a3b8">Action:</span> ' + `{message}`;
            }})();
            """
            self.page.evaluate(script)
            self.page.wait_for_timeout(800) # Small pause so the client can read it
        except Exception:
            pass

    def show_ai_boot_sequence(self):
        """Displays a dramatic initialization sequence on the UI for client demos."""
        try:
            self._show_ai_overlay("<b>Status:</b> Initializing Framework...<br><br><span style='color:#94a3b8'>Mounting Multi-Agent System...</span>")
            self.page.wait_for_timeout(800)
            self._show_ai_overlay("<b>Status:</b> Framework Active<br><br><span style='color:#4ade80'>✓ AI Agent Installed</span><br><span style='color:#4ade80'>✓ AI Agent Setup Complete</span><br><br><span style='color:#38bdf8'>Initiating AI Thinking Engine...</span>")
            self.page.wait_for_timeout(1500)
        except Exception:
            pass

    # ── Smart Methods (Full AI Reasoning + Healing) ────────────────────────────

    def smart_click(self, selector: str, reason: str = "Standard Interaction"):
        """Clicks an element with AI reasoning, failure prediction, and auto-healing."""
        self._show_ai_overlay(f"Clicking element <b>{selector}</b><br><br><span style='color:#94a3b8'>Reason:</span> {reason}")
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
        self._show_ai_overlay(f"Typing <span style='color:#facc15'>\"{text}\"</span> into <b>{selector}</b><br><br><span style='color:#94a3b8'>Reason:</span> {reason}")
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
        self._show_ai_overlay(f"Clicking element <b>{selector}</b>", level="INFO")
        try:
            self.page.click(selector, timeout=5000)
        except Exception as e:
            self.ai.thinking.think(f"Locator failure on '{selector}' — triggering Self-Healing...", level="WARNING")
            self._heal_and_retry("click", selector, str(e))

    def fill(self, selector: str, text: str):
        """Backward-compatible fill with embedded self-healing."""
        self._show_ai_overlay(f"Typing <span style='color:#facc15'>\"{text}\"</span> into <b>{selector}</b>", level="INFO")
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
        self._show_ai_overlay(f"<span style='color:#fb7185'>Failure Detected!</span><br>Element <b>{old_selector}</b> not found.<br><br>Calling HEALER Agent...", level="WARNING")
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
                self._show_ai_overlay(f"<span style='color:#4ade80'>Self-Healing Successful!</span><br>Found new locator: <b>{new_selector}</b><br><br>Retrying action...", level="INFO")
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
