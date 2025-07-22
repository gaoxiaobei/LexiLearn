"""Unit tests for translator functionality with mocking."""

import asyncio
import json
from typing import Dict, Any, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aioresponses import aioresponses

from translator import OpenAITranslator


class TestOpenAITranslator:
    """Test cases for OpenAITranslator class."""
    
    def test_translator_creation(self, test_config):
        """Test translator creation."""
        translator = OpenAITranslator(test_config)
        
        assert translator.config == test_config
        assert translator.api_key == test_config.openai_api_key
        assert translator.base_url == test_config.openai_base_url
        assert translator.model == test_config.openai_model
    
    def test_translator_creation_custom_values(self, test_config):
        """Test translator creation with custom values."""
        config = test_config
        config.openai_base_url = "https://custom.api.com"
        config.openai_model = "gpt-4"
        
        translator = OpenAITranslator(config)
        
        assert translator.base_url == "https://custom.api.com"
        assert translator.model == "gpt-4"
    
    @pytest.mark.asyncio
    async def test_translate_text_success(self, test_config, aioresponses_fixture):
        """Test successful text translation."""
        translator = OpenAITranslator(test_config)
        
        # Mock successful response
        mock_response = {
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
        }
        
        aioresponses_fixture.post(
            "https://api.openai.com/v1/chat/completions",
            status=200,
            payload=mock_response
        )
        
        result = await translator.translate_text(
            "The rapid development of artificial intelligence has fundamentally transformed modern society.",
            source_lang="en",
            target_lang="zh"
        )
        
        assert result == "人工智能的快速发展已经从根本上改变了现代社会。"
    
    @pytest.mark.asyncio
    async def test_translate_text_empty_input(self, test_config):
        """Test translation with empty input."""
        translator = OpenAITranslator(test_config)
        
        result = await translator.translate_text("")
        
        assert result == ""
    
    @pytest.mark.asyncio
    async def test_extract_vocabulary_success(self, test_config, aioresponses_fixture):
        """Test successful vocabulary extraction."""
        translator = OpenAITranslator(test_config)
        
        # Mock successful response
        vocabulary_data = {
            "vocabulary": [
                {
                    "word": "algorithm",
                    "definition": "a process or set of rules to be followed in calculations",
                    "translation": "算法",
                    "example": "The algorithm processed the data efficiently.",
                    "difficulty": "intermediate",
                    "part_of_speech": "noun"
                }
            ]
        }
        
        mock_response = {
            "id": "chatcmpl-789012",
            "object": "chat.completion",
            "created": 1677652290,
            "model": "gpt-3.5-turbo-0613",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": json.dumps(vocabulary_data)
                },
                "finish_reason": "stop"
            }]
        }
        
        aioresponses_fixture.post(
            "https://api.openai.com/v1/chat/completions",
            status=200,
            payload=mock_response
        )
        
        result = await translator.extract_vocabulary("Machine learning algorithms are sophisticated.")
        
        assert len(result) == 1
        assert result[0]["word"] == "algorithm"
        assert result[0]["translation"] == "算法"
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self, test_config, aioresponses_fixture):
        """Test API error handling."""
        translator = OpenAITranslator(test_config)
        
        # Mock API error
        error_response = {
            "error": {
                "message": "Invalid API key",
                "type": "authentication_error"
            }
        }
        
        aioresponses_fixture.post(
            "https://api.openai.com/v1/chat/completions",
            status=401,
            payload=error_response
        )
        
        with pytest.raises(Exception):
            await translator.translate_text("Test text")
    
    @pytest.mark.asyncio
    async def test_network_timeout(self, test_config, aioresponses_fixture):
        """Test network timeout handling."""
        translator = OpenAITranslator(test_config)
        
        aioresponses_fixture.post(
            "https://api.openai.com/v1/chat/completions",
            status=408
        )
        
        with pytest.raises(Exception):
            await translator.translate_text("Test text")
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, test_config, aioresponses_fixture):
        """Test handling concurrent requests."""
        translator = OpenAITranslator(test_config)
        
        # Mock successful response
        mock_response = {
            "id": "chatcmpl-concurrent",
            "object": "chat.completion",
            "created": 1677652288,
            "model": "gpt-3.5-turbo-0613",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Translated"
                },
                "finish_reason": "stop"
            }]
        }
        
        aioresponses_fixture.post(
            "https://api.openai.com/v1/chat/completions",
            status=200,
            payload=mock_response
        )
        
        # Test concurrent requests
        texts = ["Text 1", "Text 2", "Text 3"]
        tasks = [translator.translate_text(text) for text in texts]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        assert all(result == "Translated" for result in results)
    
    def test_context_manager(self, test_config):
        """Test async context manager usage."""
        async def test_context():
            async with OpenAITranslator(test_config) as translator:
                assert translator.config == test_config
        
        asyncio.run(test_context())