"""
Test suite for Barie AI prompt testing using CSV data for Connector 2
"""
import pytest
import csv
import json
import time
from pathlib import Path
from utilities.test_helpers import TestHelpers
from utilities.csv_handler import CSVHandler
from config.config import REPORTS_DIR, DATA_DIR


class TestBariePromptsConnector2:
    """Test class for testing Barie AI with prompts from connector2 CSV"""
    
    @pytest.fixture(scope="function")
    def connector2_prompts(self):
        """Load test prompts from connector2 CSV"""
        csv_file = DATA_DIR / "test_prompts_connector2.csv"
        handler = CSVHandler(csv_file)
        return handler.read_prompts()
    
    def test_all_prompts_from_connector2_csv(self, barie_page, connector2_prompts):
        """Test all prompts from connector2 CSV file"""
        if not connector2_prompts:
            pytest.skip("No prompts found in connector2 CSV file")
        
        results = []
        
        for prompt_data in connector2_prompts:
            if not prompt_data.get('prompt'):
                continue
            
            # Handle quoted prompts
            prompt_text = prompt_data.get('prompt', '').strip()
            if prompt_text.startswith('"""') and prompt_text.endswith('"""'):
                prompt_text = prompt_text[3:-3]
            elif prompt_text.startswith('"') and prompt_text.endswith('"'):
                prompt_text = prompt_text[1:-1]
            
            function_name = prompt_data.get('function_name', 'unknown')
            test_type = prompt_data.get('test_type', 'unknown')
            step = prompt_data.get('step', '')
            prompt_id = prompt_data.get('id', '')
            
            start_time = time.time()
            status = 'passed'
            error_message = ''
            actual_function = None
            function_match = True
            
            try:
                barie_page.send_prompt(prompt_text)
                
                # Get API response from JavaScript interceptor
                api_response = barie_page.get_api_response_from_interceptor()
                
                # Extract actual function name executed
                actual_function = barie_page.extract_executed_function(api_response)
                
                # Validate function name matches expected
                if not actual_function:
                    status = 'failed'
                    function_match = False
                    error_message = f"Could not determine executed function. Expected '{function_name}'"
                elif actual_function != function_name:
                    status = 'failed'
                    function_match = False
                    error_message = f"Function mismatch: Expected '{function_name}', but executed '{actual_function}'"
                
                # Serialize the full JSON response
                response_json = json.dumps(api_response, ensure_ascii=False)
                
                response_time = time.time() - start_time
                
            except Exception as e:
                status = 'failed'
                error_message = str(e)
                response_json = json.dumps({})
                response_time = time.time() - start_time
            
            results.append({
                'step': step,
                'id': prompt_id,
                'function_name': function_name,
                'actual_function': actual_function or 'N/A',
                'function_match': 'PASS' if function_match else 'FAIL',
                'test_type': test_type,
                'prompt': prompt_text,
                'response': response_json,
                'response_time_seconds': round(response_time, 2),
                'status': status,
                'error': error_message
            })
        
        self._save_results_to_csv(results)
    
    def _save_results_to_csv(self, results):
        """Save test results to CSV file"""
        if not results:
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = REPORTS_DIR / f"test_results_connector2_{timestamp}.csv"
        
        fieldnames = ['step', 'id', 'function_name', 'actual_function', 'function_match', 'test_type', 'prompt', 'response', 'response_time_seconds', 'status', 'error']
        
        with open(results_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\nResults saved to: {results_file}")

