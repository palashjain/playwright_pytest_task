from playwright.sync_api import Page
from pages.base_page import BasePage
import allure


class HomePage(BasePage):

    STORES_NAV = "//span[@data-testid='components_SidebarNav_index_span'][contains(text(),'Stores')]"
    USER_PROFILE = "//div[@id='avatarContainer']"
    LOGOUT_BUTTON = "text=Log Out"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger.info("Home page initialized")

    @allure.step("Navigate to Stores section")
    def navigate_to_stores(self) -> None:
        self.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(5000)
        self.click(self.STORES_NAV)
        self.logger.info("Navigated to Stores section")

    @allure.step("Click user profile")
    def click_user_profile(self) -> None:
        self.click(self.USER_PROFILE)
        self.logger.info("Clicked user profile")

    @allure.step("Logout from application")
    def logout(self) -> None:
        self.click_user_profile()
        self.page.wait_for_timeout(2000)
        logout_option = self.page.locator(self.LOGOUT_BUTTON)
        logout_option.is_visible(timeout=3000)
        logout_option.click()
        self.wait_for_load_state('networkidle')
        self.logger.info("Logged out successfully")
