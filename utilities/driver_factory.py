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
            options.add_argument("--headless=new")
        
        # Core browser options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        
        # Disable background networking and Google services
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-breakpad")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-component-update")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-domain-reliability")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-prompt-on-repost")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-web-resources")
        options.add_argument("--enable-automation")
        options.add_argument("--enable-features=NetworkService,NetworkServiceLogging")
        options.add_argument("--force-color-profile=srgb")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--mute-audio")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-pings")
        options.add_argument("--password-store=basic")
        options.add_argument("--use-mock-keychain")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        
        # Reduce log verbosity
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Disable Google services
        options.add_argument("--disable-background-downloads")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--disable-preconnect")
        options.add_argument("--disable-remote-fonts")
        options.add_argument("--disable-software-rasterizer")
        
        # Performance logging for network interception
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        # Suppress Chrome service logs
        try:
            service = ChromeService(ChromeDriverManager().install())
            service.log_path = 'NUL'  # Windows null device to suppress logs
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"ChromeDriverManager failed: {e}, trying without service")
            service = None
        
        try:
            if service:
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver = webdriver.Chrome(options=options)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"Chrome driver creation failed: {e}")
            driver = webdriver.Chrome(options=options)
        
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

