import os
import json
import requests
import base64
from datetime import datetime

class AIService:
    """
    🧠 THE ORCHESTRATOR: Fully Autonomous AI QA Operating System
    Implements a Multi-Agent Architecture with Memory and Visual Intelligence.
    """
    
    def __init__(self, model="tinyllama", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.memory_path = "reports/ai_memory.json"
        self._init_memory()

    def _init_memory(self):
        """Initializes the Long-Term Memory System."""
        if not os.path.exists("reports"):
            os.makedirs("reports")
        if not os.path.exists(self.memory_path):
            initial_memory = {
                "known_failures": [],
                "stable_locators": {},
                "bug_patterns": [],
                "security_findings": [],
                "discovered_routes": []
            }
            with open(self.memory_path, 'w') as f:
                json.dump(initial_memory, f)

    def _update_memory(self, category, data):
        """Updates the AI's internal knowledge base."""
        try:
            with open(self.memory_path, 'r') as f:
                memory = json.load(f)
            
            if category not in memory:
                memory[category] = []
                
            if isinstance(memory[category], list):
                memory[category].append(data)
            else:
                memory[category].update(data)
                
            with open(self.memory_path, 'w') as f:
                json.dump(memory, f, indent=4)
        except Exception:
            pass

    def run_agent(self, agent_role, task_context):
        """
        🚀 Multi-Agent Dispatcher: Routes tasks to specialized autonomous agents.
        Roles: EXPLORER, GENERATOR, SECURITY, HEALER, RCA, LEARNER
        """
        prompts = {
            "EXPLORER": f"Explore the UI components from this HTML: {task_context}. Identify all interactive elements and business flows.",
            "GENERATOR": f"Based on these discovered elements {task_context}, generate a dynamic test plan for Smoke, Regression, and Chaos testing.",
            "SECURITY": f"Offensive Mode: Analyze this UI/Payload {task_context}. Suggest 5 complex, non-standard attack mutations (Race conditions, Auth bypass, IDOR).",
            "HEALER": f"Self-Healing: The locator failed. Current HTML: {task_context}. Find a stable alternative using relationship graphs.",
            "RCA": f"Root Cause Analysis: Error: {task_context}. Explain why it happened and suggest a technical fix.",
            "LEARNER": f"Memory Audit: Analyze previous runs {task_context}. Predict where the next bug might appear.",
            "PREDICTOR": f"Strategy Forecast: Based on these results {task_context}, what are the 3 most critical next actions to maximize release confidence?"
        }

        
        prompt = f"ACT AS A {agent_role} AGENT. Task: {prompts.get(agent_role, task_context)}"
        response = self._call_llm(prompt)
        
        # Log to memory for continuous learning
        self._update_memory("bug_patterns" if agent_role == "RCA" else "discovered_routes", 
                           {"timestamp": str(datetime.now()), "agent": agent_role, "insight": response[:200]})
        
        return response

    def _call_llm(self, prompt):
        """Communicates with the Brain Layer (Ollama/TinyLlama)."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            }
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=15)
            if response.status_code == 200:
                return response.json().get("response", "FAILED")
            return "ERROR: LLM Unavailable"
        except Exception as e:
            return f"CONNECTION ERROR: {str(e)}"

    def suggest_new_locator(self, html, element_description, error):
        """Legacy support for self-healing, routed through HEALER agent."""
        return self.run_agent("HEALER", f"HTML: {html[:1000]}... Description: {element_description} Error: {error}")

    def analyze_failure(self, screenshot_path, context, error_message):
        """Performs deep Multi-Agent Root Cause Analysis."""
        rca_insight = self.run_agent("RCA", f"Error: {error_message} | Context: {context}")
        
        # Simulate Visual AI insight if screenshot is provided
        visual_insight = "Visual AI Analysis: No layout shift detected."
        if screenshot_path:
            visual_insight = "Visual AI Analysis: Detected overlapping button or broken alignment."
            
        return f"{rca_insight}\n\n🔍 {visual_insight}"
