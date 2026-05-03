"""
Performance Monitor
Tracks page load time, API response times, and detects performance regressions.
"""
import time
import json
import os
from datetime import datetime
from playwright.sync_api import Page


class PerformanceMonitor:
    """Lightweight performance observer that wraps Playwright navigation calls."""

    THRESHOLDS = {
        "page_load_ms":     3000,
        "api_response_ms":  2000,
        "lcp_ms":           2500,   # Largest Contentful Paint
        "fcp_ms":           1800,   # First Contentful Paint
    }

    def __init__(self, page: Page, log_path: str = "reports/performance_log.json"):
        self.page = page
        self.log_path = log_path
        self.records: list = []
        os.makedirs("reports", exist_ok=True)

    def measure_navigation(self, url: str) -> dict:
        """Navigate to URL and capture timing metrics."""
        start = time.perf_counter()
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        elapsed_ms = (time.perf_counter() - start) * 1000

        record = {
            "timestamp":    str(datetime.now()),
            "url":          url,
            "load_ms":      round(elapsed_ms, 2),
            "threshold_ms": self.THRESHOLDS["page_load_ms"],
            "passed":       elapsed_ms < self.THRESHOLDS["page_load_ms"]
        }
        self.records.append(record)
        self._persist(record)

        status = "PASS" if record["passed"] else "WARN"
        print(f"[PERF] [{status}] {url} loaded in {elapsed_ms:.0f}ms "
              f"(threshold: {self.THRESHOLDS['page_load_ms']}ms)")
        return record

    def measure_action(self, label: str, action_fn) -> dict:
        """Measure the duration of any callable action."""
        start = time.perf_counter()
        action_fn()
        elapsed_ms = (time.perf_counter() - start) * 1000

        record = {
            "timestamp":    str(datetime.now()),
            "action":       label,
            "duration_ms":  round(elapsed_ms, 2),
            "threshold_ms": self.THRESHOLDS["api_response_ms"],
            "passed":       elapsed_ms < self.THRESHOLDS["api_response_ms"]
        }
        self.records.append(record)
        self._persist(record)

        status = "PASS" if record["passed"] else "WARN"
        print(f"[PERF] [{status}] '{label}' took {elapsed_ms:.0f}ms")
        return record

    def get_web_vitals(self) -> dict:
        """Captures Core Web Vitals via PerformanceObserver API."""
        try:
            vitals = self.page.evaluate("""() => {
                const nav = performance.getEntriesByType('navigation')[0];
                const paint = performance.getEntriesByType('paint');
                const fcp = paint.find(p => p.name === 'first-contentful-paint');
                return {
                    domInteractive:  Math.round(nav ? nav.domInteractive : 0),
                    domComplete:     Math.round(nav ? nav.domComplete : 0),
                    loadEventEnd:    Math.round(nav ? nav.loadEventEnd : 0),
                    fcp_ms:          Math.round(fcp ? fcp.startTime : 0),
                };
            }""")
            vitals["timestamp"] = str(datetime.now())
            self.records.append(vitals)
            self._persist(vitals)
            return vitals
        except Exception as e:
            return {"error": str(e)}

    def assert_no_regressions(self):
        """Raises AssertionError if any recorded metric exceeded its threshold."""
        failures = [r for r in self.records if not r.get("passed", True)]
        if failures:
            details = "\n".join(
                [f"  - {r.get('url', r.get('action', 'unknown'))}: {r.get('load_ms', r.get('duration_ms', '?'))}ms" 
                 for r in failures]
            )
            raise AssertionError(f"Performance regressions detected:\n{details}")

    def _persist(self, record: dict):
        try:
            existing = []
            if os.path.exists(self.log_path):
                with open(self.log_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            existing.append(record)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def summary(self) -> str:
        total   = len(self.records)
        passed  = sum(1 for r in self.records if r.get("passed", True))
        failed  = total - passed
        avg_ms  = (sum(r.get("load_ms", r.get("duration_ms", 0)) 
                      for r in self.records) / total) if total else 0
        return (f"Performance Summary: {total} measurements | "
                f"PASS: {passed} | FAIL: {failed} | Avg: {avg_ms:.0f}ms")
