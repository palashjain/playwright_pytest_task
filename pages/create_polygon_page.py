from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from typing import Optional
import csv
import os
import math


class CreatePolygonPage(BasePage):

    HEADER_TITLE = "h1:has-text('Create New Polygon')"
    CREATE_BUTTON = "button:has-text('Create')"

    POLYGON_NAME_INPUT = "role=textbox[name='Add name of polygon']"

    QUICK_COMMERCE_RADIO = "div[class*='JMRadioCard']:has-text('Quick Commerce')"
    SLOTTED_DELIVERY_RADIO = "div[class*='JMRadioCard']:has-text('Slotted Delivery')"

    TRAVEL_TIME_TAB = "div[class*='_item_1hxwt_13']:has-text('Travel Time')"
    TRAVEL_DISTANCE_TAB = "div[class*='_item_1hxwt_13']:has-text('Travel Distance')"
    MANUAL_TAB = "div[class*='_item_1hxwt_13']:has-text('Manual')"

    TRAVEL_TIME_INPUT = "input#polygon\\.attributes\\.travel_time"
    TRAVEL_DISTANCE_INPUT = "input#polygon\\.attributes\\.travel_distance"

    UPLOAD_CSV_BUTTON = "input[type='file']"
    UPLOAD_CORDINATES_BUTTON = "//div[normalize-space()='Upload Coordinates']"
    MANUAL_DRAWING_OPTION = "text=Manual Drawing"

    MAX_PROMISE_TIME_INPUT = "//input[@id='meta.max_promise_time']"
    FLAT_DELIVERY_FEE_INPUT = "//input[@id='meta.flat_delivery_fee']"

    GROCERY_STORE_TYPE = "//div[contains(@class, 'JMRadioCard') and .//div[text()='Grocery']]"
    DIGITAL_STORE_TYPE = "//div[contains(@class, 'JMRadioCard') and .//div[text()='Digital']]"

    EDIT_HEADER = "h1:has-text('Edit Polygon')"
    UPDATE_BUTTON = "button:has-text('Update')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger.info("Create Polygon page initialized")

    @allure.step("Verify create polygon page is displayed")
    def is_create_polygon_page_displayed(self) -> bool:
        return self.is_visible(self.HEADER_TITLE) or self.is_visible(self.EDIT_HEADER)

    @allure.step("Enter polygon name: {name}")
    def enter_polygon_name(self, name: str) -> None:
        self.fill(self.POLYGON_NAME_INPUT, name)
        self.logger.info(f"Entered polygon name: {name}")

    @allure.step("Select delivery type: Quick Commerce")
    def select_quick_commerce(self) -> None:
        self.click(self.QUICK_COMMERCE_RADIO)
        self.logger.info("Quick Commerce delivery type is selected")

    @allure.step("Select delivery type: Slotted Delivery")
    def select_slotted_delivery(self) -> None:
        self.click(self.SLOTTED_DELIVERY_RADIO)
        self.logger.info("Selected Slotted Delivery type")

    @allure.step("Select Travel Time tab")
    def select_travel_time_tab(self) -> None:
        self.click(self.TRAVEL_TIME_TAB, timeout=2000)
        self.logger.info("Selected Travel Time tab")

    @allure.step("Select Travel Distance tab")
    def select_travel_distance_tab(self) -> None:
        self.click(self.TRAVEL_DISTANCE_TAB, timeout=2000)
        self.logger.info("Selected Travel Distance tab")

    @allure.step("Select Manual tab")
    def select_manual_tab(self) -> None:
        self.click(self.MANUAL_TAB, timeout=2000)
        self.logger.info("Selected Manual tab")

    @allure.step("Enter travel time: {minutes} minutes")
    def enter_travel_time(self, minutes: int) -> None:
        travel_time_input = self.page.locator(self.TRAVEL_TIME_INPUT)
        travel_time_input.click()
        travel_time_input.fill(str(minutes))
        self.logger.info(f"Entered travel time: {minutes} minutes")

    @allure.step("Enter travel distance: {distance} meters")
    def enter_travel_distance(self, distance: int) -> None:
        travel_distance_input = self.page.locator(self.TRAVEL_DISTANCE_INPUT)
        travel_distance_input.click()
        travel_distance_input.fill(str(distance))
        self.logger.info(f"Entered travel distance: {distance} meters")

    @allure.step("Enter maximum promise time: {minutes} minutes")
    def enter_max_promise_time(self, minutes: int) -> None:
        max_promise_input = self.page.locator(self.MAX_PROMISE_TIME_INPUT)
        max_promise_input.click()
        max_promise_input.fill(str(minutes))
        self.logger.info(f"Entered maximum promise time: {minutes} minutes")

    @allure.step("Enter flat delivery fee: {fee}")
    def enter_flat_delivery_fee(self, fee: int) -> None:
        delivery_fee_input = self.page.locator(self.FLAT_DELIVERY_FEE_INPUT)
        delivery_fee_input.click()
        delivery_fee_input.fill(str(fee))
        self.logger.info(f"Entered flat delivery fee: {fee}")

    @allure.step("Select store type: Grocery")
    def select_grocery_store_type(self) -> None:
        self.click(self.GROCERY_STORE_TYPE)
        self.logger.info("Selected Grocery store type")

    @allure.step("Select store type: Digital")
    def select_digital_store_type(self) -> None:
        self.click(self.DIGITAL_STORE_TYPE)
        self.logger.info("Selected Digital store type")

    @allure.step("Upload CSV file: {file_path}")
    def upload_csv_file(self, file_path: str) -> None:
        self.click(self.UPLOAD_CORDINATES_BUTTON)
        file_input = self.page.locator(self.UPLOAD_CSV_BUTTON)
        file_input.set_input_files(file_path)
        self.logger.info(f"Uploaded CSV file: {file_path}")

    @allure.step("Select manual drawing option")
    def select_manual_drawing(self) -> None:
        self.select_manual_tab()
        self.logger.info("Selected manual drawing option")

    @allure.step("Draw polygon on map using coordinates")
    def draw_polygon_on_map(self) -> None:
        self.page.wait_for_timeout(1000)

        box = self.page.evaluate("""
            () => {
                const iframe = document.querySelector('iframe');
                if (iframe) {
                    const rect = iframe.getBoundingClientRect();
                    return { x: rect.x, y: rect.y, width: rect.width, height: rect.height };
                }
                return null;
            }
        """)

        if box:
            center_x = box['x'] + box['width'] / 2
            center_y = box['y'] + box['height'] / 2

            radius = 50
            points = []
            for i in range(5):
                angle = (2 * math.pi * i) / 5
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))

            if points:
                points.append(points[0])

            for x, y in points:
                self.page.mouse.click(x, y)
                self.page.wait_for_timeout(300)

        self.logger.info("Drew polygon on map using mouse clicks")

    def _get_coordinates_from_csv(self) -> list:
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'testData', 'lat_long_coordinates.csv')

        coordinates = []
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                lat = float(row['latitude'])
                lng = float(row['longitude'])
                coordinates.append((lat, lng))

        return coordinates

    @allure.step("Click Create button")
    def click_create(self) -> None:
        self.click(self.CREATE_BUTTON)
        self.wait_for_load_state('networkidle')
        self.logger.info("Clicked Create button")

    @allure.step("Click Update button")
    def click_update(self) -> None:
        self.click(self.UPDATE_BUTTON)
        self.wait_for_load_state('networkidle')
        self.logger.info("Clicked Update button")

    @allure.step("Create QC polygon with travel time")
    def create_qc_polygon_travel_time(
        self,
        name: str,
        travel_time: int,
        max_promise_time: Optional[int] = None
    ) -> None:

        self.enter_polygon_name(name)
        self.select_quick_commerce()
        self.select_travel_time_tab()
        self.enter_travel_time(travel_time)

        if max_promise_time:
            self.enter_max_promise_time(max_promise_time)

        self.click_create()
        self.logger.info(f"Created QC polygon with travel time: {name}")

    @allure.step("Create Slotted Delivery polygon with travel distance")
    def create_slotted_polygon_travel_distance(
        self,
        name: str,
        travel_distance: int,
        flat_delivery_fee: Optional[int] = None,
        store_type: Optional[str] = None
    ) -> None:

        self.enter_polygon_name(name)
        self.select_slotted_delivery()
        self.select_travel_distance_tab()
        self.enter_travel_distance(travel_distance)

        if flat_delivery_fee:
            self.enter_flat_delivery_fee(flat_delivery_fee)

        if store_type:
            if store_type.lower() == 'grocery':
                self.select_grocery_store_type()
            elif store_type.lower() == 'digital':
                self.select_digital_store_type()

        self.click_create()
        self.logger.info(f"Created Slotted Delivery polygon: {name}")

    @allure.step("Create QC polygon with manual CSV upload")
    def create_qc_polygon_manual_csv(self, name: str, csv_file_path: str) -> None:
        self.enter_polygon_name(name)
        self.select_quick_commerce()
        self.select_manual_tab()
        self.upload_csv_file(csv_file_path)
        self.page.wait_for_timeout(2000)
        self.click_create()
        self.logger.info(f"Created QC polygon with manual CSV: {name}")

    @allure.step("Create Slotted Delivery polygon with manual drawing")
    def create_slotted_polygon_manual_drawing(self, name: str) -> None:
        self.enter_polygon_name(name)
        self.select_slotted_delivery()
        self.select_manual_tab()
        self.draw_polygon_on_map()
        self.click_create()
        self.logger.info(f"Created Slotted Delivery polygon with manual drawing: {name}")

    @allure.step("Edit polygon - change from travel time to travel distance")
    def edit_polygon_change_to_travel_distance(self, travel_distance: int) -> None:
        self.select_travel_distance_tab()
        self.enter_travel_distance(travel_distance)
        self.click_update()
        self.logger.info(f"Edited polygon to travel distance: {travel_distance}")
