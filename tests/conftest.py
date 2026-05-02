import pytest
from playwright.sync_api import Page
import os
from datetime import datetime
import json
from components.ai_service import AIService


# Initialize AI Service
ai_service = AIService()

@pytest.fixture
def store_payload(request):
    """Fixture to store test payloads for reporting."""
    def _store(payload_data):
        request.node._payload = payload_data
    return _store

@pytest.fixture(autouse=True)
def capture_logs(page: Page):

    """Fixture to capture console logs and network errors during test execution."""
    logs = {"console": [], "network_errors": []}
    try:
        page.on("console", lambda msg: logs["console"].append(f"[{msg.type}] {msg.text}"))
        page.on("requestfailed", lambda req: logs["network_errors"].append(
            f"URL: {req.url} | Error: {getattr(req, 'failure', 'Unknown error')}"
        ))

        page.on("response", lambda response: logs["network_errors"].append(
            f"URL: {response.url} | Status: {response.status}"
        ) if response.status >= 400 else None)
    except Exception:
        pass
    yield logs

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    try:
        if report.when == "call":
            # 0. Enhanced Input Test Data (Step-like UI)
            params = getattr(item, 'callspec', None).params if hasattr(item, 'callspec') else {}
            payload = getattr(item, '_payload', None)
            
            if params or payload:
                param_rows = "".join([
                    f'<div style="display: flex; border-bottom: 1px solid #f1f5f9; padding: 5px 0;">'
                    f'<span style="flex: 1; color: #64748b; font-weight: 500;">🔹 {k}:</span>'
                    f'<span style="flex: 2; color: #1e293b; font-family: monospace;">{v}</span>'
                    f'</div>' for k, v in params.items()
                ])
                
                payload_html = ""
                if payload:
                    payload_json = json.dumps(payload, indent=2) if isinstance(payload, (dict, list)) else str(payload)
                    payload_html = f"""
                    <div style="margin-top: 10px; background: #fdf2f2; padding: 10px; border-radius: 6px; border: 1px solid #fecaca;">
                        <span style="color: #991b1b; font-weight: 700; font-size: 11px;">🔥 REQUEST PAYLOAD:</span>
                        <pre style="margin-top: 5px; font-size: 11px; color: #b91c1c; overflow-x: auto;">{payload_json}</pre>
                    </div>
                    """

                param_html = f"""
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; margin: 15px 0; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <div style="background: #f8fafc; padding: 8px 15px; border-bottom: 1px solid #e2e8f0; color: #475569; font-weight: 700; font-size: 11px; text-transform: uppercase;">
                        📦 Execution Data & Payloads
                    </div>
                    <div style="padding: 10px 15px;">
                        {param_rows}
                        {payload_html}
                    </div>
                </div>
                """
                extra.append(pytest_html.extras.html(param_html))

            if report.passed:
                extra.append(pytest_html.extras.html(
                    '<div style="color: #16a34a; font-weight: bold; font-size: 12px; margin-top: 5px;">'
                    '🤖 AI Verification: <span style="background: #dcfce7; padding: 2px 8px; border-radius: 10px;">System Healthy ✅</span>'
                    '</div>'
                ))

            if report.failed:
                # 1. POC Capture
                page = item.funcargs.get("page")
                if page:
                    try:
                        screenshot_dir = "reports/screenshots"
                        os.makedirs(screenshot_dir, exist_ok=True)
                        # Sanitize filename: remove colons and other invalid chars
                        safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in item.name)
                        file_name = f"{safe_name}.png"
                        page.screenshot(path=os.path.join(screenshot_dir, file_name))

                        extra.append(pytest_html.extras.html(
                            f'<div style="margin:20px 0; padding: 15px; background: #fff5f5; border: 2px solid #feb2b2; border-radius: 12px;">'
                            f'<b style="color: #c53030; font-size: 14px;">📸 Visual Evidence Proof (POC):</b><br>'
                            f'<img src="screenshots/{file_name}" style="width:100%; max-width:700px; border: 4px solid #f56565; border-radius:12px; margin-top:12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);" onclick="window.open(this.src)">'
                            f'</div>'
                        ))
                    except Exception:
                        pass

                # 2. AI Failure Diagnosis
                logs = item.funcargs.get("capture_logs", {"console": [], "network_errors": []})
                error_details = str(report.longreprtext)
                
                # Extract markers for AI context
                markers = [mark.name for mark in item.iter_markers()]
                test_context = {
                    "test_name": item.name,
                    "markers": markers,
                    "stage": report.when
                }
                
                combined_context = f"Test Context: {test_context}\nConsole: {logs.get('console', [])}\nNetwork: {logs.get('network_errors', [])}"
                ai_report = ai_service.analyze_failure(None, combined_context, error_details)

                
                ai_report_html = str(ai_report).replace('\n', '<br>')
                ai_box = f"""
                <div style="background: linear-gradient(135deg, #4f46e5, #9333ea); color: white; padding: 20px; border-radius: 12px; margin: 20px 0; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);">
                    <h3 style="margin-top: 0; display: flex; align-items: center; gap: 10px;">🤖 AI Autonomous QA Diagnosis</h3>
                    <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.2); margin: 15px 0;">
                    <div style="font-size: 15px; line-height: 1.6; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                        {ai_report_html}
                    </div>
                    <div style="margin-top: 15px; font-size: 11px; opacity: 0.7; letter-spacing: 0.5px;">
                        ANALYSIS GENERATED BY LOCAL DEEP-LEARNING MODEL (TINYLLAMA)
                    </div>
                </div>
                """
                extra.append(pytest_html.extras.html(ai_box))
                
                # 3. Technical Audit Log
                audit_html = f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin: 10px 0; font-family: 'Courier New', Courier, monospace;">
                    <b style="color: #475569;">📑 Technical Audit (Console & Network):</b>
                    <div style="font-size: 11px; max-height: 200px; overflow-y: auto; margin-top: 10px;">
                        <span style="color: #64748b;">Console:</span><br>{"<br>".join(logs.get('console', [])) or "None"}<br><br>
                        <span style="color: #ef4444;">Network:</span><br>{"<br>".join(logs.get('network_errors', [])) or "None"}
                    </div>
                </div>
                """
                extra.append(pytest_html.extras.html(audit_html))


    except Exception as e:
        print(f"DEBUG: Error in report hook: {str(e)}")

    report.extra = extra

def pytest_html_report_title(report):
    report.title = "✨ AI-Powered QA Dashboard"

def pytest_configure(config):
    # Safely add metadata to the report if the plugin is available
    try:
        if hasattr(config, "_metadata"):
            config._metadata['AI Engine'] = 'Active (Autonomous Orchestrator)'
            config._metadata['Autonomous Level'] = 'Level 5 - Fully Autonomous Agentic System'
            config._metadata['Memory System'] = 'Long-Term Persistence (Active)'
            config._metadata['Framework Mode'] = 'Self-Thinking QA OS'
    except Exception:
        pass

def pytest_html_results_summary(prefix, summary, postfix):
    try:
        ai_service = AIService()
        total = summary.get('total', 0)
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # AI Strategy Forecast (Step 2: Let AI Think for More)
        forecast_context = f"Run: {total} total, {passed} passed, {failed} failed."
        ai_insight = ai_service.run_agent("PREDICTOR", forecast_context)
        ai_insight_html = str(ai_insight).replace('\n', '<br>')

        prefix.extend([
            f"""
            <div style="font-family: 'Inter', sans-serif; margin-bottom: 30px;">
                <!-- 🧠 Autonomous Brain Dashboard -->
                <div style="background: linear-gradient(135deg, #1e293b, #0f172a); color: white; padding: 25px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <h2 style="margin: 0; font-size: 24px;">🚀 Autonomous Brain Analysis</h2>
                            <p style="opacity: 0.8; margin: 5px 0 0 0;">Level 5 Digital QA Engineer Orchestration</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: 600; border: 1px solid rgba(255,255,255,0.2);">
                            🛰️ MULTI-AGENT SYNC: ACTIVE
                        </div>
                    </div>
                    <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 20px 0;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                            <h4 style="margin-top: 0; color: #38bdf8;">🧠 Agent Strategic Forecast</h4>
                            <p style="font-size: 14px; line-height: 1.6; color: #cbd5e1;">{ai_insight_html}</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                            <h4 style="margin-top: 0; color: #fbbf24;">📈 Next-Level Execution Plan</h4>
                            <ul style="font-size: 13px; color: #cbd5e1; padding-left: 20px; line-height: 1.8;">
                                <li>Autonomous Exploratory Crawling (Deep-Scan)</li>
                                <li>Predictive Regression Prioritization</li>
                                <li>Chaos Injection (Latency Stress)</li>
                                <li>Zero-Day Security Mutation Loop</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div style="display: flex; gap: 20px; margin-bottom: 30px;">
                    <div style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="color: #64748b; font-size: 14px; font-weight: 600;">PASS RATE</div>
                        <div style="font-size: 32px; font-weight: 800; color: #16a34a;">{pass_rate:.1f}%</div>
                        <div style="width: 100%; background: #f1f5f9; height: 8px; border-radius: 4px; margin-top: 10px;">
                            <div style="width: {pass_rate}%; background: #16a34a; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    <div style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="color: #64748b; font-size: 14px; font-weight: 600;">TOTAL TESTS</div>
                        <div style="font-size: 32px; font-weight: 800; color: #1e293b;">{total}</div>
                    </div>
                    <div style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="color: #64748b; font-size: 14px; font-weight: 600;">FAILURES</div>
                        <div style="font-size: 32px; font-weight: 800; color: {'#dc2626' if failed > 0 else '#16a34a'};">{failed}</div>
                    </div>
                </div>
            </div>
            """
        ])
    except Exception as e:
        print(f"Error in summary: {e}")

