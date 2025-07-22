#!/usr/bin/env python3
"""
Test setup script for LexiLearn refactored implementation.
This script creates test files and performs basic validation.
"""

import asyncio
import os
from pathlib import Path
from config import config
from article_processor import ArticleProcessor
from logger import logger


def create_test_files():
    """Create test files for validation."""
    print("🧪 Creating test files...")
    
    # Create test article
    test_article = """The ubiquitous technology has revolutionized the way we communicate. 
However, some people remain skeptical about its pervasive influence on society.
The juxtaposition of traditional values and modern innovation creates interesting dilemmas."""

    with open("test_article.txt", "w", encoding="utf-8") as f:
        f.write(test_article)
    
    # Create known words
    known_words = ["the", "and", "we", "some", "people", "about", "its", "on", "of", "values"]
    with open("test_known_words.txt", "w", encoding="utf-8") as f:
        for word in known_words:
            f.write(f"{word}\n")
    
    # Create target words
    target_words = ["ubiquitous", "revolutionized", "skeptical", "pervasive", "juxtaposition", "dilemmas"]
    with open("test_target_words.txt", "w", encoding="utf-8") as f:
        for word in target_words:
            f.write(f"{word}\n")
    
    # Create empty learned words
    Path("test_learned_words.txt").touch()
    
    print("✅ Test files created successfully!")


async def test_configuration():
    """Test configuration loading."""
    print("🔧 Testing configuration...")
    
    try:
        config.validate()
        print("✅ Configuration is valid")
        
        # Print key configuration
        print(f"   API Model: {config.api.model}")
        print(f"   Batch Size: {config.processing.batch_size}")
        print(f"   Use Target Words: {config.processing.use_target_words}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    return True


async def test_vocabulary_manager():
    """Test vocabulary manager initialization."""
    print("📚 Testing vocabulary manager...")
    
    try:
        from vocabulary import VocabularyManager
        
        vocab_manager = VocabularyManager(
            "test_known_words.txt",
            "test_target_words.txt",
            "test_learned_words.txt"
        )
        
        await vocab_manager.initialize()
        
        stats = vocab_manager.get_statistics()
        print("✅ Vocabulary manager initialized")
        print(f"   Known words: {stats['known_words']}")
        print(f"   Target words: {stats['target_words']}")
        print(f"   Learned words: {stats['learned_words']}")
        
    except Exception as e:
        print(f"❌ Vocabulary manager error: {e}")
        return False
    
    return True


async def test_text_processor():
    """Test text processing functionality."""
    print("📝 Testing text processor...")
    
    try:
        from text_processor import TextProcessor
        
        processor = TextProcessor()
        
        # Test basic functionality
        test_sentence = "The beautiful cat sat on the comfortable mat."
        words = processor.extract_words_for_processing(
            test_sentence,
            lambda x: x in ["beautiful", "comfortable"]
        )
        
        print("✅ Text processor working")
        print(f"   Found words to process: {[w[0] for w in words]}")
        
    except Exception as e:
        print(f"❌ Text processor error: {e}")
        return False
    
    return True


async def test_article_processing():
    """Test the complete article processing pipeline."""
    print("🔄 Testing article processing...")
    
    try:
        # Skip if no API key
        if not config.api.api_key or config.api.api_key == "your-api-key-here":
            print("⚠️  Skipping API test - no API key configured")
            return True
        
        processor = ArticleProcessor()
        
        # Override config for testing
        config.files.input_article = "test_article.txt"
        config.files.known_words = "test_known_words.txt"
        config.files.target_words = "test_target_words.txt"
        config.files.learned_words = "test_learned_words.txt"
        config.files.output_article = "test_output.txt"
        
        # Process article
        processed, new_words, word_bank = await processor.process_article("test_article.txt")
        
        print("✅ Article processing completed")
        print(f"   Processed characters: {len(processed)}")
        print(f"   New words learned: {len(new_words)}")
        print(f"   Word bank entries: {len(word_bank)}")
        
        # Save results
        await processor.save_results(processed, word_bank, "test_output.txt")
        print("✅ Results saved to test_output.txt")
        
    except Exception as e:
        print(f"❌ Article processing error: {e}")
        return False
    
    return True


async def run_tests():
    """Run all tests."""
    print("🚀 Starting LexiLearn validation tests...\n")
    
    # Check if API key is configured
    if not config.api.api_key or config.api.api_key == "your-api-key-here":
        print("⚠️  Warning: No API key configured")
        print("   Set OPENAI_API_KEY environment variable for full testing")
        print("   Continuing with configuration tests...\n")
    
    # Create test files
    create_test_files()
    
    # Run tests
    tests = [
        test_configuration,
        test_vocabulary_manager,
        test_text_processor,
    ]
    
    # Only add API test if API key is configured
    if config.api.api_key and config.api.api_key != "your-api-key-here":
        tests.append(test_article_processing)
    else:
        print("⚠️  Skipping API test - no API key configured\n")
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("="*50)
    print("Test Summary")
    print("="*50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! LexiLearn is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the logs above.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    exit(0 if success else 1)