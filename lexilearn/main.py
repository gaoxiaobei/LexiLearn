#!/usr/bin/env python3
"""
LexiLearn - English Reading Assistant with Targeted Vocabulary Translation

A production-ready application that helps English learners by providing
contextual translations for vocabulary words while reading articles.

Usage:
    python main.py
    python main.py --config custom_config.env
    python main.py --article custom_article.txt

Environment Variables:
    OPENAI_API_KEY: Required API key for OpenAI
    API_BASE_URL: Custom API endpoint (optional)
    API_MODEL: Model to use (default: gpt-4o-mini)
    LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
"""

import asyncio
import argparse
import sys
from pathlib import Path
from .logger import logger
from .config import config
from .article_processor import ArticleProcessor


class LexiLearnApp:
    """Main application class for LexiLearn."""
    
    def __init__(self) -> None:
        """Initialize the LexiLearn application."""
        self.processor = ArticleProcessor()
    
    async def run(self, article_path: str = None) -> None:
        """
        Run the LexiLearn application.
        
        Args:
            article_path: Path to the article file (optional)
        """
        try:
            # Use provided path or default from config
            input_path = article_path or config.files.input_article
            
            # Validate input file
            if not Path(input_path).exists():
                logger.error(f"Input file not found: {input_path}")
                print(f"Error: Input file '{input_path}' not found.")
                print("Please create the file or specify a different path.")
                return
            
            # Log configuration
            logger.info("Starting LexiLearn application...")
            logger.info(f"Input file: {input_path}")
            logger.info(f"Output file: {config.files.output_article}")
            logger.info(f"Mode: {'Target words' if config.processing.use_target_words else 'All words'}")
            
            # Process the article
            processed_article, new_words, word_bank_entries = await self.processor.process_article(input_path)
            
            # Save results
            await self.processor.save_results(
                processed_article,
                word_bank_entries,
                config.files.output_article
            )
            
            # Print summary
            self.processor.print_summary()
            
            if new_words:
                print(f"\n✅ Successfully learned {len(new_words)} new words!")
                print(f"📄 Results saved to: {config.files.output_article}")
            else:
                print("\n✅ Article processed successfully!")
                print("No new words were found to learn.")
            
        except KeyboardInterrupt:
            logger.warning("Application interrupted by user")
            print("\n\n👋 Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
            print("Please check the log file for details.")
            sys.exit(1)


def setup_environment() -> None:
    """Set up the application environment."""
    # Create required files if they don't exist
    required_files = [
        config.files.known_words,
        config.files.target_words,
        config.files.learned_words,
        config.files.input_article
    ]
    
    for file_path in required_files:
        path = Path(file_path)
        if not path.exists():
            path.touch()
            logger.info(f"Created missing file: {file_path}")
    
    # Validate API key
    if not config.api.api_key:
        print("❌ Error: OpenAI API key not found!")
        print("Please set the OPENAI_API_KEY environment variable:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)


def main() -> None:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="LexiLearn - English Reading Assistant"
    )
    parser.add_argument(
        "--article",
        type=str,
        help="Path to article file (default: input_article.txt)"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to custom configuration file"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="LexiLearn 2.0.0"
    )
    
    args = parser.parse_args()
    
    # Setup environment
    setup_environment()
    
    # Run application
    app = LexiLearnApp()
    
    try:
        asyncio.run(app.run(args.article))
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
