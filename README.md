# LexiLearn - English Reading Assistant

A production-ready English reading assistant that provides targeted vocabulary translations to help language learners improve their reading comprehension. Built with a modular, extensible architecture designed for scalability and maintainability.

## 🚀 Features

- **Smart Vocabulary Management**: Tracks known, target, and learned words with persistent storage
- **Contextual Translation**: Uses AI to provide accurate translations based on context
- **Batch Processing**: Efficiently processes large articles with intelligent rate limiting
- **Modular Architecture**: Clean separation of concerns with dedicated modules for each responsibility
- **Configurable**: Comprehensive environment-based configuration for easy deployment
- **Production Ready**: Comprehensive error handling, logging, monitoring, and validation
- **Async/Await**: Modern asynchronous programming for optimal performance
- **Type Safety**: Full type hints and runtime validation

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## 🏗️ Architecture

LexiLearn follows a clean, modular architecture with clear separation of concerns:

```
lexilearn/
├── main.py                 # CLI entry point
├── config.py              # Configuration management (API, processing, files, logging)
├── logger.py              # Structured logging with decorators
├── vocabulary.py          # Vocabulary management (known/target/learned words)
├── text_processor.py      # Text processing (tokenization, normalization, POS tagging)
├── translator.py          # OpenAI API client for translations
├── article_processor.py   # Main processing pipeline orchestration
├── setup_nltk.py          # NLTK data setup
├── validate.py            # Validation script entry point
├── validate_structure.py  # Code quality validation
├── .env.example          # Configuration template
├── requirements.txt      # Dependencies
└── docs/                 # Additional documentation
```

### Core Modules

- **[`config.py`](lexilearn/config.py)**: Centralized configuration management with validation
- **[`logger.py`](lexilearn/logger.py)**: Structured logging with async exception handling
- **[`vocabulary.py`](lexilearn/vocabulary.py)**: Vocabulary state management with file persistence
- **[`text_processor.py`](lexilearn/text_processor.py)**: Advanced text processing utilities
- **[`translator.py`](lexilearn/translator.py)**: OpenAI API integration with rate limiting
- **[`article_processor.py`](lexilearn/article_processor.py)**: Main processing orchestration

## 🚀 Quick Start

### 1. Installation

```bash
# Install LexiLearn package
pip install lexilearn

# Set up NLTK data (required first-time setup)
lexilearn-setup
```

### 2. Configuration

Create a `.env` file with your configuration:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional - customize as needed
API_MODEL=gpt-4o-mini
BATCH_SIZE=10
USE_TARGET_WORDS=true
LOG_LEVEL=INFO
```

### 3. Prepare Your Files

Create the following files in your project directory:

- `input_article.txt` - Your English article
- `known_words.txt` - Words you already know (one per line)
- `target_words.txt` - Words you want to focus on (optional)
- `learned_words.txt` - Words you've learned (auto-updated)

### 4. Run the Application

```bash
# Basic usage
lexilearn

# With custom article
lexilearn --article my_article.txt

# Check help
lexilearn --help
```

## ⚙️ Configuration

LexiLearn uses a comprehensive configuration system with environment variables. See [Configuration Guide](docs/CONFIGURATION.md) for detailed documentation.

### Quick Configuration

```bash
# Core API settings
export OPENAI_API_KEY="sk-..."
export API_MODEL="gpt-4o-mini"

# Processing settings
export BATCH_SIZE=10
export MAX_CONCURRENT_REQUESTS=5
export USE_TARGET_WORDS=true

# File locations
export INPUT_ARTICLE="my_article.txt"
export KNOWN_WORDS_FILE="vocabulary/known.txt"
```

## 📖 Usage

### CLI Usage

```bash
# Basic processing
lexilearn

# Custom article file
lexilearn --article documents/article.txt

# Custom configuration via environment
OPENAI_API_KEY="sk-..." BATCH_SIZE=5 lexilearn

# Debug mode
LOG_LEVEL=DEBUG lexilearn --article test.txt
```

### Programmatic Usage

```python
import asyncio
from lexilearn import LexiLearnApp

async def process_article():
    app = LexiLearnApp()
    await app.run("my_article.txt")

# Run async
asyncio.run(process_article())
```

### Advanced Usage Examples

See [Usage Examples](docs/USAGE_EXAMPLES.md) for comprehensive examples including:
- Custom vocabulary management
- Batch processing multiple articles
- Integration with other applications
- Custom logging configuration

## 📚 API Documentation

Comprehensive API documentation is available for all modules:

- **[Configuration API](docs/API_CONFIG.md)**: Configuration management
- **[Logger API](docs/API_LOGGER.md)**: Logging and monitoring
- **[Vocabulary API](docs/API_VOCABULARY.md)**: Word list management
- **[Text Processor API](docs/API_TEXT_PROCESSOR.md)**: Text processing utilities
- **[Translator API](docs/API_TRANSLATOR.md)**: Translation services
- **[Article Processor API](docs/API_ARTICLE_PROCESSOR.md)**: Main processing pipeline

## 📖 Additional Documentation

- **[Installation Guide](docs/INSTALLATION.md)**: Complete setup instructions
- **[Configuration Guide](docs/CONFIGURATION.md)**: Configuration options
- **[Usage Examples](docs/USAGE_EXAMPLES.md)**: Practical examples
- **[Contributing Guidelines](docs/CONTRIBUTING.md)**: How to contribute
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)**: Common issues
- **[Release Process](docs/RELEASE.md)**: How to release new versions

## 🧪 Development

### Prerequisites

- Python 3.8+
- OpenAI API key
- Git

### Setup Development Environment

```bash
# Clone and setup
git clone <repository-url>
cd lexilearn
python -m venv venv
source venv/bin/activate

# Install development dependencies
make install-dev

# Run setup
lexilearn-setup
```

Alternatively, you can manually install dependencies:

```bash
# Clone and setup
git clone <repository-url>
cd lexilearn
python -m venv venv
source venv/bin/activate
pip install -e .[dev]

# Run setup
lexilearn-setup
```

### Running Tests

Using Makefile (recommended):

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run end-to-end tests only
make test-e2e

# Run tests with coverage
make coverage
```

Manual testing:

```bash
# Run all tests
python -m pytest

# Run specific test
lexilearn-validate

# Run with coverage
python -m pytest --cov=lexilearn
```

### Code Quality

Using Makefile (recommended):

```bash
# Format code
make format

# Lint code
make lint

# Run all code quality checks
make check

# Run security checks
make security
```

Manual code quality:

```bash
# Format code
black .
isort .

# Lint
flake8
pylint lexilearn

# Type checking
mypy .

# Validate structure
lexilearn-validate
```

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Run quality checks: `make check` or `lexilearn-validate`
5. Run tests: `make test`
6. Commit changes: `git commit -am 'Add new feature'`
7. Push to branch: `git push origin feature/new-feature`
8. Create Pull Request

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for detailed information on:
- Code style and standards
- Testing requirements
- Pull request process
- Issue reporting
- Development setup

## 🐛 Troubleshooting

### Common Issues

1. **"Input file not found"**
   - Ensure file exists in the specified location
   - Check file permissions
   - Use absolute paths if necessary

2. **"API key not found"**
   - Set `OPENAI_API_KEY` environment variable
   - Check `.env` file configuration
   - Verify API key validity

3. **"Rate limit exceeded"**
   - Reduce `BATCH_SIZE` and `MAX_CONCURRENT_REQUESTS`
   - Increase `SLEEP_TIME` between batches
   - Check OpenAI account limits

4. **"NLTK data download failed"**
   - Run: `lexilearn-setup`
   - Manual: `python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"`

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
LOG_LEVEL=DEBUG lexilearn --article test.txt
```

### Log Analysis

Check application logs for detailed error information:

```bash
# View recent logs
tail -f lexilearn.log

# Search for errors
grep ERROR lexilearn.log

# Debug specific module
LOG_LEVEL=DEBUG lexilearn 2>&1 | grep -E "(ERROR|DEBUG)"
```

## 📊 Monitoring and Observability

- **Logging**: Structured JSON logging with configurable levels
- **Metrics**: Processing statistics and vocabulary tracking
- **Error Tracking**: Comprehensive exception handling and reporting
- **Performance**: Batch processing metrics and timing information

## 🔒 Security

- API keys stored in environment variables (never commit to git)
- Input validation on all user-provided data
- Secure file handling with proper permissions
- No sensitive data in logs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the translation API
- NLTK team for text processing tools
- Python asyncio community for async best practices

---

**Need help?** Check our [troubleshooting guide](docs/TROUBLESHOOTING.md) or [open an issue](https://github.com/your-repo/lexilearn/issues).
