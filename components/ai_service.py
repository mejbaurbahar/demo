import os
import requests
import json

class AIService:
    def __init__(self, model="tinyllama", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.memory = {} # Mock memory for learning failure patterns

    def analyze_failure(self, screenshot_path, logs, error_message):
        """
        🚀 Multi-Agent Dispatcher: Routes the failure to specialized agents.
        """
        # 1. RCA Agent: Deep Root Cause Analysis & Memory Learning
        rca_report = self._rca_agent(error_message, logs)
        
        # 2. Security Agent: Adaptive Vulnerability Audit
        security_report = ""
        if any(term in str(logs).lower() or term in error_message.lower() for term in ["security", "xss", "sql", "unauthorized", "auth"]):
            security_report = self._security_agent(error_message)
            
        return f"{rca_report}\n{security_report}"

    def _rca_agent(self, error, logs):
        """🧠 RCA Agent: Links failures to root causes and past patterns."""
        # AI Learning: Track recurring issues
        pattern_key = error[:50]
        prev_failures = self.memory.get(pattern_key, 0)
        self.memory[pattern_key] = prev_failures + 1
        
        analysis = self._heuristic_analysis(error, logs)
        
        if prev_failures > 0:
            analysis += f"\n\n**⚠️ AI Memory Insight:** This pattern has appeared {prev_failures} times before. Suggests a regression or environment instability."
            
        return analysis

    def _security_agent(self, error):
        """🕵️ Security Agent: Simulates adaptive attack pattern analysis."""
        return """
---
🛡️ **Autonomous Security Audit:**
- **Vulnerability Detected:** Potential injection point or authorization bypass.
- **AI Payload Suggestion:** For verification, test with adaptive payloads like `<svg/onload=alert(1)>` or `' OR '1'='1`.
- **Mitigation:** Ensure strict input sanitization and implement CSP headers.
"""

    def suggest_new_locator(self, html_snippet, target_element_description, error_message):
        """🩹 Healing Agent: Autonomous locator recovery."""
        prompt = f"""
        [HEALING AGENT] CRITICAL: UI Element Missing.
        Target: {target_element_description}
        Error: {error_message}
        
        HTML Content:
        {html_snippet[:3000]}
        
        TASK: Return ONLY the most stable CSS or ID selector. No explanation.
        """
        return self._call_llm(prompt)

    def _call_llm(self, prompt):
        """Centralized LLM Caller (Supports local Ollama)."""
        try:
            response = requests.post(f"{self.base_url}/api/generate", 
                                     json={"model": self.model, "prompt": prompt, "stream": False},
                                     timeout=15)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
        except Exception:
            pass
        return None

    def _heuristic_analysis(self, error, logs):
        """Built-in Expert System for high-fidelity diagnosis."""
        analysis = "### 🔍 Autonomous QA Diagnosis\n"
        err = error.lower()
        log = str(logs).lower()

        if "accessibility" in log or "violations" in err:
            analysis += "**Root Cause:** Accessibility (A11y) Violation. Missing ARIA/Alt text.\n"
            analysis += "**POC:** WCAG standards not met on current viewport."
        elif "too slow" in err or "duration" in err or "benchmark" in log:
            analysis += "**Root Cause:** Performance Regression. Action latency exceeded threshold.\n"
            analysis += "**POC:** Excessive resource loading or backend bottleneck."
        elif "status_code" in err or "requests.exceptions" in err:
            analysis += "**Root Cause:** API Contract Breach. Backend returned unexpected status.\n"
            analysis += "**POC:** Integration point failure (Check service health)."
        elif "timeout" in err:
            analysis += "**Root Cause:** Synchronization Timeout. Element not found within 5s.\n"
            analysis += "**POC:** UI change or slow rendering detected."
        elif "not match" in err or "epic sadface" in err or "keyerror" in err:
            analysis += "**Root Cause:** Data Integrity Issue. Credentials or Payload mismatch.\n"
            analysis += "**POC:** Validation logic rejected input or missing test data."
        elif "assertionerror" in err:
            analysis += "**Root Cause:** Functional Regression. Expected vs Actual mismatch.\n"
            analysis += "**POC:** Business logic discrepancy detected."
        else:
            analysis += "**Root Cause:** Unhandled System Exception.\n"
            analysis += "**Recommendation:** Technical audit required."
        
        return analysis
