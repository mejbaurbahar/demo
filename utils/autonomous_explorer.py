"""
Autonomous UI Explorer
Independently crawls the target application, discovers all interactive surfaces,
generates a dynamic test strategy, and performs a predictive security audit.
Can be run standalone: python -m utils.autonomous_explorer [URL]
"""
import sys
import os
from playwright.sync_api import sync_playwright
from components.ai_service import AIService


def run_autonomous_exploration(url: str = "https://www.saucedemo.com/"):
    """
    Full 3-phase autonomous exploration:
    Phase 1 — Crawl & Discover (EXPLORER agent)
    Phase 2 — Dynamic Strategy Generation (GENERATOR agent)
    Phase 3 — Predictive Security Audit (SECURITY agent)
    """
    ai = AIService()
    print(f"[EXPLORER] Starting autonomous exploration of: {url}")
    ai.thinking.think(f"Autonomous Exploration initiated for: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (compatible; AutonomousQABot/1.0)"
        )
        page = context.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")

        # ── Phase 1: Crawl & Discover ─────────────────────────────────────
        print("[EXPLORER] Phase 1: Crawling interactive elements...")
        ai.thinking.think("Phase 1: Extracting DOM structure and interactive nodes...")

        html_snippet = page.content()[:3000]
        elements     = page.evaluate("""() => {
            return JSON.stringify(Array.from(
                document.querySelectorAll('input,button,select,a[href],form')
            ).map(el => ({
                tag:      el.tagName,
                id:       el.id,
                name:     el.name,
                type:     el.type,
                text:     (el.innerText || '').trim().slice(0,60),
                dataTest: el.dataset.test || '',
                href:     el.href || ''
            })));
        }""")

        ai.thinking.think(f"Discovered {len(elements)} characters of element data.")
        discovery = ai.run_agent("EXPLORER", html_snippet)
        print(f"[EXPLORER] Discovery Report:\n{discovery}\n")

        # ── Phase 2: Dynamic Strategy ─────────────────────────────────────
        print("[EXPLORER] Phase 2: Generating dynamic test strategy...")
        ai.thinking.think("Phase 2: GENERATOR agent brainstorming test scenarios...")
        strategy = ai.run_agent("GENERATOR", discovery)
        print(f"[EXPLORER] Test Strategy:\n{strategy}\n")

        # ── Phase 3: Security Audit ───────────────────────────────────────
        print("[EXPLORER] Phase 3: Predictive Security Audit...")
        ai.thinking.think("Phase 3: SECURITY agent performing offensive analysis...")
        security_findings = ai.run_agent("SECURITY", discovery)
        print(f"[EXPLORER] Security Findings:\n{security_findings}\n")

        # ── Save findings to memory ───────────────────────────────────────
        ai._update_memory("security_findings", {
            "timestamp": str(__import__("datetime").datetime.now()),
            "url":       url,
            "findings":  security_findings[:400]
        })

        browser.close()

    ai.thinking.think("Autonomous Exploration complete. Intelligence stored in memory.")
    print("[EXPLORER] Exploration complete.")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://www.saucedemo.com/"
    run_autonomous_exploration(target)
