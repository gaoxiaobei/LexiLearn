"""
Configuration management for LexiLearn application.

This module provides centralized configuration management using environment variables
and configuration files for the LexiLearn English reading assistant.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging
from pathlib import Path


@dataclass
class APIConfig:
    """Configuration for API connections."""
    base_url: str = field(default="https://api.openai.com/v1/chat/completions")
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = field(default="gpt-4o-mini")
    max_retries: int = field(default=3)
    timeout: int = field(default=30)
    
    def validate(self) -> None:
        """Validate API configuration."""
        if not self.api_key:
            raise ValueError("API key is required. Set OPENAI_API_KEY environment variable.")
        if not self.base_url:
            raise ValueError("API base URL is required.")


@dataclass
class ProcessingConfig:
    """Configuration for text processing."""
    batch_size: int = field(default=10)
    connector_limit: int = field(default=10)
    sleep_time: float = field(default=0.5)
    use_target_words: bool = field(default=True)
    max_concurrent_requests: int = field(default=5)
    
    def validate(self) -> None:
        """Validate processing configuration."""
        if self.batch_size <= 0:
            raise ValueError("Batch size must be positive")
        if self.connector_limit <= 0:
            raise ValueError("Connector limit must be positive")
        if self.sleep_time < 0:
            raise ValueError("Sleep time must be non-negative")


@dataclass
class FileConfig:
    """Configuration for file paths."""
    input_article: str = field(default="input_article.txt")
    known_words: str = field(default="known_words.txt")
    target_words: str = field(default="target_words.txt")
    learned_words: str = field(default="learned_words.txt")
    output_article: str = field(default="output_article.txt")
    log_file: str = field(default="lexilearn.log")
    
    def validate(self) -> None:
        """Validate file configuration."""
        required_files = [self.input_article, self.known_words]
        for file_path in required_files:
            if not Path(file_path).exists():
                logging.warning(f"Required file not found: {file_path}")


@dataclass
class LoggingConfig:
    """Configuration for logging."""
    level: str = field(default="INFO")
    format: str = field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_enabled: bool = field(default=True)
    console_enabled: bool = field(default=True)
    
    def validate(self) -> None:
        """Validate logging configuration."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.level not in valid_levels:
            raise ValueError(f"Invalid log level: {self.level}")


class Config:
    """Main configuration class for LexiLearn."""
    
    def __init__(self) -> None:
        """Initialize configuration from environment variables and defaults."""
        self.api = APIConfig()
        self.processing = ProcessingConfig()
        self.files = FileConfig()
        self.logging = LoggingConfig()
        
        # Override with environment variables
        self._load_from_env()
        
        # Skip validation for testing purposes
        # self.validate()  # Will be called explicitly when needed
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # API configuration
        self.api.base_url = os.getenv("API_BASE_URL", self.api.base_url)
        self.api.model = os.getenv("API_MODEL", self.api.model)
        self.api.max_retries = int(os.getenv("API_MAX_RETRIES", str(self.api.max_retries)))
        self.api.timeout = int(os.getenv("API_TIMEOUT", str(self.api.timeout)))
        
        # Processing configuration
        self.processing.batch_size = int(os.getenv("BATCH_SIZE", str(self.processing.batch_size)))
        self.processing.connector_limit = int(os.getenv("CONNECTOR_LIMIT", str(self.processing.connector_limit)))
        self.processing.sleep_time = float(os.getenv("SLEEP_TIME", str(self.processing.sleep_time)))
        self.processing.use_target_words = os.getenv("USE_TARGET_WORDS", "true").lower() == "true"
        self.processing.max_concurrent_requests = int(os.getenv("MAX_CONCURRENT_REQUESTS", str(self.processing.max_concurrent_requests)))
        
        # File configuration
        self.files.input_article = os.getenv("INPUT_ARTICLE", self.files.input_article)
        self.files.known_words = os.getenv("KNOWN_WORDS_FILE", self.files.known_words)
        self.files.target_words = os.getenv("TARGET_WORDS_FILE", self.files.target_words)
        self.files.learned_words = os.getenv("LEARNED_WORDS_FILE", self.files.learned_words)
        self.files.output_article = os.getenv("OUTPUT_ARTICLE", self.files.output_article)
        self.files.log_file = os.getenv("LOG_FILE", self.files.log_file)
        
        # Logging configuration
        self.logging.level = os.getenv("LOG_LEVEL", self.logging.level)
        self.logging.file_enabled = os.getenv("LOG_TO_FILE", "true").lower() == "true"
        self.logging.console_enabled = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"
    
    def validate(self) -> None:
        """Validate all configurations."""
        self.api.validate()
        self.processing.validate()
        self.files.validate()
        self.logging.validate()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "api": self.api.__dict__,
            "processing": self.processing.__dict__,
            "files": self.files.__dict__,
            "logging": self.logging.__dict__
        }


# Global configuration instance
config = Config()