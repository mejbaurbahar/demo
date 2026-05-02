import pytest
import time
from pages.login_page import LoginPage

@pytest.mark.performance
@pytest.mark.benchmark
def test_login_performance_benchmark(page):
    """
    Benchmark Testing: Measures the time taken for the login action.
    """
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com/")
    
    start_time = time.time()
    login_page.login("standard_user", "secret_sauce")
    end_time = time.time()
    
    duration = end_time - start_time
    print(f"\nLogin took {duration:.2f} seconds")
    
    # Assert performance threshold (e.g., < 2 seconds)
    assert duration < 5, f"Login was too slow: {duration:.2f}s"

@pytest.mark.load
@pytest.mark.stress
def test_simulated_load_stress(page):
    """
    Load/Stress Testing: Simulated repeated interactions.
    """
    login_page = LoginPage(page)
    for i in range(3):  # Simulating repeated load
        login_page.navigate("https://www.saucedemo.com/")
        login_page.login("standard_user", "secret_sauce")
        assert "inventory.html" in page.url
        page.goto("https://www.saucedemo.com/") # Go back to login
