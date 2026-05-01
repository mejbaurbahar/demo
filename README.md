# AI-Powered Autonomous Automation Testing Framework

This is a production-ready, scalable automation ecosystem built with **Playwright (Python)**, **GitHub Actions**, and **AI-assisted testing** capabilities.

## 🚀 Features

- **End-to-End Testing**: Modular Page Object Model (POM) architecture.
- **AI-Powered Analysis**: Integrated with AI models (DeepSeek, Ollama, Qwen) for:
  - Failure root cause analysis.
  - Bug summary generation.
  - Self-healing locator suggestions.
- **Security & SSL Monitoring**: Automated checks for security headers and SSL certificate expiry.
- **API Testing**: Integrated REST API validation.
- **CI/CD Ready**: Pre-configured GitHub Actions for nightly regressions and PR checks.
- **Comprehensive Reporting**: HTML reports with embedded screenshots, videos, and Playwright traces.
- **Dockerized**: Easy execution in any environment using Docker.

## 🛠️ Project Structure

```text
saucedemo_automation/
├── .github/workflows/    # CI/CD pipelines
├── components/           # AI, Reporting, Notifications
├── pages/                # Page Object Model (POM)
├── tests/                # E2E, API, Security tests
├── utils/                # Config, Helpers, Logger
├── docker/               # Docker configuration
├── requirements.txt      # Dependencies
└── pytest.ini            # Test configuration
```

## ⚙️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd saucedemo_automation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

## 🤖 AI Integration

To enable AI failure analysis, set your API key:
```bash
export AI_API_KEY="your-api-key"
```
Or for local Ollama:
1. Install [Ollama](https://ollama.ai/).
2. Pull a model: `ollama pull deepseek-coder`.
3. The framework will automatically detect and use local models if configured in `components/ai_service.py`.

## 🐳 Docker Execution

```bash
docker build -t automation-framework -f docker/Dockerfile .
docker run -v $(pwd)/reports:/app/reports automation-framework
```

## 📊 Reporting

Reports are generated in the `reports/` directory. Open `report.html` in any browser to view detailed execution logs, screenshots, and AI analysis.

---
Built by Antigravity AI Assistant.
