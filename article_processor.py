"""
Article processing module for LexiLearn application.

This module handles the main processing pipeline for articles,
including text processing, translation, and output generation.
"""

import asyncio
from typing import List, Set, Dict, Tuple
from pathlib import Path
import aiofiles
from tqdm.asyncio import tqdm_asyncio
from logger import logger
from config import config
from vocabulary import VocabularyManager
from text_processor import TextProcessor
from translator import Translator


class ArticleProcessingError(Exception):
    """Custom exception for article processing errors."""
    pass


class ArticleProcessor:
    """Main article processing class for LexiLearn."""
    
    def __init__(self) -> None:
        """Initialize the article processor."""
        self.text_processor = TextProcessor()
        self.vocab_manager = VocabularyManager(
            config.files.known_words,
            config.files.target_words,
            config.files.learned_words
        )
    
    async def process_article(self, article_path: str) -> Tuple[str, Set[str], List[str]]:
        """
        Process an entire article for vocabulary learning.
        
        Args:
            article_path: Path to the article file
            
        Returns:
            Tuple of (processed_article, new_words, word_bank_entries)
        """
        logger.info(f"Starting article processing: {article_path}")
        
        # Initialize vocabulary manager
        await self.vocab_manager.initialize()
        
        # Load article
        article_content = await self._load_article(article_path)
        if not article_content.strip():
            raise ArticleProcessingError("Article is empty")
        
        # Normalize text
        article_content = self.text_processor.normalize_text(article_content)
        
        # Split into paragraphs
        paragraphs = article_content.split('\n\n')
        
        # Process each paragraph
        processed_paragraphs = []
        all_new_words = set()
        word_translations = {}
        
        total_sentences = sum(
            len(self.text_processor.tokenize_sentences(p)) 
            for p in paragraphs if p.strip()
        )
        
        logger.info(f"Processing {len(paragraphs)} paragraphs with {total_sentences} sentences")
        
        # Process paragraphs with progress bar
        async with Translator() as translator:
            with tqdm_asyncio(total=total_sentences, desc="Processing sentences") as pbar:
                for paragraph in paragraphs:
                    if not paragraph.strip():
                        processed_paragraphs.append('')
                        continue
                    
                    processed_paragraph = await self._process_paragraph(
                        paragraph,
                        translator,
                        pbar,
                        word_translations
                    )
                    processed_paragraphs.append(processed_paragraph)
        
        # Generate word bank
        word_bank_entries = self._generate_word_bank(word_translations)
        
        # Update vocabulary
        if word_translations:
            await self.vocab_manager.add_words_batch(set(word_translations.keys()))
        
        # Combine processed paragraphs
        processed_article = '\n\n'.join(processed_paragraphs)
        
        logger.info(f"Article processing completed. New words learned: {len(all_new_words)}")
        
        return processed_article, all_new_words, word_bank_entries
    
    async def _load_article(self, article_path: str) -> str:
        """
        Load article content from file.
        
        Args:
            article_path: Path to the article file
            
        Returns:
            Article content as string
        """
        try:
            async with aiofiles.open(article_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            logger.info(f"Loaded article: {len(content)} characters")
            return content
        except FileNotFoundError:
            raise ArticleProcessingError(f"Article file not found: {article_path}")
        except Exception as e:
            raise ArticleProcessingError(f"Error loading article: {e}")
    
    async def _process_paragraph(
        self,
        paragraph: str,
        translator: Translator,
        pbar,
        word_translations: Dict[str, str]
    ) -> str:
        """
        Process a single paragraph.
        
        Args:
            paragraph: The paragraph to process
            translator: Translator instance
            pbar: Progress bar
            word_translations: Dictionary to store translations
            
        Returns:
            Processed paragraph
        """
        sentences = self.text_processor.tokenize_sentences(paragraph)
        if not sentences:
            return paragraph
        
        processed_sentences = []
        
        # Process sentences in batches
        for i in range(0, len(sentences), config.processing.batch_size):
            batch = sentences[i:i + config.processing.batch_size]
            batch_results = await self._process_sentence_batch(
                batch,
                translator,
                word_translations
            )
            processed_sentences.extend(batch_results)
            
            # Update progress bar
            pbar.update(len(batch))
            
            # Sleep between batches
            if i + config.processing.batch_size < len(sentences):
                await asyncio.sleep(config.processing.sleep_time)
        
        return ' '.join(processed_sentences)
    
    async def _process_sentence_batch(
        self,
        sentences: List[str],
        translator: Translator,
        word_translations: Dict[str, str]
    ) -> List[str]:
        """
        Process a batch of sentences.
        
        Args:
            sentences: List of sentences to process
            translator: Translator instance
            word_translations: Dictionary to store translations
            
        Returns:
            List of processed sentences
        """
        tasks = [
            self._process_single_sentence(sentence, translator, word_translations)
            for sentence in sentences
        ]
        
        return await asyncio.gather(*tasks)
    
    async def _process_single_sentence(
        self,
        sentence: str,
        translator: Translator,
        word_translations: Dict[str, str]
    ) -> str:
        """
        Process a single sentence.
        
        Args:
            sentence: The sentence to process
            translator: Translator instance
            word_translations: Dictionary to store translations
            
        Returns:
            Processed sentence with annotations
        """
        # Extract words that need translation
        words_to_process = self.text_processor.extract_words_for_processing(
            sentence,
            self.vocab_manager.should_translate
        )
        
        if not words_to_process:
            return sentence
        
        # Get translations for new words
        new_translations = []
        for original_word, base_form in words_to_process:
            if base_form not in word_translations:
                new_translations.append((original_word, base_form))
        
        if new_translations:
            # Get translations from API
            translation_requests = [
                (original, sentence) for original, base in new_translations
            ]
            
            results = await translator.translate_words_batch(translation_requests)
            
            # Store successful translations
            for (original_word, base_form), (_, translation, success) in zip(
                new_translations, results
            ):
                if success and translation != "翻译失败":
                    word_translations[base_form] = translation
        
        # Build annotated sentence
        words = self.text_processor.tokenize_words(sentence)
        annotated_words = []
        
        for word in words:
            if not self.text_processor.is_valid_word(word):
                annotated_words.append(word)
                continue
            
            base_form = self.text_processor.get_word_base_form(word)
            if base_form in word_translations:
                annotated_word = f"{word}({word_translations[base_form]})"
                annotated_words.append(annotated_word)
            else:
                annotated_words.append(word)
        
        return self.text_processor.detokenize_words(annotated_words)
    
    def _generate_word_bank(self, word_translations: Dict[str, str]) -> List[str]:
        """
        Generate formatted word bank entries.
        
        Args:
            word_translations: Dictionary of word translations
            
        Returns:
            List of formatted word bank entries
        """
        if not word_translations:
            return []
        
        entries = [
            f"{word}: {translation}"
            for word, translation in sorted(word_translations.items())
        ]
        
        return entries
    
    async def save_results(
        self,
        processed_article: str,
        word_bank_entries: List[str],
        output_path: str
    ) -> None:
        """
        Save processing results to file.
        
        Args:
            processed_article: The processed article content
            word_bank_entries: List of word bank entries
            output_path: Path to save the results
        """
        try:
            # Format word bank
            word_bank_content = self._format_word_bank(word_bank_entries)
            
            # Combine content
            full_content = processed_article + word_bank_content
            
            # Save to file
            async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
                await f.write(full_content)
            
            logger.info(f"Results saved to: {output_path}")
            
        except Exception as e:
            raise ArticleProcessingError(f"Error saving results: {e}")
    
    def _format_word_bank(self, word_bank_entries: List[str]) -> str:
        """
        Format word bank entries for display.
        
        Args:
            word_bank_entries: List of word bank entries
            
        Returns:
            Formatted word bank string
        """
        if not word_bank_entries:
            return "\n\n" + "="*50 + "\nWord Bank\n" + "="*50 + "\n无新词汇\n"
        
        max_word_length = max(len(entry.split(':')[0].strip()) for entry in word_bank_entries)
        
        word_bank = "\n\n" + "="*50 + "\n"
        word_bank += "Word Bank\n"
        word_bank += "="*50 + "\n\n"
        
        for entry in word_bank_entries:
            word, translation = entry.split(':', 1)
            word = word.strip()
            translation = translation.strip()
            word_bank += f"{word:<{max_word_length}} : {translation}\n"
        
        return word_bank
    
    def print_summary(self) -> None:
        """Print processing summary statistics."""
        stats = self.vocab_manager.get_statistics()
        
        logger.info("="*50)
        logger.info("Processing Summary")
        logger.info("="*50)
        logger.info(f"Known words: {stats['known_words']}")
        logger.info(f"Learned words: {stats['learned_words']}")
        logger.info(f"Target words: {stats['target_words']}")
        
        if stats['use_target_mode']:
            logger.info(f"Remaining target words: {stats['remaining_target_words']}")
        
        logger.info(f"Mode: {'Target words' if stats['use_target_mode'] else 'All words'}")