# Translator API Documentation

The translator module provides async OpenAI API integration with intelligent rate limiting, retry logic, and comprehensive error handling.

## Overview

The translator handles all communication with OpenAI's API for word translations with features:
- Async/await support for concurrent requests
- Automatic retry with exponential backoff
- Rate limiting and batch processing
- Context-aware translations
- Comprehensive error handling
- Connection pooling with aiohttp

## Core Classes

### Translator

**Location**: [`translator.py`](../translator.py:20)

Main translation client with async context management.

```python
from translator import Translator

# Using async context manager (recommended)
async with Translator() as translator:
    translation = await translator.translate_word("hello", "Hello world!")
    print(translation)

# Manual initialization
translator = Translator()
await translator.__aenter__()
try:
    translation = await translator.translate_word("hello", "Hello world!")
finally:
    await translator.__aexit__(None, None, None)
```

### Constructor

```python
def __init__(self) -> None:
    """
    Initialize translator with configuration from Config.
    Creates aiohttp session for HTTP requests.
    """
```

## Core Methods

### translate_word()

**Location**: [`translator.py`](../translator.py:50)

Translate a single word with context.

```python
async def translate_word(
    self, 
    word: str, 
    context: str, 
    source_lang: str = "English", 
    target_lang: str = "Chinese"
) -> str:
    """
    Translate a word based on its context.
    
    Args:
        word: The word to translate
        context: The sentence or paragraph containing the word
        source_lang: Source language (default: English)
        target_lang: Target language (default: Chinese)
    
    Returns:
        The translated word in target language
    
    Raises:
        TranslationError: If translation fails after retries
    """
```

### translate_words_batch()

**Location**: [`translator.py`](../translator.py:156)

Translate multiple words efficiently with concurrent requests.

```python
async def translate_words_batch(
    self,
    words_contexts: List[Tuple[str, str]],
    source_lang: str = "English",
    target_lang: str = "Chinese"
) -> Dict[str, str]:
    """
    Translate multiple words with their contexts concurrently.
    
    Args:
        words_contexts: List of (word, context) tuples
        source_lang: Source language (default: English)
        target_lang: Target language (default: Chinese)
    
    Returns:
        Dictionary mapping original words to translations
    
    Raises:
        TranslationError: If any translation fails
    """
```

## Usage Examples

### Basic Translation

```python
import asyncio
from translator import Translator

async def translate_single_word():
    async with Translator() as translator:
        context = "The ephemeral beauty of cherry blossoms."
        translation = await translator.translate_word("ephemeral", context)
        print(f"'ephemeral' -> '{translation}'")
        # Output: 'ephemeral' -> '短暂的'

asyncio.run(translate_single_word())
```

### Context-Aware Translation

```python
import asyncio
from translator import Translator

async def context_aware_translation():
    async with Translator() as translator:
        # Same word, different contexts
        contexts = [
            ("bank", "I deposited money in the bank."),
            ("bank", "The river bank was muddy."),
            ("bank", "The plane will bank to the left.")
        ]
        
        for word, context in contexts:
            translation = await translator.translate_word(word, context)
            print(f"'{word}' in '{context}' -> '{translation}'")

asyncio.run(context_aware_translation())
```

### Batch Translation

```python
import asyncio
from translator import Translator

async def batch_translation():
    async with Translator() as translator:
        words_contexts = [
            ("serendipity", "Finding that book was pure serendipity."),
            ("ephemeral", "The ephemeral beauty of cherry blossoms."),
            ("ubiquitous", "Smartphones are now ubiquitous in society."),
            ("quintessential", "She is the quintessential professional.")
        ]
        
        translations = await translator.translate_words_batch(words_contexts)
        
        for word, translation in translations.items():
            print(f"{word}: {translation}")

asyncio.run(batch_translation())
```

### Error Handling

```python
import asyncio
from translator import Translator

async def handle_translation_errors():
    try:
        async with Translator() as translator:
            # Invalid API key
            translation = await translator.translate_word("test", "This is a test.")
    except Exception as e:
        print(f"Translation failed: {e}")
        # Handle gracefully, maybe use fallback or skip

asyncio.run(handle_translation_errors())
```

## Configuration

### API Configuration

```python
from config import Config
from translator import Translator

# Configure via environment variables
import os
os.environ['OPENAI_API_KEY'] = 'your-api-key'
os.environ['API_MODEL'] = 'gpt-4o-mini'
os.environ['API_TIMEOUT'] = '30'

# Use with configuration
config = Config()
async with Translator() as translator:
    # Uses configuration from Config
    translation = await translator.translate_word("hello", "Hello world!")
```

### Custom API Settings

```python
import os
from translator import Translator

# Custom API settings
os.environ.update({
    'OPENAI_API_KEY': 'sk-...',
    'API_BASE_URL': 'https://api.openai.com/v1/chat/completions',
    'API_MODEL': 'gpt-4',
    'API_TIMEOUT': '60',
    'API_MAX_RETRIES': '5'
})

async with Translator() as translator:
    translation = await translator.translate_word("test", "Test sentence")
```

## Advanced Usage

### Custom Translation Prompts

```python
import asyncio
from translator import Translator

class CustomTranslator(Translator):
    async def translate_with_custom_prompt(
        self, 
        word: str, 
        context: str, 
        custom_prompt: str
    ) -> str:
        """Translate with custom prompt template."""
        # This would require extending the base Translator class
        # to support custom prompt templates
        pass

# Usage
async def custom_translation():
    async with CustomTranslator() as translator:
        custom_prompt = "Translate the word '{word}' from the context: {context}. Provide only the translation."
        # Implementation would use custom prompt
```

### Translation with Metadata

```python
import asyncio
from translator import Translator
from typing import Dict, Any

async def translate_with_metadata():
    async with Translator() as translator:
        word = "bank"
        context = "I deposited money in the bank."
        
        # Future enhancement: return translation with metadata
        # result = await translator.translate_word_with_metadata(word, context)
        # print(f"Translation: {result.translation}")
        # print(f"Confidence: {result.confidence}")
        # print(f"Part of speech: {result.pos}")
        pass
```

### Rate Limiting

```python
import asyncio
from translator import Translator

async def rate_limited_translation():
    """Demonstrate rate limiting in action."""
    async with Translator() as translator:
        words = ["word1", "word2", "word3", "word4", "word5"]
        contexts = ["context1", "context2", "context3", "context4", "context5"]
        
        # Process with rate limiting
        batch_size = 2
        for i in range(0, len(words), batch_size):
            batch = list(zip(words[i:i+batch_size], contexts[i:i+batch_size]))
            translations = await translator.translate_words_batch(batch)
            
            print(f"Batch {i//batch_size + 1}: {translations}")
            
            # Optional: Add delay between batches
            if i + batch_size < len(words):
                await asyncio.sleep(1)

asyncio.run(rate_limited_translation())
```

## Error Types and Handling

### Network Errors

```python
import asyncio
from translator import Translator

async def handle_network_errors():
    async with Translator() as translator:
        try:
            translation = await translator.translate_word("test", "Test")
        except aiohttp.ClientError as e:
            print(f"Network error: {e}")
            # Retry or use fallback
        except asyncio.TimeoutError:
            print("Request timeout")
            # Handle timeout
        except Exception as e:
            print(f"Unexpected error: {e}")
            # Log and handle gracefully

asyncio.run(handle_network_errors())
```

### API Errors

```python
import asyncio
from translator import Translator

async def handle_api_errors():
    async with Translator() as translator:
        try:
            translation = await translator.translate_word("test", "Test")
        except Exception as e:
            if "rate_limit" in str(e).lower():
                print("Rate limit hit, waiting...")
                await asyncio.sleep(60)  # Wait and retry
            elif "invalid_api_key" in str(e).lower():
                print("Invalid API key")
                # Handle authentication error
            else:
                print(f"API error: {e}")

asyncio.run(handle_api_errors())
```

## Testing

### Mock Translator for Testing

```python
import asyncio
from unittest.mock import AsyncMock, patch
from translator import Translator

async def test_translator():
    with patch('translator.Translator') as mock_translator:
        # Mock successful translation
        mock_instance = AsyncMock()
        mock_instance.translate_word.return_value = "测试"
        mock_instance.translate_words_batch.return_value = {"test": "测试"}
        
        # Use mock
        result = await mock_instance.translate_word("test", "This is a test")
        assert result == "测试"

asyncio.run(test_translator())
```

### Integration Testing

```python
import asyncio
import pytest
from translator import Translator

@pytest.mark.asyncio
async def test_real_translation():
    """Integration test with real API (requires valid API key)."""
    async with Translator() as translator:
        translation = await translator.translate_word("hello", "Hello world")
        assert isinstance(translation, str)
        assert len(translation) > 0
```

## Performance Optimization

### Connection Reuse

```python
import asyncio
from translator import Translator

async def efficient_translation():
    """Reuse connection for multiple translations."""
    async with Translator() as translator:
        # All translations use the same session
        words = ["hello", "world", "test", "example"]
        contexts = ["Hello world"] * len(words)
        
        translations = await translator.translate_words_batch(
            list(zip(words, contexts))
        )
        
        return translations

asyncio.run(efficient_translation())
```

### Batch Processing

```python
import asyncio
from translator import Translator

async def optimized_batch_processing():
    """Process large batches efficiently."""
    async with Translator() as translator:
        # Prepare large batch
        words_contexts = [
            (f"word_{i}", f"This is word {i} in context")
            for i in range(100)
        ]
        
        # Process in chunks
        chunk_size = 10
        all_translations = {}
        
        for i in range(0, len(words_contexts), chunk_size):
            chunk = words_contexts[i:i+chunk_size]
            chunk_translations = await translator.translate_words_batch(chunk)
            all_translations.update(chunk_translations)
        
        return all_translations

asyncio.run(optimized_batch_processing())
```

## Best Practices

1. **Use context manager** for automatic resource management
2. **Handle errors gracefully** with try-except blocks
3. **Use batch processing** for multiple translations
4. **Implement retry logic** for transient failures
5. **Monitor API usage** and implement rate limiting
6. **Cache translations** for repeated words
7. **Log translation errors** for debugging
8. **Validate inputs** before translation
9. **Use appropriate timeouts** for network requests
10. **Test with mock data** in development

## Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive configuration
- Validate all inputs before sending to API
- Implement rate limiting to prevent abuse
- Monitor API usage for unexpected patterns