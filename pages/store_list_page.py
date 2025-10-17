from playwright.sync_api import Page
from pages.base_page import BasePage
import allure


class StoreListPage(BasePage):

    SEARCH_STORE_INPUT = "role=textbox[name='Search by Store Code']"
    STORE_CODE_DROPDOWN = "text=Code"

    STORE_BUTTON_TEMPLATE = "button:has-text('{store_name}')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger.info("Store List page initialized")

    @allure.step("Search for store: {store_code}")
    def search_store(self, store_code: str) -> None:
        self.fill(self.SEARCH_STORE_INPUT, store_code)
        self.logger.info(f"Searched for store: {store_code}")

    @allure.step("Click on store: {store_name}")
    def click_store(self, store_name: str) -> None:
        store_button = f"button:has-text('{store_name}')"

        self.wait_for_element(store_button)

        self.page.get_by_role('button').filter(has_text=store_name).first.click()
        self.wait_for_load_state('networkidle')

        self.logger.info(f"Clicked on store: {store_name}")

    @allure.step("Verify stores page is displayed")
    def is_stores_page_displayed(self) -> bool:
        self.wait_for_load_state('networkidle')
        try:
            current_url = self.page.url.lower()
            if 'store' in current_url or 'stores' in current_url:
                return True

            if self.is_visible(self.SEARCH_STORE_INPUT):
                return True

        except Exception as e:
            self.logger.warning(f"Error checking stores page: {e}")

        return False

    @allure.step("Click on first active store")
    def click_first_active_store(self) -> str:

        self.wait_for_load_state('networkidle')
        self.wait_for_element(self.SEARCH_STORE_INPUT, timeout=10000)
        self.page.wait_for_timeout(3000)

        active_stores = self.page.locator("//span[@data-testid='components_JMBadge_JMBadge_span'][normalize-space()='Active']").all()
        first_active = active_stores[0]

        store_text = first_active.inner_text()
        lines = [line.strip() for line in store_text.split('\n') if line.strip()]
        store_name = next((line for line in lines if line and 'Active' not in line), lines[0] if lines else store_text.strip())

        first_active.click()
        self.wait_for_load_state('networkidle')

        self.logger.info(f"Clicked on first active store: {store_name}")
        return store_name
