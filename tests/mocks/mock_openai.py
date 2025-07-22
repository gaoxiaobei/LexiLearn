"""Mock OpenAI API responses for testing."""

import json
from typing import Dict, Any, Optional
from unittest.mock import AsyncMock, MagicMock

import aiohttp
from aioresponses import aioresponses


class MockOpenAIResponse:
    """Mock OpenAI API responses for testing."""
    
    def __init__(self):
        self.responses = {
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
            
            "successful_vocabulary": {
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
                                    "definition": "a process or set of rules to be followed",
                                    "translation": "算法",
                                    "example": "The algorithm processed the data efficiently.",
                                    "difficulty": "intermediate",
                                    "part_of_speech": "noun"
                                },
                                {
                                    "word": "sophisticated",
                                    "definition": "having a refined knowledge",
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
            },
            
            "timeout_error": {
                "error": {
                    "message": "Request timed out",
                    "type": "timeout_error",
                    "code": "request_timeout"
                }
            },
            
            "invalid_json_response": {
                "id": "chatcmpl-invalid",
                "object": "chat.completion",
                "created": 1677652290,
                "model": "gpt-3.5-turbo-0613",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Invalid JSON response"
                    },
                    "finish_reason": "stop"
                }]
            }
        }
    
    def get_response(self, response_type: str) -> Dict[str, Any]:
        """Get a mock response by type."""
        if response_type not in self.responses:
            raise ValueError(f"Unknown response type: {response_type}")
        return self.responses[response_type]
    
    def setup_mock_response(
        self,
        mock_aioresponses: aioresponses,
        response_type: str,
        status: int = 200,
        url: str = "https://api.openai.com/v1/chat/completions"
    ):
        """Set up a mock response for aioresponses."""
        response_data = self.get_response(response_type)
        mock_aioresponses.post(url, status=status, payload=response_data)


class MockTranslator:
    """Mock translator for testing without actual API calls."""
    
    def __init__(self, delay: float = 0.1):
        self.delay = delay
        self.call_count = 0
        self.last_request = None
    
    async def translate_text(self, text: str, source_lang: str = "en", target_lang: str = "zh") -> str:
        """Mock translation method."""
        self.call_count += 1
        self.last_request = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        # Simulate async delay
        import asyncio
        await asyncio.sleep(self.delay)
        
        # Simple mock translation
        translations = {
            "hello": "你好",
            "world": "世界",
            "algorithm": "算法",
            "machine learning": "机器学习",
            "artificial intelligence": "人工智能"
        }
        
        for eng, chn in translations.items():
            if eng.lower() in text.lower():
                return text.lower().replace(eng.lower(), chn)
        
        return f"翻译: {text}"
    
    async def extract_vocabulary(self, text: str) -> List[Dict[str, Any]]:
        """Mock vocabulary extraction."""
        self.call_count += 1
        self.last_request = {"text": text}
        
        import asyncio
        await asyncio.sleep(self.delay)
        
        # Return mock vocabulary
        return [
            {
                "word": "algorithm",
                "definition": "a process or set of rules to be followed",
                "translation": "算法",
                "example": "The algorithm processed the data efficiently.",
                "difficulty": "intermediate",
                "part_of_speech": "noun"
            }
        ]


class MockAiohttpSession:
    """Mock aiohttp session for testing."""
    
    def __init__(self):
        self.requests = []
        self.responses = []
    
    def post(self, url: str, **kwargs) -> AsyncMock:
        """Mock POST request."""
        mock_response = AsyncMock()
        self.requests.append({
            "url": url,
            "method": "POST",
            "kwargs": kwargs
        })
        return mock_response
    
    def get(self, url: str, **kwargs) -> AsyncMock:
        """Mock GET request."""
        mock_response = AsyncMock()
        self.requests.append({
            "url": url,
            "method": "GET",
            "kwargs": kwargs
        })
        return mock_response


def create_mock_response(
    status: int = 200,
    json_data: Optional[Dict[str, Any]] = None,
    text: str = "",
    headers: Optional[Dict[str, str]] = None
) -> AsyncMock:
    """Create a mock aiohttp response."""
    mock_response = AsyncMock()
    mock_response.status = status
    
    if json_data:
        mock_response.json = AsyncMock(return_value=json_data)
    
    if text:
        mock_response.text = AsyncMock(return_value=text)
    
    if headers:
        mock_response.headers = headers
    else:
        mock_response.headers = {}
    
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    
    return mock_response


class NetworkErrorSimulator:
    """Simulate network errors for testing."""
    
    @staticmethod
    async def timeout_error():
        """Simulate a timeout error."""
        import asyncio
        await asyncio.sleep(0.1)
        raise asyncio.TimeoutError("Request timed out")
    
    @staticmethod
    async def connection_error():
        """Simulate a connection error."""
        import aiohttp
        raise aiohttp.ClientConnectionError("Connection failed")
    
    @staticmethod
    async def http_error(status: int = 500):
        """Simulate an HTTP error."""
        import aiohttp
        raise aiohttp.ClientResponseError(
            request_info=None,
            history=None,
            status=status,
            message=f"HTTP {status} error"
        )


class RateLimitSimulator:
    """Simulate rate limiting for testing."""
    
    def __init__(self, max_requests: int = 5, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = []
    
    async def check_rate_limit(self) -> bool:
        """Check if rate limit has been exceeded."""
        import time
        
        now = time.time()
        # Remove old requests outside the window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.window]
        
        if len(self.requests) >= self.max_requests:
            return False
        
        self.requests.append(now)
        return True
    
    def reset(self):
        """Reset the rate limit counter."""
        self.requests.clear()