"""
Helper functions for test execution
"""
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from config.config import REPORTS_DIR


class TestHelpers:
    """Helper class with utility methods for tests"""
    
    @staticmethod
    def wait_with_timeout(condition_func, timeout=30, interval=1):
        """Wait for a condition to be true with timeout"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False
    
    @staticmethod
    def save_test_result(test_name: str, prompt: str, response: str, 
                        status: str, error: str = None, metadata: Dict = None):
        """Save test result to JSON file"""
        result = {
            "test_name": test_name,
            "prompt": prompt,
            "response": response,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "metadata": metadata or {}
        }
        
        result_file = REPORTS_DIR / f"result_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return result_file
    
    @staticmethod
    def validate_response(response: str, expected_keywords: str = None) -> bool:
        """Validate response contains expected keywords"""
        if not expected_keywords:
            return True
        
        keywords = [kw.strip().lower() for kw in expected_keywords.split(',')]
        response_lower = response.lower()
        
        return any(keyword in response_lower for keyword in keywords)
    
    @staticmethod
    def extract_response_metrics(response: str) -> Dict[str, Any]:
        """Extract metrics from response"""
        return {
            "length": len(response),
            "word_count": len(response.split()),
            "has_code": "```" in response or "<code>" in response,
            "has_links": "http" in response or "www." in response,
            "sentence_count": response.count('.') + response.count('!') + response.count('?')
        }

