"""
Test suite for Barie AI prompt testing using CSV data
"""
import pytest
import logging
from utilities.test_helpers import TestHelpers
from config.config import BASE_URL


class TestBariePrompts:
    """Test class for testing Barie AI with prompts from CSV"""
    
    @pytest.fixture(autouse=True)
    def setup(self, barie_page, logger):
        """Setup for each test"""
        self.page = barie_page
        self.logger = logger
        self.helpers = TestHelpers()
    
    @pytest.mark.parametrize("prompt_data", [])
    def test_prompt_from_csv(self, prompt_data, request):
        """Test individual prompt from CSV file"""
        # This will be populated dynamically
        pass
    
    def test_single_prompt(self, barie_page, test_prompts):
        """Test a single prompt from CSV"""
        if not test_prompts:
            pytest.skip("No prompts found in CSV file")
        
        prompt_data = test_prompts[0]
        prompt_text = prompt_data.get('prompt', '')
        expected_keywords = prompt_data.get('expected_keywords', '')
        test_id = prompt_data.get('id', 'unknown')
        
        self.logger.info(f"Testing prompt ID: {test_id}")
        self.logger.info(f"Prompt: {prompt_text}")
        
        try:
            # Send prompt
            barie_page.send_prompt(prompt_text)
            
            # Wait for response
            assert barie_page.wait_for_response(), "Response not received"
            
            # Get response
            response = barie_page.get_response_text()
            self.logger.info(f"Response received: {response[:100]}...")
            
            # Validate response
            assert len(response) > 0, "Response is empty"
            
            if expected_keywords:
                assert self.helpers.validate_response(response, expected_keywords), \
                    f"Response does not contain expected keywords: {expected_keywords}"
            
            # Extract metrics
            metrics = self.helpers.extract_response_metrics(response)
            self.logger.info(f"Response metrics: {metrics}")
            
            # Save result
            self.helpers.save_test_result(
                test_name=f"test_prompt_{test_id}",
                prompt=prompt_text,
                response=response,
                status="passed",
                metadata={"metrics": metrics, "prompt_id": test_id}
            )
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            self.helpers.save_test_result(
                test_name=f"test_prompt_{test_id}",
                prompt=prompt_text,
                response="",
                status="failed",
                error=str(e),
                metadata={"prompt_id": test_id}
            )
            raise
    
    def test_all_prompts_from_csv(self, barie_page, test_prompts):
        """Test all prompts from CSV file"""
        if not test_prompts:
            pytest.skip("No prompts found in CSV file")
        
        results = []
        
        for prompt_data in test_prompts:
            prompt_text = prompt_data.get('prompt', '')
            expected_keywords = prompt_data.get('expected_keywords', '')
            test_id = prompt_data.get('id', 'unknown')
            category = prompt_data.get('category', 'unknown')
            
            self.logger.info(f"Testing prompt ID: {test_id}, Category: {category}")
            
            try:
                # Clear previous conversation if needed
                barie_page.clear_conversation()
                
                # Send prompt
                barie_page.send_prompt(prompt_text)
                
                # Wait for response
                if not barie_page.wait_for_response():
                    raise Exception("Response timeout")
                
                # Get response
                response = barie_page.get_response_text()
                
                # Validate
                assert len(response) > 0, "Response is empty"
                
                validation_passed = True
                if expected_keywords:
                    validation_passed = self.helpers.validate_response(response, expected_keywords)
                
                # Extract metrics
                metrics = self.helpers.extract_response_metrics(response)
                
                result = {
                    "prompt_id": test_id,
                    "category": category,
                    "status": "passed" if validation_passed else "failed_validation",
                    "response_length": len(response),
                    "metrics": metrics
                }
                
                results.append(result)
                
                self.logger.info(f"Prompt {test_id}: {'PASSED' if validation_passed else 'FAILED VALIDATION'}")
                
            except Exception as e:
                self.logger.error(f"Prompt {test_id} failed: {str(e)}")
                results.append({
                    "prompt_id": test_id,
                    "category": category,
                    "status": "failed",
                    "error": str(e)
                })
        
        # Summary
        passed = sum(1 for r in results if r.get("status") == "passed")
        failed = len(results) - passed
        
        self.logger.info(f"Test Summary: {passed} passed, {failed} failed out of {len(results)} prompts")
        
        assert failed == 0, f"{failed} prompts failed out of {len(results)}"
    
    def test_prompt_by_category(self, barie_page, csv_handler):
        """Test prompts filtered by category"""
        category = "general"
        prompts = csv_handler.get_prompts_by_category(category)
        
        if not prompts:
            pytest.skip(f"No prompts found for category: {category}")
        
        for prompt_data in prompts:
            prompt_text = prompt_data.get('prompt', '')
            test_id = prompt_data.get('id', 'unknown')
            
            self.logger.info(f"Testing category '{category}' prompt ID: {test_id}")
            
            barie_page.send_prompt(prompt_text)
            assert barie_page.wait_for_response(), "Response not received"
            
            response = barie_page.get_response_text()
            assert len(response) > 0, "Response is empty"

