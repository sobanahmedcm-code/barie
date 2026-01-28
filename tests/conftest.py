"""
Pytest configuration and fixtures
"""
import pytest
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from utilities.driver_factory import DriverFactory
from utilities.logger_config import setup_logger
from utilities.csv_handler import CSVHandler
from pages.barie_page import BariePage
from config.config import BASE_URL


@pytest.fixture(scope="session")
def logger():
    """Setup logger for test session"""
    return setup_logger("test_session")


@pytest.fixture(scope="function")
def driver(request):
    """Create WebDriver instance for each test"""
    browser = request.config.getoption("--browser", default=None)
    headless = request.config.getoption("--headless", default=None)
    
    driver = DriverFactory.create_driver(browser, headless)
    driver.maximize_window()
    
    yield driver
    
    if request.node.rep_call.failed:
        # Take screenshot on failure
        screenshot_path = f"screenshot_{request.node.name}_{request.node.rep_call.when}.png"
        driver.save_screenshot(str(screenshot_path))
    
    driver.quit()


@pytest.fixture(scope="function")
def barie_page(driver):
    """Create BariePage instance"""
    page = BariePage(driver)
    page.navigate_to(BASE_URL)
    return page


@pytest.fixture(scope="session")
def csv_handler():
    """Create CSVHandler instance"""
    return CSVHandler()


@pytest.fixture(scope="function")
def test_prompts(csv_handler):
    """Load test prompts from CSV"""
    return csv_handler.read_prompts()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser to use for tests (chrome, firefox, edge)"
    )
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="Run tests in headless mode (true/false)"
    )

