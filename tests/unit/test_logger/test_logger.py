"""Unit tests for logging functionality."""

import json
import logging
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import structlog

from logger import setup_logger


class TestLogger:
    """Test cases for logging functionality."""
    
    def test_setup_logger_default(self):
        """Test logger setup with default parameters."""
        logger = setup_logger("test_logger")
        
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
        
        # Check if handlers are properly configured
        assert len(logger.handlers) > 0
    
    def test_setup_logger_custom_level(self):
        """Test logger setup with custom log level."""
        logger = setup_logger("test_logger_debug", "DEBUG")
        
        assert logger.name == "test_logger_debug"
        assert logger.level == logging.DEBUG
    
    def test_setup_logger_warning_level(self):
        """Test logger setup with warning log level."""
        logger = setup_logger("test_logger_warning", "WARNING")
        
        assert logger.name == "test_logger_warning"
        assert logger.level == logging.WARNING
    
    def test_setup_logger_error_level(self):
        """Test logger setup with error log level."""
        logger = setup_logger("test_logger_error", "ERROR")
        
        assert logger.name == "test_logger_error"
        assert logger.level == logging.ERROR
    
    def test_setup_logger_critical_level(self):
        """Test logger setup with critical log level."""
        logger = setup_logger("test_logger_critical", "CRITICAL")
        
        assert logger.name == "test_logger_critical"
        assert logger.level == logging.CRITICAL
    
    def test_setup_logger_invalid_level(self):
        """Test logger setup with invalid log level."""
        logger = setup_logger("test_logger_invalid", "INVALID")
        
        # Should default to INFO for invalid levels
        assert logger.level == logging.INFO
    
    def test_logger_output_to_file(self, tmp_path):
        """Test logger output to file."""
        log_file = tmp_path / "test.log"
        logger = setup_logger("file_logger", "DEBUG", str(log_file))
        
        # Log some messages
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # Check if log file exists and contains messages
        assert log_file.exists()
        log_content = log_file.read_text()
        
        assert "Debug message" in log_content
        assert "Info message" in log_content
        assert "Warning message" in log_content
        assert "Error message" in log_content
    
    def test_logger_json_format(self, tmp_path):
        """Test logger JSON format output."""
        log_file = tmp_path / "test_json.log"
        logger = setup_logger("json_logger", "INFO", str(log_file))
        
        logger.info("Test JSON logging", extra={"custom_field": "custom_value"})
        
        log_content = log_file.read_text()
        lines = log_content.strip().split('\n')
        
        # Parse JSON log entry
        log_entry = json.loads(lines[0])
        
        assert "event" in log_entry
        assert log_entry["event"] == "Test JSON logging"
        assert "custom_field" in log_entry
        assert log_entry["custom_field"] == "custom_value"
    
    def test_logger_structured_output(self, tmp_path):
        """Test structured logging with structlog."""
        log_file = tmp_path / "structured.log"
        logger = setup_logger("structured_logger", "INFO", str(log_file))
        
        # Test with context
        logger.info(
            "Processing article",
            article_title="Test Article",
            word_count=1000,
            processing_time=1.5
        )
        
        log_content = log_file.read_text()
        lines = log_content.strip().split('\n')
        
        # Parse JSON log entry
        log_entry = json.loads(lines[0])
        
        assert log_entry["event"] == "Processing article"
        assert log_entry["article_title"] == "Test Article"
        assert log_entry["word_count"] == 1000
        assert log_entry["processing_time"] == 1.5
    
    def test_logger_exception_handling(self, tmp_path):
        """Test logger exception handling."""
        log_file = tmp_path / "exception.log"
        logger = setup_logger("exception_logger", "ERROR", str(log_file))
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("An error occurred during processing")
        
        log_content = log_file.read_text()
        
        assert "An error occurred during processing" in log_content
        assert "ValueError" in log_content
        assert "Test exception" in log_content
    
    def test_logger_multiple_handlers(self, tmp_path):
        """Test logger with multiple handlers."""
        log_file1 = tmp_path / "log1.log"
        log_file2 = tmp_path / "log2.log"
        
        logger = setup_logger("multi_handler", "INFO", str(log_file1))
        
        # Add second handler
        file_handler = logging.FileHandler(str(log_file2))
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        
        logger.info("Message to both handlers")
        
        assert log_file1.exists()
        assert log_file2.exists()
        
        content1 = log_file1.read_text()
        content2 = log_file2.read_text()
        
        assert "Message to both handlers" in content1
        assert "Message to both handlers" in content2
    
    def test_logger_performance(self, tmp_path):
        """Test logger performance with many messages."""
        log_file = tmp_path / "performance.log"
        logger = setup_logger("perf_logger", "INFO", str(log_file))
        
        # Log many messages
        num_messages = 1000
        for i in range(num_messages):
            logger.info(f"Message {i}")
        
        log_content = log_file.read_text()
        lines = log_content.strip().split('\n')
        
        assert len(lines) >= num_messages
    
    def test_logger_thread_safety(self, tmp_path):
        """Test logger thread safety."""
        import threading
        import time
        
        log_file = tmp_path / "thread_safe.log"
        logger = setup_logger("thread_logger", "INFO", str(log_file))
        
        num_threads = 10
        messages_per_thread = 100
        
        def log_messages(thread_id):
            for i in range(messages_per_thread):
                logger.info(f"Thread {thread_id} message {i}")
        
        threads = []
        for thread_id in range(num_threads):
            thread = threading.Thread(target=log_messages, args=(thread_id,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        log_content = log_file.read_text()
        lines = log_content.strip().split('\n')
        
        # Should have at least num_threads * messages_per_thread messages
        assert len(lines) >= num_threads * messages_per_thread
    
    def test_logger_format_consistency(self, tmp_path):
        """Test logger format consistency."""
        log_file = tmp_path / "format.log"
        logger = setup_logger("format_logger", "INFO", str(log_file))
        
        # Log messages with different types of data
        logger.info("Simple message")
        logger.info("Message with data", data={"key": "value"})
        logger.info("Message with number", count=42)
        logger.info("Message with boolean", flag=True)
        
        log_content = log_file.read_text()
        lines = log_content.strip().split('\n')
        
        # All lines should be valid JSON
        for line in lines:
            if line.strip():
                log_entry = json.loads(line)
                assert "event" in log_entry
                assert "timestamp" in log_entry
    
    def test_logger_level_filtering(self, tmp_path):
        """Test logger level filtering."""
        log_file = tmp_path / "level_filter.log"
        logger = setup_logger("level_logger", "WARNING", str(log_file))
        
        logger.debug("Debug message - should not appear")
        logger.info("Info message - should not appear")
        logger.warning("Warning message - should appear")
        logger.error("Error message - should appear")
        
        log_content = log_file.read_text()
        
        assert "Debug message" not in log_content
        assert "Info message" not in log_content
        assert "Warning message" in log_content
        assert "Error message" in log_content
    
    def test_logger_custom_formatter(self, tmp_path):
        """Test logger with custom formatter."""
        log_file = tmp_path / "custom_format.log"
        
        # Create custom formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        logger = setup_logger("custom_format", "INFO", str(log_file))
        
        # Replace handlers with custom formatter
        for handler in logger.handlers:
            handler.setFormatter(formatter)
        
        logger.info("Test custom format")
        
        log_content = log_file.read_text()
        
        # Should contain timestamp, logger name, level, and message
        assert "custom_format" in log_content
        assert "INFO" in log_content
        assert "Test custom format" in log_content
    
    @patch('structlog.configure')
    def test_structlog_configuration(self, mock_configure):
        """Test structlog configuration."""
        setup_logger("test_structlog")
        
        # Verify structlog was configured
        mock_configure.assert_called_once()
    
    def test_logger_cleanup(self, tmp_path):
        """Test logger cleanup and file closure."""
        log_file = tmp_path / "cleanup.log"
        logger = setup_logger("cleanup_logger", "INFO", str(log_file))
        
        logger.info("Test message")
        
        # Close all handlers
        for handler in logger.handlers:
            handler.close()
        
        # File should be closed and readable
        content = log_file.read_text()
        assert "Test message" in content


class TestLoggerIntegration:
    """Integration tests for logger."""
    
    def test_logger_with_config(self, test_config, tmp_path):
        """Test logger integration with configuration."""
        log_file = tmp_path / "config_integration.log"
        
        # Update config to use test log file
        config = test_config
        config.log_level = "DEBUG"
        
        logger = setup_logger("config_integration", config.log_level, str(log_file))
        
        logger.debug("Debug with config")
        logger.info("Info with config")
        
        log_content = log_file.read_text()
        
        assert "Debug with config" in log_content
        assert "Info with config" in log_content
    
    def test_logger_error_recovery(self, tmp_path):
        """Test logger error recovery."""
        log_file = tmp_path / "error_recovery.log"
        logger = setup_logger("error_recovery", "INFO", str(log_file))
        
        # Simulate logging after file is deleted
        log_file.unlink()
        
        # Should not crash
        logger.info("Message after file deletion")
        
        # File should be recreated
        assert log_file.exists()
        content = log_file.read_text()
        assert "Message after file deletion" in content