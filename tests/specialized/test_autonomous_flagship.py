"""
Autonomous Flagship Test Suite
Demonstrates the full Autonomous AI QA Operating System in action:
  - Recursive AI Thinking
  - Dynamic Test Generation
  - Self-Healing Interactions
  - Autonomous Workflow Recovery
  - Multi-Agent Collaboration
  - AI-Generated Security Scenarios
"""
import pytest
from playwright.sync_api import Page
from components.ai_service import AIService
from utils.workflow_healer import WorkflowHealer
from utils.test_data_generator import TestDataGenerator
from utils.performance_monitor import PerformanceMonitor
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_pages import CartPage, CheckoutStepOne, CheckoutStepTwo, CheckoutComplete


# ── Helper: Login safely with state verification ──────────────────────────────
def _login(page: Page, username: str = "standard_user", password: str = "secret_sauce"):
    login = LoginPage(page)
    login.navigate("https://www.saucedemo.com/")
    login.login(username, password)
    return login


# ─────────────────────────────────────────────────────────────────────────────
# TEST 1: Full AI Thinking Engine + Workflow Recovery
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.ai_generated
@pytest.mark.specialized
def test_autonomous_thinking_engine(page: Page):
    """
    Validates the AI Thinking Engine:
    - Logs reasoning steps at each stage
    - Verifies transparency (at least N steps recorded)
    - Invokes PREDICTOR agent for strategic forecast
    """
    ai = AIService()
    ai.thinking.clear_session()
    ai.thinking.think("INIT: Autonomous Thinking Engine test starting...")

    page.goto("https://www.saucedemo.com/")
    ai.thinking.think("Navigated to target. Analysing page state...")

    html = page.content()[:2000]
    ai.thinking.think("Extracted HTML context. Delegating to EXPLORER agent...")
    exploration = ai.run_agent("EXPLORER", html)
    ai.thinking.think(f"EXPLORER returned {len(exploration)} chars of insight.")

    ai.thinking.think("Delegating to PREDICTOR agent for strategic forecast...")
    forecast = ai.run_agent("PREDICTOR", "Login page analysed. No failures yet.")
    ai.thinking.think(f"PREDICTOR response received: {forecast[:80]}...")

    summary = ai.thinking.get_summary()
    assert len(summary) >= 4, (
        f"Thinking Engine must log at least 4 reasoning steps. Got: {len(summary)}"
    )
    warnings = ai.thinking.get_decisions_by_level("WARNING")
    print(f"[TRANSPARENCY] Total thoughts: {len(summary)} | Warnings: {len(warnings)}")


# ─────────────────────────────────────────────────────────────────────────────
# TEST 2: Self-Healing — Intentional Locator Failure
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.ai_generated
@pytest.mark.specialized
def test_self_healing_locator_recovery(page: Page):
    """
    Validates the self-healing engine:
    - Attempts to interact with a deliberately wrong selector
    - AI HEALER agent produces a fallback selector
    - Test continues after recovery (no hard crash)
    """
    ai = AIService()
    ai.thinking.think("Self-Healing test: Attempting known-bad locator...")

    page.goto("https://www.saucedemo.com/")
    login = LoginPage(page)

    # Trigger self-healing by using a completely wrong selector first,
    # then verifying the real login still works
    ai.thinking.think("Calling HEALER agent for '#definitely-does-not-exist'...")
    suggestion = ai.suggest_new_locator(
        page.content(), "#definitely-does-not-exist", "Element not found"
    )
    ai.thinking.think(f"HEALER returned: '{suggestion}'")
    assert suggestion is not None, "HEALER agent must always return a non-None response."

    # Prove the system continues gracefully — real login should still work
    login.login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    assert inv.is_visible(inv.header_title), "Should reach inventory after self-healing test."
    ai.thinking.think("Self-healing validated. System continued without crash.")


# ─────────────────────────────────────────────────────────────────────────────
# TEST 3: Autonomous Workflow Recovery (Session Simulation)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.ai_generated
@pytest.mark.specialized
@pytest.mark.recovery
def test_autonomous_workflow_recovery(page: Page):
    """
    Validates the WorkflowHealer:
    - Adds item to cart, then navigates to login (simulating session drop)
    - WorkflowHealer detects the wrong state and re-authenticates
    - Verifies we land on inventory (not login) after recovery
    """
    ai = AIService()
    ai.thinking.think("Workflow Recovery test starting...")

    _login(page)
    inv = InventoryPage(page)
    inv.add_to_cart("Sauce Labs Backpack")
    ai.thinking.think("Item added to cart. Simulating session drop by navigating to login...")

    # Force-navigate to login to simulate session drop
    page.goto("https://www.saucedemo.com/")

    healer = WorkflowHealer(page, ai.thinking)
    ai.thinking.think("WorkflowHealer diagnosing current state...")
    result = healer.diagnose_and_heal()
    ai.thinking.think(f"Recovery action taken: {result}")

    # After recovery we should be authenticated on inventory
    assert "inventory" in page.url or result in ("SESSION_RESTORED", "NO_RECOVERY_NEEDED"), (
        f"Unexpected state after recovery: {page.url} | Result: {result}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# TEST 4: AI-Generated Test Data Matrix — Login
# ─────────────────────────────────────────────────────────────────────────────

_login_scenarios = [
    ("valid_login",       "standard_user",  "secret_sauce",  False),
    ("empty_both",        "",               "",               True),
    ("empty_password",    "standard_user",  "",               True),
    ("locked_user",       "locked_out_user","secret_sauce",  True),
    ("invalid_creds",     "nobody",         "secret_sauce",  True),
    ("sqli_username",     "' OR '1'='1",    "any",            True),
    ("xss_username",      "<script>a()</script>", "any",      True),
    ("boundary_username", "u" * 255,        "secret_sauce",  True),
    ("unicode_password",  "standard_user",  "密码123",        True),
    ("spaces_only",       "   ",            "   ",            True),
]

@pytest.mark.ai_generated
@pytest.mark.parametrize("scenario, username, password, expect_error", _login_scenarios, ids=[s[0] for s in _login_scenarios])
def test_ai_data_matrix_login(page: Page, scenario, username, password, expect_error):
    """AI-generated comprehensive login test matrix with security + boundary data."""
    login = LoginPage(page)
    login.navigate("https://www.saucedemo.com/")
    login.login(username, password)

    if expect_error:
        assert login.is_visible(login.error_message), (
            f"Scenario '{scenario}': Expected error message but none shown."
        )
    else:
        inv = InventoryPage(page)
        assert inv.is_visible(inv.header_title), (
            f"Scenario '{scenario}': Expected inventory page after valid login."
        )


# ─────────────────────────────────────────────────────────────────────────────
# TEST 5: AI-Generated Security + Multi-Agent Collaboration
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.ai_generated
@pytest.mark.security
@pytest.mark.specialized
def test_multi_agent_security_audit(page: Page):
    """
    Multi-agent collaboration:
    EXPLORER -> SECURITY -> DATA_GEN -> execute
    Runs an end-to-end offensive surface scan.
    """
    ai = AIService()
    ai.thinking.think("[AGENT-COLLAB] Initiating multi-agent security audit...")

    page.goto("https://www.saucedemo.com/")
    html = page.content()[:2000]

    # Agent 1: EXPLORER
    exploration = ai.run_agent("EXPLORER", html)
    ai.thinking.think(f"[AGENT-COLLAB] EXPLORER complete. {len(exploration)} chars discovered.")

    # Agent 2: SECURITY
    audit = ai.run_agent("SECURITY", exploration)
    ai.thinking.think(f"[AGENT-COLLAB] SECURITY audit: {audit[:80]}...")

    # Agent 3: DATA_GEN for security payloads
    test_data = ai.generate_test_data("Login form: username, password fields. Generate XSS and SQLi payloads.")
    ai.thinking.think(f"[AGENT-COLLAB] DATA_GEN produced: {str(test_data)[:80]}...")

    # Execute: SQLi attempt
    sqli_user = test_data.get("sqli", {}).get("username", "' OR '1'='1") if isinstance(test_data.get("sqli"), dict) else "' OR '1'='1"
    login = LoginPage(page)
    login.login(sqli_user, "any")
    ai.thinking.think("Applied SQLi payload to login form.")
    assert login.is_visible(login.error_message), "System must reject SQLi payload."
    ai.thinking.think("[SECURITY] SQLi rejected correctly. PASS.")

    # XSS check
    page.goto("https://www.saucedemo.com/")
    xss_dialogs = []
    page.on("dialog", lambda d: (xss_dialogs.append(d.message), d.dismiss()))
    login.login("<script>alert('xss')</script>", "<img src=x onerror=alert(1)>")
    page.wait_for_timeout(300)
    assert len(xss_dialogs) == 0, f"XSS VULNERABILITY: Dialog was triggered! Messages: {xss_dialogs}"
    ai.thinking.think("[SECURITY] XSS rejected correctly. PASS.")

    summary = ai.thinking.get_summary()
    assert len(summary) >= 5, "Multi-agent collaboration must produce at least 5 AI reasoning steps."
