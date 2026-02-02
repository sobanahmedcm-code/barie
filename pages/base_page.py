"""
Base Page class with common functionality for all page objects
"""
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import EXPLICIT_WAIT


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        self.logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """Wait for page to be fully loaded"""
        try:
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            self.logger.warning("Page load timeout exceeded")
    
    def find_element(self, locator, timeout=None):
        """Find a single element with explicit wait"""
        wait_time = timeout or EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """Click on an element"""
        try:
            element = self.find_element(locator, timeout)
            self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to click element {locator}: {str(e)}")
            raise
    
    def send_keys(self, locator, text, clear_first=True):
        """Send keys to an element"""
        try:
            element = self.find_element(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Sent keys to element: {locator}")
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to send keys to element {locator}: {str(e)}")
            raise
    
    def get_text(self, locator, timeout=None):
        """Get text from an element"""
        try:
            element = self.find_element(locator, timeout)
            text = element.text
            self.logger.info(f"Retrieved text from element: {locator}")
            return text
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def is_element_present(self, locator, timeout=None):
        """Check if element is present"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    

