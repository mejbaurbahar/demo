import pytest
from playwright.sync_api import Page
import os
from datetime import datetime

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Capture screenshot on failure
            page = item.funcargs.get("page")
            if page:
                screenshot_dir = "reports/screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                file_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = os.path.join(screenshot_dir, file_name)
                page.screenshot(path=screenshot_path)
                
                if screenshot_path:
                    # Use a relative path for the HTML report
                    html = '<div><img src="screenshots/%s" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % file_name
                    extra.append(pytest_html.extras.html(html))
        report.extra = extra
