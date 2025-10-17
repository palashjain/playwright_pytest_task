from pathlib import Path

import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.store_list_page import StoreListPage
from pages.store_details_page import StoreDetailsPage
from pages.create_polygon_page import CreatePolygonPage
from utils.logger import Logger
from utils.config_manager import ConfigManager


logger = Logger()
config = ConfigManager()


@allure.feature("Polygon Management")
@allure.story("Complete Polygon Management Workflow")
@pytest.mark.smoke
class TestPolygonManagement:


    qc_polygon_name = None
    slotted_polygon_name = None
    manual_csv_polygon_name = None
    manual_drawing_polygon_name = None

    @allure.title("Complete Polygon Management E2E Test")
    @allure.description("""
        End-to-end test covering:
        1. Login
        2. Navigate to Stores
        3. Click on first store
        4. Create multiple polygons with different types
        5. Validate polygon creation
        6. Export Store data
        7. Set store as inactive
        8. Set store as active again
        9. Edit polygon
        10. Set polygon as inactive
        11. Logout
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_polygon_management_workflow(
        self,
        login_page: LoginPage,
        home_page: HomePage,
        store_list_page: StoreListPage,
        store_details_page: StoreDetailsPage,
        create_polygon_page: CreatePolygonPage,
        polygon_names: dict,
        test_data_path: Path
    ):

        TestPolygonManagement.qc_polygon_name = polygon_names['qc_travel_time']
        TestPolygonManagement.slotted_polygon_name = polygon_names['slotted_delivery']
        TestPolygonManagement.manual_csv_polygon_name = polygon_names['manual_csv']
        TestPolygonManagement.manual_drawing_polygon_name = polygon_names['manual_drawing']

        with allure.step("Step 1: Login with credentials"):
            logger.info("Step 1: Performing login")
            login_page.navigate_to_login()
            login_page.login(config.username, config.password)
            logger.info("Waiting for login redirect...")

        with allure.step("Step 2: Navigate to Stores"):
            logger.info("Step 2: Navigating to Stores")
            home_page.navigate_to_stores()
            assert store_list_page.is_stores_page_displayed(), "Stores page not displayed"
            logger.info("Navigated to Stores successfully")

        with allure.step("Step 3: Click on first Active store"):
            logger.info("Step 3: Clicking on first active store")
            first_active_store = store_list_page.click_first_active_store()
            assert store_details_page.is_store_details_page_displayed(), "Store details page not displayed"
            logger.info(f"{first_active_store} details page opened")

        with allure.step("Step 4: Click on Create Polygon button"):
            logger.info("Step 4: Clicking Create Polygon button")
            store_details_page.click_create_polygon()
            assert create_polygon_page.is_create_polygon_page_displayed(), "Create polygon page not displayed"
            logger.info("Create Polygon page opened")

        with allure.step("Step 5: Create QC polygon with Travel Time (18 mins)"):
            logger.info(f"Step 5: Creating QC polygon with travel time: {TestPolygonManagement.qc_polygon_name}")
            create_polygon_page.create_qc_polygon_travel_time(
                name=TestPolygonManagement.qc_polygon_name,
                travel_time=18,
                max_promise_time=15
            )
            logger.info("QC polygon created with travel time")

        with allure.step("Step 6: Validate QC polygon is added to the list"):
            logger.info("Step 6: Validating QC polygon in list")
            store_details_page.search_polygon(TestPolygonManagement.qc_polygon_name)

            assert store_details_page.is_polygon_visible(TestPolygonManagement.qc_polygon_name), \
                f"QC polygon '{TestPolygonManagement.qc_polygon_name}' not found in list"

            logger.info("QC polygon validated successfully")
            store_details_page.search_polygon("")

        with allure.step("Step 7: Create Slotted Delivery polygon with Travel Distance"):
            logger.info("Step 7: Creating Slotted Delivery polygon")
            store_details_page.click_create_polygon()

            create_polygon_page.create_slotted_polygon_travel_distance(
                name=TestPolygonManagement.slotted_polygon_name,
                travel_distance=5000,
                flat_delivery_fee=35,
                store_type='grocery'
            )
            logger.info("Slotted Delivery polygon created")

        with allure.step("Step 8: Validate Slotted Delivery polygon is added"):
            logger.info("Step 8: Validating Slotted Delivery polygon")
            store_details_page.search_polygon(TestPolygonManagement.slotted_polygon_name)

            assert store_details_page.is_polygon_visible(TestPolygonManagement.slotted_polygon_name), \
                f"Slotted polygon '{TestPolygonManagement.slotted_polygon_name}' not found in list"

            logger.info("Slotted Delivery polygon validated successfully")
            store_details_page.search_polygon("")

        with allure.step("Step 9: Create QC polygon with Manual CSV upload"):
            logger.info("Step 9: Creating QC polygon with manual CSV upload")

            store_details_page.click_create_polygon()

            csv_file_path = test_data_path / 'lat_long_coordinates.csv'

            create_polygon_page.create_qc_polygon_manual_csv(
                name=TestPolygonManagement.manual_csv_polygon_name,
                csv_file_path=str(csv_file_path)
            )
            logger.info("QC polygon with manual CSV created")

        with allure.step("Step 10: Validate Manual CSV polygon is added"):
            logger.info("Step 10: Validating Manual CSV polygon")
            store_details_page.search_polygon(TestPolygonManagement.manual_csv_polygon_name)

            assert store_details_page.is_polygon_visible(TestPolygonManagement.manual_csv_polygon_name), \
                f"Manual CSV polygon '{TestPolygonManagement.manual_csv_polygon_name}' not found in list"

            logger.info("Manual CSV polygon validated successfully")

            store_details_page.search_polygon("")

        with allure.step("Step 11: Create Slotted Delivery polygon with Manual Drawing"):
            logger.info("Step 11: Creating Slotted Delivery polygon with manual drawing")

            store_details_page.click_create_polygon()

            create_polygon_page.create_slotted_polygon_manual_drawing(
                name=TestPolygonManagement.manual_drawing_polygon_name
            )
            logger.info("Slotted Delivery polygon with manual drawing created")

        with allure.step("Step 12: Validate Manual Drawing polygon is added"):
            logger.info("Step 12: Validating Manual Drawing polygon")

            store_details_page.search_polygon(TestPolygonManagement.manual_drawing_polygon_name)

            assert store_details_page.is_polygon_visible(TestPolygonManagement.manual_drawing_polygon_name), \
                f"Manual Drawing polygon '{TestPolygonManagement.manual_drawing_polygon_name}' not found in list"

            logger.info("Manual Drawing polygon validated successfully")
            store_details_page.search_polygon("")

        with allure.step("Step 13: Click on 3 dots menu, Export Data and validate file is not empty"):
            logger.info("Step 13: Clicking 3 dots menu for Export Data and validate file is not empty")

            store_details_page.click_three_dots_menu()
            store_details_page.click_export_data_download_file()
            logger.info("Downloaded Store Serviceability Data")

        with allure.step("Step 14: Set store as Inactive"):
            logger.info("Step 14: Setting store as inactive")

            store_details_page.click_three_dots_menu()
            store_details_page.click_set_as_inactive()
            logger.info("Set store as inactive")

        with allure.step("Step 15: Validate store is Inactive"):
            logger.info("Step 15: Validating store inactive status")

            assert store_details_page.verify_store_status("Inactive"), \
                "Store status is not Inactive"

            logger.info("Store inactive status validated")

        with allure.step("Step 16: Set store as active"):
            logger.info("Step 16: Setting store as active")

            store_details_page.click_three_dots_menu()
            store_details_page.click_set_as_active()
            logger.info("Set store as active")

        with allure.step("Step 17: Validate store is active"):
            logger.info("Step 17: Validating store active status")

            assert store_details_page.verify_store_status("Active"), \
                "Store status is not active"

            logger.info("Store active status validated")

        with allure.step("Step 18: Edit QC polygon - change to Travel Distance"):
            logger.info("Step 18: Editing QC polygon to change to travel distance")
            store_details_page.search_polygon(TestPolygonManagement.qc_polygon_name)
            store_details_page.click_edit_polygon(TestPolygonManagement.qc_polygon_name)

            create_polygon_page.edit_polygon_change_to_travel_distance(200)
            logger.info("QC polygon edited to travel distance")

        with allure.step("Step 19: Validate edited polygon travel distance"):
            logger.info("Step 19: Validating edited polygon travel distance")

            store_details_page.search_polygon(TestPolygonManagement.qc_polygon_name)

            assert store_details_page.verify_polygon_travel_distance(TestPolygonManagement.qc_polygon_name, "Travel Distance: 200 metres"), \
                f"Polygon '{TestPolygonManagement.qc_polygon_name}' does not show 'Travel Distance: 200 metres'"

            logger.info("Edited polygon travel distance validated successfully")

        with allure.step("Step 20: Set QC polygon as Inactive"):
            logger.info("Step 20: Setting QC polygon as inactive")
            store_details_page.set_polygon_inactive(TestPolygonManagement.qc_polygon_name)
            logger.info("QC polygon set as inactive")

        with allure.step("Step 21: Validate QC polygon is Inactive"):
            logger.info("Step 21: Validating QC polygon inactive status")
            store_details_page.search_polygon(TestPolygonManagement.qc_polygon_name)

            assert store_details_page.verify_polygon_status(
                TestPolygonManagement.qc_polygon_name, "Inactive"
            ), f"QC polygon '{TestPolygonManagement.qc_polygon_name}' is not Inactive"

            logger.info("QC polygon inactive status validated")

        with allure.step("Step 22: Logout from application"):
            logger.info("Step 22: Logging out")

            home_page.logout()
            assert login_page.is_login_page_displayed(), "Logout failed - Login page not displayed"
            logger.info("Logout successful")

        logger.info("Complete polygon management workflow test completed successfully")
