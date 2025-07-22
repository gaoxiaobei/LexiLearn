"""Unit tests for article processing functionality."""

import asyncio
import tempfile
from pathlib import Path
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from article_processor import ArticleProcessor


class TestArticleProcessor:
    """Test cases for ArticleProcessor class."""
    
    def test_article_processor_creation(self, test_config):
        """Test article processor creation."""
        processor = ArticleProcessor(test_config)
        
        assert processor.config == test_config
        assert processor.output_dir == Path("output")
        assert processor.vocabulary_manager is not None
        assert processor.translator is not None
        assert processor.text_processor is not None
    
    def test_article_processor_custom_output_dir(self, test_config, tmp_path):
        """Test article processor with custom output directory."""
        custom_dir = tmp_path / "custom_output"
        processor = ArticleProcessor(test_config, str(custom_dir))
        
        assert processor.output_dir == custom_dir
    
    @pytest.mark.asyncio
    async def test_process_single_article(self, test_config, tmp_path, sample_text):
        """Test processing a single article."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create test article file
        article_file = tmp_path / "test_article.txt"
        article_file.write_text(sample_text)
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[
            {
                "word": "artificial",
                "definition": "made or produced by human beings rather than occurring naturally",
                "translation": "人工的",
                "example": "artificial intelligence",
                "difficulty": "intermediate"
            }
        ])
        
        result = await processor.process_article(str(article_file))
        
        assert result["file_path"] == str(article_file)
        assert result["word_count"] > 0
        assert result["vocabulary_count"] > 0
        assert "artificial" in [v["word"] for v in result["vocabulary"]]
        
        # Check if output files were created
        output_files = list(tmp_path.glob("*.json"))
        assert len(output_files) > 0
    
    @pytest.mark.asyncio
    async def test_process_empty_article(self, test_config, tmp_path):
        """Test processing an empty article."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create empty article file
        article_file = tmp_path / "empty.txt"
        article_file.write_text("")
        
        result = await processor.process_article(str(article_file))
        
        assert result["word_count"] == 0
        assert result["vocabulary_count"] == 0
        assert result["vocabulary"] == []
    
    @pytest.mark.asyncio
    async def test_process_nonexistent_article(self, test_config, tmp_path):
        """Test processing a nonexistent article."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        with pytest.raises(FileNotFoundError):
            await processor.process_article("nonexistent.txt")
    
    @pytest.mark.asyncio
    async def test_process_unsupported_format(self, test_config, tmp_path):
        """Test processing an unsupported file format."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create unsupported file
        unsupported_file = tmp_path / "test.xyz"
        unsupported_file.write_text("test content")
        
        with pytest.raises(ValueError):
            await processor.process_article(str(unsupported_file))
    
    @pytest.mark.asyncio
    async def test_process_multiple_articles(self, test_config, tmp_path):
        """Test processing multiple articles."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create test articles
        articles = []
        for i in range(3):
            article_file = tmp_path / f"article_{i}.txt"
            article_file.write_text(f"This is article {i} about machine learning.")
            articles.append(str(article_file))
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[
            {
                "word": "machine",
                "definition": "a mechanical device",
                "translation": "机器",
                "example": "machine learning",
                "difficulty": "beginner"
            }
        ])
        
        results = await processor.process_articles(articles)
        
        assert len(results) == 3
        for result in results:
            assert result["word_count"] > 0
            assert result["vocabulary_count"] > 0
    
    @pytest.mark.asyncio
    async def test_process_directory(self, test_config, tmp_path):
        """Test processing a directory of articles."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create test directory structure
        articles_dir = tmp_path / "articles"
        articles_dir.mkdir()
        
        # Create test files
        (articles_dir / "article1.txt").write_text("First article content")
        (articles_dir / "article2.md").write_text("# Second article\n\nContent here")
        (articles_dir / "article3.txt").write_text("Third article content")
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[
            {
                "word": "content",
                "definition": "the material dealt with in a speech or piece of writing",
                "translation": "内容",
                "example": "article content",
                "difficulty": "beginner"
            }
        ])
        
        results = await processor.process_directory(str(articles_dir))
        
        assert len(results) == 3
        assert all(result["file_path"].endswith((".txt", ".md")) for result in results)
    
    @pytest.mark.asyncio
    async def test_process_directory_recursive(self, test_config, tmp_path):
        """Test processing directory recursively."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create nested directory structure
        nested_dir = tmp_path / "articles" / "subfolder"
        nested_dir.mkdir(parents=True)
        
        # Create files in different levels
        (tmp_path / "articles" / "root.txt").write_text("Root article")
        (nested_dir / "nested.txt").write_text("Nested article")
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[
            {
                "word": "article",
                "definition": "a piece of writing",
                "translation": "文章",
                "example": "article content",
                "difficulty": "beginner"
            }
        ])
        
        results = await processor.process_directory(str(tmp_path / "articles"), recursive=True)
        
        assert len(results) == 2
    
    @pytest.mark.asyncio
    async def test_process_directory_non_recursive(self, test_config, tmp_path):
        """Test processing directory non-recursively."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create nested directory structure
        nested_dir = tmp_path / "articles" / "subfolder"
        nested_dir.mkdir(parents=True)
        
        # Create files
        (tmp_path / "articles" / "root.txt").write_text("Root article")
        (nested_dir / "nested.txt").write_text("Nested article")
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[])
        
        results = await processor.process_directory(str(tmp_path / "articles"), recursive=False)
        
        assert len(results) == 1  # Only root level
    
    @pytest.mark.asyncio
    async def test_save_results(self, test_config, tmp_path):
        """Test saving processing results."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create test result
        result = {
            "file_path": str(tmp_path / "test.txt"),
            "word_count": 100,
            "vocabulary_count": 5,
            "vocabulary": [
                {"word": "test", "definition": "test definition", "translation": "测试"}
            ]
        }
        
        output_file = tmp_path / "results.json"
        processor._save_results([result], str(output_file))
        
        assert output_file.exists()
        
        # Verify saved content
        import json
        saved_data = json.loads(output_file.read_text())
        assert len(saved_data) == 1
        assert saved_data[0]["word_count"] == 100
    
    @pytest.mark.asyncio
    async def test_vocabulary_deduplication(self, test_config, tmp_path):
        """Test vocabulary deduplication across articles."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create articles with overlapping vocabulary
        article1 = tmp_path / "article1.txt"
        article1.write_text("Machine learning is important.")
        
        article2 = tmp_path / "article2.txt"
        article2.write_text("Machine learning applications are growing.")
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[
            {
                "word": "machine",
                "definition": "a mechanical device",
                "translation": "机器",
                "example": "machine learning",
                "difficulty": "beginner"
            },
            {
                "word": "learning",
                "definition": "acquiring knowledge",
                "translation": "学习",
                "example": "machine learning",
                "difficulty": "beginner"
            }
        ])
        
        results = await processor.process_articles([str(article1), str(article2)])
        
        # Check that vocabulary is properly tracked
        total_vocab = set()
        for result in results:
            for vocab in result["vocabulary"]:
                total_vocab.add(vocab["word"])
        
        assert len(total_vocab) >= 2
    
    @pytest.mark.asyncio
    async def test_error_handling_in_processing(self, test_config, tmp_path):
        """Test error handling during article processing."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create test article
        article_file = tmp_path / "test.txt"
        article_file.write_text("Test content")
        
        # Mock translator to raise an error
        processor.translator.translate_text = AsyncMock(side_effect=Exception("API Error"))
        
        with pytest.raises(Exception):
            await processor.process_article(str(article_file))
    
    @pytest.mark.asyncio
    async def test_progress_callback(self, test_config, tmp_path):
        """Test progress callback functionality."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create test articles
        articles = []
        for i in range(3):
            article_file = tmp_path / f"article_{i}.txt"
            article_file.write_text(f"Article {i}")
            articles.append(str(article_file))
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[])
        
        progress_calls = []
        
        def progress_callback(current, total):
            progress_calls.append((current, total))
        
        await processor.process_articles(articles, progress_callback=progress_callback)
        
        assert len(progress_calls) == 3
        assert progress_calls[0] == (1, 3)
        assert progress_calls[1] == (2, 3)
        assert progress_calls[2] == (3, 3)
    
    @pytest.mark.asyncio
    async def test_generate_summary(self, test_config, tmp_path):
        """Test article summary generation."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create test article
        article_file = tmp_path / "test.txt"
        article_file.write_text("This is a long article about machine learning and artificial intelligence.")
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="关于机器学习和人工智能的长篇文章")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[])
        
        result = await processor.process_article(str(article_file))
        
        assert "summary" in result or "translated_summary" in result
    
    def test_get_supported_formats(self, test_config):
        """Test getting supported file formats."""
        processor = ArticleProcessor(test_config)
        
        formats = processor.get_supported_formats()
        
        assert isinstance(formats, list)
        assert "txt" in formats
        assert "md" in formats
        assert "pdf" in formats
        assert "docx" in formats
    
    @pytest.mark.asyncio
    async def test_cleanup_temp_files(self, test_config, tmp_path):
        """Test cleanup of temporary files."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create test article
        article_file = tmp_path / "test.txt"
        article_file.write_text("Test content")
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[])
        
        await processor.process_article(str(article_file))
        
        # Check that no temporary files are left
        temp_files = list(tmp_path.glob("*.tmp"))
        assert len(temp_files) == 0
    
    @pytest.mark.asyncio
    async def test_batch_processing_with_errors(self, test_config, tmp_path):
        """Test batch processing with some files causing errors."""
        processor = ArticleProcessor(test_config, str(tmp_path))
        
        # Create mix of valid and invalid files
        valid_file = tmp_path / "valid.txt"
        valid_file.write_text("Valid content")
        
        invalid_file = tmp_path / "invalid.xyz"
        invalid_file.write_text("Invalid content")
        
        # Mock translator responses
        processor.translator.translate_text = AsyncMock(return_value="翻译后的文本")
        processor.translator.extract_vocabulary = AsyncMock(return_value=[])
        
        results = await processor.process_articles([str(valid_file), str(invalid_file)])
        
        # Should process valid files and handle invalid ones gracefully
        assert len(results) >= 1
        assert all(result["file_path"].endswith(".txt") for result in results)