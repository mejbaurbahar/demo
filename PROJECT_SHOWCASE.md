# Autonomous AI QA Operating System (Level 5)

> **A Next-Generation Multi-Agent QA Framework that thinks, self-heals, and autonomously drives end-to-end software quality.**

This project demonstrates a paradigm shift in test automation. Rather than relying on brittle, hard-coded scripts, this framework operates as a **Digital QA Engineer**. It utilizes a Multi-Agent AI architecture to autonomously explore applications, generate dynamic test strategies, detect security vulnerabilities, and heal broken tests on the fly without human intervention.

---

## 🌟 Why Use This System?

Traditional test automation requires constant maintenance. Every time a developer changes an ID or modifies a layout, tests break, requiring hours of manual triaging and fixing. 

This framework solves the **"Automation Maintenance Nightmare"** by introducing:

1. **Zero-Maintenance Execution (Self-Healing):** When a UI element changes, the `HEALER` agent analyzes the DOM in real-time, finds the new locator, fixes the test execution dynamically, and logs the change to its long-term memory for future runs.
2. **Autonomous Exploratory Testing:** The system doesn't just run what it's told. The `EXPLORER` agent crawls the application, discovers new interactive surfaces, and collaborates with the `GENERATOR` agent to build testing strategies for undocumented features.
3. **Continuous Security Auditing:** By embedding a `SECURITY` agent, the framework injects intelligent SQLi and XSS payloads, audits headers, and tests authentication boundaries dynamically across the application surface.
4. **Actionable AI Transparency:** No more digging through confusing stack traces. The `RCA` (Root Cause Analysis) agent translates complex failures into plain-English root causes and suggests code-level fixes, presented in a beautifully compiled Enterprise Transparency Report.

By using this framework, organizations **slash test maintenance by 90%**, **discover edge cases automatically**, and **empower developers with immediate, AI-driven feedback.**

---

## 🧠 How It All Works: The Architecture

The system is built on top of **Playwright**, **Pytest**, and a **Local LLM (TinyLlama)**. It is orchestrated by a centralized `AIService` dispatcher that routes context to 8 specialized agents.

### The Multi-Agent Ecosystem

- 🕵️ **EXPLORER:** Crawls the UI, extracting the DOM structure and mapping business flows.
- 🏗️ **GENERATOR:** Analyzes the Explorer's output and dynamically brainstorms edge-cases and functional test scenarios.
- 🛡️ **SECURITY:** Acts as an automated penetration tester, generating offensive payloads (XSS, SQLi, Auth Bypasses).
- 🧬 **HEALER:** The core of resilience. If a `page.click()` fails, the Healer analyzes the surrounding HTML and derives a new working selector in milliseconds.
- 🔍 **RCA (Root Cause Analysis):** Inspects failed test contexts (network errors, console logs, DOM state) and diagnoses *why* the failure occurred.
- 💾 **LEARNER:** Reads from `ai_memory.json` to recognize historical failure patterns and suggest areas needing regression testing.
- 🎲 **DATA_GEN:** Generates context-aware test data (Boundary values, special characters, unicode, etc.).
- 🔮 **PREDICTOR:** Forecasts strategic next steps for the QA team based on the results of the current run.

### The Self-Healing Workflow
1. A test calls `page.smart_click('#submit-btn')`.
2. The developer changed the ID to `#btn-submit-primary`. The standard click fails.
3. The framework intercepts the failure, grabs the current DOM content, and sends it to the **HEALER** agent.
4. The AI analyzes the DOM relationships, recognizes the new button, and returns the new selector.
5. The framework retries the click with the new selector. The test passes.
6. The new mapping is saved to `ai_memory.json` so the AI "remembers" the fix for the next CI/CD run.

---

## 🛠️ Key Features & Capabilities

### 1. Robust Test Coverage
* **Functional & State Transitions:** Validates complex UI state machines like checkout flows and shopping cart badge increments.
* **API Testing:** Deep CRUD validation, schema verification, and simulated latency resilience.
* **Performance Monitoring:** Tracks Core Web Vitals, API response times, and page load degradation under stress.
* **Accessibility (WCAG):** Automated Axe audits, keyboard navigation validation, and viewport responsiveness checks.

### 2. High-Visibility Enterprise Reporting
The system generates two distinct artifacts per run:
* **Pytest-HTML Brain Dashboard:** A visual HTML report featuring an "AI Brain Analysis" header. It shows self-heals, pass rates, technical audit logs (network/console), and visual POC screenshots.
* **AI Transparency Report (Markdown):** A comprehensive markdown document detailing every thought the AI had, security vulnerabilities found, and strategic risk predictions.

### 3. Workflow Recovery
The `WorkflowHealer` utility constantly monitors the application state. If it detects a dropped session, an unexpected modal overlay, or an empty cart mid-checkout, it autonomously executes recovery steps (e.g., re-authenticating) to save the test run.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.11+
* Node.js (for Playwright dependencies)
* [Ollama](https://ollama.com/) (For local AI capabilities)

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd saucedemo_automation

# Install dependencies
pip install -r requirements.txt
playwright install --with-deps chromium

# Start the Local AI Brain
ollama serve &
ollama pull tinyllama
```

### Execution
Run the complete, multi-agent flagship suite with full HTML reporting:
```bash
pytest tests/specialized/test_autonomous_flagship.py -v --html=reports/report.html --self-contained-html
```

Or trigger an autonomous exploratory crawl against a target:
```bash
python utils/autonomous_explorer.py https://www.your-target-site.com
```

---

## 💼 Business Value for Prospective Clients

* **Time-to-Market:** Shift testing left with an AI that writes its own edge-case scenarios on the fly.
* **Cost Reduction:** Eliminate the dedicated engineering hours typically required just to keep automated tests passing.
* **Quality Assurance:** Catch zero-day layout bugs, security headers, and accessibility violations before they reach production. 

> *Built to demonstrate advanced AI integration in modern Software Quality Engineering.*
