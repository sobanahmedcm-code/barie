"""
Logger configuration for test framework
"""
import logging
import sys
from pathlib import Path
from config.config import LOGS_DIR, LOG_LEVEL, LOG_FORMAT


def setup_logger(name=None, log_file=None):
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name or __name__)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # File handler
    if log_file:
        log_file_path = LOGS_DIR / log_file
    else:
        log_file_path = LOGS_DIR / "test_execution.log"
    
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

