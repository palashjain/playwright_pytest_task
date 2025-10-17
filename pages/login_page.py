from playwright.sync_api import Page
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):

    EMAIL_INPUT = "role=textbox[name='abc@example.com']"
    PASSWORD_INPUT = "role=textbox[name='Enter Password']"
    ACCEPT_TERMS_CHECKBOX = "[data-testid='Auth_Login_index_Checkbox']"
    LOGIN_BUTTON = "[data-testid='Auth_Login_index_Button']"
    LOGO = "img[alt='logo']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger.info("Login page initialized")

    @allure.step("Navigate to login page")
    def navigate_to_login(self) -> None:
        self.navigate(self.config.base_url)
        self.wait_for_element(self.EMAIL_INPUT)
        self.logger.info("Navigated to login page")

    @allure.step("Enter email: {email}")
    def enter_email(self, email: str) -> None:
        self.fill(self.EMAIL_INPUT, email)
        self.logger.info(f"Entered email: {email}")

    @allure.step("Enter password")
    def enter_password(self, password: str) -> None:
        self.fill(self.PASSWORD_INPUT, password)
        self.logger.info("Entered password")

    @allure.step("Accept terms and conditions")
    def accept_terms(self) -> None:
        self.click(self.ACCEPT_TERMS_CHECKBOX)
        self.logger.info("Accepted terms and conditions")

    @allure.step("Click login button")
    def click_login(self) -> None:
        self.click(self.LOGIN_BUTTON)
        self.logger.info("Clicked login button")

    @allure.step("Login with credentials")
    def login(self, email: str, password: str) -> None:
        self.logger.info(f"Attempting to login with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.accept_terms()
        self.click_login()

        self.page.wait_for_load_state('networkidle')
        self.logger.info("Login successful")

    @allure.step("Verify login page is displayed")
    def is_login_page_displayed(self) -> bool:
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(9000)
        url_has_login = "/login" in self.page.url
        logo_visible = self.is_visible(self.LOGO, timeout=5000)
        self.logger.info("Login page displayed")
        return url_has_login and logo_visible
