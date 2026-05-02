import os
import requests
import json

class AIService:
    def __init__(self, model="tinyllama", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_key = os.getenv("AI_API_KEY") # Optional fallback

    def analyze_failure(self, screenshot_path, logs, error_message):
        """
        Analyze a test failure using local AI (Ollama).
        """
        prompt = f"""
        Analyze this Playwright test failure:
        Error: {error_message}
        Logs: {logs[-500:]} # Last 500 chars
        
        Provide:
        - Root Cause:
        - Suggested Fix:
        """
        
        # Try local Ollama first (No API key needed)
        try:
            response = requests.post(f"{self.base_url}/api/generate", 
                                     json={"model": self.model, "prompt": prompt, "stream": False},
                                     timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "AI analysis completed.")
        except Exception:
            pass

        # Fallback to intelligent rule-based analysis if AI is offline
        return self._heuristic_analysis(error_message, logs)

    def _heuristic_analysis(self, error, logs):
        """Rule-based engine that acts as a lightweight AI for CI environments."""
        analysis = "### 🔍 Failure Investigation\n"
        error_lower = error.lower()
        logs_lower = str(logs).lower()

        # 1. Accessibility Checks
        if "accessibility" in logs_lower or "violations" in error_lower:
            analysis += "**Root Cause:** Accessibility (A11y) Compliance Violation.\n"
            analysis += "**POC Explanation:** The page contains elements that do not meet WCAG standards (e.g., missing ARIA labels, low contrast, or missing alt text).\n"
            analysis += "**Recommendation:** Review the accessibility report and ensure all interactive elements have descriptive labels."
        
        # 2. Performance Checks
        elif "too slow" in error_lower or "duration" in error_lower or "benchmark" in logs_lower:
            analysis += "**Root Cause:** Performance Regression / Latency Issues.\n"
            analysis += "**POC Explanation:** The action took longer than the defined threshold. This could be due to heavy assets, unoptimized database queries, or server load.\n"
            analysis += "**Recommendation:** Optimize page assets or investigate backend response times."

        # 3. API Failures
        elif "status_code" in error_lower or "requests.exceptions" in error_lower:
            analysis += "**Root Cause:** Backend API Integration Error.\n"
            analysis += "**POC Explanation:** The service received an unexpected response from the API (e.g., 401 Unauthorized or 500 Server Error).\n"
            analysis += "**Recommendation:** Verify API endpoint availability and authentication tokens."

        # 4. Standard UI Timeouts
        elif "timeout" in error_lower:
            analysis += "**Root Cause:** Element Synchronization Timeout.\n"
            analysis += "**POC Explanation:** The system waited for an element that never appeared. The screenshot shows the current page state, which might be an intermediate loading state or a wrong page.\n"
            analysis += "**Recommendation:** Check if the element selector has changed or increase the wait timeout."
        
        # 5. Auth/Validation
        elif "not match" in error_lower or "epic sadface" in error_lower:
            analysis += "**Root Cause:** Authentication or Input Validation Failure.\n"
            analysis += "**POC Explanation:** The credentials or form data provided were rejected by the application logic.\n"
            analysis += "**Recommendation:** If this is a positive test, verify the test credentials; if negative, the system is behaving as expected."
        
        # 6. Assertion Logic
        elif "assertionerror" in error_lower:
            analysis += "**Root Cause:** Functional Logic Mismatch (Assertion Failed).\n"
            analysis += "**POC Explanation:** The actual value observed in the application did not match the expected value defined in the test case.\n"
            analysis += "**Recommendation:** Compare the expected vs actual values in the logs to identify the functional discrepancy."
        
        else:
            analysis += "**Root Cause:** General System Exception / Unhandled Error.\n"
            analysis += f"**Details Snippet:** {error[:150]}...\n"
            analysis += "**Recommendation:** A manual review by the QA engineering team is required for this unique failure pattern."
        
        return analysis


    def _call_openai_compatible(self, prompt):
        # OpenAI/DeepSeek/Qwen logic
        try:
            # Simplified mock for demonstration
            return f"AI Analysis (Model: {self.model}): The failure seems related to a timeout waiting for the element. Suggest checking the network latency or increasing wait time."
        except Exception as e:
            return f"AI API Error: {str(e)}"

    def suggest_new_locator(self, html_snippet, target_element_description):
        """
        AI-assisted locator handling (Self-healing).
        """
        prompt = f"Given this HTML: {html_snippet}, find a stable CSS or ID selector for: {target_element_description}"
        # AI would return a selector
        return "#suggested-id"
