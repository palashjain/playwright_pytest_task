from playwright.sync_api import Page
import allure
from pages.base_page import BasePage
from utils.helpers import validate_downloaded_file, generate_unique_filename

class StoreDetailsPage(BasePage):

    STORE_DETAILS_HEADING = "h4:has-text('Store Details')"

    STORE_POLYGONS_LABEL = "text=Store polygons"
    CREATE_POLYGON_BUTTON = "[data-testid='components_JMButton_JMButton_Button']"
    SEARCH_POLYGON_INPUT = "role=textbox[name='Search Polygon']"

    THREE_DOTS_MENU = "[data-testid='StoreDetails_SidebarHeader_SidebarHeader_SvgIcMoreVertical']"
    EXPORT_DATA_OPTION = "text=Export Data"
    SET_INACTIVE_OPTION = "text=Set as Inactive"
    SET_ACTIVE_OPTION = "text=Set as Active"

    EDIT_BUTTON = "text=Edit"
    DISTANCE_TEXT = "//p[@data-testid='StoreDetails_PolygonCard_PolygonCard_p']"
    POLYGON_INACTIVE_OPTION = "(//a[@target='_self'][normalize-space()='Set as Inactive'])[2]"
    POLYGON_MENU_BUTTON = "//span[@data-testid='StoreDetails_PolygonCard_PolygonCard_span']/div[@class='JMMenu']"

    DIALOG_SAVE_BUTTON = "button:has-text('Save')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger.info("Store Details page initialized")

    @allure.step("Verify store details page is displayed")
    def is_store_details_page_displayed(self) -> bool:
        self.wait_for_load_state('networkidle')
        return self.is_visible(self.STORE_DETAILS_HEADING)

    @allure.step("Get store name")
    def get_store_name(self) -> str:
        return self.get_text("h4")

    @allure.step("Click create polygon button")
    def click_create_polygon(self) -> None:
        self.click(self.CREATE_POLYGON_BUTTON)
        self.wait_for_load_state('networkidle')
        self.logger.info("Clicked create polygon button")

    @allure.step("Search for polygon: {polygon_name}")
    def search_polygon(self, polygon_name: str) -> None:
        self.page.wait_for_load_state('networkidle')
        self.fill(self.SEARCH_POLYGON_INPUT, polygon_name)
        self.logger.info(f"Searched for polygon: {polygon_name}")

    @allure.step("Verify polygon exists: {polygon_name}")
    def is_polygon_visible(self, polygon_name: str) -> bool:
        polygon_heading = f"h4:has-text('{polygon_name}')"
        is_visible = self.is_visible(polygon_heading, timeout=5000)
        self.logger.info(f"Polygon '{polygon_name}' visible: {is_visible}")
        return is_visible

    @allure.step("Verify polygon status: {polygon_name} - {expected_status}")
    def verify_polygon_status(self, polygon_name: str, expected_status: str) -> bool:
        status_element = self.page.locator(f"//h4[normalize-space()='{polygon_name}']/../..//span[@data-testid='components_JMBadge_JMBadge_span'][normalize-space()='{expected_status}']")
        is_status_correct = status_element.is_visible()

        self.logger.info(f"Polygon '{polygon_name}' has status '{expected_status}': {is_status_correct}")
        return is_status_correct

    @allure.step("Click three dots menu for Store")
    def click_three_dots_menu(self) -> None:
        self.click(self.THREE_DOTS_MENU)
        self.logger.info("Clicked three dots menu")

    @allure.step("Click Export Data and validate file is downloaded")
    def click_export_data_download_file(self) -> None:
        with self.page.expect_download() as download_info:
            self.click(self.EXPORT_DATA_OPTION)
            self.logger.info("Clicked Export Data option")
            download = download_info.value

            unique_filename = generate_unique_filename(download.suggested_filename)
            file_path = self.config.downloads_path / unique_filename
            download.save_as(file_path)
            self.logger.info(f"File downloaded successfully: {unique_filename}")

            validate_downloaded_file(file_path)
            self.logger.info(f"File validation successful - Size: {file_path.stat().st_size} bytes")

    @allure.step("Set store status to: {status}")
    def set_store_status(self, status: str) -> None:
        if status not in ['Active', 'Inactive']:
            raise ValueError(f"Invalid status: {status}. Must be 'Active' or 'Inactive'")
        self.page.wait_for_timeout(2000)
        option_locator = self.SET_ACTIVE_OPTION if status == 'Active' else self.SET_INACTIVE_OPTION
        self.page.locator(option_locator).first.click()
        self.wait_for_load_state('networkidle')
        self.logger.info(f"Set store status to {status}")

    @allure.step("Click Set as Inactive option")
    def click_set_as_inactive(self) -> None:
        self.set_store_status('Inactive')

    @allure.step("Click Set as Active option")
    def click_set_as_active(self) -> None:
        self.set_store_status('Active')

    @allure.step("Verify store status: {expected_status}")
    def verify_store_status(self, expected_status: str) -> bool:
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(5000)
        status_locator = (f"(//span[@data-testid='components_JMBadge_JMBadge_span'][normalize-space()='{expected_status}'])[1]")
        is_status_visible = self.is_visible(status_locator)
        self.logger.info(f"Store status '{expected_status}' visible: {is_status_visible}")
        return is_status_visible

    @allure.step("Click polygon three dots menu: {polygon_name}")
    def click_polygon_menu(self, polygon_name: str) -> None:
        self.click(self.POLYGON_MENU_BUTTON)
        self.logger.info(f"Clicked menu for polygon: {polygon_name}")

    @allure.step("Click Edit polygon: {polygon_name}")
    def click_edit_polygon(self, polygon_name: str) -> None:
        self.click_polygon_menu(polygon_name)
        self.click(self.EDIT_BUTTON)
        self.wait_for_load_state('networkidle')
        self.logger.info(f"Clicked Edit for polygon: {polygon_name}")

    @allure.step("Set polygon as inactive: {polygon_name}")
    def set_polygon_inactive(self, polygon_name: str) -> None:
        self.click_polygon_menu(polygon_name)
        self.click(self.POLYGON_INACTIVE_OPTION)
        self.wait_for_load_state('networkidle')
        self.logger.info(f"Set polygon '{polygon_name}' as inactive")

    @allure.step("Verify polygon travel distance: {polygon_name} - {expected_distance}")
    def verify_polygon_travel_distance(self, polygon_name: str, expected_distance: str) -> bool:
        actual_distance_text = self.get_text(self.DISTANCE_TEXT)
        is_distance_correct = expected_distance in actual_distance_text

        self.logger.info(f"Polygon '{polygon_name}' - Expected: '{expected_distance}', Actual: '{actual_distance_text}', Match: {is_distance_correct}")
        return is_distance_correct
