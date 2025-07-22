"""Unit tests for configuration management."""

import os
from pathlib import Path
from typing import Dict, Any

import pytest
from pydantic import ValidationError

from config import Config, load_config


class TestConfig:
    """Test cases for Config class."""
    
    def test_config_defaults(self):
        """Test default configuration values."""
        config = Config(openai_api_key="test-key")
        
        assert config.openai_api_key == "test-key"
        assert config.openai_base_url == "https://api.openai.com/v1"
        assert config.openai_model == "gpt-3.5-turbo"
        assert config.max_tokens == 1000
        assert config.temperature == 0.7
        assert config.log_level == "INFO"
        assert config.max_concurrent_requests == 5
        assert config.request_timeout == 30
        assert config.retry_attempts == 3
        assert config.retry_delay == 1.0
        assert config.vocabulary_file == "vocabulary.json"
        assert config.output_dir == "output"
        assert config.supported_formats == ["txt", "pdf", "docx", "md"]
    
    def test_config_custom_values(self):
        """Test configuration with custom values."""
        config = Config(
            openai_api_key="custom-key",
            openai_base_url="https://custom.api.com",
            openai_model="gpt-4",
            max_tokens=2000,
            temperature=0.5,
            log_level="DEBUG",
            max_concurrent_requests=10,
            request_timeout=60,
            retry_attempts=5,
            retry_delay=2.0,
            vocabulary_file="custom_vocab.json",
            output_dir="custom_output",
            supported_formats=["txt", "md"]
        )
        
        assert config.openai_api_key == "custom-key"
        assert config.openai_base_url == "https://custom.api.com"
        assert config.openai_model == "gpt-4"
        assert config.max_tokens == 2000
        assert config.temperature == 0.5
        assert config.log_level == "DEBUG"
        assert config.max_concurrent_requests == 10
        assert config.request_timeout == 60
        assert config.retry_attempts == 5
        assert config.retry_delay == 2.0
        assert config.vocabulary_file == "custom_vocab.json"
        assert config.output_dir == "custom_output"
        assert config.supported_formats == ["txt", "md"]
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test invalid temperature
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", temperature=2.5)
        
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", temperature=-0.5)
        
        # Test invalid max_tokens
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", max_tokens=-100)
        
        # Test invalid max_concurrent_requests
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", max_concurrent_requests=0)
        
        # Test invalid request_timeout
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", request_timeout=0)
        
        # Test invalid retry_attempts
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", retry_attempts=0)
        
        # Test invalid retry_delay
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", retry_delay=0)
    
    def test_config_from_env(self, monkeypatch):
        """Test configuration loading from environment variables."""
        env_vars = {
            "OPENAI_API_KEY": "env-key",
            "OPENAI_BASE_URL": "https://env.api.com",
            "OPENAI_MODEL": "gpt-4",
            "MAX_TOKENS": "1500",
            "TEMPERATURE": "0.6",
            "LOG_LEVEL": "DEBUG",
            "MAX_CONCURRENT_REQUESTS": "8",
            "REQUEST_TIMEOUT": "45",
            "RETRY_ATTEMPTS": "4",
            "RETRY_DELAY": "1.5",
            "VOCABULARY_FILE": "env_vocab.json",
            "OUTPUT_DIR": "env_output",
            "SUPPORTED_FORMATS": "txt,md,html"
        }
        
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)
        
        config = load_config()
        
        assert config.openai_api_key == "env-key"
        assert config.openai_base_url == "https://env.api.com"
        assert config.openai_model == "gpt-4"
        assert config.max_tokens == 1500
        assert config.temperature == 0.6
        assert config.log_level == "DEBUG"
        assert config.max_concurrent_requests == 8
        assert config.request_timeout == 45
        assert config.retry_attempts == 4
        assert config.retry_delay == 1.5
        assert config.vocabulary_file == "env_vocab.json"
        assert config.output_dir == "env_output"
        assert config.supported_formats == ["txt", "md", "html"]
    
    def test_config_from_file(self, tmp_path):
        """Test configuration loading from file."""
        config_file = tmp_path / "test_config.json"
        config_data = {
            "openai_api_key": "file-key",
            "openai_model": "gpt-4",
            "max_tokens": 1200,
            "temperature": 0.8,
            "log_level": "WARNING"
        }
        
        import json
        config_file.write_text(json.dumps(config_data))
        
        config = load_config(str(config_file))
        
        assert config.openai_api_key == "file-key"
        assert config.openai_model == "gpt-4"
        assert config.max_tokens == 1200
        assert config.temperature == 0.8
        assert config.log_level == "WARNING"
    
    def test_config_missing_api_key(self):
        """Test configuration validation with missing API key."""
        with pytest.raises(ValidationError):
            Config(openai_api_key="")
        
        with pytest.raises(ValidationError):
            Config(openai_api_key=None)
    
    def test_config_edge_cases(self):
        """Test configuration edge cases."""
        # Test with empty supported formats
        config = Config(
            openai_api_key="test",
            supported_formats=[]
        )
        assert config.supported_formats == []
        
        # Test with single format
        config = Config(
            openai_api_key="test",
            supported_formats=["txt"]
        )
        assert config.supported_formats == ["txt"]
        
        # Test with duplicate formats (should be handled by pydantic)
        config = Config(
            openai_api_key="test",
            supported_formats=["txt", "txt", "pdf"]
        )
        assert config.supported_formats == ["txt", "pdf"]
    
    def test_config_to_dict(self):
        """Test configuration serialization to dictionary."""
        config = Config(
            openai_api_key="test-key",
            openai_model="gpt-4",
            max_tokens=2000
        )
        
        config_dict = config.model_dump()
        
        assert config_dict["openai_api_key"] == "test-key"
        assert config_dict["openai_model"] == "gpt-4"
        assert config_dict["max_tokens"] == 2000
        assert "supported_formats" in config_dict
    
    def test_config_from_dict(self):
        """Test configuration creation from dictionary."""
        config_dict = {
            "openai_api_key": "dict-key",
            "openai_model": "gpt-4",
            "max_tokens": 1800,
            "temperature": 0.6
        }
        
        config = Config(**config_dict)
        
        assert config.openai_api_key == "dict-key"
        assert config.openai_model == "gpt-4"
        assert config.max_tokens == 1800
        assert config.temperature == 0.6


class TestLoadConfig:
    """Test cases for load_config function."""
    
    def test_load_config_default(self):
        """Test loading configuration with defaults."""
        config = load_config()
        assert isinstance(config, Config)
        assert config.openai_api_key is not None
    
    def test_load_config_with_env_file(self, tmp_path, monkeypatch):
        """Test loading configuration with .env file."""
        env_file = tmp_path / ".env"
        env_content = """
        OPENAI_API_KEY=env-file-key
        OPENAI_MODEL=gpt-4
        MAX_TOKENS=2000
        """
        env_file.write_text(env_content)
        
        monkeypatch.chdir(tmp_path)
        
        config = load_config()
        assert config.openai_api_key == "env-file-key"
        assert config.openai_model == "gpt-4"
        assert config.max_tokens == 2000
    
    def test_load_config_priority(self, tmp_path, monkeypatch):
        """Test configuration priority (env vars override file)."""
        # Create config file
        config_file = tmp_path / "config.json"
        file_config = {
            "openai_api_key": "file-key",
            "openai_model": "gpt-3.5-turbo"
        }
        import json
        config_file.write_text(json.dumps(file_config))
        
        # Set environment variable
        monkeypatch.setenv("OPENAI_API_KEY", "env-key")
        
        config = load_config(str(config_file))
        
        # Environment variable should take precedence
        assert config.openai_api_key == "env-key"
        assert config.openai_model == "gpt-3.5-turbo"
    
    def test_load_config_invalid_file(self, tmp_path):
        """Test loading configuration with invalid file."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("invalid json content")
        
        with pytest.raises(SystemExit):
            load_config(str(invalid_file))
    
    def test_load_config_nonexistent_file(self):
        """Test loading configuration with nonexistent file."""
        config = load_config("nonexistent.json")
        assert isinstance(config, Config)
        # Should fall back to environment variables or defaults


class TestConfigValidation:
    """Additional validation tests."""
    
    @pytest.mark.parametrize("temperature", [0.0, 0.5, 1.0, 2.0])
    def test_valid_temperature_range(self, temperature):
        """Test valid temperature values."""
        config = Config(openai_api_key="test", temperature=temperature)
        assert config.temperature == temperature
    
    @pytest.mark.parametrize("temperature", [-0.1, 2.1, 3.0])
    def test_invalid_temperature_range(self, temperature):
        """Test invalid temperature values."""
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", temperature=temperature)
    
    @pytest.mark.parametrize("max_tokens", [1, 100, 1000, 4000])
    def test_valid_max_tokens(self, max_tokens):
        """Test valid max_tokens values."""
        config = Config(openai_api_key="test", max_tokens=max_tokens)
        assert config.max_tokens == max_tokens
    
    @pytest.mark.parametrize("max_tokens", [0, -1, -100])
    def test_invalid_max_tokens(self, max_tokens):
        """Test invalid max_tokens values."""
        with pytest.raises(ValidationError):
            Config(openai_api_key="test", max_tokens=max_tokens)