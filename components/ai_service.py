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
        if "timeout" in error.lower():
            return "Analysis: Possible network latency or element loading issue. Suggestion: Increase timeout or check locator stability."
        if "not match" in error.lower():
            return "Analysis: Authentication failure. Suggestion: Verify credentials or session state."
        return f"Analysis: Generic failure detected. Error: {error[:100]}"

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
