# Logger API Documentation

The logging system provides structured, configurable logging with async exception handling and decorators.

## Overview

LexiLearn uses a custom logging system built on Python's standard `logging` module with additional features:
- Structured JSON logging
- Async exception handling
- Configurable log levels
- File and console output
- Exception decorators for automatic error logging

## Core Classes

### LexiLearnLogger

**Location**: [`logger.py`](../logger.py:15)

Custom logger class with enhanced functionality.

```python
from logger import LexiLearnLogger

# Create logger
logger = LexiLearnLogger("my_module")
logger.info("Application started")

# With custom level
logger = LexiLearnLogger("my_module", level="DEBUG")
```

### Constructor

```python
def __init__(self, name: str = "lexilearn", level: str = "INFO") -> None:
    """
    Initialize a new logger instance.
    
    Args:
        name: Logger name (usually module name)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
```

## Logging Methods

### Standard Logging Methods

```python
logger.debug("Debug message")
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Exception Logging

```python
try:
    risky_operation()
except Exception as e:
    logger.exception("Operation failed with exception")
```

## Exception Decorators

### log_async_exception

**Location**: [`logger.py`](../logger.py:58)

Decorator for automatic async exception logging.

```python
from logger import log_async_exception

@log_async_exception
async def fetch_data():
    # If this raises an exception, it will be automatically logged
    response = await api_call()
    return response

# Usage
result = await fetch_data()
```

### log_exception

**Location**: [`logger.py`](../logger.py:69)

Decorator for automatic sync exception logging.

```python
from logger import log_exception

@log_exception
def process_data():
    # If this raises an exception, it will be automatically logged
    return expensive_computation()

# Usage
result = process_data()
```

## Configuration

### Basic Configuration

```python
from logger import LexiLearnLogger
from config import Config

# Use with configuration
config = Config()
logger = LexiLearnLogger("my_module", config.logging.level)
```

### Custom Configuration

```python
import logging
from logger import LexiLearnLogger

# Create logger with custom settings
logger = LexiLearnLogger(
    name="custom_module",
    level="DEBUG"
)

# Access underlying logger
underlying_logger = logger.logger
underlying_logger.setLevel(logging.DEBUG)
```

## Log Format

### Standard Format
```
2024-01-15 10:30:45,123 - lexilearn.module - INFO - Processing started
2024-01-15 10:30:45,234 - lexilearn.module - ERROR - API call failed: Connection timeout
```

### JSON Format (Future Enhancement)
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "ERROR",
  "logger": "lexilearn.module",
  "message": "API call failed",
  "error": "Connection timeout",
  "context": {...}
}
```

## Usage Examples

### Basic Usage

```python
from logger import LexiLearnLogger

logger = LexiLearnLogger("text_processor")

def process_text(text: str) -> str:
    logger.info(f"Processing text of length {len(text)}")
    try:
        result = expensive_operation(text)
        logger.info("Text processing completed successfully")
        return result
    except Exception as e:
        logger.error(f"Text processing failed: {e}")
        raise
```

### Async Usage

```python
from logger import LexiLearnLogger, log_async_exception

logger = LexiLearnLogger("translator")

@log_async_exception
async def translate_word(word: str) -> str:
    logger.debug(f"Translating word: {word}")
    translation = await api.translate(word)
    logger.debug(f"Translation completed: {word} -> {translation}")
    return translation
```

### Class-based Usage

```python
from logger import LexiLearnLogger

class TextProcessor:
    def __init__(self):
        self.logger = LexiLearnLogger("text_processor")
    
    def process(self, text: str) -> str:
        self.logger.info("Starting text processing")
        # ... processing logic ...
        self.logger.info("Text processing completed")
```

### Module-level Logger

```python
# In your module
from logger import LexiLearnLogger

logger = LexiLearnLogger(__name__)

def module_function():
    logger.info("Module function called")
```

## Integration with Configuration

```python
from config import Config
from logger import LexiLearnLogger

# Initialize configuration
config = Config()

# Create module logger
logger = LexiLearnLogger(
    "article_processor",
    level=config.logging.level
)

# Use throughout module
logger.info(f"Processing with batch size: {config.processing.batch_size}")
```

## Best Practices

1. **Use module-level loggers** with `__name__`
2. **Log at appropriate levels**:
   - `DEBUG`: Detailed information for debugging
   - `INFO`: General information about operations
   - `WARNING`: Something unexpected happened
   - `ERROR`: An error occurred but operation can continue
   - `CRITICAL`: A serious error occurred
3. **Use exception decorators** for automatic error logging
4. **Include context** in log messages
5. **Avoid logging sensitive information**

## Testing with Logging

```python
import pytest
from logger import LexiLearnLogger
from unittest.mock import patch

def test_logging():
    logger = LexiLearnLogger("test_module")
    
    with patch.object(logger.logger, 'info') as mock_info:
        logger.info("Test message")
        mock_info.assert_called_once_with("Test message")
```

## Performance Considerations

- Loggers are lightweight and can be created per module
- Async decorators add minimal overhead
- Log level filtering happens early to avoid unnecessary processing
- File I/O is buffered for performance