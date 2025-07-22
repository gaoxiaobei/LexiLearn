"""Pytest configuration and shared fixtures for LexiLearn tests."""
import asyncio
import os
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Dict, Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from aiohttp import ClientSession
from aioresponses import aioresponses

# Import LexiLearn modules
from config import Config, load_config
from logger import setup_logger
from vocabulary import VocabularyManager
from translator import OpenAITranslator
from text_processor import TextProcessor
from article_processor import ArticleProcessor


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Get the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def temp_dir() -> Path:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    env_vars = {
        "OPENAI_API_KEY": "test-api-key",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "OPENAI_MODEL": "gpt-3.5-turbo",
        "LOG_LEVEL": "DEBUG",
        "MAX_TOKENS": "1000",
        "TEMPERATURE": "0.7",
        "MAX_CONCURRENT_REQUESTS": "5",
        "REQUEST_TIMEOUT": "30",
        "RETRY_ATTEMPTS": "3",
        "RETRY_DELAY": "1.0",
        "VOCABULARY_FILE": "test_vocabulary.json",
        "OUTPUT_DIR": "test_output",
        "SUPPORTED_FORMATS": "txt,pdf,docx,md",
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    return env_vars


@pytest.fixture
def test_config(mock_env_vars) -> Config:
    """Create a test configuration."""
    return load_config()


@pytest.fixture
def test_logger():
    """Create a test logger."""
    return setup_logger("test_logger", "DEBUG")


@pytest.fixture
def sample_text() -> str:
    """Sample English text for testing."""
    return """
    The rapid advancement of artificial intelligence has fundamentally transformed 
    modern society. Machine learning algorithms now power everything from recommendation 
    systems to autonomous vehicles. Natural language processing enables computers to 
    understand and generate human-like text, revolutionizing how we interact with technology.
    
    However, these developments also raise important ethical questions about privacy, 
    bias, and the future of work. As AI systems become more sophisticated, society must 
    carefully consider how to harness their benefits while mitigating potential risks.
    """


@pytest.fixture
def sample_chinese_text() -> str:
    """Sample Chinese text for testing."""
    return """
    人工智能的快速发展已经从根本上改变了现代社会。机器学习算法现在为从推荐系统
    到自动驾驶汽车的一切提供动力。自然语言处理使计算机能够理解和生成类似人类的文本，
    彻底改变了我们与技术的交互方式。
    
    然而，这些发展也引发了关于隐私、偏见和工作未来的重要伦理问题。随着人工智能
    系统变得越来越复杂，社会必须仔细考虑如何利用其好处，同时减轻潜在风险。
    """


@pytest.fixture
def sample_vocabulary_data() -> Dict[str, Any]:
    """Sample vocabulary data for testing."""
    return {
        "hello": {
            "word": "hello",
            "definition": "used as a greeting or to begin a phone conversation",
            "translation": "你好",
            "example": "Hello, how are you today?",
            "difficulty": "beginner",
            "frequency": 0.95,
            "added_date": "2024-01-01T00:00:00Z"
        },
        "world": {
            "word": "world",
            "definition": "the earth, together with all of its countries and peoples",
            "translation": "世界",
            "example": "He wants to travel the world.",
            "difficulty": "beginner",
            "frequency": 0.92,
            "added_date": "2024-01-01T00:00:00Z"
        },
        "algorithm": {
            "word": "algorithm",
            "definition": "a process or set of rules to be followed in calculations",
            "translation": "算法",
            "example": "The search algorithm found the optimal solution.",
            "difficulty": "intermediate",
            "frequency": 0.75,
            "added_date": "2024-01-02T00:00:00Z"
        }
    }


@pytest.fixture
def mock_openai_response() -> Dict[str, Any]:
    """Mock OpenAI API response."""
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-3.5-turbo-0613",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": '{"vocabulary": [{"word": "hello", "definition": "used as a greeting", "translation": "你好", "example": "Hello, how are you?"}]}'
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 56,
            "completion_tokens": 31,
            "total_tokens": 87
        }
    }


@pytest.fixture
def mock_openai_error_response() -> Dict[str, Any]:
    """Mock OpenAI API error response."""
    return {
        "error": {
            "message": "Invalid API key",
            "type": "invalid_request_error",
            "code": "invalid_api_key"
        }
    }


@pytest.fixture
def vocabulary_manager(temp_dir, test_config) -> VocabularyManager:
    """Create a vocabulary manager for testing."""
    vocab_file = temp_dir / "test_vocabulary.json"
    return VocabularyManager(str(vocab_file))


@pytest.fixture
def text_processor(test_config) -> TextProcessor:
    """Create a text processor for testing."""
    return TextProcessor(test_config)


@pytest.fixture
def mock_translator(test_config):
    """Create a mock translator for testing."""
    translator = OpenAITranslator(test_config)
    translator.translate_text = AsyncMock(return_value="测试翻译")
    translator.extract_vocabulary = AsyncMock(return_value=[{
        "word": "test",
        "definition": "a procedure intended to establish the quality",
        "translation": "测试",
        "example": "This is a test example."
    }])
    return translator


@pytest.fixture
def article_processor_with_mocks(test_config, mock_translator, temp_dir):
    """Create an article processor with mocked dependencies."""
    processor = ArticleProcessor(test_config)
    processor.translator = mock_translator
    processor.output_dir = temp_dir / "output"
    return processor


@pytest.fixture
def aioresponses_fixture():
    """Mock aiohttp responses."""
    with aioresponses() as mocked:
        yield mocked


@pytest.fixture(scope="session")
def sample_files(temp_dir) -> Dict[str, Path]:
    """Create sample files for testing."""
    files = {}
    
    # Create sample text file
    text_file = temp_dir / "sample.txt"
    text_file.write_text("""
    Machine learning is a subset of artificial intelligence that focuses on the development 
    of algorithms and statistical models that enable computer systems to improve their 
    performance on a specific task through experience, without being explicitly programmed.
    """)
    files["txt"] = text_file
    
    # Create sample markdown file
    md_file = temp_dir / "sample.md"
    md_file.write_text("""
    # Machine Learning Fundamentals
    
    ## Introduction
    Machine learning represents a paradigm shift in how we approach problem-solving 
    in computer science. Rather than explicitly programming rules, we provide data 
    and allow algorithms to learn patterns.
    
    ## Key Concepts
    - **Supervised Learning**: Learning from labeled examples
    - **Unsupervised Learning**: Finding patterns in unlabeled data
    - **Reinforcement Learning**: Learning through interaction and feedback
    """)
    files["md"] = md_file
    
    return files


@pytest.fixture
def mock_session():
    """Create a mock aiohttp session."""
    session = MagicMock(spec=ClientSession)
    return session


@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Clean up temporary files after each test."""
    yield
    # Cleanup code would go here if needed


@pytest.fixture
def benchmark_config():
    """Configuration for benchmark tests."""
    return {
        "num_articles": 10,
        "article_length": 1000,
        "vocabulary_size": 100,
        "concurrent_requests": 5
    }