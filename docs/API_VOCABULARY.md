# Vocabulary API Documentation

The vocabulary management system provides persistent storage and intelligent filtering for known, target, and learned words.

## Overview

The vocabulary system manages three word categories:
- **Known Words**: Words the user already knows
- **Target Words**: Words the user wants to focus on learning
- **Learned Words**: Words the user has successfully learned (auto-updated)

## Core Classes

### VocabularyManager

**Location**: [`vocabulary.py`](../vocabulary.py:21)

Main class for vocabulary management with async file I/O.

```python
from vocabulary import VocabularyManager

# Initialize vocabulary manager
vocab_manager = VocabularyManager(
    known_words_file="known_words.txt",
    target_words_file="target_words.txt",
    learned_words_file="learned_words.txt"
)

# Initialize from files
await vocab_manager.initialize()
```

### Constructor

```python
def __init__(
    self,
    known_words_file: str = "known_words.txt",
    target_words_file: str = "target_words.txt",
    learned_words_file: str = "learned_words.txt"
) -> None:
    """
    Initialize vocabulary manager with file paths.
    
    Args:
        known_words_file: Path to known words file
        target_words_file: Path to target words file (optional)
        learned_words_file: Path to learned words file
    """
```

## Core Methods

### initialize()

**Location**: [`vocabulary.py`](../vocabulary.py:48)

Initialize vocabulary sets by loading from files.

```python
await vocab_manager.initialize()
```

### should_translate()

**Location**: [`vocabulary.py`](../vocabulary.py:104)

Determine if a word should be translated based on vocabulary rules.

```python
if vocab_manager.should_translate("example"):
    print("This word should be translated")
```

**Rules**:
- Returns `False` if word is in known words
- Returns `True` if word is in target words (when enabled)
- Returns `True` for unknown words (when target words disabled)
- Case-insensitive matching

### add_words_batch()

**Location**: [`vocabulary.py`](../vocabulary.py:134)

Add multiple words to the learned vocabulary.

```python
new_words = {"apple", "banana", "cherry"}
count = await vocab_manager.add_words_batch(new_words)
print(f"Added {count} new learned words")
```

### get_statistics()

**Location**: [`vocabulary.py`](../vocabulary.py:169)

Get vocabulary statistics for monitoring and reporting.

```python
stats = vocab_manager.get_statistics()
print(f"Known words: {stats['known_count']}")
print(f"Target words: {stats['target_count']}")
print(f"Learned words: {stats['learned_count']}")
```

## File Formats

### Known Words File (`known_words.txt`)
```
the
and
or
but
```

### Target Words File (`target_words.txt`)
```
serendipity
ephemeral
ubiquitous
```

### Learned Words File (`learned_words.txt`)
```
apple
banana
cherry
```

**Format Rules**:
- One word per line
- Case-insensitive storage
- Automatic deduplication
- UTF-8 encoding

## Usage Examples

### Basic Usage

```python
import asyncio
from vocabulary import VocabularyManager

async def main():
    # Initialize vocabulary manager
    vocab = VocabularyManager()
    await vocab.initialize()
    
    # Check vocabulary
    print(f"Known words: {len(vocab.known_words)}")
    print(f"Target words: {len(vocab.target_words)}")
    print(f"Learned words: {len(vocab.learned_words)}")

asyncio.run(main())
```

### Custom File Paths

```python
from vocabulary import VocabularyManager

vocab = VocabularyManager(
    known_words_file="vocabulary/known.txt",
    target_words_file="vocabulary/target.txt",
    learned_words_file="vocabulary/learned.txt"
)
await vocab.initialize()
```

### Word Filtering

```python
from vocabulary import VocabularyManager

vocab = VocabularyManager()
await vocab.initialize()

# Test word filtering
test_words = ["the", "apple", "serendipity", "unknown"]
for word in test_words:
    should_translate = vocab.should_translate(word)
    print(f"{word}: {'Translate' if should_translate else 'Skip'}")
```

### Batch Learning

```python
from vocabulary import VocabularyManager

vocab = VocabularyManager()
await vocab.initialize()

# Learn new words from processing
processed_words = {"ephemeral", "ubiquitous", "quintessential"}
await vocab.add_words_batch(processed_words)

# Check updated statistics
stats = vocab.get_statistics()
print(f"Learned words updated: {stats['learned_count']}")
```

## Integration with Configuration

```python
from config import Config
from vocabulary import VocabularyManager

# Initialize configuration
config = Config()

# Create vocabulary manager with configured paths
vocab = VocabularyManager(
    known_words_file=config.file.known_words_file,
    target_words_file=config.file.target_words_file,
    learned_words_file=config.file.learned_words_file
)
await vocab.initialize()
```

## Advanced Usage

### Dynamic Vocabulary Management

```python
from vocabulary import VocabularyManager
import aiofiles

async def add_known_word(word: str, vocab: VocabularyManager):
    """Add a single word to known vocabulary."""
    async with aiofiles.open(vocab.known_words_file, 'a') as f:
        await f.write(f"{word}\n")
    
    # Reload vocabulary
    await vocab.initialize()

async def remove_from_target(word: str, vocab: VocabularyManager):
    """Remove a word from target vocabulary."""
    # Read current target words
    async with aiofiles.open(vocab.target_words_file, 'r') as f:
        words = {line.strip() for line in await f.readlines()}
    
    # Remove word
    words.discard(word.lower())
    
    # Write back
    async with aiofiles.open(vocab.target_words_file, 'w') as f:
        for word in sorted(words):
            await f.write(f"{word}\n")
    
    # Reload vocabulary
    await vocab.initialize()
```

### Vocabulary Analysis

```python
from vocabulary import VocabularyManager

async def analyze_vocabulary(vocab: VocabularyManager):
    """Analyze vocabulary overlap and statistics."""
    stats = vocab.get_statistics()
    
    # Calculate overlaps
    known_target_overlap = len(vocab.known_words & vocab.target_words)
    known_learned_overlap = len(vocab.known_words & vocab.learned_words)
    target_learned_overlap = len(vocab.target_words & vocab.learned_words)
    
    print("Vocabulary Analysis:")
    print(f"  Known words: {stats['known_count']}")
    print(f"  Target words: {stats['target_count']}")
    print(f"  Learned words: {stats['learned_count']}")
    print(f"  Known ∩ Target: {known_target_overlap}")
    print(f"  Known ∩ Learned: {known_learned_overlap}")
    print(f"  Target ∩ Learned: {target_learned_overlap}")
```

## Error Handling

### File Not Found

```python
from vocabulary import VocabularyManager

vocab = VocabularyManager(known_words_file="missing.txt")

try:
    await vocab.initialize()
except FileNotFoundError as e:
    print(f"Vocabulary file not found: {e}")
    # Handle missing file gracefully
```

### Permission Errors

```python
import os
from vocabulary import VocabularyManager

vocab = VocabularyManager(learned_words_file="/root/protected.txt")

try:
    await vocab.initialize()
except PermissionError as e:
    print(f"Permission denied: {e}")
    # Use alternative location
    vocab = VocabularyManager(learned_words_file="learned_words.txt")
    await vocab.initialize()
```

## Testing

### Mock Vocabulary for Testing

```python
import tempfile
import os
from vocabulary import VocabularyManager

async def test_vocabulary():
    # Create temporary files
    with tempfile.TemporaryDirectory() as tmpdir:
        known_file = os.path.join(tmpdir, "known.txt")
        target_file = os.path.join(tmpdir, "target.txt")
        learned_file = os.path.join(tmpdir, "learned.txt")
        
        # Write test data
        with open(known_file, 'w') as f:
            f.write("the\nand\nor\n")
        
        with open(target_file, 'w') as f:
            f.write("example\ntest\n")
        
        # Test vocabulary manager
        vocab = VocabularyManager(
            known_words_file=known_file,
            target_words_file=target_file,
            learned_words_file=learned_file
        )
        await vocab.initialize()
        
        # Run tests
        assert not vocab.should_translate("the")
        assert vocab.should_translate("example")
        assert vocab.should_translate("unknown")
```

## Performance Considerations

- **Memory**: All vocabulary loaded into memory for fast lookups
- **File I/O**: Async file operations for non-blocking I/O
- **Case Handling**: Case-insensitive matching with lowercase storage
- **Deduplication**: Automatic removal of duplicates during loading

## Best Practices

1. **Initialize once** at application startup
2. **Handle file errors** gracefully
3. **Use absolute paths** for production deployments
4. **Monitor vocabulary growth** with statistics
5. **Backup vocabulary files** regularly
6. **Validate word lists** before processing