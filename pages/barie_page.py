"""
Page Object Model for Barie AI main page
"""
import re
import time
import requests
from pages.base_page import BasePage
from locators.barie_locators import BarieLocators
from config.config import LOGIN_EMAIL, LOGIN_PASSWORD, LOGIN_URL, CHAT_URL
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BariePage(BasePage):
    """Page object for Barie AI application"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = BarieLocators()
        self._network_requests = []
        self._inject_network_interceptor()
        self._inject_network_interceptor()
    
    def login(self):
        """Login to Barie AI"""
        self.navigate_to(LOGIN_URL)
        self._inject_network_interceptor()
        self.send_keys(self.locators.EMAIL_FIELD, LOGIN_EMAIL)
        self.click_element(self.locators.CONTINUE_BUTTON)
        time.sleep(2)
        self.send_keys(self.locators.PASSWORD_FIELD, LOGIN_PASSWORD)
        self.click_element(self.locators.LOGIN_BUTTON)
        self.wait.until(EC.url_contains("/chat"))
        # Re-inject interceptor after page navigation
        self._inject_network_interceptor()
    
    def wait_for_response_complete(self, timeout=60):
        """Wait until response is complete (spinning ends)"""
        from selenium.webdriver.support.ui import WebDriverWait
        
        wait = WebDriverWait(self.driver, timeout)
        
        def is_response_complete(driver):
            try:
                # Check if active chat error is present (should not be)
                error_elements = driver.find_elements(*self.locators.ACTIVE_CHAT_ERROR)
                if error_elements and any(elem.is_displayed() for elem in error_elements):
                    return False
                
                # Check if loading indicator is gone
                loading_elements = driver.find_elements(*self.locators.RESPONSE_LOADING)
                if loading_elements and any(elem.is_displayed() for elem in loading_elements):
                    return False
                
                # Check if textarea is ready and enabled
                textarea_elements = driver.find_elements(*self.locators.PROMPT_TEXTAREA)
                if not textarea_elements:
                    return False
                
                textarea = textarea_elements[0]
                if not (textarea.is_displayed() and textarea.is_enabled()):
                    return False
                
                return True
                
            except:
                return False
        
        wait.until(is_response_complete)
    
    def send_prompt(self, prompt_text):
        """Send a prompt to AI"""
        # Wait for previous response to complete (spinning ends)
        self.wait_for_response_complete()
        
        # Re-inject interceptor to ensure it's active
        self._inject_network_interceptor()
        self._clear_captured_responses()
        
        # Type the prompt
        textarea = self.find_element(self.locators.PROMPT_TEXTAREA, timeout=10)
        textarea.clear()
        textarea.send_keys(prompt_text)
        
        # Button enables after typing, so click it
        self.click_element(self.locators.SUBMIT_BUTTON)
        
        # Wait for AI message to appear
        self.wait.until(EC.presence_of_element_located(self.locators.AI_MESSAGE))
        
        # Wait a bit for network requests to complete
        time.sleep(3)
    
    def _inject_network_interceptor(self):
        """Inject JavaScript to intercept fetch/XHR requests"""
        script = """
        window.capturedResponses = [];
        
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            return originalFetch.apply(this, args).then(response => {
                const clonedResponse = response.clone();
                clonedResponse.json().then(data => {
                    window.capturedResponses.push({
                        url: response.url,
                        status: response.status,
                        statusText: response.statusText,
                        type: 'fetch',
                        data: data,
                        timestamp: new Date().toISOString()
                    });
                }).catch(() => {
                    clonedResponse.text().then(text => {
                        window.capturedResponses.push({
                            url: response.url,
                            status: response.status,
                            statusText: response.statusText,
                            type: 'fetch',
                            data: text,
                            timestamp: new Date().toISOString()
                        });
                    }).catch(() => {});
                });
                return response;
            });
        };
        
        const originalXHROpen = XMLHttpRequest.prototype.open;
        const originalXHRSend = XMLHttpRequest.prototype.send;
        
        XMLHttpRequest.prototype.open = function(method, url) {
            this._url = url;
            this._method = method;
            return originalXHROpen.apply(this, arguments);
        };
        
        XMLHttpRequest.prototype.send = function() {
            this.addEventListener('load', function() {
                try {
                    const data = JSON.parse(this.responseText);
                    window.capturedResponses.push({
                        url: this._url,
                        method: this._method,
                        status: this.status,
                        statusText: this.statusText,
                        type: 'xhr',
                        data: data,
                        timestamp: new Date().toISOString()
                    });
                } catch (e) {
                    window.capturedResponses.push({
                        url: this._url,
                        method: this._method,
                        status: this.status,
                        statusText: this.statusText,
                        type: 'xhr',
                        data: this.responseText,
                        timestamp: new Date().toISOString()
                    });
                }
            });
            return originalXHRSend.apply(this, arguments);
        };
        """
        try:
            self.driver.execute_script(script)
        except:
            pass
    
    def _clear_captured_responses(self):
        """Clear captured responses"""
        try:
            self.driver.execute_script("window.capturedResponses = [];")
        except:
            pass
    
    def _get_captured_responses(self):
        """Get captured network responses"""
        try:
            responses = self.driver.execute_script("return window.capturedResponses || [];")
            return responses
        except:
            return []
    
    def get_api_response_from_interceptor(self, timeout=30):
        """Get API response from JavaScript interceptor for /api/chats/ requests"""
        start_time = time.time()
        chat_id_pattern = re.compile(r'/api/chats/([a-f0-9]{24})')
        
        while time.time() - start_time < timeout:
            captured = self._get_captured_responses()
            
            for cap in captured:
                url = cap.get('url', '')
                if '/api/chats/' in url:
                    match = chat_id_pattern.search(url)
                    if match:
                        data = cap.get('data', {})
                        if data:
                            if isinstance(data, str):
                                try:
                                    import json as json_module
                                    return json_module.loads(data)
                                except:
                                    return {"raw_response": data}
                            return data
            
            time.sleep(0.5)
        
        raise TimeoutException("API response not found in captured network requests")
    
    def get_response_text(self):
        """Get AI response text"""
        return self.get_text(self.locators.AI_MESSAGE)
    
    def extract_executed_function(self, api_response):
        """Extract the actual function name executed from the API response"""
        import re
        
        if not api_response or not isinstance(api_response, dict):
            return None
        
        # Look for function calls in the conversation logs
        data = api_response.get('data', {})
        conversation = data.get('conversation', [])
        
        # Pattern to match function calls like: barie_mcp_cli tool call mcp_RC_*
        # Also matches patterns like: tool call mcp_RC_* or mcp_RC_* in various formats
        function_patterns = [
            re.compile(r'tool call\s+([a-zA-Z0-9_]+)'),
            re.compile(r'barie_mcp_cli\s+tool\s+call\s+([a-zA-Z0-9_]+)'),
            re.compile(r'mcp_[A-Z0-9_]+', re.IGNORECASE)
        ]
        
        found_functions = []
        
        for conv_item in conversation:
            logs = conv_item.get('logs', [])
            for log in logs:
                # Check barie_computer_logs for tool call commands
                if log.get('type') == 'barie_computer_logs':
                    log_data = log.get('log', {})
                    if isinstance(log_data, dict):
                        content = log_data.get('content', '')
                        if content:
                            # Try all patterns
                            for pattern in function_patterns:
                                matches = pattern.findall(content)
                                if matches:
                                    # Filter to get actual function names (starting with mcp_)
                                    for match in matches:
                                        if isinstance(match, tuple):
                                            match = match[0] if match else None
                                        if match and match.startswith('mcp_'):
                                            found_functions.append(match)
                
                # Check processing_logs for tool call commands
                if log.get('type') == 'processing_logs':
                    log_data = log.get('log', {})
                    if isinstance(log_data, dict):
                        result = log_data.get('result', '')
                        if result:
                            for pattern in function_patterns:
                                matches = pattern.findall(result)
                                if matches:
                                    for match in matches:
                                        if isinstance(match, tuple):
                                            match = match[0] if match else None
                                        if match and match.startswith('mcp_'):
                                            found_functions.append(match)
        
        # Return the first unique function found, or None if none found
        if found_functions:
            # Return the most recent/last function call (usually the one we care about)
            return found_functions[-1]
        
        return None

