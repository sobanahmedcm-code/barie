"""
Base Page class with common functionality for all page objects
"""
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from config.config import EXPLICIT_WAIT, SCREENSHOTS_DIR, SCREENSHOT_ON_FAILURE
from datetime import datetime


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.actions = ActionChains(driver)
    
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
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements with explicit wait"""
        wait_time = timeout or EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        try:
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            self.logger.warning(f"Elements not found: {locator}")
            return []
    
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
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible"""
        try:
            wait_time = timeout or EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_invisible(self, locator, timeout=None):
        """Wait for element to become invisible"""
        wait_time = timeout or EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        try:
            wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            self.logger.warning(f"Element still visible: {locator}")
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from an element"""
        try:
            element = self.find_element(locator, timeout)
            return element.get_attribute(attribute)
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to get attribute from element {locator}: {str(e)}")
            raise
    
    def take_screenshot(self, filename=None):
        """Take a screenshot"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        filepath = SCREENSHOTS_DIR / filename
        self.driver.save_screenshot(str(filepath))
        self.logger.info(f"Screenshot saved: {filepath}")
        return filepath
    
    def scroll_to_element(self, locator):
        """Scroll to an element"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info(f"Scrolled to element: {locator}")
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to scroll to element {locator}: {str(e)}")
            raise
    
    def execute_javascript(self, script, *args):
        """Execute JavaScript code"""
        return self.driver.execute_script(script, *args)
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title

