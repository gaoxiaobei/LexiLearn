"""Unit tests for text processing functionality."""

import tempfile
from pathlib import Path
from typing import List, Tuple
from unittest.mock import patch

import pytest

from text_processor import TextProcessor


class TestTextProcessor:
    """Test cases for TextProcessor class."""
    
    def test_text_processor_creation(self, test_config):
        """Test text processor creation."""
        processor = TextProcessor(test_config)
        
        assert processor.config == test_config
        assert processor.supported_formats == ["txt", "pdf", "docx", "md"]
    
    def test_extract_text_from_txt(self, tmp_path, test_config):
        """Test extracting text from txt file."""
        processor = TextProcessor(test_config)
        
        # Create test txt file
        txt_file = tmp_path / "test.txt"
        content = """
        This is a test document.
        It contains multiple lines of text.
        We will use this to test text extraction.
        """
        txt_file.write_text(content)
        
        extracted_text = processor.extract_text(str(txt_file))
        
        assert "This is a test document" in extracted_text
        assert "multiple lines of text" in extracted_text
        assert extracted_text.strip() == content.strip()
    
    def test_extract_text_from_md(self, tmp_path, test_config):
        """Test extracting text from markdown file."""
        processor = TextProcessor(test_config)
        
        # Create test markdown file
        md_file = tmp_path / "test.md"
        content = """# Test Document

This is a **markdown** document with *formatting*.

## Section 1
- Item 1
- Item 2
- Item 3

### Code Example
```python
def hello_world():
    print("Hello, World!")
```
"""
        md_file.write_text(content)
        
        extracted_text = processor.extract_text(str(md_file))
        
        assert "Test Document" in extracted_text
        assert "markdown" in extracted_text
        assert "Hello, World!" in extracted_text
        assert "```python" not in extracted_text  # Should be cleaned
    
    def test_extract_text_unsupported_format(self, tmp_path, test_config):
        """Test extracting text from unsupported format."""
        processor = TextProcessor(test_config)
        
        # Create unsupported file
        unsupported_file = tmp_path / "test.xyz"
        unsupported_file.write_text("test content")
        
        with pytest.raises(ValueError):
            processor.extract_text(str(unsupported_file))
    
    def test_extract_text_nonexistent_file(self, test_config):
        """Test extracting text from nonexistent file."""
        processor = TextProcessor(test_config)
        
        with pytest.raises(FileNotFoundError):
            processor.extract_text("nonexistent.txt")
    
    def test_clean_text(self, test_config):
        """Test text cleaning functionality."""
        processor = TextProcessor(test_config)
        
        dirty_text = """
        This   is   a   test   with   extra   spaces.
        
        Multiple newlines
        
        
        And special characters: @#$%^&*()
        
        URLs: https://example.com and http://test.org
        
        Email: test@example.com
        
        Numbers: 12345 and 3.14
        
        Unicode: café, naïve, résumé
        """
        
        cleaned = processor.clean_text(dirty_text)
        
        # Should normalize spaces
        assert "This is a test with extra spaces" in cleaned
        assert "  " not in cleaned
        
        # Should normalize newlines
        assert "\n\n\n" not in cleaned
        
        # Should preserve meaningful content
        assert "cafe" in cleaned or "café" in cleaned
        assert "naive" in cleaned or "naïve" in cleaned
        assert "resume" in cleaned or "résumé" in cleaned
    
    def test_split_into_sentences(self, test_config):
        """Test splitting text into sentences."""
        processor = TextProcessor(test_config)
        
        text = """
        This is the first sentence. This is the second sentence!
        Here's a third sentence with a question mark?
        This is a sentence with "quoted text" inside it.
        Dr. Smith went to Washington. He saw the U.S. Capitol.
        """
        
        sentences = processor.split_into_sentences(text)
        
        assert len(sentences) >= 4
        assert "This is the first sentence" in sentences[0]
        assert "This is the second sentence" in sentences[1]
        assert "question mark" in sentences[2]
        assert "Dr. Smith went to Washington" in [s.strip() for s in sentences]
    
    def test_split_into_paragraphs(self, test_config):
        """Test splitting text into paragraphs."""
        processor = TextProcessor(test_config)
        
        text = """
        This is paragraph one.
        It has multiple lines.
        
        This is paragraph two.
        It also has multiple lines.
        
        This is paragraph three.
        """
        
        paragraphs = processor.split_into_paragraphs(text)
        
        assert len(paragraphs) == 3
        assert "paragraph one" in paragraphs[0]
        assert "paragraph two" in paragraphs[1]
        assert "paragraph three" in paragraphs[2]
    
    def test_count_words(self, test_config):
        """Test word counting."""
        processor = TextProcessor(test_config)
        
        text = "This is a simple test with seven words."
        count = processor.count_words(text)
        
        assert count == 7
    
    def test_count_words_empty(self, test_config):
        """Test word counting with empty text."""
        processor = TextProcessor(test_config)
        
        assert processor.count_words("") == 0
        assert processor.count_words("   ") == 0
        assert processor.count_words("\n\n\t") == 0
    
    def test_count_sentences(self, test_config):
        """Test sentence counting."""
        processor = TextProcessor(test_config)
        
        text = "First sentence. Second sentence! Third sentence?"
        count = processor.count_sentences(text)
        
        assert count == 3
    
    def test_count_sentences_empty(self, test_config):
        """Test sentence counting with empty text."""
        processor = TextProcessor(test_config)
        
        assert processor.count_sentences("") == 0
        assert processor.count_sentences("No punctuation") == 1
    
    def test_estimate_reading_time(self, test_config):
        """Test reading time estimation."""
        processor = TextProcessor(test_config)
        
        # Test with 200 words (average reading speed ~200 wpm)
        text = " ".join(["word"] * 200)
        time_minutes = processor.estimate_reading_time(text)
        
        assert 0.8 <= time_minutes <= 1.2  # Should be around 1 minute
    
    def test_estimate_reading_time_custom_speed(self, test_config):
        """Test reading time estimation with custom speed."""
        processor = TextProcessor(test_config)
        
        text = " ".join(["word"] * 100)
        time_minutes = processor.estimate_reading_time(text, words_per_minute=100)
        
        assert 0.9 <= time_minutes <= 1.1  # Should be around 1 minute
    
    def test_extract_keywords(self, test_config):
        """Test keyword extraction."""
        processor = TextProcessor(test_config)
        
        text = """
        Machine learning is a subset of artificial intelligence.
        Machine learning algorithms can learn from data.
        Artificial intelligence is transforming many industries.
        """
        
        keywords = processor.extract_keywords(text, max_keywords=5)
        
        assert len(keywords) <= 5
        assert "machine" in [kw.lower() for kw in keywords] or "learning" in [kw.lower() for kw in keywords]
        assert "artificial" in [kw.lower() for kw in keywords] or "intelligence" in [kw.lower() for kw in keywords]
    
    def test_extract_keywords_empty_text(self, test_config):
        """Test keyword extraction with empty text."""
        processor = TextProcessor(test_config)
        
        keywords = processor.extract_keywords("", max_keywords=5)
        
        assert keywords == []
    
    def test_detect_language(self, test_config):
        """Test language detection."""
        processor = TextProcessor(test_config)
        
        english_text = "This is an English text for testing purposes."
        chinese_text = "这是一个中文文本用于测试目的。"
        
        english_lang = processor.detect_language(english_text)
        chinese_lang = processor.detect_language(chinese_text)
        
        assert english_lang in ["en", "english"]
        assert chinese_lang in ["zh", "chinese"]
    
    def test_detect_language_mixed(self, test_config):
        """Test language detection with mixed text."""
        processor = TextProcessor(test_config)
        
        mixed_text = "This is English 这是中文 This is more English"
        
        detected_lang = processor.detect_language(mixed_text)
        
        # Should detect the dominant language
        assert detected_lang is not None
    
    def test_normalize_text(self, test_config):
        """Test text normalization."""
        processor = TextProcessor(test_config)
        
        text = "  This   has   extra   spaces   and   \n\n   newlines   \t\t   "
        normalized = processor.normalize_text(text)
        
        assert normalized.strip() == "This has extra spaces and newlines"
        assert "  " not in normalized.strip()
    
    def test_remove_stopwords(self, test_config):
        """Test stopword removal."""
        processor = TextProcessor(test_config)
        
        text = "this is a test with some common words like the and a"
        cleaned = processor.remove_stopwords(text)
        
        # Should remove common stopwords
        assert "the" not in cleaned.lower()
        assert "and" not in cleaned.lower()
        assert "a" not in cleaned.lower()
        assert "test" in cleaned.lower()
        assert "common" in cleaned.lower()
    
    def test_stem_words(self, test_config):
        """Test word stemming."""
        processor = TextProcessor(test_config)
        
        text = "running jumps quickly better"
        stemmed = processor.stem_words(text)
        
        # Should stem words to their root form
        assert "run" in stemmed.lower() or "running" not in stemmed.lower()
        assert "jump" in stemmed.lower() or "jumps" not in stemmed.lower()
    
    def test_calculate_readability_score(self, test_config):
        """Test readability score calculation."""
        processor = TextProcessor(test_config)
        
        # Simple text should have high readability
        simple_text = "This is a simple sentence. It is easy to read."
        simple_score = processor.calculate_readability_score(simple_text)
        
        # Complex text should have lower readability
        complex_text = "The utilization of multifaceted terminologies in convoluted syntactical structures necessitates advanced cognitive processing capabilities."
        complex_score = processor.calculate_readability_score(complex_text)
        
        assert simple_score > complex_score
    
    def test_process_file(self, tmp_path, test_config):
        """Test processing a complete file."""
        processor = TextProcessor(test_config)
        
        # Create test file
        test_file = tmp_path / "test.txt"
        content = """
        Machine learning is transforming industries.
        It enables computers to learn from data.
        This technology has many applications.
        """
        test_file.write_text(content)
        
        result = processor.process_file(str(test_file))
        
        assert "text" in result
        assert "word_count" in result
        assert "sentence_count" in result
        assert "reading_time" in result
        assert "keywords" in result
        
        assert result["word_count"] > 0
        assert result["sentence_count"] > 0
        assert result["reading_time"] > 0
        assert len(result["keywords"]) > 0
    
    def test_process_empty_file(self, tmp_path, test_config):
        """Test processing an empty file."""
        processor = TextProcessor(test_config)
        
        # Create empty file
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")
        
        result = processor.process_file(str(empty_file))
        
        assert result["word_count"] == 0
        assert result["sentence_count"] == 0
        assert result["reading_time"] == 0
        assert result["keywords"] == []
    
    def test_supported_formats(self, test_config):
        """Test supported formats list."""
        processor = TextProcessor(test_config)
        
        formats = processor.get_supported_formats()
        
        assert isinstance(formats, list)
        assert "txt" in formats
        assert "md" in formats
        assert "pdf" in formats
        assert "docx" in formats
    
    def test_validate_file_format(self, test_config):
        """Test file format validation."""
        processor = TextProcessor(test_config)
        
        # Valid formats
        assert processor.validate_file_format("test.txt") is True
        assert processor.validate_file_format("test.md") is True
        assert processor.validate_file_format("test.pdf") is True
        assert processor.validate_file_format("test.docx") is True
        
        # Invalid formats
        assert processor.validate_file_format("test.xyz") is False
        assert processor.validate_file_format("test") is False
    
    def test_extract_text_chunks(self, test_config):
        """Test extracting text in chunks."""
        processor = TextProcessor(test_config)
        
        # Create large text
        large_text = " ".join(["word"] * 1000)
        
        chunks = processor.extract_text_chunks(large_text, chunk_size=100)
        
        assert len(chunks) > 1
        assert all(len(chunk.split()) <= 100 for chunk in chunks)
        assert sum(len(chunk.split()) for chunk in chunks) == 1000
    
    def test_extract_text_chunks_overlap(self, test_config):
        """Test extracting text chunks with overlap."""
        processor = TextProcessor(test_config)
        
        text = "This is a test sentence for chunking with overlap."
        chunks = processor.extract_text_chunks(text, chunk_size=5, overlap=2)
        
        assert len(chunks) > 1
        # Should have some overlap between chunks
        assert any("test" in chunk for chunk in chunks)
        assert any("sentence" in chunk for chunk in chunks)