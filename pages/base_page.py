from playwright.sync_api import Page, Locator, expect
from utils.logger import Logger
from utils.config_manager import ConfigManager
from typing import Optional
import allure
from pathlib import Path
from datetime import datetime


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.logger = Logger()
        self.config = ConfigManager()

    @allure.step("Navigate to URL: {url}")
    def navigate(self, url: str) -> None:
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle')

    @allure.step("Click element")
    def click(self, locator: str | Locator, timeout: Optional[int] = 1000) -> None:
        self.page.wait_for_load_state('networkidle')
        element = self._get_element(locator)
        self.logger.info(f"Clicking element: {locator}")

        element.scroll_into_view_if_needed()
        element.click(timeout=timeout)

    @allure.step("Fill text")
    def fill(self, locator: str | Locator, text: str, timeout: Optional[int] = 1000) -> None:
        element = self._get_element(locator)
        self.logger.info(f"Filling text in element: {locator}")
        element.scroll_into_view_if_needed()
        element.fill(text, timeout=timeout)

    @allure.step("Get text from element")
    def get_text(self, locator: str | Locator) -> str:
        element = self._get_element(locator)
        text = element.text_content()
        self.logger.info(f"Got text from element: {text}")
        return text.strip() if text else ""

    @allure.step("Check if element is visible")
    def is_visible(self, locator: str | Locator, timeout: int = 5000) -> bool:
        try:
            element = self._get_element(locator)
            return element.is_visible(timeout=timeout)
        except Exception as e:
            self.logger.debug(f"Element not visible: {e}")
            return False

    @allure.step("Wait for element to be visible")
    def wait_for_element(self, locator: str | Locator, timeout: Optional[int] = None, state: str = 'visible') -> None:
        element = self._get_element(locator)
        self.logger.info(f"Waiting for element: {locator} to be {state}")
        element.wait_for(state=state, timeout=timeout)

    @allure.step("Upload file")
    def upload_file(self, locator: str | Locator, file_path: str) -> None:
        element = self._get_element(locator)
        self.logger.info(f"Uploading file: {file_path}")
        element.set_input_files(file_path)

    @allure.step("Assert element contains text")
    def assert_text_contains(self, locator: str | Locator, expected_text: str) -> None:
        element = self._get_element(locator)
        self.logger.info(f"Asserting element contains text: {expected_text}")
        expect(element).to_contain_text(expected_text)

    @allure.step("Assert element is visible")
    def assert_visible(self, locator: str | Locator) -> None:
        element = self._get_element(locator)
        self.logger.info(f"Asserting element is visible: {locator}")
        expect(element).to_be_visible()

    @allure.step("Press key")
    def press_key(self, key: str) -> None:

        self.logger.info(f"Pressing key: {key}")
        self.page.keyboard.press(key)

    @allure.step("Wait for page load")
    def wait_for_load_state(self, state: str = 'networkidle', timeout: Optional[int] = None) -> None:
        self.logger.info(f"Waiting for page load state: {state}")
        self.page.wait_for_load_state(state, timeout=timeout)

    @allure.step("Scroll to element")
    def scroll_to_element(self, locator: str | Locator) -> None:
        element = self._get_element(locator)
        self.logger.info(f"Scrolling to element: {locator}")
        element.scroll_into_view_if_needed()

    def _get_element(self, locator: str | Locator) -> Locator:
        self.page.wait_for_timeout(1000)
        if isinstance(locator, str):
            return self.page.locator(locator)
        return locator

    @allure.step("Take screenshot")
    def take_screenshot(self, name: str) -> None:

        screenshots_dir = Path(__file__).parent.parent / 'screenshots'
        screenshots_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = screenshots_dir / f"{name}_{timestamp}.png"

        self.page.screenshot(path=str(screenshot_path))
        allure.attach.file(
            str(screenshot_path),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        self.logger.info(f"Screenshot saved: {screenshot_path}")
