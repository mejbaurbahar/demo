import pytest
from playwright.sync_api import Page
import os
from datetime import datetime
from components.ai_service import AIService

# Initialize AI Service
ai_service = AIService()

@pytest.fixture(autouse=True)
def capture_logs(page: Page):
    """Fixture to capture console logs and network errors during test execution."""
    logs = {"console": [], "network_errors": []}
    
    # Listen for console logs
    page.on("console", lambda msg: logs["console"].append(f"[{msg.type}] {msg.text}"))
    
    # Listen for network errors (failed requests)
    page.on("requestfailed", lambda request: logs["network_errors"].append(
        f"URL: {request.url} | Error: {request.failure.error_text if request.failure else 'Unknown error'}"
    ))
    
    # Listen for response errors (4xx, 5xx)
    page.on("response", lambda response: logs["network_errors"].append(
        f"URL: {response.url} | Status: {response.status} {response.status_text}"
    ) if response.status >= 400 else None)

    yield logs

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        # Get logs from the fixture
        logs = item.funcargs.get("capture_logs", {"console": [], "network_errors": []})
        
        if (report.skipped and xfail) or (report.failed and not xfail):
            # 1. Capture Screenshot as POC
            page = item.funcargs.get("page")
            screenshot_html = ""
            if page:
                screenshot_dir = "reports/screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                file_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = os.path.join(screenshot_dir, file_name)
                page.screenshot(path=screenshot_path)
                screenshot_html = f'<div><p><b>POC (Proof of Concept):</b></p><img src="screenshots/{file_name}" alt="screenshot" style="width:600px; border: 2px solid red;" onclick="window.open(this.src)"/></div>'
            
            # 2. Format Console and Network Logs
            console_log_str = "\n".join(logs["console"][-20:]) # Last 20 logs
            network_log_str = "\n".join(logs["network_errors"][-20:])
            
            log_html = f"""
            <div style="background-color: #f1f1f1; padding: 10px; border: 1px solid #ccc; margin-top: 10px; font-family: monospace; font-size: 12px;">
                <h5 style="margin-top: 0;">🌐 Network & Console Audit</h5>
                <p><b>Recent Console Logs:</b></p>
                <pre>{console_log_str or "No console logs captured."}</pre>
                <p><b>Network Errors/Failures:</b></p>
                <pre style="color: #dc3545;">{network_log_str or "No network errors detected."}</pre>
            </div>
            """
            
            # 3. AI Failure Analysis (including logs)
            error_msg = str(report.longreprtext)
            combined_logs = f"Console:\n{console_log_str}\nNetwork:\n{network_log_str}"
            ai_analysis = ai_service.analyze_failure(None, combined_logs, error_msg)
            
            ai_html = f"""
            <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin-top: 10px; border: 1px solid #f5c6cb;">
                <h4 style="margin-top: 0;">🤖 AI Autonomous Insights</h4>
                <p><b>Analysis:</b> {ai_analysis}</p>
                <p><small>Analyzed by local TinyLlama model.</small></p>
            </div>
            """
            
            # 4. Add to report
            extra.append(pytest_html.extras.html(ai_html))
            extra.append(pytest_html.extras.html(log_html))
            if screenshot_html:
                extra.append(pytest_html.extras.html(screenshot_html))
                
        report.extra = extra

def pytest_html_report_title(report):
    report.title = "🚀 Autonomous AI Testing Dashboard"

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([f"<h3>Environment: Production/Staging</h3>"])
    prefix.extend([f"<p>This report contains automated E2E, API, and Security validation results with AI-powered failure categorization and Network/Console audit.</p>"])

def pytest_configure(config):
    config._metadata['Project Name'] = 'SauceDemo AI Automation'
    config._metadata['Tester'] = 'AI QA Agent'
    config._metadata['Framework'] = 'Playwright + Python + Ollama'
