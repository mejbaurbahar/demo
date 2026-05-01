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
        if "timeout" in error.lower():
            analysis += "**Root Cause:** The system waited for an element that never appeared (Timeout).\n"
            analysis += "**POC Explanation:** The screenshot shows the page state when the timeout occurred. It likely failed because of a slow network or a change in the application UI.\n"
            analysis += "**Recommendation:** Check if the element selector has changed or increase the synchronization timeout."
        elif "not match" in error.lower() or "Epic sadface" in error:
            analysis += "**Root Cause:** Authentication or Validation Error.\n"
            analysis += "**POC Explanation:** The application correctly rejected the input as per the test scenario (Negative Testing).\n"
            analysis += "**Recommendation:** If this was a valid login attempt, verify the credentials in the test data."
        elif "AssertionError" in error:
            analysis += "**Root Cause:** Logic Mismatch (Assertion Failed).\n"
            analysis += "**POC Explanation:** The actual value on the screen did not match the expected value defined in the test script.\n"
            analysis += "**Recommendation:** Verify if the business logic has changed or if there is a functional bug."
        else:
            analysis += f"**Root Cause:** General System Exception.\n"
            analysis += f"**Details:** {error[:200]}...\n"
            analysis += "**Recommendation:** Technical debug required by the QA team."
        
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
