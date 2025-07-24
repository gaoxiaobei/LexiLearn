"""
Vocabulary management module for LexiLearn application.

This module handles loading, managing, and updating vocabulary lists
including known words, target words, and learned words.
"""

import asyncio
from pathlib import Path
from typing import Set, List, Optional
import aiofiles
from .logger import logger
from .config import config


class VocabularyError(Exception):
    """Custom exception for vocabulary-related errors."""
    pass


class VocabularyManager:
    """Manages vocabulary lists for the LexiLearn application."""
    
    def __init__(
        self,
        known_words_path: str,
        target_words_path: str,
        learned_words_path: str
    ) -> None:
        """
        Initialize the vocabulary manager.
        
        Args:
            known_words_path: Path to file containing known words
            target_words_path: Path to file containing target words
            learned_words_path: Path to file containing learned words
        """
        self.known_words_path = Path(known_words_path)
        self.target_words_path = Path(target_words_path)
        self.learned_words_path = Path(learned_words_path)
        
        self.known_words: Set[str] = set()
        self.target_words: Set[str] = set()
        self.learned_words: Set[str] = set()
        
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize vocabulary sets by loading from files."""
        if self._initialized:
            return
            
        logger.info("Initializing vocabulary manager...")
        
        # Load known words
        self.known_words = await self._load_words(self.known_words_path)
        logger.info(f"Loaded {len(self.known_words)} known words")
        
        # Load learned words
        self.learned_words = await self._load_words(self.learned_words_path)
        logger.info(f"Loaded {len(self.learned_words)} learned words")
        
        # Load target words if they exist
        try:
            self.target_words = await self._load_words(self.target_words_path)
            logger.info(f"Loaded {len(self.target_words)} target words")
            if not self.target_words:
                config.processing.use_target_words = False
                logger.warning("Target words file is empty, disabling target words mode")
        except FileNotFoundError:
            self.target_words = set()
            config.processing.use_target_words = False
            logger.warning(f"Target words file not found: {self.target_words_path}")
        
        self._initialized = True
    
    async def _load_words(self, file_path: Path) -> Set[str]:
        """
        Load words from a file asynchronously.
        
        Args:
            file_path: Path to the words file
            
        Returns:
            Set of words loaded from the file
        """
        if not file_path.exists():
            logger.debug(f"Words file not found: {file_path}")
            return set()
        
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                words = {
                    word.strip().lower() 
                    for word in content.splitlines() 
                    if word.strip() and not word.strip().startswith('#')
                }
                return words
        except Exception as e:
            logger.error(f"Error loading words from {file_path}: {e}")
            return set()
    
    def should_translate(self, word: str) -> bool:
        """
        Determine if a word should be translated based on vocabulary lists.
        
        Args:
            word: The word to check
            
        Returns:
            True if the word should be translated, False otherwise
        """
        if not isinstance(word, str):
            return False
            
        word = word.lower().strip()
        
        if not word:
            return False
        
        if config.processing.use_target_words:
            return (
                word in self.target_words and
                word not in self.known_words and
                word not in self.learned_words
            )
        else:
            return (
                word not in self.known_words and
                word not in self.learned_words
            )
    
    async def add_words_batch(self, words: Set[str]) -> int:
        """
        Add new words to the learned vocabulary.
        
        Args:
            words: Set of words to add
            
        Returns:
            Number of new words actually added
        """
        if not self._initialized:
            await self.initialize()
        
        new_words = {
            word.lower().strip() 
            for word in words 
            if isinstance(word, str) and word.strip()
        } - self.learned_words
        
        if not new_words:
            return 0
        
        self.learned_words.update(new_words)
        
        try:
            async with aiofiles.open(self.learned_words_path, 'a', encoding='utf-8') as f:
                for word in sorted(new_words):
                    await f.write(f"{word}\n")
            
            logger.info(f"Added {len(new_words)} new words to learned vocabulary")
            return len(new_words)
        except Exception as e:
            logger.error(f"Error adding words to learned vocabulary: {e}")
            raise VocabularyError(f"Failed to update learned words: {e}")
    
    def get_statistics(self) -> dict:
        """
        Get vocabulary statistics.
        
        Returns:
            Dictionary containing vocabulary statistics
        """
        return {
            "known_words": len(self.known_words),
            "learned_words": len(self.learned_words),
            "target_words": len(self.target_words),
            "remaining_target_words": len(
                self.target_words - self.known_words - self.learned_words
            ) if config.processing.use_target_words else 0,
            "use_target_mode": config.processing.use_target_words
        }
    
    def is_word_known(self, word: str) -> bool:
        """Check if a word is in the known vocabulary."""
        return word.lower().strip() in self.known_words
    
    def is_word_learned(self, word: str) -> bool:
        """Check if a word is in the learned vocabulary."""
        return word.lower().strip() in self.learned_words
    
    def is_word_target(self, word: str) -> bool:
        """Check if a word is in the target vocabulary."""
        return word.lower().strip() in self.target_words