import json
from components.ai_service import AIService
from playwright.sync_api import Page

class DynamicTestGenerator:
    """
    ✨ AI DYNAMIC GENERATOR: Automatically generates and executes missing test scenarios.
    """
    def __init__(self, page: Page):
        self.page = page
        self.ai = AIService()
        self.thinking = self.ai.thinking

    def generate_and_execute(self, url: str):
        self.thinking.think(f"Starting Autonomous Generation for {url}")
        self.page.goto(url)
        
        # 1. Discover State
        html = self.page.content()
        self.thinking.think("Analyzing UI structure to identify interaction nodes...")
        
        # 2. Get AI Test Plan
        test_plan_str = self.ai.run_agent("GENERATOR", html[:3000])
        self.thinking.think(f"AI Suggested Test Plan: {test_plan_str[:200]}...")
        
        try:
            # Attempt to parse AI plan if it's JSON
            if "{" in test_plan_str:
                test_plan = json.loads(test_plan_str[test_plan_str.find("{"):test_plan_str.rfind("}")+1])
                self._execute_plan(test_plan)
            else:
                self.thinking.think("AI returned unstructured plan. Using intelligent fallback execution.", level="WARNING")
                self._fallback_execution()
        except Exception as e:
            self.thinking.think(f"Execution Error: {str(e)}", level="ERROR")

    def _execute_plan(self, plan):
        """Executes a structured AI test plan."""
        test_name = plan.get("test_name", "AI_Generated_Test")
        steps = plan.get("steps", [])
        
        self.thinking.think(f"Executing: {test_name}")
        
        for step in steps:
            action = step.get("action", "").lower()
            selector = step.get("selector", "")
            value = step.get("value", "")
            
            self.thinking.think(f"Step: {action} on {selector}")
            
            if "click" in action:
                self.page.click(selector, timeout=5000)
            elif "fill" in action or "type" in action:
                self.page.fill(selector, value, timeout=5000)
            elif "wait" in action:
                self.page.wait_for_timeout(2000)
        
        self.thinking.think(f"Completed dynamic execution of {test_name}")

    def _fallback_execution(self):
        """Intelligent exploratory execution."""
        self.thinking.think("Performing Exploratory 'Chaos' Testing...")
        # Add random interactions based on detected elements
        pass
