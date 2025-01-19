import unittest
from main import VocabularyManager, get_word_base_form, is_proper_noun
import tempfile
import os

class TestVocabularyManager(unittest.TestCase):
    def setUp(self):
        # 创建临时文件作为词汇表
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"hello\nworld\n")
        self.temp_file.close()
        self.vocab_manager = VocabularyManager(self.temp_file.name)

    def tearDown(self):
        # 清理临时文件
        os.unlink(self.temp_file.name)

    def test_load_known_words(self):
        self.assertEqual(len(self.vocab_manager.known_words), 2)
        self.assertTrue("hello" in self.vocab_manager.known_words)
        self.assertTrue("world" in self.vocab_manager.known_words)

    def test_is_known_word(self):
        self.assertTrue(self.vocab_manager.is_known_word("hello"))
        self.assertFalse(self.vocab_manager.is_known_word("unknown"))

    def test_add_words_batch(self):
        new_words = {"test", "new"}
        self.vocab_manager.add_words_batch(new_words)
        self.assertTrue(self.vocab_manager.is_known_word("test"))
        self.assertTrue(self.vocab_manager.is_known_word("new"))

class TestWordProcessing(unittest.TestCase):
    def test_word_base_form(self):
        self.assertEqual(get_word_base_form("running"), "run")
        self.assertEqual(get_word_base_form("cities"), "city")
        self.assertEqual(get_word_base_form("better"), "good")

    def test_proper_noun_detection(self):
        self.assertTrue(is_proper_noun("John", "John is a good student"))
        self.assertFalse(is_proper_noun("student", "John is a good student"))

if __name__ == '__main__':
    unittest.main()
