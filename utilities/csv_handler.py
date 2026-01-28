"""
CSV handler for reading test prompts
"""
import csv
import logging
from pathlib import Path
from typing import List, Dict
from config.config import CSV_PROMPTS_FILE


class CSVHandler:
    """Handle CSV file operations for test data"""
    
    def __init__(self, csv_file=None):
        self.csv_file = Path(csv_file) if csv_file else CSV_PROMPTS_FILE
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def read_prompts(self) -> List[Dict[str, str]]:
        """Read all prompts from CSV file"""
        prompts = []
        
        if not self.csv_file.exists():
            self.logger.warning(f"CSV file not found: {self.csv_file}")
            self._create_sample_csv()
            return prompts
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    prompts.append(row)
            self.logger.info(f"Read {len(prompts)} prompts from {self.csv_file}")
        except Exception as e:
            self.logger.error(f"Error reading CSV file: {str(e)}")
            raise
        
        return prompts
    
    def get_prompt_by_id(self, prompt_id: str) -> Dict[str, str]:
        """Get a specific prompt by ID"""
        prompts = self.read_prompts()
        for prompt in prompts:
            if prompt.get('id') == prompt_id or prompt.get('ID') == prompt_id:
                return prompt
        raise ValueError(f"Prompt with ID {prompt_id} not found")
    
    def get_prompts_by_category(self, category: str) -> List[Dict[str, str]]:
        """Get all prompts in a specific category"""
        prompts = self.read_prompts()
        return [p for p in prompts if p.get('category', '').lower() == category.lower()]
    
    def _create_sample_csv(self):
        """Create a sample CSV file if it doesn't exist"""
        sample_data = [
            {
                'id': '1',
                'prompt': 'What is artificial intelligence?',
                'category': 'general',
                'expected_keywords': 'AI, intelligence, machine',
                'description': 'Basic AI question'
            },
            {
                'id': '2',
                'prompt': 'Explain quantum computing',
                'category': 'technical',
                'expected_keywords': 'quantum, computing, qubit',
                'description': 'Technical question about quantum computing'
            },
            {
                'id': '3',
                'prompt': 'Write a Python function to reverse a string',
                'category': 'coding',
                'expected_keywords': 'Python, function, reverse',
                'description': 'Coding request'
            }
        ]
        
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                if sample_data:
                    fieldnames = sample_data[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(sample_data)
            self.logger.info(f"Created sample CSV file: {self.csv_file}")
        except Exception as e:
            self.logger.error(f"Error creating sample CSV file: {str(e)}")
            raise

