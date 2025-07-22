"""End-to-end integration tests for LexiLearn."""

import asyncio
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List

import pytest
from aioresponses import aioresponses

from article_processor import ArticleProcessor
from config import load_config
from vocabulary import VocabularyManager


class TestEndToEndProcessing:
    """End-to-end integration tests."""
    
    @pytest.mark.asyncio
    async def test_complete_article_processing_workflow(self, tmp_path):
        """Test complete article processing workflow."""
        # Setup configuration
        config = load_config()
        config.openai_api_key = "test-key"
        
        # Create test article
        article_file = tmp_path / "test_article.txt"
        article_content = """
        Machine learning is a subset of artificial intelligence that focuses on the development 
        of algorithms and statistical models that enable computer systems to improve their 
        performance on a specific task through experience, without being explicitly programmed.
        
        Deep learning, a subset of machine learning, uses neural networks with multiple layers 
        to progressively extract higher-level features from raw input. This approach has led 
        to breakthroughs in fields such as computer vision and natural language processing.
        """
        article_file.write_text(article_content)
        
        # Create article processor
        processor = ArticleProcessor(config, str(tmp_path / "output"))
        
        # Mock OpenAI API responses
        with aioresponses() as mocked:
            # Mock translation response
            translation_response = {
                "id": "chatcmpl-translate",
                "object": "chat.completion",
                "created": 1677652288,
                "model": "gpt-3.5-turbo-0613",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "机器学习是人工智能的一个子集，专注于开发算法和统计模型，使计算机系统能够通过经验提高在特定任务上的表现，而无需明确编程。"
                    },
                    "finish_reason": "stop"
                }]
            }
            
            # Mock vocabulary extraction response
            vocabulary_response = {
                "id": "chatcmpl-vocab",
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
                                    "word": "machine learning",
                                    "definition": "a subset of artificial intelligence that enables systems to learn from data",
                                    "translation": "机器学习",
                                    "example": "Machine learning algorithms can improve over time.",
                                    "difficulty": "intermediate"
                                },
                                {
                                    "word": "algorithm",
                                    "definition": "a process or set of rules to be followed in calculations",
                                    "translation": "算法",
                                    "example": "The algorithm processed the data efficiently.",
                                    "difficulty": "intermediate"
                                },
                                {
                                    "word": "neural networks",
                                    "definition": "computing systems inspired by biological neural networks",
                                    "translation": "神经网络",
                                    "example": "Neural networks are used in deep learning.",
                                    "difficulty": "advanced"
                                }
                            ]
                        })
                    },
                    "finish_reason": "stop"
                }]
            }
            
            mocked.post("https://api.openai.com/v1/chat/completions", status=200, payload=translation_response)
            mocked.post("https://api.openai.com/v1/chat/completions", status=200, payload=vocabulary_response)
            
            # Process the article
            result = await processor.process_article(str(article_file))
        
        # Verify results
        assert result["file_path"] == str(article_file)
        assert result["word_count"] > 50
        assert result["vocabulary_count"] == 3
        assert len(result["vocabulary"]) == 3
        
        # Check vocabulary items
        vocab_words = [v["word"] for v in result["vocabulary"]]
        assert "machine learning" in vocab_words
        assert "algorithm" in vocab_words
        assert "neural networks" in vocab_words
        
        # Check output files
        output_files = list((tmp_path / "output").glob("*"))
        assert len(output_files) >= 2  # JSON and possibly other formats
    
    @pytest.mark.asyncio
    async def test_batch_processing_multiple_articles(self, tmp_path):
        """Test batch processing of multiple articles."""
        config = load_config()
        config.openai_api_key = "test-key"
        
        # Create multiple test articles
        articles = []
        for i in range(3):
            article_file = tmp_path / f"article_{i}.txt"
            article_file.write_text(f"""
            Article {i} about technology and innovation.
            This article discusses various aspects of modern technology.
            Key concepts include artificial intelligence and data science.
            """)
            articles.append(str(article_file))
        
        processor = ArticleProcessor(config, str(tmp_path / "output"))
        
        # Mock API responses
        with aioresponses() as mocked:
            # Mock responses for all articles
            for _ in range(6):  # 3 articles * 2 API calls each
                mocked.post(
                    "https://api.openai.com/v1/chat/completions",
                    status=200,
                    payload={
                        "id": "chatcmpl-batch",
                        "object": "chat.completion",
                        "created": 1677652288,
                        "model": "gpt-3.5-turbo-0613",
                        "choices": [{
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": "翻译内容" if _ % 2 == 0 else json.dumps({
                                    "vocabulary": [
                                        {
                                            "word": "technology",
                                            "definition": "the application of scientific knowledge",
                                            "translation": "技术",
                                            "example": "modern technology",
                                            "difficulty": "beginner"
                                        }
                                    ]
                                })
                            },
                            "finish_reason": "stop"
                        }]
                    }
                )
            
            # Process all articles
            results = await processor.process_articles(articles)
        
        assert len(results) == 3
        for result in results:
            assert result["word_count"] > 0
            assert result["vocabulary_count"] >= 1
    
    @pytest.mark.asyncio
    async def test_directory_processing_with_subdirectories(self, tmp_path):
        """Test processing directories with nested structure."""
        config = load_config()
        config.openai_api_key = "test-key"
        
        # Create nested directory structure
        base_dir = tmp_path / "articles"
        base_dir.mkdir()
        
        # Create files in different directories
        (base_dir / "tech.txt").write_text("Technology article content")
        (base_dir / "science.txt").write_text("Science article content")
        
        sub_dir = base_dir / "subfolder"
        sub_dir.mkdir()
        (sub_dir / "nested.txt").write_text("Nested article content")
        
        processor = ArticleProcessor(config, str(tmp_path / "output"))
        
        # Mock API responses
        with aioresponses() as mocked:
            for _ in range(6):  # 3 files * 2 API calls each
                mocked.post(
                    "https://api.openai.com/v1/chat/completions",
                    status=200,
                    payload={
                        "id": "chatcmpl-dir",
                        "object": "chat.completion",
                        "created": 1677652288,
                        "model": "gpt-3.5-turbo-0613",
                        "choices": [{
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": "翻译" if _ % 2 == 0 else json.dumps({
                                    "vocabulary": [{"word": "article", "definition": "a piece of writing", "translation": "文章", "difficulty": "beginner"}]
                                })
                            },
                            "finish_reason": "stop"
                        }]
                    }
                )
            
            # Process directory recursively
            results = await processor.process_directory(str(base_dir), recursive=True)
        
        assert len(results) == 3
        file_names = [Path(r["file_path"]).name for r in results]
        assert "tech.txt" in file_names
        assert "science.txt" in file_names
        assert "nested.txt" in file_names
    
    @pytest.mark.asyncio
    async def test_vocabulary_persistence_across_sessions(self, tmp_path):
        """Test vocabulary persistence across processing sessions."""
        config = load_config()
        config.openai_api_key = "test-key"
        config.vocabulary_file = str(tmp_path / "vocabulary.json")
        
        # Create vocabulary manager
        vocab_manager = VocabularyManager(config.vocabulary_file)
        
        # Create test articles
        article1 = tmp_path / "article1.txt"
        article1.write_text("First article about machine learning")
        
        article2 = tmp_path / "article2.txt"
        article2.write_text("Second article about machine learning and AI")
        
        processor1 = ArticleProcessor(config, str(tmp_path / "output1"))
        processor2 = ArticleProcessor(config, str(tmp_path / "output2"))
        
        # Mock API responses
        with aioresponses() as mocked:
            for _ in range(4):  # 2 articles * 2 API calls each
                mocked.post(
                    "https://api.openai.com/v1/chat/completions",
                    status=200,
                    payload={
                        "id": "chatcmpl-persist",
                        "object": "chat.completion",
                        "created": 1677652288,
                        "model": "gpt-3.5-turbo-0613",
                        "choices": [{
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": "翻译" if _ % 2 == 0 else json.dumps({
                                    "vocabulary": [
                                        {"word": "machine", "definition": "a device", "translation": "机器", "difficulty": "beginner"},
                                        {"word": "learning", "definition": "acquiring knowledge", "translation": "学习", "difficulty": "beginner"}
                                    ]
                                })
                            },
                            "finish_reason": "stop"
                        }]
                    }
                )
            
            # Process first article
            result1 = await processor1.process_article(str(article1))
            
            # Process second article
            result2 = await processor2.process_article(str(article2))
        
        # Check vocabulary persistence
        vocab_manager.load()
        vocab_words = list(vocab_manager.vocabulary.keys())
        
        assert "machine" in vocab_words
        assert "learning" in vocab_words
        
        # Check that vocabulary is cumulative
        assert len(vocab_words) >= 2
    
    @pytest.mark.asyncio
    async def test_error_recovery_and_continuation(self, tmp_path):
        """Test error recovery and continuation in batch processing."""
        config = load_config()
        config.openai_api_key = "test-key"
        
        # Create test articles
        articles = []
        for i in range(5):
            article_file = tmp_path / f"article_{i}.txt"
            article_file.write_text(f"Article {i} content")
            articles.append(str(article_file))
        
        processor = ArticleProcessor(config, str(tmp_path / "output"))
        
        # Mock API responses with some failures
        call_count = 0
        
        def mock_api_response(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            if call_count <= 2:  # First article fails
                raise Exception("API Error")
            else:  # Subsequent articles succeed
                return "翻译内容" if call_count % 2 == 1 else [
                    {"word": "article", "definition": "a piece of writing", "translation": "文章", "difficulty": "beginner"}
                ]
        
        processor.translator.translate_text = AsyncMock(side_effect=mock_api_response)
        processor.translator.extract_vocabulary = AsyncMock(side_effect=mock_api_response)
        
        # Process articles with error handling
        successful_results = []
        failed_files = []
        
        for article in articles:
            try:
                result = await processor.process_article(article)
                successful_results.append(result)
            except Exception as e:
                failed_files.append((article, str(e)))
        
        # Should have some successful results despite initial failures
        assert len(successful_results) > 0
        assert len(failed_files) >= 1
    
    @pytest.mark.asyncio
    async def test_performance_with_large_articles(self, tmp_path):
        """Test performance with large articles."""
        config = load_config()
        config.openai_api_key = "test-key"
        
        # Create large article
        large_article = tmp_path / "large.txt"
        large_content = " ".join(["word"] * 1000) + " This is additional content about technology and innovation."
        large_article.write_text(large_content)
        
        processor = ArticleProcessor(config, str(tmp_path / "output"))
        
        # Mock API responses
        with aioresponses() as mocked:
            mocked.post(
                "https://api.openai.com/v1/chat/completions",
                status=200,
                payload={
                    "id": "chatcmpl-large",
                    "object": "chat.completion",
                    "created": 1677652288,
                    "model": "gpt-3.5-turbo-0613",
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "大型文章翻译"
                        },
                        "finish_reason": "stop"
                    }]
                }
            )
            
            mocked.post(
                "https://api.openai.com/v1/chat/completions",
                status=200,
                payload={
                    "id": "chatcmpl-vocab-large",
                    "object": "chat.completion",
                    "created": 1677652290,
                    "model": "gpt-3.5-turbo-0613",
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": json.dumps({
                                "vocabulary": [
                                    {"word": "technology", "definition": "applied science", "translation": "技术", "difficulty": "beginner"},
                                    {"word": "innovation", "definition": "new method or idea", "translation": "创新", "difficulty": "intermediate"}
                                ]
                            })
                        },
                        "finish_reason": "stop"
                    }]
                }
            )
            
            # Process large article
            start_time = asyncio.get_event_loop().time()
            result = await processor.process_article(str(large_article))
            end_time = asyncio.get_event_loop().time()
            
            processing_time = end_time - start_time
        
        assert result["word_count"] == 1008  # 1000 words + additional content
        assert result["vocabulary_count"] == 2
        assert processing_time < 10  # Should complete within reasonable time
    
    @pytest.mark.asyncio
    async def test_configuration_validation_integration(self, tmp_path):
        """Test configuration validation in integration context."""
        from config import Config
        
        # Test with invalid configuration
        with pytest.raises(Exception):
            invalid_config = Config(openai_api_key="")
            ArticleProcessor(invalid_config, str(tmp_path / "output"))
        
        # Test with valid configuration
        valid_config = Config(openai_api_key="test-key")
        processor = ArticleProcessor(valid_config, str(tmp_path / "output"))
        assert processor is not None


class TestConfigurationLoading:
    """Integration tests for configuration loading."""
    
    def test_env_file_loading(self, tmp_path):
        """Test loading configuration from .env file."""
        env_file = tmp_path / ".env"
        env_content = """
        OPENAI_API_KEY=test-env-key
        OPENAI_MODEL=gpt-4
        MAX_TOKENS=2000
        LOG_LEVEL=DEBUG
        """
        env_file.write_text(env_content)
        
        # Temporarily change directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            config = load_config()
            assert config.openai_api_key == "test-env-key"
            assert config.openai_model == "gpt-4"
            assert config.max_tokens == 2000
            assert config.log_level == "DEBUG"
        finally:
            os.chdir(original_cwd)
    
    def test_json_config_loading(self, tmp_path):
        """Test loading configuration from JSON file."""
        config_file = tmp_path / "config.json"
        config_data = {
            "openai_api_key": "test-json-key",
            "openai_model": "gpt-3.5-turbo",
            "max_tokens": 1500,
            "temperature": 0.8
        }
        config_file.write_text(json.dumps(config_data))
        
        config = load_config(str(config_file))
        assert config.openai_api_key == "test-json-key"
        assert config.openai_model == "gpt-3.5-turbo"
        assert config.max_tokens == 1500
        assert config.temperature == 0.8


class TestVocabularyIntegration:
    """Integration tests for vocabulary management."""
    
    def test_vocabulary_file_creation(self, tmp_path):
        """Test automatic vocabulary file creation."""
        vocab_file = tmp_path / "test_vocabulary.json"
        
        # Create vocabulary manager
        vocab_manager = VocabularyManager(str(vocab_file))
        
        # Add some vocabulary
        from vocabulary import VocabularyItem
        item = VocabularyItem(
            word="test",
            definition="test definition",
            translation="测试",
            example="test example"
        )
        vocab_manager.add_word(item)
        vocab_manager.save()
        
        assert vocab_file.exists()
        
        # Verify content
        with open(vocab_file) as f:
            data = json.load(f)
            assert "test" in data
            assert data["test"]["translation"] == "测试"
    
    def test_vocabulary_backup_creation(self, tmp_path):
        """Test automatic backup creation."""
        vocab_file = tmp_path / "vocabulary.json"
        backup_file = tmp_path / "vocabulary_backup.json"
        
        # Create initial vocabulary
        vocab_manager = VocabularyManager(str(vocab_file))
        from vocabulary import VocabularyItem
        
        item = VocabularyItem(
            word="backup_test",
            definition="backup test",
            translation="备份测试",
            example="backup example"
        )
        vocab_manager.add_word(item)
        vocab_manager.save()
        
        # Create backup
        vocab_manager.backup(str(backup_file))
        
        assert backup_file.exists()
        
        # Verify backup content
        with open(backup_file) as f:
            data = json.load(f)
            assert "backup_test" in data