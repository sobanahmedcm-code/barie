"""
WebDriver factory for creating browser instances
"""
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT


class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def create_driver(browser_name=None, headless=None):
        """Create and return a WebDriver instance"""
        browser = browser_name or BROWSER
        is_headless = headless if headless is not None else HEADLESS
        logger = logging.getLogger(__name__)
        
        logger.info(f"Creating {browser} driver (headless={is_headless})")
        
        if browser.lower() == "chrome":
            return DriverFactory._create_chrome_driver(is_headless)
        elif browser.lower() == "firefox":
            return DriverFactory._create_firefox_driver(is_headless)
        elif browser.lower() == "edge":
            return DriverFactory._create_edge_driver(is_headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _create_chrome_driver(headless):
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless):
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        return driver
    
    @staticmethod
    def _create_edge_driver(headless):
        """Create Edge WebDriver"""
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        return driver

