# Text Processor API Documentation

The text processor provides advanced text analysis capabilities including tokenization, normalization, part-of-speech tagging, and word extraction.

## Overview

The text processor handles all text manipulation operations with support for:
- Text normalization and cleaning
- Sentence and word tokenization
- Part-of-speech (POS) tagging
- Word base form extraction (lemmatization)
- Proper noun detection
- Word validation and filtering

## Core Classes

### TextProcessor

**Location**: [`text_processor.py`](../text_processor.py:23)

Main text processing class with NLTK integration.

```python
from text_processor import TextProcessor

# Initialize processor
processor = TextProcessor()

# Ensure NLTK data is available
processor._ensure_nltk_data()
```

### Constructor

```python
def __init__(self) -> None:
    """
    Initialize text processor with NLTK data.
    Automatically downloads required NLTK corpora if missing.
    """
```

## Core Methods

### normalize_text()

**Location**: [`text_processor.py`](../text_processor.py:53)

Normalize text by removing extra whitespace and standardizing format.

```python
text = "  Hello   World!  This   is   a   test.  "
normalized = processor.normalize_text(text)
# Result: "Hello World! This is a test."
```

### tokenize_sentences()

**Location**: [`text_processor.py`](../text_processor.py:80)

Split text into individual sentences using NLTK's Punkt tokenizer.

```python
text = "Hello world! This is a test. Is this working?"
sentences = processor.tokenize_sentences(text)
# Result: ["Hello world!", "This is a test.", "Is this working?"]
```

### tokenize_words()

**Location**: [`text_processor.py`](../text_processor.py:100)

Tokenize text into individual words using NLTK's word tokenizer.

```python
text = "Hello, world! This is a test."
words = processor.tokenize_words(text)
# Result: ["Hello", ",", "world", "!", "This", "is", "a", "test", "."]
```

### get_word_base_form()

**Location**: [`text_processor.py`](../text_processor.py:119)

Get the base form (lemma) of a word using NLTK's WordNet lemmatizer.

```python
# Lemmatization examples
processor.get_word_base_form("running")    # "run"
processor.get_word_base_form("better")     # "good"
processor.get_word_base_form("children")   # "child"
processor.get_word_base_form("apple")      # "apple"
```

### is_proper_noun()

**Location**: [`text_processor.py`](../text_processor.py:150)

Determine if a word is a proper noun based on context and POS tagging.

```python
# Context-aware proper noun detection
context = "Apple is a technology company."
is_proper = processor.is_proper_noun("Apple", context)
# Result: True (company name)

context = "I ate an apple for lunch."
is_proper = processor.is_proper_noun("apple", context)
# Result: False (common noun)
```

### is_valid_word()

**Location**: [`text_processor.py`](../text_processor.py:176)

Validate if a word should be processed for translation.

```python
# Validation criteria
valid_words = [
    "hello",      # Valid: alphabetic
    "test",       # Valid: alphabetic
    "123",        # Invalid: numeric
    "test123",    # Invalid: alphanumeric
    "!",          # Invalid: punctuation
    "test-word",  # Invalid: hyphenated
    "test_word",  # Invalid: underscore
    "test's",     # Invalid: apostrophe
]
```

### detokenize_words()

**Location**: [`text_processor.py`](../text_processor.py:203)

Reconstruct text from tokenized words with proper spacing.

```python
words = ["Hello", ",", "world", "!"]
text = processor.detokenize_words(words)
# Result: "Hello, world!"
```

### extract_words_for_processing()

**Location**: [`text_processor.py`](../text_processor.py:222)

Extract and filter words for translation processing.

```python
sentence = "The quick brown fox jumps over the lazy dog."
known_words = {"the", "over"}
target_words = {"quick", "brown"}
use_target_filter = True

words_to_process = processor.extract_words_for_processing(
    sentence, known_words, target_words, use_target_filter
)
# Result: {"quick", "brown"} (only target words)
```

## Usage Examples

### Basic Text Processing

```python
from text_processor import TextProcessor

processor = TextProcessor()

# Process a paragraph
text = "Natural language processing (NLP) is a field of AI. It's very exciting!"

# Normalize text
normalized = processor.normalize_text(text)
print(f"Normalized: {normalized}")

# Tokenize sentences
sentences = processor.tokenize_sentences(normalized)
print(f"Sentences: {sentences}")

# Process each sentence
for sentence in sentences:
    words = processor.tokenize_words(sentence)
    print(f"Words in '{sentence}': {words}")
```

### Word Analysis Pipeline

```python
from text_processor import TextProcessor

processor = TextProcessor()

def analyze_words(text: str):
    """Analyze all words in text for translation."""
    words = processor.tokenize_words(text)
    
    analysis = []
    for word in words:
        if processor.is_valid_word(word):
            base_form = processor.get_word_base_form(word.lower())
            analysis.append({
                'original': word,
                'base_form': base_form,
                'is_valid': True
            })
    
    return analysis

# Example usage
text = "The cats are running quickly through the beautiful garden."
analysis = analyze_words(text)
for item in analysis:
    print(f"{item['original']} -> {item['base_form']}")
```

### Context-aware Processing

```python
from text_processor import TextProcessor

processor = TextProcessor()

def process_article(article: str, known_words: set, target_words: set):
    """Process article for translation with context awareness."""
    sentences = processor.tokenize_sentences(article)
    
    processing_data = []
    for sentence in sentences:
        words = processor.extract_words_for_processing(
            sentence, known_words, target_words, use_target_filter=True
        )
        
        # Filter out proper nouns
        final_words = {
            word for word in words 
            if not processor.is_proper_noun(word, sentence)
        }
        
        processing_data.append({
            'sentence': sentence,
            'words_to_translate': final_words
        })
    
    return processing_data

# Example usage
article = "Google announced new AI features. The technology is amazing!"
known = {"the", "is"}
target = {"announced", "features", "technology", "amazing"}
result = process_article(article, known, target)
```

## Advanced Usage

### Custom Word Filtering

```python
from text_processor import TextProcessor

processor = TextProcessor()

class CustomWordFilter:
    def __init__(self, processor: TextProcessor):
        self.processor = processor
    
    def filter_words(self, text: str, min_length: int = 3):
        """Filter words based on custom criteria."""
        words = self.processor.tokenize_words(text)
        
        filtered = []
        for word in words:
            if not self.processor.is_valid_word(word):
                continue
            
            base_form = self.processor.get_word_base_form(word.lower())
            
            # Custom filtering
            if len(base_form) < min_length:
                continue
            
            if base_form in {"the", "and", "or", "but"}:
                continue
            
            filtered.append(base_form)
        
        return set(filtered)

# Usage
filter = CustomWordFilter(processor)
text = "The quick brown fox jumps over the lazy dog."
unique_words = filter.filter_words(text, min_length=4)
```

### Sentence Processing Pipeline

```python
from text_processor import TextProcessor

processor = TextProcessor()

class SentenceProcessor:
    def __init__(self, processor: TextProcessor):
        self.processor = processor
    
    def process_sentence(self, sentence: str, known_words: set):
        """Process a single sentence for translation."""
        # Normalize
        normalized = self.processor.normalize_text(sentence)
        
        # Extract words
        all_words = self.processor.extract_words_for_processing(
            normalized, known_words, set(), use_target_filter=False
        )
        
        # Filter proper nouns
        content_words = {
            word for word in all_words
            if not self.processor.is_proper_noun(word, normalized)
        }
        
        # Get base forms
        base_forms = {
            self.processor.get_word_base_form(word.lower())
            for word in content_words
        }
        
        return {
            'original': sentence,
            'normalized': normalized,
            'content_words': content_words,
            'base_forms': base_forms
        }

# Usage
processor = SentenceProcessor(TextProcessor())
result = processor.process_sentence(
    "The quick brown fox jumps.", 
    {"the"}
)
```

## Error Handling

### NLTK Data Issues

```python
from text_processor import TextProcessor

processor = TextProcessor()

try:
    processor._ensure_nltk_data()
except Exception as e:
    print(f"Failed to download NLTK data: {e}")
    # Handle gracefully or provide fallback
```

### Text Processing Errors

```python
from text_processor import TextProcessor

processor = TextProcessor()

def safe_process_text(text: str):
    """Safely process text with error handling."""
    try:
        if not text or not text.strip():
            return []
        
        normalized = processor.normalize_text(text)
        sentences = processor.tokenize_sentences(normalized)
        
        return sentences
    
    except Exception as e:
        print(f"Text processing failed: {e}")
        return [text]  # Return original as single sentence

# Usage
sentences = safe_process_text("Hello world! This is a test.")
```

## Performance Considerations

### Caching Base Forms

```python
from functools import lru_cache
from text_processor import TextProcessor

processor = TextProcessor()

@lru_cache(maxsize=1000)
def cached_base_form(word: str) -> str:
    """Cache base form lookups for performance."""
    return processor.get_word_base_form(word)

# Usage
base_form = cached_base_form("running")
```

### Batch Processing

```python
from text_processor import TextProcessor

processor = TextProcessor()

def process_text_batch(texts: list[str]) -> list[dict]:
    """Process multiple texts efficiently."""
    results = []
    
    for text in texts:
        sentences = processor.tokenize_sentences(text)
        word_count = sum(
            1 for sentence in sentences
            for word in processor.tokenize_words(sentence)
            if processor.is_valid_word(word)
        )
        
        results.append({
            'text': text,
            'sentences': len(sentences),
            'words': word_count
        })
    
    return results
```

## Testing

### Unit Tests

```python
import pytest
from text_processor import TextProcessor

@pytest.fixture
def processor():
    return TextProcessor()

def test_normalize_text(processor):
    text = "  Hello   World!  "
    result = processor.normalize_text(text)
    assert result == "Hello World!"

def test_tokenize_sentences(processor):
    text = "Hello! How are you?"
    sentences = processor.tokenize_sentences(text)
    assert len(sentences) == 2

def test_word_base_form(processor):
    assert processor.get_word_base_form("running") == "run"
    assert processor.get_word_base_form("children") == "child"
```

### Integration Tests

```python
import pytest
from text_processor import TextProcessor

def test_full_processing_pipeline():
    processor = TextProcessor()
    
    article = "The quick brown fox jumps. Dogs are running quickly!"
    known_words = {"the", "are"}
    
    sentences = processor.tokenize_sentences(article)
    assert len(sentences) == 2
    
    for sentence in sentences:
        words = processor.extract_words_for_processing(
            sentence, known_words, set(), use_target_filter=False
        )
        assert len(words) > 0
```

## Best Practices

1. **Initialize once**: Create TextProcessor instance once and reuse
2. **Handle edge cases**: Empty text, single words, punctuation-only
3. **Use base forms**: Always use lemmatized forms for consistency
4. **Filter properly**: Remove proper nouns and invalid words
5. **Test thoroughly**: Include edge cases in tests
6. **Monitor performance**: Cache expensive operations when possible