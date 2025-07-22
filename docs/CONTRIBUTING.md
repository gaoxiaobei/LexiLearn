# Contributing to LexiLearn

Thank you for your interest in contributing to LexiLearn! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Workflow](#contributing-workflow)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## 🤝 Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
- **Be respectful**: Use inclusive language and be welcoming to newcomers
- **Be collaborative**: Work together to find the best solutions
- **Be constructive**: Provide helpful feedback and suggestions
- **Be patient**: Remember that everyone is learning

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- OpenAI API key (for testing)

### Quick Start
```bash
# Fork the repository on GitHub
git clone https://github.com/your-username/lexilearn.git
cd lexilearn

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists

# Set up development environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Run tests to verify setup
python test_setup.py
```

## 🛠️ Development Setup

### Development Tools
```bash
# Install development tools
pip install pytest pytest-asyncio pytest-cov
pip install black flake8 mypy
pip install pre-commit

# Set up pre-commit hooks
pre-commit install
```

### IDE Configuration

#### VS Code
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "python.testing.pytestEnabled": true,
    "python.testing.pytestPath": "pytest"
}
```

#### PyCharm
1. Set interpreter to project virtual environment
2. Enable code style: File → Settings → Editor → Code Style → Python → Black
3. Enable inspections: File → Settings → Editor → Inspections → Python

## 🔄 Contributing Workflow

### 1. Find an Issue
- Check [existing issues](https://github.com/your-repo/lexilearn/issues)
- Look for issues labeled `good first issue` or `help wanted`
- Create a new issue if none exists

### 2. Create Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 3. Make Changes
- Write code following [Code Standards](#code-standards)
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Test Changes
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_vocabulary.py -v

# Run with coverage
pytest --cov=lexilearn --cov-report=html

# Run linting
flake8 .
black --check .
mypy .

# Run validation
python validate_structure.py
```

### 5. Submit Pull Request
- Push branch to your fork
- Create pull request with detailed description
- Address review feedback

## 📏 Code Standards

### Python Style Guide
- **PEP 8**: Follow Python style conventions
- **Black**: Use Black for code formatting
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings

### Code Formatting
```python
# Good example
async def process_word(
    word: str, 
    context: str, 
    translator: Translator
) -> str:
    """
    Process a single word for translation.
    
    Args:
        word: The word to translate
        context: The sentence containing the word
        translator: Translator instance
        
    Returns:
        The translated word
        
    Raises:
        TranslationError: If translation fails
    """
    return await translator.translate(word, context)
```

### Naming Conventions
- **Classes**: PascalCase (`ArticleProcessor`)
- **Functions/Variables**: snake_case (`process_article`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_BATCH_SIZE`)
- **Private**: _leading_underscore (`_internal_method`)

### Async/Await Guidelines
- **Always async**: Use async/await for I/O operations
- **Avoid blocking**: Never use blocking calls in async functions
- **Context managers**: Use async context managers for resources

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── test_config.py
├── test_vocabulary.py
├── test_text_processor.py
├── test_translator.py
├── test_article_processor.py
├── fixtures/
│   ├── sample_articles/
│   └── vocabulary_files/
└── conftest.py
```

### Writing Tests
```python
import pytest
from vocabulary import VocabularyManager

@pytest.mark.asyncio
async def test_vocabulary_initialization():
    """Test vocabulary manager initialization."""
    vocab = VocabularyManager()
    await vocab.initialize()
    
    assert isinstance(vocab.known_words, set)
    assert isinstance(vocab.target_words, set)
    assert isinstance(vocab.learned_words, set)

@pytest.mark.asyncio
async def test_word_filtering():
    """Test word filtering logic."""
    vocab = VocabularyManager()
    await vocab.initialize()
    
    # Test known word filtering
    vocab.known_words.add("test")
    assert not vocab.should_translate("test")
    
    # Test unknown word
    assert vocab.should_translate("unknown")
```

### Test Categories
- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test under load

### Test Data
- Use fixtures for test data
- Keep test data minimal but representative
- Use temporary files for file operations

## 📚 Documentation

### Code Documentation
- **Docstrings**: All public functions and classes
- **Type Hints**: All function parameters and returns
- **Examples**: Include usage examples in docstrings
- **README**: Update for new features

### Documentation Standards
```python
class ArticleProcessor:
    """
    Main processing orchestrator for article translation.
    
    This class coordinates the complete translation pipeline including:
    - Article loading and validation
    - Text processing and tokenization
    - Vocabulary management
    - Translation with context
    - Result generation and output
    
    Example:
        >>> processor = ArticleProcessor()
        >>> processed_text, new_words, word_bank = await processor.process_article("article.txt")
    """
```

## 🐛 Issue Reporting

### Bug Report Template
```markdown
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- LexiLearn version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information.
```

### Feature Request Template
```markdown
**Feature Description**
A clear description of the feature.

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives**
Any alternative solutions considered.

**Additional Context**
Any other relevant information.
```

## 🔄 Pull Request Process

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No breaking changes (or properly documented)

### PR Description Template
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Review Process
1. **Automated Checks**: CI/CD runs tests and linting
2. **Code Review**: At least one maintainer reviews
3. **Testing**: Manual testing for complex changes
4. **Approval**: Maintainer approves and merges

## 🏷️ Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes
- **refactor**: Code refactoring
- **test**: Test additions/changes
- **chore**: Build process or auxiliary tool changes

### Examples
```bash
feat(translator): add support for custom translation prompts

Add ability to provide custom prompts for translation context,
enabling more accurate translations for specific domains.

Closes #123
```

```bash
fix(vocabulary): handle empty vocabulary files gracefully

Previously, empty vocabulary files would cause initialization errors.
Now they are handled as empty sets without errors.

Fixes #456
```

## 🚀 Release Process

### Version Numbering
- **Major**: Breaking changes (1.0.0 → 2.0.0)
- **Minor**: New features (1.0.0 → 1.1.0)
- **Patch**: Bug fixes (1.0.0 → 1.0.1)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in setup.py
- [ ] Git tag created
- [ ] GitHub release created

## 🛡️ Security Guidelines

### API Key Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly
- Monitor API usage

### Code Security
- Validate all inputs
- Use parameterized queries (if applicable)
- Avoid hardcoded secrets
- Regular security audits

## 📊 Performance Guidelines

### Profiling
```bash
# Profile with cProfile
python -m cProfile -o profile.stats main.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

### Memory Profiling
```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler main.py
```

## 🎯 Good First Issues

Looking to contribute? Start with these:

1. **Add more test cases** for existing functionality
2. **Improve error messages** with more helpful context
3. **Add type hints** to existing code
4. **Update documentation** with examples
5. **Add logging** for better debugging
6. **Improve performance** with profiling

## 🤔 Getting Help

### Resources
- **Documentation**: Check the docs/ directory
- **Issues**: Browse existing issues for solutions
- **Discussions**: Use GitHub Discussions for questions
- **Discord**: Join our community Discord (if available)

### Contact
- **Issues**: Create GitHub issue for bugs/features
- **Email**: Contact maintainers for security issues
- **Discussions**: Use GitHub Discussions for general questions

## 📈 Contribution Recognition

### Contributors
- Listed in README.md
- Mentioned in release notes
- GitHub contributor graph

### Maintainer Guidelines
- Welcome new contributors
- Provide constructive feedback
- Help with onboarding
- Recognize good contributions

## 🔄 Continuous Integration

### GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    - name: Lint with flake8
      run: flake8 .
    - name: Format with black
      run: black --check .
    - name: Type check with mypy
      run: mypy .
    - name: Test with pytest
      run: pytest --cov=lexilearn --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

Thank you for contributing to LexiLearn! 🎉