"""
Configuration file for test environment settings
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Test data
CSV_PROMPTS_FILE = DATA_DIR / "test_prompts.csv"

# Browser settings
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

# Application URLs
BASE_URL = os.getenv("BASE_URL", "https://stg.barie.ai")
LOGIN_URL = f"{BASE_URL}/"
CHAT_URL = f"{BASE_URL}/chat"

# Login credentials
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL", "sobanahmed.cm@pf.com.pk")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "10December2025")

# Screenshot settings
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_ON_SUCCESS = False

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create directories if they don't exist
for directory in [DATA_DIR, REPORTS_DIR, LOGS_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

