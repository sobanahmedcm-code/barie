"""
Page Object Model for Barie AI main page
"""
import time
from pages.base_page import BasePage
from locators.barie_locators import BarieLocators


class BariePage(BasePage):
    """Page object for Barie AI application"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = BarieLocators()
    
    def is_page_loaded(self):
        """Check if the page is fully loaded"""
        return self.is_element_present(self.locators.PROMPT_INPUT) or \
               self.is_element_present(self.locators.PROMPT_TEXTAREA)
    
    def enter_prompt(self, prompt_text):
        """Enter a prompt into the input field"""
        self.logger.info(f"Entering prompt: {prompt_text[:50]}...")
        
        # Try different input locators
        if self.is_element_present(self.locators.PROMPT_INPUT):
            self.send_keys(self.locators.PROMPT_INPUT, prompt_text)
        elif self.is_element_present(self.locators.PROMPT_TEXTAREA):
            self.send_keys(self.locators.PROMPT_TEXTAREA, prompt_text)
        else:
            raise Exception("Prompt input field not found")
    
    def submit_prompt(self):
        """Submit the prompt"""
        self.logger.info("Submitting prompt")
        
        # Try different submit button locators
        if self.is_element_present(self.locators.SUBMIT_BUTTON):
            self.click_element(self.locators.SUBMIT_BUTTON)
        elif self.is_element_present(self.locators.SEND_BUTTON):
            self.click_element(self.locators.SEND_BUTTON)
        else:
            # Try pressing Enter key
            if self.is_element_present(self.locators.PROMPT_INPUT):
                element = self.find_element(self.locators.PROMPT_INPUT)
                element.send_keys("\n")
            elif self.is_element_present(self.locators.PROMPT_TEXTAREA):
                element = self.find_element(self.locators.PROMPT_TEXTAREA)
                element.send_keys("\n")
    
    def send_prompt(self, prompt_text):
        """Enter and submit a prompt in one action"""
        self.enter_prompt(prompt_text)
        self.submit_prompt()
    
    def wait_for_response(self, timeout=30):
        """Wait for AI response to appear"""
        self.logger.info("Waiting for AI response")
        
        # Wait for loading to disappear
        if self.is_element_present(self.locators.RESPONSE_LOADING):
            self.wait_for_element_invisible(self.locators.RESPONSE_LOADING, timeout)
        
        # Wait for response to appear
        try:
            self.find_element(self.locators.RESPONSE_CONTAINER, timeout)
            return True
        except:
            # Try alternative response locators
            if self.is_element_present(self.locators.AI_MESSAGE, timeout=5):
                return True
            return False
    
    def get_response_text(self):
        """Get the AI response text"""
        self.logger.info("Retrieving response text")
        
        # Try different response locators
        if self.is_element_present(self.locators.RESPONSE_TEXT):
            return self.get_text(self.locators.RESPONSE_TEXT)
        elif self.is_element_present(self.locators.AI_MESSAGE):
            return self.get_text(self.locators.AI_MESSAGE)
        elif self.is_element_present(self.locators.RESPONSE_CONTAINER):
            return self.get_text(self.locators.RESPONSE_CONTAINER)
        else:
            raise Exception("Response text not found")
    
    def is_error_present(self):
        """Check if an error message is present"""
        return self.is_element_present(self.locators.ERROR_MESSAGE, timeout=5)
    
    def get_error_message(self):
        """Get error message if present"""
        if self.is_error_present():
            return self.get_text(self.locators.ERROR_MESSAGE)
        return None
    
    def clear_conversation(self):
        """Clear the conversation"""
        if self.is_element_present(self.locators.CLEAR_BUTTON):
            self.click_element(self.locators.CLEAR_BUTTON)
            self.logger.info("Conversation cleared")
    
    def get_all_messages(self):
        """Get all chat messages"""
        messages = []
        if self.is_element_present(self.locators.CHAT_MESSAGES):
            elements = self.find_elements(self.locators.CHAT_MESSAGES)
            messages = [elem.text for elem in elements]
        return messages
    
    def wait_for_response_complete(self, max_wait_time=60):
        """Wait for response to be complete (no loading indicators)"""
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            if not self.is_element_present(self.locators.RESPONSE_LOADING, timeout=2):
                if self.is_element_present(self.locators.RESPONSE_CONTAINER, timeout=2) or \
                   self.is_element_present(self.locators.AI_MESSAGE, timeout=2):
                    return True
            time.sleep(1)
        return False

