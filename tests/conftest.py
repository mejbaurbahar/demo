"""
Master conftest.py — Autonomous AI QA Framework
Provides:
  - store_payload fixture (for API test data visibility)
  - capture_logs fixture (console + network error tracking)
  - pytest_runtest_makereport hook (screenshot POC + AI diagnosis on failure)
  - pytest_html_report_title
  - pytest_configure (report metadata)
  - pytest_sessionfinish (auto-generate AI Transparency Report)
  - pytest_html_results_summary (AI brain dashboard in report header)
"""
import pytest
from playwright.sync_api import Page
import os
import json
from datetime import datetime
from components.ai_service import AIService


# ── Module-level AI service (single instance for the full session) ────────────
ai_service = AIService()


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def store_payload(request):
    """Allows a test to attach a request payload to the HTML report."""
    def _store(payload_data):
        request.node._payload = payload_data
    return _store


@pytest.fixture(autouse=True)
def capture_logs(page: Page):
    """Auto-fixture: captures browser console messages and network failures."""
    logs = {"console": [], "network_errors": []}
    try:
        page.on("console", lambda msg: logs["console"].append(f"[{msg.type}] {msg.text}"))
        page.on("requestfailed", lambda req: logs["network_errors"].append(
            f"URL: {req.url} | Failure: {req.failure}"
        ))
        page.on("response", lambda resp: logs["network_errors"].append(
            f"HTTP {resp.status} — {resp.url}"
        ) if resp.status >= 400 else None)
    except Exception:
        pass
    yield logs


# ── Report Hooks ──────────────────────────────────────────────────────────────

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome     = yield
    report      = outcome.get_result()
    extra       = getattr(report, "extra", [])

    try:
        if report.when == "call":

            # ── 1. Execution Data / Payload Panel ──────────────────────────
            params  = getattr(item, "callspec", None)
            params  = params.params if params else {}
            payload = getattr(item, "_payload", None)

            if params or payload:
                param_rows = "".join([
                    f'<div style="display:flex;border-bottom:1px solid #f1f5f9;padding:5px 0;">'
                    f'<span style="flex:1;color:#64748b;font-weight:500;">{k}:</span>'
                    f'<span style="flex:2;color:#1e293b;font-family:monospace;">{v}</span>'
                    f'</div>' for k, v in params.items()
                ])
                payload_html = ""
                if payload:
                    payload_json = json.dumps(payload, indent=2) if isinstance(payload, (dict, list)) else str(payload)
                    payload_html = (
                        '<div style="margin-top:10px;background:#fdf2f2;padding:10px;'
                        'border-radius:6px;border:1px solid #fecaca;">'
                        '<span style="color:#991b1b;font-weight:700;font-size:11px;">REQUEST PAYLOAD:</span>'
                        f'<pre style="margin-top:5px;font-size:11px;color:#b91c1c;overflow-x:auto;">{payload_json}</pre>'
                        '</div>'
                    )
                extra.append(pytest_html.extras.html(
                    '<div style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;'
                    'margin:15px 0;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.05);">'
                    '<div style="background:#f8fafc;padding:8px 15px;border-bottom:1px solid #e2e8f0;'
                    'color:#475569;font-weight:700;font-size:11px;text-transform:uppercase;">'
                    'Execution Data &amp; Payloads</div>'
                    f'<div style="padding:10px 15px;">{param_rows}{payload_html}</div></div>'
                ))

            # ── 2. Pass badge ─────────────────────────────────────────────
            if report.passed:
                extra.append(pytest_html.extras.html(
                    '<div style="color:#16a34a;font-weight:bold;font-size:12px;margin-top:5px;">'
                    'AI Verification: <span style="background:#dcfce7;padding:2px 8px;'
                    'border-radius:10px;">System Healthy — PASS</span></div>'
                ))

            # ── 3. Failure: Screenshot + AI Diagnosis ─────────────────────
            if report.failed:
                page_obj = item.funcargs.get("page")
                if page_obj:
                    try:
                        screenshot_dir = "reports/screenshots"
                        os.makedirs(screenshot_dir, exist_ok=True)
                        safe_name = "".join(
                            c if c.isalnum() or c in ("_", "-") else "_" for c in item.name
                        )
                        file_name = f"{safe_name}.png"
                        page_obj.screenshot(path=os.path.join(screenshot_dir, file_name))
                        extra.append(pytest_html.extras.html(
                            f'<div style="margin:20px 0;padding:15px;background:#fff5f5;'
                            f'border:2px solid #feb2b2;border-radius:12px;">'
                            f'<b style="color:#c53030;font-size:14px;">Visual Evidence (POC Screenshot):</b><br>'
                            f'<img src="screenshots/{file_name}" style="width:100%;max-width:700px;'
                            f'border:4px solid #f56565;border-radius:12px;margin-top:12px;'
                            f'box-shadow:0 10px 15px -3px rgba(0,0,0,.1);" onclick="window.open(this.src)">'
                            f'</div>'
                        ))
                    except Exception:
                        pass

                # AI Root Cause Analysis
                logs         = item.funcargs.get("capture_logs", {"console": [], "network_errors": []})
                error_details = str(report.longreprtext)
                markers       = [m.name for m in item.iter_markers()]
                context       = (
                    f"Test: {item.name} | Markers: {markers} | Stage: {report.when} | "
                    f"Console: {logs.get('console', [])[:5]} | "
                    f"Network: {logs.get('network_errors', [])[:5]}"
                )
                ai_report     = ai_service.analyze_failure(None, context, error_details)
                ai_html       = str(ai_report).replace("\n", "<br>")

                extra.append(pytest_html.extras.html(
                    '<div style="background:linear-gradient(135deg,#4f46e5,#9333ea);color:#fff;'
                    'padding:20px;border-radius:12px;margin:20px 0;box-shadow:0 10px 25px -5px rgba(0,0,0,.2);">'
                    '<h3 style="margin-top:0;">AI Autonomous QA Diagnosis</h3>'
                    '<hr style="border:0;border-top:1px solid rgba(255,255,255,.2);margin:15px 0;">'
                    f'<div style="font-size:14px;line-height:1.6;background:rgba(255,255,255,.1);'
                    f'padding:15px;border-radius:8px;">{ai_html}</div>'
                    '<div style="margin-top:15px;font-size:11px;opacity:.7;letter-spacing:.5px;">'
                    'ANALYSIS BY AUTONOMOUS AI QA ENGINE</div></div>'
                ))

                # Technical Audit Log
                console_html = "<br>".join(logs.get("console", [])[:20]) or "None"
                network_html = "<br>".join(logs.get("network_errors", [])[:20]) or "None"
                extra.append(pytest_html.extras.html(
                    '<div style="background:#f8fafc;border:1px solid #e2e8f0;padding:15px;'
                    'border-radius:8px;margin:10px 0;font-family:monospace;">'
                    '<b style="color:#475569;">Technical Audit (Console &amp; Network):</b>'
                    '<div style="font-size:11px;max-height:200px;overflow-y:auto;margin-top:10px;">'
                    f'<span style="color:#64748b;">Console:</span><br>{console_html}<br><br>'
                    f'<span style="color:#ef4444;">Network Errors:</span><br>{network_html}</div></div>'
                ))

    except Exception as e:
        print(f"DEBUG conftest hook error: {e}")

    report.extra = extra


# ── Report Configuration ──────────────────────────────────────────────────────

def pytest_html_report_title(report):
    report.title = "AI-Powered Autonomous QA Dashboard"


def pytest_configure(config):
    try:
        if hasattr(config, "_metadata"):
            config._metadata["AI Engine"]        = "Active (Multi-Agent Orchestrator)"
            config._metadata["Autonomous Level"] = "Level 5 — Fully Autonomous QA OS"
            config._metadata["Memory System"]    = "Long-Term JSON Persistence"
            config._metadata["Self-Healing"]     = "Enabled (DOM Relationship Analysis)"
            config._metadata["Framework Mode"]   = "Self-Thinking QA Operating System"
    except Exception:
        pass


def pytest_html_results_summary(prefix, summary, postfix):
    """Injects the AI Brain Dashboard into the HTML report header."""
    try:
        # summary is a list of strings in pytest-html; parse totals from it
        total  = 0
        passed = 0
        failed = 0
        for item in summary:
            s = str(item).lower()
            # e.g. "12 passed, 3 failed, 1 error"
            import re
            m_pass = re.search(r"(\d+)\s+passed", s)
            m_fail = re.search(r"(\d+)\s+failed", s)
            m_total = re.search(r"(\d+)\s+test", s)
            if m_pass:  passed  = int(m_pass.group(1))
            if m_fail:  failed  = int(m_fail.group(1))
            if m_total: total   = int(m_total.group(1))

        if total == 0:
            total = passed + failed

        pass_rate = (passed / total * 100) if total > 0 else 0

        # Strategy forecast from AI
        forecast_context = f"Run completed: {total} tests total, {passed} passed, {failed} failed."
        ai_insight = ai_service.run_agent("PREDICTOR", forecast_context)
        ai_insight_html = str(ai_insight).replace("\n", "<br>")

        # Load healed element count from memory
        healed_count = len(ai_service.get_memory().get("healed_elements", {}))

        prefix.extend([f"""
        <div style="font-family:'Inter',sans-serif;margin-bottom:30px;">
            <!-- AI Brain Dashboard -->
            <div style="background:linear-gradient(135deg,#1e293b,#0f172a);color:#fff;
                        padding:25px;border-radius:16px;margin-bottom:30px;
                        box-shadow:0 20px 25px -5px rgba(0,0,0,.3);">
                <div style="display:flex;align-items:center;justify-content:space-between;">
                    <div>
                        <h2 style="margin:0;font-size:24px;">Autonomous AI Brain Analysis</h2>
                        <p style="opacity:.8;margin:5px 0 0 0;">
                            Level 5 Digital QA Engineer Orchestration
                        </p>
                    </div>
                    <div style="background:rgba(255,255,255,.1);padding:8px 16px;border-radius:20px;
                                font-size:13px;font-weight:600;border:1px solid rgba(255,255,255,.2);">
                        MULTI-AGENT SYNC: ACTIVE
                    </div>
                </div>
                <hr style="border:0;border-top:1px solid rgba(255,255,255,.1);margin:20px 0;">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
                    <div style="background:rgba(255,255,255,.05);padding:20px;border-radius:12px;
                                border:1px solid rgba(255,255,255,.1);">
                        <h4 style="margin-top:0;color:#38bdf8;">Agent Strategic Forecast</h4>
                        <p style="font-size:14px;line-height:1.6;color:#cbd5e1;">{ai_insight_html}</p>
                    </div>
                    <div style="background:rgba(255,255,255,.05);padding:20px;border-radius:12px;
                                border:1px solid rgba(255,255,255,.1);">
                        <h4 style="margin-top:0;color:#fbbf24;">Next Execution Plan</h4>
                        <ul style="font-size:13px;color:#cbd5e1;padding-left:20px;line-height:1.8;">
                            <li>Autonomous Exploratory Crawl (Deep-Scan)</li>
                            <li>Predictive Regression Prioritisation</li>
                            <li>Chaos Injection (Latency + State Corruption)</li>
                            <li>Zero-Day Security Mutation Loop</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Metrics Row -->
            <div style="display:flex;gap:20px;margin-bottom:30px;">
                <div style="flex:1;background:#fff;border:1px solid #e2e8f0;padding:20px;
                            border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.1);">
                    <div style="color:#64748b;font-size:14px;font-weight:600;">PASS RATE</div>
                    <div style="font-size:32px;font-weight:800;color:#16a34a;">{pass_rate:.1f}%</div>
                    <div style="width:100%;background:#f1f5f9;height:8px;border-radius:4px;margin-top:10px;">
                        <div style="width:{pass_rate}%;background:#16a34a;height:100%;border-radius:4px;"></div>
                    </div>
                </div>
                <div style="flex:1;background:#fff;border:1px solid #e2e8f0;padding:20px;
                            border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.1);">
                    <div style="color:#64748b;font-size:14px;font-weight:600;">TOTAL TESTS</div>
                    <div style="font-size:32px;font-weight:800;color:#1e293b;">{total}</div>
                </div>
                <div style="flex:1;background:#fff;border:1px solid #e2e8f0;padding:20px;
                            border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.1);">
                    <div style="color:#64748b;font-size:14px;font-weight:600;">FAILURES</div>
                    <div style="font-size:32px;font-weight:800;
                                color:{'#dc2626' if failed > 0 else '#16a34a'};">{failed}</div>
                </div>
                <div style="flex:1;background:#fff;border:1px solid #e2e8f0;padding:20px;
                            border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.1);">
                    <div style="color:#64748b;font-size:14px;font-weight:600;">SELF-HEALS</div>
                    <div style="font-size:32px;font-weight:800;color:#7c3aed;">{healed_count}</div>
                </div>
            </div>
        </div>
        """])
    except Exception as e:
        print(f"conftest summary error: {e}")


def pytest_sessionfinish(session, exitstatus):
    """Auto-generate the AI Transparency Report after each session."""
    try:
        from utils.generate_ai_report import generate_enterprise_report
        generate_enterprise_report()
    except Exception as e:
        print(f"[REPORT] Could not generate AI Transparency Report: {e}")
