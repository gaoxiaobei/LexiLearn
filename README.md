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
├── setup.py               # NLTK data setup
├── test_setup.py          # Testing utilities
├── validate_structure.py  # Code quality validation
├── .env.example          # Configuration template
├── requirements.txt      # Dependencies
└── docs/                 # Additional documentation
```

### Core Modules

- **[`config.py`](config.py): Centralized configuration management with validation
- **[`logger.py`](logger.py): Structured logging with async exception handling
- **[`vocabulary.py`](vocabulary.py): Vocabulary state management with file persistence
- **[`text_processor.py`](text_processor.py): Advanced text processing utilities
- **[`translator.py`](translator.py): OpenAI API integration with rate limiting
- **[`article_processor.py`](article_processor.py): Main processing orchestration

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd lexilearn

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up NLTK data
python setup.py

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key
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
python main.py

# With custom article
python main.py --article my_article.txt

# Check help
python main.py --help
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
python main.py

# Custom article file
python main.py --article documents/article.txt

# Custom configuration via environment
OPENAI_API_KEY="sk-..." BATCH_SIZE=5 python main.py

# Debug mode
LOG_LEVEL=DEBUG python main.py --article test.txt
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
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run setup
python setup.py
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test
python test_setup.py

# Run with coverage
python -m pytest --cov=.

# Validate code structure
python validate_structure.py
```

### Code Quality

```bash
# Format code
black .

# Lint
flake8

# Type checking
mypy .

# Validate structure
python validate_structure.py
```

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Run quality checks: `python validate_structure.py`
5. Commit changes: `git commit -am 'Add new feature'`
6. Push to branch: `git push origin feature/new-feature`
7. Create Pull Request

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
   - Run: `python setup.py`
   - Manual: `python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"`

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
LOG_LEVEL=DEBUG python main.py --article test.txt
```

### Log Analysis

Check application logs for detailed error information:

```bash
# View recent logs
tail -f lexilearn.log

# Search for errors
grep ERROR lexilearn.log

# Debug specific module
LOG_LEVEL=DEBUG python main.py 2>&1 | grep -E "(ERROR|DEBUG)"
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
