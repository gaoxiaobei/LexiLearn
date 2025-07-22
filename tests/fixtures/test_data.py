"""Test data fixtures for LexiLearn tests."""

import json
from pathlib import Path
from typing import Dict, Any, List

# Sample vocabulary data
SAMPLE_VOCABULARY = {
    "hello": {
        "word": "hello",
        "definition": "used as a greeting or to begin a phone conversation",
        "translation": "你好",
        "example": "Hello, how are you today?",
        "difficulty": "beginner",
        "frequency": 0.95,
        "part_of_speech": "interjection",
        "phonetic": "/həˈloʊ/",
        "synonyms": ["hi", "greetings", "salutation"],
        "added_date": "2024-01-01T00:00:00Z"
    },
    "world": {
        "word": "world",
        "definition": "the earth, together with all of its countries and peoples",
        "translation": "世界",
        "example": "He wants to travel the world.",
        "difficulty": "beginner",
        "frequency": 0.92,
        "part_of_speech": "noun",
        "phonetic": "/wɜːrld/",
        "synonyms": ["earth", "globe", "planet"],
        "added_date": "2024-01-01T00:00:00Z"
    },
    "algorithm": {
        "word": "algorithm",
        "definition": "a process or set of rules to be followed in calculations or problem-solving",
        "translation": "算法",
        "example": "The search algorithm found the optimal solution.",
        "difficulty": "intermediate",
        "frequency": 0.75,
        "part_of_speech": "noun",
        "phonetic": "/ˈælɡərɪðəm/",
        "synonyms": ["procedure", "method", "process"],
        "added_date": "2024-01-02T00:00:00Z"
    },
    "sophisticated": {
        "word": "sophisticated",
        "definition": "having a refined knowledge of the ways of the world",
        "translation": "复杂的，老练的",
        "example": "She has sophisticated tastes in music.",
        "difficulty": "advanced",
        "frequency": 0.65,
        "part_of_speech": "adjective",
        "phonetic": "/səˈfɪstɪkeɪtɪd/",
        "synonyms": ["complex", "refined", "advanced"],
        "added_date": "2024-01-03T00:00:00Z"
    }
}

# Sample articles for testing
SAMPLE_ARTICLES = {
    "tech_article": {
        "title": "The Future of Artificial Intelligence",
        "content": """
        Artificial intelligence continues to evolve at an unprecedented pace. Machine learning 
        algorithms are becoming more sophisticated, enabling breakthroughs in natural language 
        processing and computer vision. These technological advances promise to revolutionize 
        industries from healthcare to transportation.
        
        However, the rapid deployment of AI systems raises important ethical considerations. 
        Issues such as algorithmic bias, privacy concerns, and the potential displacement of 
        human workers require careful attention from policymakers and technologists alike.
        """,
        "metadata": {
            "author": "Tech Reporter",
            "date": "2024-01-15",
            "category": "technology",
            "word_count": 85
        }
    },
    "science_article": {
        "title": "Climate Change and Renewable Energy",
        "content": """
        Climate change represents one of the most pressing challenges of our time. The 
        accumulation of greenhouse gases in the atmosphere has led to rising global 
        temperatures and increasingly severe weather patterns. Addressing this crisis 
        requires a comprehensive transition to renewable energy sources.
        
        Solar and wind power technologies have achieved remarkable efficiency improvements 
        in recent years. These sustainable alternatives offer the potential to significantly 
        reduce carbon emissions while creating new economic opportunities and jobs.
        """,
        "metadata": {
            "author": "Environmental Scientist",
            "date": "2024-01-20",
            "category": "science",
            "word_count": 78
        }
    },
    "business_article": {
        "title": "Global Economic Trends in 2024",
        "content": """
        The global economy faces unprecedented challenges and opportunities in 2024. 
        Digital transformation continues to accelerate across industries, creating new 
        business models and disrupting traditional approaches. Companies that successfully 
        adapt to these changes are likely to thrive in the evolving marketplace.
        
        Supply chain resilience has become a critical priority for businesses worldwide. 
        Organizations are investing in advanced analytics and artificial intelligence to 
        optimize their operations and mitigate potential disruptions.
        """,
        "metadata": {
            "author": "Business Analyst",
            "date": "2024-01-25",
            "category": "business",
            "word_count": 72
        }
    }
}

# Mock OpenAI API responses
MOCK_OPENAI_RESPONSES = {
    "successful_translation": {
        "id": "chatcmpl-123456",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-3.5-turbo-0613",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "人工智能的快速发展已经从根本上改变了现代社会。"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 25,
            "completion_tokens": 15,
            "total_tokens": 40
        }
    },
    
    "successful_vocabulary_extraction": {
        "id": "chatcmpl-789012",
        "object": "chat.completion",
        "created": 1677652290,
        "model": "gpt-3.5-turbo-0613",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": json.dumps({
                    "vocabulary": [
                        {
                            "word": "algorithm",
                            "definition": "a process or set of rules to be followed in calculations",
                            "translation": "算法",
                            "example": "The algorithm processed the data efficiently.",
                            "difficulty": "intermediate",
                            "part_of_speech": "noun"
                        },
                        {
                            "word": "sophisticated",
                            "definition": "having a refined knowledge of the ways of the world",
                            "translation": "复杂的，老练的",
                            "example": "The system uses sophisticated technology.",
                            "difficulty": "advanced",
                            "part_of_speech": "adjective"
                        }
                    ]
                })
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 150,
            "completion_tokens": 85,
            "total_tokens": 235
        }
    },
    
    "rate_limit_error": {
        "error": {
            "message": "Rate limit reached",
            "type": "rate_limit_error",
            "code": "rate_limit_exceeded"
        }
    },
    
    "authentication_error": {
        "error": {
            "message": "Invalid authentication credentials",
            "type": "authentication_error",
            "code": "invalid_api_key"
        }
    }
}

# Test configuration templates
TEST_CONFIG_TEMPLATES = {
    "minimal": {
        "openai_api_key": "test-key",
        "log_level": "INFO"
    },
    
    "full": {
        "openai_api_key": "test-key",
        "openai_base_url": "https://api.openai.com/v1",
        "openai_model": "gpt-3.5-turbo",
        "max_tokens": 1000,
        "temperature": 0.7,
        "log_level": "DEBUG",
        "max_concurrent_requests": 5,
        "request_timeout": 30,
        "retry_attempts": 3,
        "retry_delay": 1.0,
        "vocabulary_file": "test_vocabulary.json",
        "output_dir": "test_output",
        "supported_formats": ["txt", "pdf", "docx", "md"]
    },
    
    "invalid": {
        "openai_api_key": "",
        "max_tokens": -100,
        "temperature": 2.5
    }
}

# Expected vocabulary extraction results
EXPECTED_VOCABULARY_RESULTS = {
    "tech_keywords": [
        "artificial intelligence",
        "machine learning",
        "algorithm",
        "neural network",
        "deep learning"
    ],
    
    "business_keywords": [
        "entrepreneurship",
        "innovation",
        "strategy",
        "competitive advantage",
        "market analysis"
    ],
    
    "science_keywords": [
        "hypothesis",
        "experiment",
        "empirical",
        "peer review",
        "reproducibility"
    ]
}

def create_test_vocabulary_file(path: Path, data: Dict[str, Any] = None) -> Path:
    """Create a test vocabulary JSON file."""
    if data is None:
        data = SAMPLE_VOCABULARY
    
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return path


def create_test_article_file(path: Path, article_type: str = "tech") -> Path:
    """Create a test article file."""
    if article_type not in SAMPLE_ARTICLES:
        raise ValueError(f"Unknown article type: {article_type}")
    
    article = SAMPLE_ARTICLES[article_type]
    content = f"# {article['title']}\n\n{article['content']}"
    
    path.write_text(content)
    return path


def get_mock_openai_response(response_type: str) -> Dict[str, Any]:
    """Get a mock OpenAI API response."""
    if response_type not in MOCK_OPENAI_RESPONSES:
        raise ValueError(f"Unknown response type: {response_type}")
    
    return MOCK_OPENAI_RESPONSES[response_type]


def create_large_text(num_words: int = 1000) -> str:
    """Create a large text for performance testing."""
    base_text = """
    The evolution of technology continues to reshape our understanding of what is possible.
    From the earliest mechanical computers to modern quantum processors, each advancement
    has brought new capabilities and challenges. Machine learning represents the latest
    frontier in this ongoing transformation, promising to revolutionize how we process
    information and make decisions.
    """
    
    words = base_text.split()
    repeated_text = []
    
    for i in range(num_words // len(words) + 1):
        repeated_text.extend(words)
    
    return " ".join(repeated_text[:num_words])


# Performance test configurations
PERFORMANCE_CONFIGS = {
    "small": {
        "text_length": 100,
        "vocabulary_size": 10,
        "concurrent_requests": 1
    },
    "medium": {
        "text_length": 1000,
        "vocabulary_size": 50,
        "concurrent_requests": 5
    },
    "large": {
        "text_length": 10000,
        "vocabulary_size": 200,
        "concurrent_requests": 10
    }
}