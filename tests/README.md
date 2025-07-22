# LexiLearn Testing Guide

This directory contains comprehensive tests for the LexiLearn application, including unit tests, integration tests, and end-to-end tests.

## 📁 Directory Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_config/        # Configuration management tests
│   ├── test_logger/        # Logging functionality tests
│   ├── test_vocabulary/    # Vocabulary management tests
│   ├── test_text_processor/ # Text processing tests
│   ├── test_translator/    # Translation service tests
│   └── test_article_processor/ # Article processing tests
├── integration/            # Integration tests
│   └── test_end_to_end.py  # End-to-end workflow tests
├── e2e/                   # End-to-end tests
├── fixtures/              # Test data and fixtures
│   └── test_data.py       # Sample data for testing
├── mocks/                 # Mock objects and utilities
│   └── mock_openai.py     # OpenAI API mocking
├── data/                  # Sample files for testing
├── conftest.py            # Pytest configuration and fixtures
└── README.md             # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install testing dependencies
pip install -r requirements-test.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run tests with coverage
pytest --cov=lexilearn --cov-report=html --cov-report=term

# Run tests in parallel
pytest -n auto

# Run specific test file
pytest tests/unit/test_config/test_config.py

# Run tests with specific marker
pytest -m "not slow"
```

## 🧪 Test Categories

### Unit Tests
- **Config Tests**: Configuration loading, validation, and environment variable handling
- **Logger Tests**: Logging setup, formatting, file output, and error handling
- **Vocabulary Tests**: Vocabulary item creation, CRUD operations, and persistence
- **Text Processor Tests**: Text extraction, cleaning, analysis, and format handling
- **Translator Tests**: API integration, error handling, and response parsing
- **Article Processor Tests**: Article processing workflow and batch operations

### Integration Tests
- **End-to-End Tests**: Complete workflow from article input to vocabulary output
- **Configuration Integration**: Environment variable and file-based configuration
- **Vocabulary Persistence**: Cross-session vocabulary management
- **Error Recovery**: Handling API failures and network issues

### Performance Tests
- **Large File Processing**: Handling of large articles and batch processing
- **Concurrent Requests**: Multiple simultaneous API calls
- **Memory Usage**: Resource consumption during processing

## 🎯 Test Markers

Use markers to run specific test categories:

```bash
# Run unit tests
pytest -m unit

# Run integration tests
pytest -m integration

# Run slow tests
pytest -m slow

# Run performance tests
pytest -m performance

# Run smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression
```

## 🔧 Configuration

### Environment Variables
Set these environment variables for testing:

```bash
export OPENAI_API_KEY=test-key
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_MODEL=gpt-3.5-turbo
export LOG_LEVEL=DEBUG
```

### Test Configuration
Tests use a separate configuration that can be customized:

```python
# In conftest.py or test files
@pytest.fixture
def test_config():
    return Config(
        openai_api_key="test-key",
        openai_model="gpt-3.5-turbo",
        log_level="DEBUG"
    )
```

## 🎭 Mocking and Fixtures

### API Mocking
Tests use `aioresponses` to mock OpenAI API calls:

```python
with aioresponses() as mocked:
    mocked.post("https://api.openai.com/v1/chat/completions", status=200, payload=response)
    # Your test code here
```

### Test Fixtures
Common fixtures available in `conftest.py`:

- `test_config`: Test configuration
- `test_logger`: Test logger instance
- `temp_dir`: Temporary directory for file operations
- `sample_text`: Sample English text
- `sample_vocabulary_data`: Sample vocabulary entries
- `mock_openai_response`: Mock API responses

## 📊 Coverage Reports

Generate detailed coverage reports:

```bash
# HTML coverage report
pytest --cov=lexilearn --cov-report=html
# Open htmlcov/index.html in browser

# XML coverage report (for CI)
pytest --cov=lexilearn --cov-report=xml

# Terminal coverage report
pytest --cov=lexilearn --cov-report=term-missing
```

## 🐛 Debugging Tests

### Verbose Output
```bash
pytest -v  # Verbose output
pytest -s  # Show print statements
pytest -l  # Show local variables in tracebacks
```

### Debugging Specific Tests
```bash
# Run specific test with debugging
pytest tests/unit/test_translator/test_translator.py::TestOpenAITranslator::test_translate_text_success -v -s

# Run with pdb on failure
pytest --pdb
```

## 🔄 Continuous Integration

Tests run automatically on:
- Every push to main/develop branches
- Every pull request
- Daily scheduled runs
- Tagged releases

### CI Features
- Multi-platform testing (Ubuntu, Windows, macOS)
- Multi-Python version testing (3.8-3.12)
- Security scanning with bandit
- Performance benchmarking
- Coverage reporting to Codecov

## 📈 Performance Testing

### Benchmark Tests
```bash
# Run performance benchmarks
pytest tests/ -m performance --benchmark-only

# Compare performance
pytest tests/ -m performance --benchmark-compare
```

### Memory Profiling
```bash
# Install memory profiler
pip install memory-profiler

# Run with memory profiling
mprof run pytest tests/integration/
mprof plot
```

## 🚨 Common Issues and Solutions

### NLTK Data Missing
```bash
# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### Async Test Issues
```bash
# Ensure pytest-asyncio is installed
pip install pytest-asyncio

# Run with asyncio support
pytest --asyncio-mode=auto
```

### Coverage Not Working
```bash
# Install coverage
pip install pytest-cov

# Run with coverage
pytest --cov=lexilearn
```

## 📝 Writing New Tests

### Test Structure
```python
# tests/unit/test_new_feature/test_new_feature.py
import pytest
from new_feature import NewFeature

class TestNewFeature:
    def test_basic_functionality(self):
        """Test basic functionality."""
        feature = NewFeature()
        result = feature.do_something()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_functionality(self):
        """Test async functionality."""
        feature = NewFeature()
        result = await feature.do_something_async()
        assert result is not None
    
    @pytest.mark.parametrize("input,expected", [
        ("test1", "result1"),
        ("test2", "result2"),
    ])
    def test_parameterized(self, input, expected):
        """Test with multiple parameters."""
        feature = NewFeature()
        result = feature.process(input)
        assert result == expected
```

### Adding Fixtures
Add new fixtures to `conftest.py`:

```python
@pytest.fixture
def new_fixture():
    """Description of the fixture."""
    return NewFixture()
```

## 🎯 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Mock External Services**: Use mocks for API calls
3. **Use Fixtures**: Leverage fixtures for setup/teardown
4. **Descriptive Names**: Use clear, descriptive test names
5. **Edge Cases**: Test boundary conditions and error cases
6. **Performance**: Include performance tests for critical paths
7. **Documentation**: Document complex test scenarios

## 📞 Support

For test-related issues:
1. Check the troubleshooting section above
2. Review existing test files for examples
3. Open an issue with the `testing` label
4. Include test output and environment details