# 🚀 Autonomous AI-Powered QA Automation Framework

A state-of-the-art, production-ready automation ecosystem built with **Playwright**, **Python**, and **Local AI (Ollama)**. This framework is designed to behave like an autonomous QA engineer—capable of running tests, understanding failures, and providing intelligent reporting with zero manual intervention.

---

## 🤖 How the AI Engine Works

This framework features a "Brain" layer that integrates directly with local AI models (like TinyLlama) via **Ollama**. Here is the autonomous workflow:

1.  **Detection**: When a test fails, the framework immediately captures the **Full Trace**, **Console Logs**, and a **High-Resolution Screenshot (POC)**.
2.  **Analysis**: The error context is fed into the local AI model. The AI "reads" the failure just like a human engineer would.
3.  **Diagnosis**: The AI determines if the failure is a **Functional Bug**, a **Synchronization Issue (Timeout)**, or a **UI Change**.
4.  **Reporting**: The AI writes a human-readable investigation report, including a **Root Cause** and a **Suggested Fix**, which is injected directly into your HTML Dashboard.

**Zero-Key Architecture**: Unlike other tools, this uses **Local AI**. It requires **No API Keys** (OpenAI/DeepSeek), ensuring 100% data privacy and $0 operational costs.

---

## ✨ Core Features

### 1. Autonomous Failure Analysis (AFA)
- **What it is**: A system that replaces manual log checking.
- **How it works**: Uses NLP to categorize errors and provide debugging recommendations automatically in every report.

### 2. Intelligent Reporting & POC
- **What it is**: A stakeholder-ready HTML dashboard.
- **How it works**: Generates a self-contained report with embedded screenshots, AI insights, and color-coded categorizations (Smoke, Security, API, Regression).

### 3. Automated Security Scanner
- **OWASP Validation**: Built-in checks for **XSS (Cross-Site Scripting)** and **SQL Injection (SQLi)** vulnerabilities.
- **SSL Monitoring**: Automatically alerts the team if SSL certificates are expiring within 30 days.
- **Security Headers**: Validates the presence of critical security headers to protect against clickjacking and MIME-sniffing.

### 4. Self-Healing Locator Handling (Experimental)
- **How it works**: On failure, the AI analyzes the page's HTML structure to suggest stable alternative selectors, reducing maintenance time.

### 5. 🛡️ Comprehensive Testing Coverage (50+ Types)
This framework is engineered to provide 360-degree quality assurance. Below are the testing types implemented and supported:

| Category | Testing Types Covered | Description |
| :--- | :--- | :--- |
| **Functional** | Smoke, Sanity, Regression, Retesting, Integration, System, E2E, UAT | Validates core business flows and ensure no regressions occur after code changes. |
| **Structural** | Black Box, White Box, Gray Box, Boundary Value, Equivalence Partitioning | Uses mathematical validation techniques to ensure input field integrity. |
| **Non-Functional** | Performance, Load, Stress, Benchmark, Scalability, Stability | Monitors system behavior under load and measures action latency. |
| **Security** | Vulnerability, Penetration, SQL Injection, XSS, Auth/Authz, SSL | Automated scans for OWASP Top 10 vulnerabilities and secure header validation. |
| **Quality of Experience**| Usability, UX, Accessibility (WCAG), Localization (i18n/l10n) | Ensures the app is accessible to all users and works across different locales. |
| **Compatibility** | Cross-Browser, Cross-Platform, Responsive, Mobile Emulation | Validates UI consistency across Chrome, Firefox, Safari, and Mobile viewports. |
| **Specialized** | API Testing, Exploratory, Ad-hoc, Monkey, Chaos, Resilience | Backend validation and stability testing under unpredictable conditions. |

---

---

## 🧠 The Autonomous QA Operating System
This framework has evolved into a **Level 4 Autonomous Ecosystem** powered by a **Multi-Agent Architecture**:

### 🎭 Multi-Agent Intelligence
- **🧠 RCA Agent**: Performs deep Root Cause Analysis, linking failures to patterns in its memory.
- **🩹 Healing Agent**: Automatically recovers broken UI locators in real-time using live HTML analysis.
- **🕵️ Security Agent**: Conducts adaptive vulnerability audits, suggesting mutation payloads for XSS/SQLi.
- **📉 Performance Agent**: Detects latency bottlenecks and optimizes execution timing.
- **📝 Reporting Agent**: Generates stakeholder-ready dashboards with visual POCs and technical audits.

### 🚀 Next-Gen Roadmap
- **AI Test Case Generator**: Auto-generating test scenarios from Swagger/OpenAPI.
- **AI Visual Intelligence**: Understanding layout shifts and responsive UI alignment issues.
- **AI Smart Prioritization**: Running high-risk tests first based on Git commit history.
- **AI Production Feedback Loop**: Syncing with Grafana/Sentry to reproduce production bugs locally.





---

## 🛠️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mejbaurbahar/demo.git
   cd demo
   ```



2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. **Run All Tests**:
   ```bash
   pytest
   ```

4. **Run Specific Suite**:
   ```bash
   # Run Smoke tests
   pytest -m smoke
   
   # Run Security & Performance tests
   pytest -m "security or performance"
   
   # Run all Functional tests
   pytest tests/functional/
   ```


---

## ☁️ CI/CD Integration

The framework is fully integrated with **GitHub Actions**. On every push:
1. It provisions a Linux environment.
2. It installs and launches **Ollama** locally.
3. It executes the full test suite.
4. It **Emails a detailed HTML Report** to the stakeholders using your secure Gmail bridge.

---

## 📊 Sample Report Preview
The report includes:
- **Status Summary**: Pass/Fail/Skip counts.
- **AI Investigation**: Root cause analysis per failure.
- **Screenshots**: Visual proof for every error.
- **Trace Files**: Step-by-step recording of the failure.

---
