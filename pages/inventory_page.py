from pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header_title = ".title"
        self.sort_dropdown = ".product_sort_container"
        self.cart_link = ".shopping_cart_link"
        self.burger_menu = "id=react-burger-menu-btn"
        self.logout_link = "id=logout_sidebar_link"

    def add_to_cart(self, product_name: str):
        selector = f"id=add-to-cart-{product_name.lower().replace(' ', '-')}"
        self.click(selector)

    def remove_from_cart(self, product_name: str):
        selector = f"id=remove-{product_name.lower().replace(' ', '-')}"
        self.click(selector)

    def change_sort(self, value: str):
        # value can be: az, za, lohi, hilo
        self.page.select_option(self.sort_dropdown, value)

    def go_to_cart(self):
        self.click(self.cart_link)

    def logout(self):
        self.click(self.burger_menu)
        self.click(self.logout_link)
