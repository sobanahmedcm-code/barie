"""
Locators for Barie AI application
Separated from page objects for better maintainability
"""
from selenium.webdriver.common.by import By


class BarieLocators:
    """All locators for Barie AI application pages"""
    
    # Login elements
    EMAIL_FIELD = (By.XPATH, "//*[@id='email-field']")
    CONTINUE_BUTTON = (By.XPATH, "//*[@id='continue-button']")
    PASSWORD_FIELD = (By.XPATH, "//*[@id='password-field']")
    LOGIN_BUTTON = (By.XPATH, "//*[@id='login-button']")
    
    # Chat input elements
    PROMPT_INPUT = (By.ID, "prompt-input")
    PROMPT_TEXTAREA = (By.CSS_SELECTOR, "textarea")
    PROMPT_FIELD = (By.XPATH, "//textarea | //input[@type='text'] | //div[@contenteditable='true']")
    SUBMIT_BUTTON = (By.XPATH, "//*[@id='chat-messages-container']//button[@type='submit']")
    SEND_BUTTON = (By.XPATH, "//button[contains(text(), 'Send') or contains(text(), 'Submit') or contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')]")
    
    # Response elements
    RESPONSE_CONTAINER = (By.ID, "response-container")
    RESPONSE_TEXT = (By.CSS_SELECTOR, ".response-text, .ai-response, [class*='response']")
    RESPONSE_LOADING = (By.CSS_SELECTOR, ".loading, .spinner, [class*='loading']")
    
    # Chat interface
    CHAT_MESSAGES = (By.CSS_SELECTOR, ".message, .chat-message, [class*='message']")
    USER_MESSAGE = (By.CSS_SELECTOR, ".user-message, [class*='user']")
    AI_MESSAGE = (By.CSS_SELECTOR, ".ai-message, [class*='ai'], [class*='assistant']")
    
    # Navigation
    NAVBAR = (By.CSS_SELECTOR, "nav, .navbar, [class*='nav']")
    HOME_LINK = (By.LINK_TEXT, "Home")
    ABOUT_LINK = (By.LINK_TEXT, "About")
    
    # Error handling
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .error-message, [class*='error']")
    ACTIVE_CHAT_ERROR = (By.XPATH, "//*[contains(text(), 'You already have an active chat') or contains(text(), 'Only one chat is allowed')]")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .success-message, [class*='success']")
    
    # Modal/Dialog
    MODAL = (By.CSS_SELECTOR, ".modal, .dialog, [role='dialog']")
    MODAL_CLOSE = (By.CSS_SELECTOR, ".modal-close, button[aria-label='Close']")
    
    # Settings/Configuration
    SETTINGS_BUTTON = (By.CSS_SELECTOR, ".settings, [aria-label*='settings' i]")
    CLEAR_BUTTON = (By.CSS_SELECTOR, "button[aria-label*='clear' i], .clear-button")
    
    # Wait conditions
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "body.loaded, [data-loaded='true']")

