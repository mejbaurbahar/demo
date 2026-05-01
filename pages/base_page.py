from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")

    def click(self, selector: str):
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        self.page.fill(selector, text)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)
