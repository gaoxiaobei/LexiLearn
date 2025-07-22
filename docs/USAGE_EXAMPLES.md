# Usage Examples

Comprehensive examples showing how to use LexiLearn via CLI, programmatic interfaces, and integration with other applications.

## 📋 Table of Contents

- [CLI Usage](#cli-usage)
- [Programmatic Usage](#programmatic-usage)
- [Advanced Examples](#advanced-examples)
- [Integration Examples](#integration-examples)
- [Batch Processing](#batch-processing)
- [Custom Workflows](#custom-workflows)

## 🖥️ CLI Usage

### Basic CLI Commands

```bash
# Process default article
python main.py

# Process specific article
python main.py --article my_article.txt

# Process with custom configuration
OPENAI_API_KEY="sk-..." BATCH_SIZE=5 python main.py

# Debug mode with verbose logging
LOG_LEVEL=DEBUG python main.py --article test.txt

# Help and usage information
python main.py --help
```

### CLI with Environment Variables

```bash
# Set persistent environment variables
export OPENAI_API_KEY="sk-your-key-here"
export BATCH_SIZE=10
export USE_TARGET_WORDS=true

# Run with configured environment
python main.py --article documents/article.txt
```

### Batch CLI Processing

```bash
# Process multiple articles
for file in articles/*.txt; do
    echo "Processing $file..."
    python main.py --article "$file"
done

# Process with different configurations
for batch_size in 5 10 15; do
    BATCH_SIZE=$batch_size python main.py --article article.txt
done
```

## 🐍 Programmatic Usage

### Basic Programmatic Usage

```python
import asyncio
from main import LexiLearnApp

async def basic_usage():
    """Basic programmatic usage example."""
    app = LexiLearnApp()
    
    # Process default article
    await app.run()
    
    # Process specific article
    await app.run("my_article.txt")

# Run async function
asyncio.run(basic_usage())
```

### Custom Processing Pipeline

```python
import asyncio
from pathlib import Path
from config import Config
from vocabulary import VocabularyManager
from text_processor import TextProcessor
from translator import Translator
from article_processor import ArticleProcessor

async def custom_pipeline():
    """Build custom processing pipeline."""
    
    # Initialize components
    config = Config()
    vocab = VocabularyManager()
    processor = TextProcessor()
    
    # Initialize vocabulary
    await vocab.initialize()
    
    # Load article
    article_path = "my_article.txt"
    with open(article_path, 'r', encoding='utf-8') as f:
        article_text = f.read()
    
    # Process text
    sentences = processor.tokenize_sentences(article_text)
    
    # Extract words for translation
    all_words = set()
    for sentence in sentences:
        words = processor.extract_words_for_processing(
            sentence, 
            vocab.known_words, 
            vocab.target_words, 
            config.processing.use_target_words
        )
        all_words.update(words)
    
    # Translate words
    async with Translator() as translator:
        words_contexts = [(word, article_text) for word in all_words]
        translations = await translator.translate_words_batch(words_contexts)
    
    # Create annotated text
    annotated_text = article_text
    for word, translation in translations.items():
        annotated_text = annotated_text.replace(
            word, 
            f"{word}({translation})"
        )
    
    # Save results
    with open("annotated_article.txt", 'w', encoding='utf-8') as f:
        f.write(annotated_text)
    
    # Update learned words
    await vocab.add_words_batch(set(translations.keys()))
    
    return annotated_text

asyncio.run(custom_pipeline())
```

## 🔄 Advanced Examples

### Custom Vocabulary Management

```python
import asyncio
from vocabulary import VocabularyManager
from pathlib import Path

class VocabularyService:
    def __init__(self, vocab_dir: str = "vocabulary"):
        self.vocab_dir = Path(vocab_dir)
        self.vocab_dir.mkdir(exist_ok=True)
        
        self.vocab = VocabularyManager(
            known_words_file=str(self.vocab_dir / "known.txt"),
            target_words_file=str(self.vocab_dir / "target.txt"),
            learned_words_file=str(self.vocab_dir / "learned.txt")
        )
    
    async def add_known_words(self, words: list[str]):
        """Add words to known vocabulary."""
        await self.vocab.initialize()
        
        # Add new known words
        current_known = self.vocab.known_words
        new_known = current_known.union(set(word.lower() for word in words))
        
        # Save to file
        with open(self.vocab.known_words_file, 'w') as f:
            for word in sorted(new_known):
                f.write(f"{word}\n")
        
        # Reload vocabulary
        await self.vocab.initialize()
    
    async def get_learning_progress(self) -> dict:
        """Get vocabulary learning progress."""
        await self.vocab.initialize()
        stats = self.vocab.get_statistics()
        
        return {
            'known_words': stats['known_count'],
            'target_words': stats['target_count'],
            'learned_words': stats['learned_count'],
            'total_vocabulary': (
                stats['known_count'] + 
                stats['target_count'] + 
                stats['learned_count']
            )
        }

# Usage
async def vocabulary_example():
    service = VocabularyService()
    
    # Add known words
    await service.add_known_words(["hello", "world", "python"])
    
    # Get progress
    progress = await service.get_learning_progress()
    print(f"Learning progress: {progress}")

asyncio.run(vocabulary_example())
```

### Batch Processing with Monitoring

```python
import asyncio
import time
from pathlib import Path
from typing import List, Dict
from article_processor import ArticleProcessor
from logger import LexiLearnLogger

class BatchProcessor:
    def __init__(self):
        self.processor = ArticleProcessor()
        self.logger = LexiLearnLogger("batch_processor")
    
    async def process_directory(
        self, 
        input_dir: str, 
        output_dir: str,
        file_pattern: str = "*.txt"
    ) -> List[Dict]:
        """Process all articles in a directory."""
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = []
        article_files = list(input_path.glob(file_pattern))
        
        self.logger.info(f"Found {len(article_files)} articles to process")
        
        for article_file in article_files:
            start_time = time.time()
            
            try:
                self.logger.info(f"Processing {article_file.name}...")
                
                # Process article
                processed_text, new_words, word_bank = await self.processor.process_article(
                    str(article_file)
                )
                
                # Save custom output
                output_file = output_path / f"processed_{article_file.name}"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(processed_text)
                
                # Save word bank
                word_bank_file = output_path / f"vocabulary_{article_file.stem}.txt"
                with open(word_bank_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(word_bank))
                
                processing_time = time.time() - start_time
                
                result = {
                    'file': article_file.name,
                    'success': True,
                    'processing_time': processing_time,
                    'new_words': len(new_words),
                    'vocabulary_entries': len(word_bank),
                    'output_file': str(output_file)
                }
                
                results.append(result)
                self.logger.info(f"Completed {article_file.name} in {processing_time:.2f}s")
                
            except Exception as e:
                self.logger.error(f"Failed to process {article_file.name}: {e}")
                results.append({
                    'file': article_file.name,
                    'success': False,
                    'error': str(e)
                })
        
        return results

# Usage
async def batch_example():
    batch_processor = BatchProcessor()
    
    results = await batch_processor.process_directory(
        input_dir="articles",
        output_dir="processed",
        file_pattern="*.txt"
    )
    
    report = batch_processor.generate_report(results)
    print(report)
    
    # Save report
    with open("processing_report.txt", 'w') as f:
        f.write(report)

asyncio.run(batch_example())
```

## 🔗 Integration Examples

### Jupyter Notebook Integration

```python
# In Jupyter notebook
import asyncio
from pathlib import Path
from article_processor import ArticleProcessor

# Display progress in notebook
from tqdm.notebook import tqdm

async def notebook_processing(article_path: str):
    """Process article with notebook-friendly output."""
    
    processor = ArticleProcessor()
    
    # Process with progress
    print("Processing article...")
    processed_text, new_words, word_bank = await processor.process_article(article_path)
    
    # Display results
    from IPython.display import display, Markdown
    
    display(Markdown("## Processed Article"))
    display(Markdown(processed_text[:1000] + "..."))  # Show first 1000 chars
    
    display(Markdown("## New Vocabulary"))
    for entry in word_bank[:10]:  # Show first 10 entries
        display(Markdown(f"- {entry}"))
    
    display(Markdown(f"## Summary"))
    display(Markdown(f"- **New words learned**: {len(new_words)}"))
    display(Markdown(f"- **Vocabulary entries**: {len(word_bank)}"))
    
    return processed_text, new_words, word_bank

# Usage in notebook
# result = await notebook_processing("my_article.txt")
```

### Streamlit Web App

```python
# save as streamlit_app.py
import streamlit as st
import asyncio
import tempfile
import os
from main import LexiLearnApp

st.title("LexiLearn - English Reading Assistant")

# File upload
uploaded_file = st.file_uploader("Choose an article", type=['txt'])

# Configuration
use_target_words = st.checkbox("Use target words filtering", value=True)
batch_size = st.slider("Batch size", min_value=1, max_value=20, value=10)

if uploaded_file is not None:
    if st.button("Process Article"):
        with st.spinner("Processing article..."):
            # Save uploaded file
            with tempfile.NamedTemporaryFile(
                mode='w+b', 
                suffix='.txt', 
                delete=False
            ) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                # Configure processing
                os.environ['USE_TARGET_WORDS'] = str(use_target_words)
                os.environ['BATCH_SIZE'] = str(batch_size)
                
                # Process article
                app = LexiLearnApp()
                asyncio.run(app.run(tmp_path))
                
                # Display results
                if os.path.exists("output_article.txt"):
                    with open("output_article.txt", 'r', encoding='utf-8') as f:
                        processed_text = f.read()
                    
                    st.subheader("Processed Article")
                    st.text_area("", processed_text, height=300)
                
                if os.path.exists("word_bank.txt"):
                    with open("word_bank.txt", 'r', encoding='utf-8') as f:
                        vocabulary = f.read()
                    
                    st.subheader("Vocabulary")
                    st.text_area("", vocabulary, height=200)
                
            finally:
                os.unlink(tmp_path)

# Run with: streamlit run streamlit_app.py
```

## 🎯 Best Practices

1. **Error Handling**: Always wrap processing in try-except blocks
2. **Resource Management**: Use context managers for file operations
3. **Configuration**: Use environment variables for sensitive data
4. **Testing**: Test with small articles before processing large files
5. **Monitoring**: Use logging for production deployments
6. **Caching**: Cache translations for repeated words when possible
7. **Batching**: Use batch processing for multiple articles
8. **Validation**: Validate input files before processing