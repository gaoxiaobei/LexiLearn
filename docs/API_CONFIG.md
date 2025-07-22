# Configuration API Documentation

The configuration system provides centralized, type-safe configuration management with validation and documentation.

## Overview

LexiLearn uses a hierarchical configuration system with environment variable support. All configuration is validated at startup with helpful error messages.

## Core Classes

### Config

**Location**: [`config.py`](../config.py:86)

Main configuration class that aggregates all configuration sections.

```python
from config import Config

# Initialize configuration
config = Config()

# Access configuration values
print(config.api.api_key)
print(config.processing.batch_size)
```

### APIConfig

**Location**: [`config.py`](../config.py:15)

Configuration for OpenAI API connections.

```python
@dataclass
class APIConfig:
    api_key: str                    # OpenAI API key (required)
    base_url: str = "https://api.openai.com/v1/chat/completions"
    model: str = "gpt-4o-mini"
    max_retries: int = 3
    timeout: int = 30
    
    def validate(self) -> None:
        """Validates API configuration."""
```

**Environment Variables**:
- `OPENAI_API_KEY` (required)
- `API_BASE_URL`
- `API_MODEL`
- `API_MAX_RETRIES`
- `API_TIMEOUT`

### ProcessingConfig

**Location**: [`config.py`](../config.py:32)

Configuration for text processing and batch operations.

```python
@dataclass
class ProcessingConfig:
    batch_size: int = 10           # Sentences per batch
    connector_limit: int = 10      # Max concurrent connections
    sleep_time: float = 0.5        # Delay between batches (seconds)
    use_target_words: bool = True  # Filter by target words
    max_concurrent_requests: int = 5
    
    def validate(self) -> None:
        """Validates processing configuration."""
```

**Environment Variables**:
- `BATCH_SIZE`
- `CONNECTOR_LIMIT`
- `SLEEP_TIME`
- `USE_TARGET_WORDS`
- `MAX_CONCURRENT_REQUESTS`

### FileConfig

**Location**: [`config.py`](../config.py:51)

Configuration for file paths and locations.

```python
@dataclass
class FileConfig:
    input_article: str = "input_article.txt"
    known_words_file: str = "known_words.txt"
    target_words_file: str = "target_words.txt"
    learned_words_file: str = "learned_words.txt"
    output_article: str = "output_article.txt"
    log_file: str = "lexilearn.log"
    
    def validate(self) -> None:
        """Validates file configuration."""
```

**Environment Variables**:
- `INPUT_ARTICLE`
- `KNOWN_WORDS_FILE`
- `TARGET_WORDS_FILE`
- `LEARNED_WORDS_FILE`
- `OUTPUT_ARTICLE`
- `LOG_FILE`

### LoggingConfig

**Location**: [`config.py`](../config.py:69)

Configuration for logging behavior.

```python
@dataclass
class LoggingConfig:
    level: str = "INFO"            # Logging level (DEBUG, INFO, WARNING, ERROR)
    log_to_file: bool = True       # Enable file logging
    log_to_console: bool = True    # Enable console logging
    
    def validate(self) -> None:
        """Validates logging configuration."""
```

**Environment Variables**:
- `LOG_LEVEL`
- `LOG_TO_FILE`
- `LOG_TO_CONSOLE`

## Usage Examples

### Basic Configuration

```python
from config import Config

# Load configuration from environment
config = Config()

# Access configuration
print(f"Using model: {config.api.model}")
print(f"Batch size: {config.processing.batch_size}")
```

### Custom Configuration

```python
import os
from config import Config

# Set environment variables
os.environ['BATCH_SIZE'] = '5'
os.environ['API_MODEL'] = 'gpt-4'

# Load configuration
config = Config()
```

### Configuration Validation

```python
from config import Config, APIConfig

# Manual validation
api_config = APIConfig(
    api_key="your-key",
    model="gpt-4o-mini"
)
api_config.validate()  # Raises ValueError if invalid

# Full configuration validation
config = Config()
config.validate()  # Validates all sections
```

### Configuration as Dictionary

```python
from config import Config

config = Config()
config_dict = config.to_dict()

# Export configuration
import json
print(json.dumps(config_dict, indent=2))
```

## Error Handling

Configuration validation provides detailed error messages:

```python
try:
    config = Config()
    config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    # Example: "Configuration error: OPENAI_API_KEY is required"
```

## Environment Variable Precedence

Configuration is loaded in this order:
1. Environment variables (highest priority)
2. Default values (lowest priority)

## Type Safety

All configuration values are type-checked at runtime:

```python
# This will raise ValueError
os.environ['BATCH_SIZE'] = 'invalid'
config = Config()  # Raises ValueError: BATCH_SIZE must be an integer
```

## Best Practices

1. **Always validate configuration** before use
2. **Use type hints** for configuration access
3. **Document environment variables** in `.env.example`
4. **Handle configuration errors** gracefully
5. **Use configuration sections** for organization

## Integration Example

```python
from config import Config
from logger import LexiLearnLogger

# Initialize configuration
config = Config()
config.validate()

# Use configuration in other modules
logger = LexiLearnLogger("my_module", config.logging.level)