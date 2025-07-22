"""Unit tests for vocabulary management."""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any
from unittest.mock import patch

import pytest

from vocabulary import VocabularyManager, VocabularyItem


class TestVocabularyItem:
    """Test cases for VocabularyItem class."""
    
    def test_vocabulary_item_creation(self):
        """Test vocabulary item creation with all fields."""
        item = VocabularyItem(
            word="algorithm",
            definition="a process or set of rules to be followed",
            translation="算法",
            example="The algorithm processed the data efficiently.",
            difficulty="intermediate",
            frequency=0.75,
            part_of_speech="noun",
            phonetic="/ˈælɡərɪðəm/",
            synonyms=["procedure", "method", "process"]
        )
        
        assert item.word == "algorithm"
        assert item.definition == "a process or set of rules to be followed"
        assert item.translation == "算法"
        assert item.example == "The algorithm processed the data efficiently."
        assert item.difficulty == "intermediate"
        assert item.frequency == 0.75
        assert item.part_of_speech == "noun"
        assert item.phonetic == "/ˈælɡərɪðəm/"
        assert item.synonyms == ["procedure", "method", "process"]
    
    def test_vocabulary_item_minimal(self):
        """Test vocabulary item creation with minimal fields."""
        item = VocabularyItem(
            word="hello",
            definition="used as a greeting",
            translation="你好",
            example="Hello, how are you?"
        )
        
        assert item.word == "hello"
        assert item.definition == "used as a greeting"
        assert item.translation == "你好"
        assert item.example == "Hello, how are you?"
        assert item.difficulty == "beginner"
        assert item.frequency == 0.5
        assert item.part_of_speech is None
        assert item.phonetic is None
        assert item.synonyms == []
    
    def test_vocabulary_item_to_dict(self):
        """Test vocabulary item serialization to dictionary."""
        item = VocabularyItem(
            word="test",
            definition="a procedure intended to establish quality",
            translation="测试",
            example="This is a test example.",
            difficulty="intermediate",
            frequency=0.8
        )
        
        item_dict = item.model_dump()
        
        assert item_dict["word"] == "test"
        assert item_dict["definition"] == "a procedure intended to establish quality"
        assert item_dict["translation"] == "测试"
        assert item_dict["example"] == "This is a test example."
        assert item_dict["difficulty"] == "intermediate"
        assert item_dict["frequency"] == 0.8
    
    def test_vocabulary_item_from_dict(self):
        """Test vocabulary item creation from dictionary."""
        data = {
            "word": "sophisticated",
            "definition": "having a refined knowledge",
            "translation": "复杂的，老练的",
            "example": "The system uses sophisticated technology.",
            "difficulty": "advanced",
            "frequency": 0.65,
            "part_of_speech": "adjective"
        }
        
        item = VocabularyItem(**data)
        
        assert item.word == "sophisticated"
        assert item.definition == "having a refined knowledge"
        assert item.translation == "复杂的，老练的"
        assert item.example == "The system uses sophisticated technology."
        assert item.difficulty == "advanced"
        assert item.frequency == 0.65
        assert item.part_of_speech == "adjective"
    
    def test_vocabulary_item_validation(self):
        """Test vocabulary item validation."""
        # Test empty word
        with pytest.raises(ValueError):
            VocabularyItem(
                word="",
                definition="test definition",
                translation="测试",
                example="test example"
            )
        
        # Test empty definition
        with pytest.raises(ValueError):
            VocabularyItem(
                word="test",
                definition="",
                translation="测试",
                example="test example"
            )
        
        # Test empty translation
        with pytest.raises(ValueError):
            VocabularyItem(
                word="test",
                definition="test definition",
                translation="",
                example="test example"
            )
        
        # Test empty example
        with pytest.raises(ValueError):
            VocabularyItem(
                word="test",
                definition="test definition",
                translation="测试",
                example=""
            )
        
        # Test invalid difficulty
        with pytest.raises(ValueError):
            VocabularyItem(
                word="test",
                definition="test definition",
                translation="测试",
                example="test example",
                difficulty="invalid"
            )
        
        # Test invalid frequency
        with pytest.raises(ValueError):
            VocabularyItem(
                word="test",
                definition="test definition",
                translation="测试",
                example="test example",
                frequency=1.5
            )
        
        with pytest.raises(ValueError):
            VocabularyItem(
                word="test",
                definition="test definition",
                translation="测试",
                example="test example",
                frequency=-0.1
            )


class TestVocabularyManager:
    """Test cases for VocabularyManager class."""
    
    def test_vocabulary_manager_creation(self, tmp_path):
        """Test vocabulary manager creation."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        assert manager.vocabulary_file == str(vocab_file)
        assert manager.vocabulary == {}
    
    def test_add_word(self, tmp_path):
        """Test adding a word to vocabulary."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        item = VocabularyItem(
            word="algorithm",
            definition="a process or set of rules to be followed",
            translation="算法",
            example="The algorithm processed the data efficiently."
        )
        
        manager.add_word(item)
        
        assert "algorithm" in manager.vocabulary
        assert manager.vocabulary["algorithm"].word == "algorithm"
        assert manager.vocabulary["algorithm"].translation == "算法"
    
    def test_add_duplicate_word(self, tmp_path):
        """Test adding a duplicate word."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        item1 = VocabularyItem(
            word="test",
            definition="first definition",
            translation="测试1",
            example="first example"
        )
        
        item2 = VocabularyItem(
            word="test",
            definition="second definition",
            translation="测试2",
            example="second example"
        )
        
        manager.add_word(item1)
        manager.add_word(item2)
        
        # Should update the existing word
        assert len(manager.vocabulary) == 1
        assert manager.vocabulary["test"].definition == "second definition"
        assert manager.vocabulary["test"].translation == "测试2"
    
    def test_get_word(self, tmp_path):
        """Test getting a word from vocabulary."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        item = VocabularyItem(
            word="hello",
            definition="used as a greeting",
            translation="你好",
            example="Hello, how are you?"
        )
        
        manager.add_word(item)
        
        retrieved = manager.get_word("hello")
        assert retrieved is not None
        assert retrieved.word == "hello"
        assert retrieved.translation == "你好"
        
        # Test non-existent word
        non_existent = manager.get_word("nonexistent")
        assert non_existent is None
    
    def test_remove_word(self, tmp_path):
        """Test removing a word from vocabulary."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        item = VocabularyItem(
            word="test",
            definition="test definition",
            translation="测试",
            example="test example"
        )
        
        manager.add_word(item)
        assert "test" in manager.vocabulary
        
        manager.remove_word("test")
        assert "test" not in manager.vocabulary
        
        # Test removing non-existent word
        manager.remove_word("nonexistent")  # Should not raise
    
    def test_list_words(self, tmp_path):
        """Test listing all words in vocabulary."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        # Add multiple words
        words = ["hello", "world", "test", "algorithm"]
        for word in words:
            item = VocabularyItem(
                word=word,
                definition=f"definition of {word}",
                translation=f"翻译{word}",
                example=f"example of {word}"
            )
            manager.add_word(item)
        
        word_list = manager.list_words()
        assert len(word_list) == 4
        assert set(word_list) == set(words)
    
    def test_search_words(self, tmp_path):
        """Test searching words in vocabulary."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        # Add test words
        words = [
            VocabularyItem(
                word="algorithm",
                definition="a process or set of rules",
                translation="算法",
                example="algorithm example",
                difficulty="intermediate"
            ),
            VocabularyItem(
                word="hello",
                definition="used as a greeting",
                translation="你好",
                example="hello example",
                difficulty="beginner"
            ),
            VocabularyItem(
                word="sophisticated",
                definition="having refined knowledge",
                translation="复杂的",
                example="sophisticated example",
                difficulty="advanced"
            )
        ]
        
        for word in words:
            manager.add_word(word)
        
        # Test search by word
        results = manager.search_words(query="algo")
        assert len(results) == 1
        assert results[0].word == "algorithm"
        
        # Test search by definition
        results = manager.search_words(query="greeting")
        assert len(results) == 1
        assert results[0].word == "hello"
        
        # Test search by translation
        results = manager.search_words(query="算法")
        assert len(results) == 1
        assert results[0].word == "algorithm"
        
        # Test search by difficulty
        results = manager.search_words(difficulty="beginner")
        assert len(results) == 1
        assert results[0].word == "hello"
        
        # Test search with no results
        results = manager.search_words(query="nonexistent")
        assert len(results) == 0
    
    def test_filter_by_difficulty(self, tmp_path):
        """Test filtering words by difficulty."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        # Add words with different difficulties
        difficulties = ["beginner", "intermediate", "advanced", "beginner"]
        words = ["word1", "word2", "word3", "word4"]
        
        for word, difficulty in zip(words, difficulties):
            item = VocabularyItem(
                word=word,
                definition=f"definition of {word}",
                translation=f"翻译{word}",
                example=f"example of {word}",
                difficulty=difficulty
            )
            manager.add_word(item)
        
        # Test filtering
        beginner_words = manager.filter_by_difficulty("beginner")
        assert len(beginner_words) == 2
        assert all(word.difficulty == "beginner" for word in beginner_words)
        
        intermediate_words = manager.filter_by_difficulty("intermediate")
        assert len(intermediate_words) == 1
        assert intermediate_words[0].word == "word2"
        
        advanced_words = manager.filter_by_difficulty("advanced")
        assert len(advanced_words) == 1
        assert advanced_words[0].word == "word3"
    
    def test_get_statistics(self, tmp_path):
        """Test getting vocabulary statistics."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        # Add test words
        words = [
            VocabularyItem(
                word="hello",
                definition="greeting",
                translation="你好",
                example="hello",
                difficulty="beginner",
                frequency=0.9
            ),
            VocabularyItem(
                word="world",
                definition="earth",
                translation="世界",
                example="world",
                difficulty="beginner",
                frequency=0.8
            ),
            VocabularyItem(
                word="algorithm",
                definition="process",
                translation="算法",
                example="algorithm",
                difficulty="intermediate",
                frequency=0.7
            )
        ]
        
        for word in words:
            manager.add_word(word)
        
        stats = manager.get_statistics()
        
        assert stats["total_words"] == 3
        assert stats["beginner_words"] == 2
        assert stats["intermediate_words"] == 1
        assert stats["advanced_words"] == 0
        assert stats["average_frequency"] == pytest.approx(0.8, 0.01)
    
    def test_save_and_load(self, tmp_path):
        """Test saving and loading vocabulary."""
        vocab_file = tmp_path / "test_vocabulary.json"
        manager = VocabularyManager(str(vocab_file))
        
        # Add some words
        words = [
            VocabularyItem(
                word="test1",
                definition="definition1",
                translation="翻译1",
                example="example1"
            ),
            VocabularyItem(
                word="test2",
                definition="definition2",
                translation="翻译2",
                example="example2"
            )
        ]
        
        for word in words:
            manager.add_word(word)
        
        # Save to file
        manager.save()
        assert vocab_file.exists()
        
        # Create new manager and load
        new_manager = VocabularyManager(str(vocab_file))
        new_manager.load()
        
        assert len(new_manager.vocabulary) == 2
        assert "test1" in new_manager.vocabulary
        assert "test2" in new_manager.vocabulary
        assert new_manager.vocabulary["test1"].translation == "翻译1"
        assert new_manager.vocabulary["test2"].translation == "翻译2"
    
    def test_load_nonexistent_file(self, tmp_path):
        """Test loading from nonexistent file."""
        vocab_file = tmp_path / "nonexistent.json"
        manager = VocabularyManager(str(vocab_file))
        
        # Should not raise exception, just start with empty vocabulary
        manager.load()
        assert manager.vocabulary == {}
    
    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON file."""
        vocab_file = tmp_path / "invalid.json"
        vocab_file.write_text("invalid json content")
        
        manager = VocabularyManager(str(vocab_file))
        
        # Should handle invalid JSON gracefully
        manager.load()
        assert manager.vocabulary == {}
    
    def test_export_to_csv(self, tmp_path):
        """Test exporting vocabulary to CSV."""
        vocab_file = tmp_path / "test_vocabulary.json"
        csv_file = tmp_path / "vocabulary.csv"
        
        manager = VocabularyManager(str(vocab_file))
        
        # Add test word
        item = VocabularyItem(
            word="test",
            definition="test definition",
            translation="测试",
            example="test example"
        )
        manager.add_word(item)
        
        # Export to CSV
        manager.export_to_csv(str(csv_file))
        
        assert csv_file.exists()
        csv_content = csv_file.read_text()
        
        assert "test" in csv_content
        assert "test definition" in csv_content
        assert "测试" in csv_content
    
    def test_import_from_csv(self, tmp_path):
        """Test importing vocabulary from CSV."""
        vocab_file = tmp_path / "test_vocabulary.json"
        csv_file = tmp_path / "import.csv"
        
        # Create CSV content
        csv_content = """word,definition,translation,example,difficulty
hello,used as a greeting,你好,Hello world,beginner
world,the earth,世界,Hello world,beginner"""
        
        csv_file.write_text(csv_content)
        
        manager = VocabularyManager(str(vocab_file))
        manager.import_from_csv(str(csv_file))
        
        assert len(manager.vocabulary) == 2
        assert "hello" in manager.vocabulary
        assert "world" in manager.vocabulary
        assert manager.vocabulary["hello"].translation == "你好"
        assert manager.vocabulary["world"].translation == "世界"
    
    def test_backup_and_restore(self, tmp_path):
        """Test vocabulary backup and restore."""
        vocab_file = tmp_path / "test_vocabulary.json"
        backup_file = tmp_path / "backup.json"
        
        manager = VocabularyManager(str(vocab_file))
        
        # Add test word
        item = VocabularyItem(
            word="backup_test",
            definition="backup test",
            translation="备份测试",
            example="backup example"
        )
        manager.add_word(item)
        
        # Save and backup
        manager.save()
        manager.backup(str(backup_file))
        
        assert backup_file.exists()
        
        # Modify original
        manager.vocabulary = {}
        manager.save()
        
        # Restore from backup
        manager.restore(str(backup_file))
        
        assert len(manager.vocabulary) == 1
        assert "backup_test" in manager.vocabulary
        assert manager.vocabulary["backup_test"].translation == "备份测试"