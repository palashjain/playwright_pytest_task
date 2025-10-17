import pytest
from playwright.sync_api import Page, Browser, BrowserContext, Playwright, sync_playwright
from pathlib import Path
from datetime import datetime
import allure
from utils.config_manager import ConfigManager
from utils.logger import Logger
from utils.helpers import generate_polygon_name
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.store_list_page import StoreListPage
from pages.store_details_page import StoreDetailsPage
from pages.create_polygon_page import CreatePolygonPage


config = ConfigManager()
logger = Logger()

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="function")
def browser(playwright_instance: Playwright) -> Browser:
    logger.info("Launching browser...")
    browser_type = getattr(playwright_instance, config.browser)
    browser = browser_type.launch(
        headless=config.headless,
        slow_mo=config.get_int('APP', 'slow_mo', 100)
    )

    yield browser

    logger.info("Closing browser...")
    browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    logger.info("Creating browser context...")

    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        accept_downloads=True
    )

    context.set_default_timeout(config.timeout)

    yield context

    logger.info("Closing browser context...")
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    logger.info("Creating new page...")
    page = context.new_page()

    yield page

    logger.info("Closing page...")
    page.close()

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture(scope="function")
def home_page(page: Page) -> HomePage:
    return HomePage(page)

@pytest.fixture(scope="function")
def store_list_page(page: Page) -> StoreListPage:
    return StoreListPage(page)

@pytest.fixture(scope="function")
def store_details_page(page: Page) -> StoreDetailsPage:
    return StoreDetailsPage(page)

@pytest.fixture(scope="function")
def create_polygon_page(page: Page) -> CreatePolygonPage:
    return CreatePolygonPage(page)

@pytest.fixture(scope="function", autouse=True)
def test_setup_teardown(request):
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")

    yield

    logger.info(f"Finished test: {test_name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    # Capture screenshot if test failed and we have a page fixture
    if rep.when == "call" and rep.failed and hasattr(item, 'fixturenames') and 'page' in item.fixturenames:
        try:
            logger.error(f"Test failed: {item.name}")

            # Get the page fixture from the item
            page = item._request.getfixturevalue('page')

            screenshot_dir = Path(__file__).parent / 'screenshots'
            screenshot_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = screenshot_dir / f"failure_{item.name}_{timestamp}.png"

            page.screenshot(path=str(screenshot_path))
            allure.attach.file(
                str(screenshot_path),
                name=f"Failure Screenshot - {item.name}",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")

@pytest.fixture(scope="function")
def polygon_names():
    names = {
        'qc_travel_time': generate_polygon_name('qc_polygon'),
        'slotted_delivery': generate_polygon_name('slotted_polygon'),
        'manual_csv': generate_polygon_name('manual_csv_polygon'),
        'manual_drawing': generate_polygon_name('manual_drawing_polygon')
    }

    logger.info(f"Generated polygon names: {names}")
    return names

@pytest.fixture(scope="session")
def test_data_path():
    return config.testdata_path

@pytest.fixture(scope="session")
def downloads_path():
    path = config.downloads_path
    path.mkdir(exist_ok=True)
    return path

def pytest_configure():
    base_path = Path(__file__).parent

    directories = [
        base_path / 'logs',
        base_path / 'screenshots',
        base_path / 'downloads',
        base_path / 'allure-results',
    ]

    for directory in directories:
        directory.mkdir(exist_ok=True)

    logger.info("Pytest configuration completed")
