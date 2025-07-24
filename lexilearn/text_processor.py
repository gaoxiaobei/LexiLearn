"""
Text processing module for LexiLearn application.

This module handles text tokenization, lemmatization, and other
text processing operations needed for vocabulary learning.
"""

import re
import nltk
from typing import List, Tuple
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize.treebank import TreebankWordDetokenizer
from .logger import logger


class TextProcessingError(Exception):
    """Custom exception for text processing errors."""
    pass


class TextProcessor:
    """Handles text processing operations for LexiLearn."""
    
    def __init__(self) -> None:
        """Initialize the text processor with required NLTK data."""
        self._ensure_nltk_data()
        self.lemmatizer = WordNetLemmatizer()
        self.detokenizer = TreebankWordDetokenizer()
        
    def _ensure_nltk_data(self) -> None:
        """Ensure required NLTK data is downloaded."""
        required_data = [
            'tokenizers/punkt',
            'tokenizers/punkt_tab',
            'corpora/wordnet',
            'taggers/averaged_perceptron_tagger',
            'taggers/averaged_perceptron_tagger_eng'
        ]
        
        for data_path in required_data:
            try:
                nltk.data.find(data_path)
            except LookupError:
                logger.info(f"Downloading required NLTK data: {data_path}")
                try:
                    nltk.download(data_path.split('/')[-1], quiet=True)
                except Exception as e:
                    logger.error(f"Failed to download NLTK data {data_path}: {e}")
                    raise TextProcessingError(f"NLTK data download failed: {e}")
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text by standardizing quotes and apostrophes.
        
        Args:
            text: Input text to normalize
            
        Returns:
            Normalized text
        """
        if not isinstance(text, str):
            raise TextProcessingError("Text must be a string")
        
        # Standardize quotes and apostrophes
        normalized = (
            text
            .replace("’", "'")
            .replace("‘", "'")
            .replace("`", "'")
            .replace("“", '"')
            .replace("”", '"')
            .replace("–", "-")
            .replace("—", "-")
        )
        
        return normalized
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        if not isinstance(text, str):
            raise TextProcessingError("Text must be a string")
        
        try:
            sentences = sent_tokenize(text)
            return [s.strip() for s in sentences if s.strip()]
        except Exception as e:
            logger.error(f"Error tokenizing sentences: {e}")
            raise TextProcessingError(f"Failed to tokenize sentences: {e}")
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Split text into words.
        
        Args:
            text: Input text
            
        Returns:
            List of words
        """
        if not isinstance(text, str):
            raise TextProcessingError("Text must be a string")
        
        try:
            return word_tokenize(text)
        except Exception as e:
            logger.error(f"Error tokenizing words: {e}")
            raise TextProcessingError(f"Failed to tokenize words: {e}")
    
    def get_word_base_form(self, word: str) -> str:
        """
        Get the base form (lemma) of a word.
        
        Args:
            word: Input word
            
        Returns:
            Base form of the word
        """
        if not isinstance(word, str):
            raise TextProcessingError("Word must be a string")
        
        word = word.lower().strip()
        if not word:
            return ""
        
        try:
            # Apply lemmatization for different parts of speech
            base_form = self.lemmatizer.lemmatize(
                self.lemmatizer.lemmatize(
                    self.lemmatizer.lemmatize(word, pos='v'),
                    pos='n'
                ),
                pos='a'
            )
            return base_form
        except Exception as e:
            logger.error(f"Error getting base form for '{word}': {e}")
            return word
    
    def is_proper_noun(self, word: str, context: str) -> bool:
        """
        Determine if a word is a proper noun based on context.
        
        Args:
            word: The word to check
            context: The sentence or context containing the word
            
        Returns:
            True if the word is a proper noun, False otherwise
        """
        if not isinstance(word, str) or not isinstance(context, str):
            return False
        
        try:
            words = word_tokenize(context)
            tagged = pos_tag(words)
            
            for w, tag in tagged:
                if w.lower() == word.lower():
                    return tag in ['NNP', 'NNPS']
            return False
        except Exception as e:
            logger.error(f"Error checking proper noun for '{word}': {e}")
            return False
    
    def is_valid_word(self, word: str) -> bool:
        """
        Check if a token is a valid word for processing.
        
        Args:
            word: The word to check
            
        Returns:
            True if the word is valid for processing, False otherwise
        """
        if not isinstance(word, str):
            return False
        
        word = word.strip()
        if not word:
            return False
        
        # Skip contractions and possessives
        if word.startswith("'") and len(word) > 1:
            return False
        
        # Check if word contains only letters and apostrophes
        if not re.match(r'^[a-zA-Z\']+$', word):
            return False
        
        return True
    
    def detokenize_words(self, words: List[str]) -> str:
        """
        Combine a list of words back into a sentence.
        
        Args:
            words: List of words to combine
            
        Returns:
            Combined sentence
        """
        if not isinstance(words, list):
            raise TextProcessingError("Words must be a list")
        
        try:
            return self.detokenizer.detokenize(words)
        except Exception as e:
            logger.error(f"Error detokenizing words: {e}")
            raise TextProcessingError(f"Failed to detokenize words: {e}")
    
    def extract_words_for_processing(
        self, 
        sentence: str, 
        vocabulary_check_func
    ) -> List[Tuple[str, str]]:
        """
        Extract words that need processing from a sentence.
        
        Args:
            sentence: The sentence to process
            vocabulary_check_func: Function to check if word should be processed
            
        Returns:
            List of tuples (original_word, base_form) for words to process
        """
        if not isinstance(sentence, str):
            raise TextProcessingError("Sentence must be a string")
        
        words = self.tokenize_words(sentence)
        words_to_process = []
        
        for word in words:
            if not self.is_valid_word(word):
                continue
            
            if self.is_proper_noun(word, sentence):
                continue
            
            base_form = self.get_word_base_form(word)
            if not base_form:
                continue
            
            if vocabulary_check_func(base_form):
                words_to_process.append((word, base_form))
        
        return words_to_process