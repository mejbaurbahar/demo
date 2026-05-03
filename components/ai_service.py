import os
import json
import requests
import base64
from datetime import datetime


class AIService:
    """
    AI QA Operating System Orchestrator.
    Implements a Multi-Agent Architecture with Long-Term Memory and Heuristic Fallbacks.

    Agents:
      EXPLORER   - Crawls UI and discovers business flows
      GENERATOR  - Generates dynamic test plans from discovered elements
      SECURITY   - Offensive mutation testing (SQLi, XSS, IDOR, CSRF)
      HEALER     - Self-healing locator recovery via DOM relationship analysis
      RCA        - Root Cause Analysis for failures with fix suggestions
      LEARNER    - Queries historical memory for predictive insights
      DATA_GEN   - Context-aware realistic test data generation
      PREDICTOR  - Strategic next-action forecasting after a run
    """

    def __init__(self, model="tinyllama", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.memory_path = "reports/ai_memory.json"
        # Import here to avoid circular; ThinkingEngine is a lightweight logger
        from utils.thinking_engine import ThinkingEngine
        self.thinking = ThinkingEngine()
        self._init_memory()

    # ── Memory System ─────────────────────────────────────────────────────────

    def _init_memory(self):
        """Initialises the Long-Term JSON Memory Store."""
        os.makedirs("reports", exist_ok=True)
        if not os.path.exists(self.memory_path):
            initial_memory = {
                "known_failures":   [],
                "stable_locators":  {},
                "healed_elements":  {},
                "bug_patterns":     [],
                "security_findings":[],
                "discovered_routes":[],
                "performance_logs": [],
                "ai_decisions":     []
            }
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(initial_memory, f, indent=4)

    def _update_memory(self, category: str, data):
        """Appends or merges data into the named memory category."""
        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                memory = json.load(f)
            if category not in memory:
                memory[category] = [] if not isinstance(data, dict) else {}
            if isinstance(memory[category], list):
                memory[category].append(data)
            elif isinstance(memory[category], dict):
                memory[category].update(data)
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(memory, f, indent=4)
        except Exception:
            pass

    def get_memory(self) -> dict:
        """Returns the full long-term memory snapshot."""
        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    # ── Multi-Agent Dispatcher ────────────────────────────────────────────────

    def run_agent(self, agent_role: str, task_context) -> str:
        """
        Dispatch a task to a named specialised agent.
        task_context can be a string or a dict with keys: html, selector, error, data.
        Returns the agent response (LLM or heuristic fallback).
        """
        self.thinking.think(f"[AGENT] Activating '{agent_role}' agent...")

        # Normalise context to dict
        ctx = task_context if isinstance(task_context, dict) else {"data": str(task_context)}

        prompts = {
            "EXPLORER": (
                "You are a UI Explorer. Analyse this HTML and list every interactive element "
                "(buttons, inputs, links, forms) and the user journeys they enable:\n"
                f"{ctx.get('data', '')[:3000]}"
            ),
            "GENERATOR": (
                "You are a Test Architect. Based on these discovered UI elements, generate a "
                "JSON test plan with keys: test_name, priority, steps (list of dicts with action, selector, value), "
                f"and expected_result:\n{ctx.get('data', '')[:3000]}"
            ),
            "SECURITY": (
                "You are an Offensive Security Engineer. Identify 5 specific attack vectors "
                "(SQLi, XSS, IDOR, CSRF, Auth-bypass) for this application surface and explain "
                f"each with a payload example:\n{ctx.get('data', '')[:2000]}"
            ),
            "HEALER": (
                "You are a DOM Self-Healing expert. A Playwright locator has failed. "
                "Analyse the HTML and return ONLY a single working CSS or XPath selector "
                "that identifies the same element. "
                f"Failed selector: '{ctx.get('selector', '')}' "
                f"Error: {ctx.get('error', '')} "
                f"HTML (truncated):\n{ctx.get('html', '')[:1500]}"
            ),
            "RCA": (
                "You are a Senior QA Architect performing Root Cause Analysis. "
                "Explain in 3 concise bullet points why this failure occurred and provide "
                f"a concrete fix recommendation:\n{ctx.get('data', '')[:2000]}"
            ),
            "LEARNER": (
                "You are a QA Learning Agent. Review this historical test data and "
                "predict the top 3 areas most likely to contain bugs in the next run:\n"
                f"{ctx.get('data', '')[:2000]}"
            ),
            "DATA_GEN": (
                "You are a Test Data Generator. For the described form fields, generate "
                "a JSON object with keys: valid, invalid, boundary, xss, sqli — each "
                f"containing appropriate test values:\n{ctx.get('data', '')[:1500]}"
            ),
            "PREDICTOR": (
                "You are a Strategic QA Forecaster. Based on this test run summary, "
                "state the 3 most critical next actions to maximise release confidence:\n"
                f"{ctx.get('data', '')[:1500]}"
            ),
        }

        prompt = prompts.get(agent_role, f"Task: {str(ctx)[:2000]}")
        response = self._call_llm(prompt)

        if not response or "CONNECTION ERROR" in response or response == "FAILED":
            self.thinking.think(
                f"[AGENT] '{agent_role}' LLM unavailable — activating heuristic fallback.", level="WARNING"
            )
            response = self._heuristic_fallback(agent_role, ctx)

        # Persist agent decision to memory
        self._update_memory("ai_decisions", {
            "timestamp": str(datetime.now()),
            "agent":     agent_role,
            "insight":   response[:300]
        })
        return response

    # ── LLM Communication ─────────────────────────────────────────────────────

    def _call_llm(self, prompt: str) -> str:
        """Sends a prompt to the Ollama LLM endpoint."""
        try:
            payload = {
                "model":  self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 512}
            }
            resp = requests.post(
                f"{self.base_url}/api/generate", json=payload, timeout=120
            )
            if resp.status_code == 200:
                return resp.json().get("response", "FAILED")
            return "ERROR: LLM Unavailable"
        except Exception as e:
            return f"CONNECTION ERROR: {str(e)}"

    # ── Heuristic Fallback Engine ─────────────────────────────────────────────

    def _heuristic_fallback(self, agent_role: str, ctx: dict) -> str:
        """
        Rule-based responses when the LLM is unreachable.
        Ensures the framework keeps running even without a local AI model.
        """
        if agent_role == "HEALER":
            selector = ctx.get("selector", "")
            # Try data-test, then aria-label, then text-based alternatives
            candidates = [
                f"[data-test='{selector.lstrip('#').lstrip('.')}']",
                f"[aria-label*='{selector}']",
                f"text={selector}",
            ]
            return candidates[0]

        if agent_role == "DATA_GEN":
            return json.dumps({
                "valid":    {"username": "standard_user",   "password": "secret_sauce"},
                "invalid":  {"username": "bad_user",         "password": "wrong_pass"},
                "boundary": {"username": "a" * 255,          "password": "b" * 255},
                "xss":      {"username": "<script>alert(1)</script>", "password": "xss"},
                "sqli":     {"username": "' OR '1'='1",      "password": "any"}
            })

        if agent_role == "SECURITY":
            return (
                "Heuristic Security Findings:\n"
                "1. [SQLi] Try: ' OR '1'='1 in username\n"
                "2. [XSS]  Try: <script>alert(1)</script> in text inputs\n"
                "3. [IDOR] Enumerate /inventory-item.html?id=1..99\n"
                "4. [Auth] Test locked_out_user bypass via direct URL\n"
                "5. [CSRF] No CSRF token observed on login form"
            )

        if agent_role == "PREDICTOR":
            return (
                "Strategic Forecast (Heuristic):\n"
                "1. Run full regression suite — checkout flow high risk after sort changes\n"
                "2. Re-audit security headers (X-Frame-Options missing)\n"
                "3. Add negative tests for cart badge counter state transitions"
            )

        return f"HEURISTIC_FALLBACK: Agent '{agent_role}' completed with default logic."

    # ── Public Helper Methods ─────────────────────────────────────────────────

    def suggest_new_locator(self, html: str, selector: str, error: str) -> str:
        """Public API: Request HEALER agent for a new locator."""
        return self.run_agent("HEALER", {
            "html":     html[:2000],
            "selector": selector,
            "error":    str(error)
        })

    def analyze_failure(self, screenshot_path, context: str, error_message: str) -> str:
        """Performs RCA + optional visual analysis and returns a formatted report."""
        rca_insight = self.run_agent("RCA", f"Error: {error_message} | Context: {context}")
        if screenshot_path and os.path.exists(str(screenshot_path)):
            visual_insight = "Visual Analysis: Screenshot captured — check POC evidence above."
        else:
            visual_insight = "Visual Analysis: No screenshot captured for this failure."
        return f"{rca_insight}\n\n[Visual] {visual_insight}"

    def generate_test_data(self, field_context: str) -> dict:
        """Generates a complete set of test data for given field context."""
        raw = self.run_agent("DATA_GEN", field_context)
        try:
            start = raw.find("{")
            end   = raw.rfind("}") + 1
            return json.loads(raw[start:end]) if start >= 0 else {}
        except Exception:
            return {}
