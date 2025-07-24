"""
LexiLearn - AI-powered English reading assistant with vocabulary management.

This package provides tools for processing English articles, identifying vocabulary words,
and providing contextual translations to help English learners improve their reading skills.
"""

# Expose main components at package level
from .main import main
from .config import config
from .article_processor import ArticleProcessor
from .text_processor import TextProcessor
from .translator import Translator
from .vocabulary import VocabularyManager
from .logger import logger

__version__ = "1.0.0"
__author__ = "LexiLearn Team"
__email__ = "team@lexilearn.dev"