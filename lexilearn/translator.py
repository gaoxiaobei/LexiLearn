"""
Translation module for LexiLearn application.

This module handles API communication for word translations
using OpenAI's GPT models.
"""

import asyncio
import aiohttp
from typing import Tuple, Optional
from .logger import logger
from .config import config


class TranslationError(Exception):
    """Custom exception for translation-related errors."""
    pass


class Translator:
    """Handles API communication for word translations."""
    
    def __init__(self) -> None:
        """Initialize the translator with configuration."""
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(config.processing.max_concurrent_requests)
    
    async def __aenter__(self):
        """Async context manager entry."""
        connector = aiohttp.TCPConnector(
            limit=config.processing.connector_limit,
            limit_per_host=config.processing.connector_limit
        )
        timeout = aiohttp.ClientTimeout(total=config.api.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {config.api.api_key}",
                "Content-Type": "application/json"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def translate_word(
        self,
        word: str,
        context: str,
        is_retry: bool = False
    ) -> Tuple[str, bool]:
        """
        Translate a single word based on context.
        
        Args:
            word: The word to translate
            context: The sentence context for accurate translation
            is_retry: Whether this is a retry attempt
            
        Returns:
            Tuple of (translation, success_flag)
        """
        if not self.session:
            raise TranslationError("Translator not properly initialized")
        
        async with self.semaphore:
            return await self._make_translation_request(word, context, is_retry)
    
    async def _make_translation_request(
        self,
        word: str,
        context: str,
        is_retry: bool = False
    ) -> Tuple[str, bool]:
        """
        Make the actual API request for translation.
        
        Args:
            word: The word to translate
            context: The sentence context
            is_retry: Whether this is a retry attempt
            
        Returns:
            Tuple of (translation, success_flag)
        """
        data = {
            "model": config.api.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a translation assistant. Provide accurate Chinese translations "
                        "for English words based on context. For proper nouns (names, places), "
                        "keep the original English. Return only the translation without explanations."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Translate the word '{word}' to Chinese based on this context:\n"
                        f"{context}\n\nProvide only the Chinese translation."
                    )
                }
            ],
            "max_tokens": 50,
            "temperature": 0.1
        }
        
        try:
            async with self.session.post(config.api.base_url, json=data) as response:
                if response.status == 429:
                    if not is_retry:
                        logger.warning("Rate limit hit, waiting before retry...")
                        await asyncio.sleep(2)
                        return await self._make_translation_request(word, context, True)
                    else:
                        logger.error("Rate limit exceeded after retry")
                        return "翻译失败", False
                
                if response.status != 200:
                    logger.error(f"API request failed with status {response.status}")
                    return "翻译失败", False
                
                result = await response.json()
                
                if 'choices' not in result or not result['choices']:
                    logger.error("Invalid API response format")
                    return "翻译失败", False
                
                translation = result['choices'][0]['message']['content'].strip()
                
                # Clean up the translation
                translation = translation.strip('"\'').strip()
                
                if not translation or translation.lower() in ['translation', '翻译', '']:
                    logger.warning(f"Empty or invalid translation for '{word}'")
                    return "翻译失败", False
                
                logger.debug(f"Successfully translated '{word}' to '{translation}'")
                return translation, True
                
        except asyncio.TimeoutError:
            logger.error(f"Translation timeout for word '{word}'")
            return "翻译失败", False
        except aiohttp.ClientError as e:
            logger.error(f"Network error during translation: {e}")
            return "翻译失败", False
        except Exception as e:
            logger.error(f"Unexpected error during translation: {e}")
            return "翻译失败", False
    
    async def translate_words_batch(
        self,
        words_contexts: List[Tuple[str, str]]
    ) -> List[Tuple[str, str, bool]]:
        """
        Translate multiple words in batch.
        
        Args:
            words_contexts: List of (word, context) tuples
            
        Returns:
            List of (word, translation, success) tuples
        """
        if not self.session:
            raise TranslationError("Translator not properly initialized")
        
        tasks = [
            self.translate_word(word, context)
            for word, context in words_contexts
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_results = []
        for (word, context), result in zip(words_contexts, results):
            if isinstance(result, Exception):
                logger.error(f"Translation task failed for '{word}': {result}")
                processed_results.append((word, "翻译失败", False))
            else:
                translation, success = result
                processed_results.append((word, translation, success))
        
        return processed_results