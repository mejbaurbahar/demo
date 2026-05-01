from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.checkout_button = "id=checkout"

    def click_checkout(self):
        self.click(self.checkout_button)

class CheckoutStepOne(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name = "id=first-name"
        self.last_name = "id=last-name"
        self.zip_code = "id=postal-code"
        self.continue_button = "id=continue"

    def fill_form(self, first, last, zip):
        self.fill(self.first_name, first)
        self.fill(self.last_name, last)
        self.fill(self.zip_code, zip)
        self.click(self.continue_button)

class CheckoutStepTwo(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.finish_button = "id=finish"

    def click_finish(self):
        self.click(self.finish_button)

class CheckoutComplete(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.complete_header = ".complete-header"

    def get_success_message(self):
        return self.get_text(self.complete_header)
