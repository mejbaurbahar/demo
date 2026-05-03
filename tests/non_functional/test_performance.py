"""
Advanced Performance Test Suite
Uses the PerformanceMonitor to measure and assert on all critical page loads and actions.
"""
import pytest
import time
from playwright.sync_api import Page
from utils.performance_monitor import PerformanceMonitor
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_pages import CartPage, CheckoutStepOne, CheckoutStepTwo, CheckoutComplete


@pytest.mark.performance
@pytest.mark.benchmark
def test_login_page_load_performance(page: Page):
    """Benchmarks the login page initial load time."""
    monitor = PerformanceMonitor(page)
    record  = monitor.measure_navigation("https://www.saucedemo.com/")
    print(f"\n[PERF] Login page load: {record['load_ms']}ms")
    assert record["load_ms"] < 5000, f"Login page too slow: {record['load_ms']}ms"


@pytest.mark.performance
@pytest.mark.benchmark
def test_login_action_performance(page: Page):
    """Benchmarks the login form submission response time."""
    page.goto("https://www.saucedemo.com/")
    login   = LoginPage(page)
    monitor = PerformanceMonitor(page)

    record = monitor.measure_action(
        "login_form_submit",
        lambda: login.login("standard_user", "secret_sauce")
    )
    print(f"\n[PERF] Login action: {record['duration_ms']}ms")
    assert record["duration_ms"] < 5000, f"Login action too slow: {record['duration_ms']}ms"


@pytest.mark.performance
@pytest.mark.benchmark
def test_inventory_page_load(page: Page):
    """Benchmarks inventory page load after authentication."""
    login = LoginPage(page)
    login.navigate("https://www.saucedemo.com/")
    login.login("standard_user", "secret_sauce")

    monitor = PerformanceMonitor(page)
    record  = monitor.measure_navigation("https://www.saucedemo.com/inventory.html")
    print(f"\n[PERF] Inventory page load: {record['load_ms']}ms")
    assert record["load_ms"] < 5000


@pytest.mark.performance
@pytest.mark.benchmark
def test_core_web_vitals(page: Page):
    """Captures Core Web Vitals for the login page."""
    page.goto("https://www.saucedemo.com/")
    page.wait_for_load_state("networkidle")
    monitor = PerformanceMonitor(page)
    vitals  = monitor.get_web_vitals()
    print(f"\n[PERF] Web Vitals: {vitals}")
    assert "error" not in vitals, f"Could not collect Web Vitals: {vitals}"
    assert vitals.get("loadEventEnd", 0) < 10000, "Load event must complete within 10s"


@pytest.mark.load
@pytest.mark.stress
def test_simulated_load_stress(page: Page):
    """Simulates repeated logins to detect degradation under load."""
    login   = LoginPage(page)
    monitor = PerformanceMonitor(page)
    durations = []

    for i in range(3):
        start = time.perf_counter()
        login.navigate("https://www.saucedemo.com/")
        login.login("standard_user", "secret_sauce")
        assert "inventory.html" in page.url, f"Iteration {i}: Did not reach inventory."
        elapsed = (time.perf_counter() - start) * 1000
        durations.append(elapsed)
        print(f"[LOAD] Iteration {i+1}: {elapsed:.0f}ms")
        page.goto("https://www.saucedemo.com/")

    avg = sum(durations) / len(durations)
    print(f"[LOAD] Average over {len(durations)} iterations: {avg:.0f}ms")
    assert avg < 10000, f"Average login time too slow under load: {avg:.0f}ms"


@pytest.mark.performance
@pytest.mark.chaos
def test_api_chaos_latency_injection(page: Page):
    """Injects 500ms artificial latency on all requests and verifies UI survives."""
    delay_ms = 500

    def slow_route(route):
        time.sleep(delay_ms / 1000)
        route.continue_()

    page.route("**/*", slow_route)

    login = LoginPage(page)
    start = time.perf_counter()
    login.navigate("https://www.saucedemo.com/")
    login.login("standard_user", "secret_sauce")
    duration = (time.perf_counter() - start) * 1000

    inv = InventoryPage(page)
    assert inv.is_visible(inv.header_title), "UI must survive latency injection."
    assert duration > delay_ms, "Verified that latency was injected."
    print(f"\n[CHAOS] Completed under {delay_ms}ms injected latency in {duration:.0f}ms total.")
