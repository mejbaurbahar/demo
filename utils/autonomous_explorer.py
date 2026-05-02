import sys
import os
from playwright.sync_api import sync_playwright
from components.ai_service import AIService

def run_autonomous_exploration(url):
    """
    🕵️ UI Explorer Agent: Independently crawls and understands the application.
    """
    ai = AIService()
    print(f"🚀 Starting Autonomous Exploration of {url}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # 1. Crawl & Discover
        print("🔍 AI is crawling interactive elements...")
        html_context = page.content()[:2000] # Representative snippet
        discovery = ai.run_agent("EXPLORER", html_context)
        print(f"📄 AI Discovery Report:\n{discovery}\n")

        # 2. Dynamic Strategy Generation
        print("🧠 AI is generating a dynamic test strategy...")
        strategy = ai.run_agent("GENERATOR", discovery)
        print(f"📋 Dynamic Test Plan:\n{strategy}\n")

        # 3. Security Audit (Offensive Mode)
        print("🕵️ AI is performing a predictive security audit...")
        security_findings = ai.run_agent("SECURITY", discovery)
        print(f"🛡️ Security Mutation Report:\n{security_findings}\n")

        browser.close()
        print("✅ Autonomous Exploration Complete. Intelligence stored in Memory.")

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.saucedemo.com/"
    run_autonomous_exploration(target_url)
