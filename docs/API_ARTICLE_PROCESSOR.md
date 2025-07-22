# Article Processor API Documentation

The article processor orchestrates the complete text processing pipeline, combining vocabulary management, text processing, and translation into a cohesive workflow.

## Overview

The article processor provides the main processing pipeline that:
- Loads and validates input articles
- Processes text in configurable batches
- Manages vocabulary state
- Generates formatted output
- Provides comprehensive progress tracking
- Handles error recovery and logging

## Core Classes

### ArticleProcessor

**Location**: [`article_processor.py`](../article_processor.py:25)

Main processing orchestrator for the complete article translation pipeline.

```python
from article_processor import ArticleProcessor

# Initialize processor
processor = ArticleProcessor()

# Process an article
result = await processor.process_article("input_article.txt")
processed_text, new_words, word_bank = result
```

### Constructor

```python
def __init__(self) -> None:
    """
    Initialize article processor with all required components.
    Automatically initializes configuration, logger, and dependencies.
    """
```

## Core Methods

### process_article()

**Location**: [`article_processor.py`](../article_processor.py:37)

Process a complete article through the translation pipeline.

```python
async def process_article(
    self, 
    article_path: str
) -> Tuple[str, Set[str], List[str]]:
    """
    Process an article file through the complete translation pipeline.
    
    Args:
        article_path: Path to the article file to process
    
    Returns:
        Tuple containing:
        - processed_article: Article with translations inserted
        - new_learned_words: Set of newly learned words
        - word_bank: List of vocabulary entries
    
    Raises:
        FileNotFoundError: If article file doesn't exist
        ProcessingError: If processing fails at any stage
    """
```

### save_results()

**Location**: [`article_processor.py`](../article_processor.py:278)

Save processing results to files.

```python
async def save_results(
    self,
    processed_article: str,
    word_bank: List[str],
    output_path: str = None
) -> None:
    """
    Save processed article and word bank to files.
    
    Args:
        processed_article: The processed article text
        word_bank: List of vocabulary entries
        output_path: Custom output path (optional)
    """
```

### print_summary()

**Location**: [`article_processor.py`](../article_processor.py:335)

Print processing summary to console.

```python
def print_summary(self) -> None:
    """Print a comprehensive summary of the processing results."""
```

## Processing Pipeline

### 1. Article Loading
- Validates file existence and readability
- Loads article content with proper encoding
- Handles large files efficiently

### 2. Text Processing
- Normalizes text formatting
- Tokenizes into sentences and paragraphs
- Identifies words for translation

### 3. Vocabulary Filtering
- Filters known words
- Applies target word filtering (if enabled)
- Removes proper nouns and invalid words

### 4. Translation
- Processes words in configurable batches
- Uses context-aware translations
- Implements rate limiting and retries

### 5. Result Generation
- Creates annotated article with translations
- Generates vocabulary word bank
- Updates learned words file

### 6. Output Generation
- Saves processed article
- Creates word bank file
- Provides processing summary

## Usage Examples

### Basic Article Processing

```python
import asyncio
from article_processor import ArticleProcessor

async def process_basic_article():
    processor = ArticleProcessor()
    
    try:
        # Process article
        processed_text, new_words, word_bank = await processor.process_article(
            "input_article.txt"
        )
        
        print(f"Processing complete!")
        print(f"New words learned: {len(new_words)}")
        print(f"Vocabulary entries: {len(word_bank)}")
        
        # Save results (optional - already done by process_article)
        await processor.save_results(processed_text, word_bank)
        
        # Print summary
        processor.print_summary()
        
    except FileNotFoundError:
        print("Article file not found")
    except Exception as e:
        print(f"Processing failed: {e}")

asyncio.run(process_basic_article())
```

### Custom Configuration Processing

```python
import asyncio
import os
from article_processor import ArticleProcessor

async def process_with_custom_config():
    # Configure processing
    os.environ.update({
        'BATCH_SIZE': '5',
        'USE_TARGET_WORDS': 'true',
        'LOG_LEVEL': 'DEBUG'
    })
    
    processor = ArticleProcessor()
    
    # Process with custom settings
    result = await processor.process_article("my_article.txt")
    processed_text, new_words, word_bank = result
    
    return processed_text

asyncio.run(process_with_custom_config())
```

### Batch Processing Multiple Articles

```python
import asyncio
from pathlib import Path
from article_processor import ArticleProcessor

async def process_multiple_articles():
    processor = ArticleProcessor()
    
    articles_dir = Path("articles")
    results = []
    
    for article_file in articles_dir.glob("*.txt"):
        try:
            print(f"Processing {article_file.name}...")
            result = await processor.process_article(str(article_file))
            results.append({
                'file': article_file.name,
                'result': result
            })
        except Exception as e:
            print(f"Failed to process {article_file.name}: {e}")
    
    return results

# Usage
asyncio.run(process_multiple_articles())
```

## Advanced Usage

### Processing with Progress Tracking

```python
import asyncio
from article_processor import ArticleProcessor
from logger import LexiLearnLogger

async def process_with_progress():
    logger = LexiLearnLogger("custom_processor")
    processor = ArticleProcessor()
    
    # Custom progress callback
    class ProgressTracker:
        def __init__(self):
            self.total = 0
            self.processed = 0
        
        def update(self, current, total):
            self.processed = current
            self.total = total
            progress = (current / total) * 100
            logger.info(f"Progress: {progress:.1f}% ({current}/{total})")
    
    # Note: Progress tracking is built into the processor
    # via tqdm for async operations
    
    result = await processor.process_article("large_article.txt")
    return result

asyncio.run(process_with_progress())
```

### Custom Output Formatting

```python
import asyncio
from article_processor import ArticleProcessor

async def custom_output_format():
    processor = ArticleProcessor()
    
    # Process article
    processed_text, new_words, word_bank = await processor.process_article(
        "input.txt"
    )
    
    # Custom formatting
    custom_output = f"""
    # Processed Article
    
    {processed_text}
    
    ## New Vocabulary
    
    {chr(10).join(word_bank)}
    
    ## Summary
    
    - Total words processed: {len(processed_text.split())}
    - New words learned: {len(new_words)}
    - Vocabulary entries: {len(word_bank)}
    """
    
    # Save custom format
    with open("custom_output.md", "w", encoding="utf-8") as f:
        f.write(custom_output)
    
    return custom_output

asyncio.run(custom_output_format())
```

### Integration with External Systems

```python
import asyncio
from article_processor import ArticleProcessor
from typing import Dict, Any

class ArticleProcessorService:
    def __init__(self):
        self.processor = ArticleProcessor()
    
    async def process_article_api(
        self, 
        article_content: str, 
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process article via API endpoint."""
        
        # Save content to temporary file
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.txt', 
            delete=False,
            encoding='utf-8'
        ) as tmp_file:
            tmp_file.write(article_content)
            tmp_path = tmp_file.name
        
        try:
            # Process article
            processed_text, new_words, word_bank = await self.processor.process_article(
                tmp_path
            )
            
            return {
                'success': True,
                'processed_text': processed_text,
                'new_words': list(new_words),
                'word_bank': word_bank,
                'summary': self._generate_summary(processed_text, new_words, word_bank)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
    
    def _generate_summary(self, text, new_words, word_bank):
        """Generate processing summary."""
        return {
            'total_words': len(text.split()),
            'new_words_count': len(new_words),
            'vocabulary_entries': len(word_bank),
            'readability_score': self._calculate_readability(text)
        }
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate basic readability score."""
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        return words / max(sentences, 1)

# Usage
service = ArticleProcessorService()
result = asyncio.run(service.process_article_api("Hello world! This is a test."))
```

## Error Handling

### File Access Errors

```python
import asyncio
from article_processor import ArticleProcessor

async def handle_file_errors():
    processor = ArticleProcessor()
    
    try:
        result = await processor.process_article("nonexistent.txt")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        # Provide helpful error message
        print("Please ensure the article file exists in the specified location")
    except PermissionError as e:
        print(f"Permission denied: {e}")
        print("Please check file permissions")
    except IsADirectoryError as e:
        print(f"Expected file but found directory: {e}")

asyncio.run(handle_file_errors())
```

### Processing Errors

```python
import asyncio
from article_processor import ArticleProcessor

async def handle_processing_errors():
    processor = ArticleProcessor()
    
    try:
        result = await processor.process_article("corrupted.txt")
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
        print("Please ensure the file is UTF-8 encoded")
    except Exception as e:
        print(f"Processing error: {e}")
        # Log full error details
        import traceback
        traceback.print_exc()

asyncio.run(handle_processing_errors())
```

## Performance Optimization

### Large File Processing

```python
import asyncio
from article_processor import ArticleProcessor

async def process_large_file():
    """Process large files with optimized settings."""
    import os
    
    # Configure for large files
    os.environ.update({
        'BATCH_SIZE': '20',  # Larger batches for efficiency
        'MAX_CONCURRENT_REQUESTS': '10',
        'SLEEP_TIME': '0.1'
    })
    
    processor = ArticleProcessor()
    
    # Check file size
    file_size = os.path.getsize("large_article.txt")
    if file_size > 1024 * 1024:  # > 1MB
        print("Processing large file, this may take a while...")
    
    result = await processor.process_article("large_article.txt")
    return result

asyncio.run(process_large_file())
```

### Memory Management

```python
import asyncio
from article_processor import ArticleProcessor

async def memory_efficient_processing():
    """Process articles with memory considerations."""
    processor = ArticleProcessor()
    
    # Process in chunks for very large files
    # This would require extending the processor for streaming
    
    # Current implementation loads entire file into memory
    # For extremely large files, consider splitting into smaller files
    
    result = await processor.process_article("article.txt")
    return result

asyncio.run(memory_efficient_processing())
```

## Testing

### Unit Testing

```python
import asyncio
import pytest
from pathlib import Path
from article_processor import ArticleProcessor

@pytest.mark.asyncio
async def test_article_processing():
    processor = ArticleProcessor()
    
    # Create test article
    test_content = "The quick brown fox jumps over the lazy dog."
    test_file = "test_article.txt"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        result = await processor.process_article(test_file)
        processed_text, new_words, word_bank = result
        
        assert isinstance(processed_text, str)
        assert isinstance(new_words, set)
        assert isinstance(word_bank, list)
        assert len(new_words) > 0
        
    finally:
        # Clean up
        Path(test_file).unlink(missing_ok=True)

asyncio.run(test_article_processing())
```

### Integration Testing

```python
import asyncio
import tempfile
import os
from article_processor import ArticleProcessor

async def integration_test():
    """Test complete processing pipeline."""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup test environment
        article_path = os.path.join(tmpdir, "test.txt")
        known_path = os.path.join(tmpdir, "known.txt")
        learned_path = os.path.join(tmpdir, "learned.txt")
        
        # Create test files
        with open(article_path, 'w') as f:
            f.write("The ephemeral beauty of nature is truly amazing.")
        
        with open(known_path, 'w') as f:
            f.write("the\nof\nis\n")
        
        # Configure for test
        os.environ.update({
            'KNOWN_WORDS_FILE': known_path,
            'LEARNED_WORDS_FILE': learned_path,
            'BATCH_SIZE': '5'
        })
        
        processor = ArticleProcessor()
        result = await processor.process_article(article_path)
        
        # Verify results
        processed_text, new_words, word_bank = result
        assert len(new_words) > 0
        assert len(word_bank) > 0
        
        return True

asyncio.run(integration_test())
```

## Best Practices

1. **Initialize once**: Create ArticleProcessor once and reuse
2. **Handle file errors**: Always check file existence and permissions
3. **Monitor progress**: Use built-in progress tracking for large files
4. **Validate configuration**: Ensure all required files exist
5. **Test with small files**: Start with small articles for testing
6. **Backup vocabulary**: Backup vocabulary files before processing
7. **Use absolute paths**: Avoid relative path issues in production
8. **Monitor API usage**: Track OpenAI API usage and costs
9. **Handle errors gracefully**: Provide meaningful error messages
10. **Log processing details**: Use debug logging for troubleshooting