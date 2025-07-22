"""
Logging configuration and utilities for LexiLearn application.

This module provides structured logging capabilities for the entire application.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from config import config


class LexiLearnLogger:
    """Custom logger class for LexiLearn application."""
    
    def __init__(self, name: str = "lexilearn") -> None:
        """Initialize the logger with configuration."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.logging.level.upper()))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(config.logging.format)
        
        # Console handler
        if config.logging.console_enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # File handler
        if config.logging.file_enabled:
            log_path = Path(config.files.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Use rotating file handler to prevent log files from growing too large
            file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self.logger


# Global logger instance
logger = LexiLearnLogger().get_logger()


def log_async_exception(func):
    """Decorator to log exceptions in async functions."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper


def log_exception(func):
    """Decorator to log exceptions in sync functions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper