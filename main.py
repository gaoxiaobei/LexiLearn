import asyncio
import argparse
from tqdm import tqdm

from core import (
    API_CONFIG,
    APP_CONFIG,
    download_nltk_data,
    VocabularyManager,
    process_article_async,
    format_word_bank,
)

async def main_async(args):
    """主程序异步实现"""
    if not API_CONFIG['api_key']:
        print("Error: API_KEY environment variable not set.")
        return

    download_nltk_data()

    print("Starting article processing...")
    print(f"Mode: {'Target Word List' if APP_CONFIG['use_target_words'] else 'Full Word List'}")
    print("Loading vocabulary...")
    
    vocab_manager = VocabularyManager(
        args.known_words,
        args.target_words,
        args.learned_words
    )

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            article_text = f.read()

        # We can use a simple progress bar here for the CLI
        pbar = tqdm(total=100, desc="Processing", unit="%")
        
        def progress_callback(progress):
            pbar.n = int(progress)
            pbar.refresh()

        processed_article, new_words, word_bank_entries = await process_article_async(
            article_text,
            vocab_manager,
            progress_callback
        )
        pbar.n = 100
        pbar.refresh()
        pbar.close()


        word_bank = format_word_bank(word_bank_entries)

        print("\nSaving processed article...")
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(processed_article)
            f.write(word_bank)
            
        print(f"\nProcessing complete! Output saved to {args.output_file}")
        print(f"Learned {len(new_words)} new words this session.")
        if APP_CONFIG["use_target_words"]:
            remaining = vocab_manager.target_words - vocab_manager.known_words - vocab_manager.learned_words
            print(f"{len(remaining)} words remaining in target list.")
        if word_bank_entries:
            print("\nNewly learned words:")
            for entry in word_bank_entries:
                print(f"- {entry}")

    except Exception as e:
        print(f"\nAn error occurred during processing: {e}")

def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description="LexiLearn - An intelligent reading assistant.")
    parser.add_argument("--gui", action="store_true", help="Launch the graphical user interface.")
    parser.add_argument("input_file", default="input_article.txt", nargs='?', help="Path to the input article file.")
    parser.add_argument("-o", "--output_file", default="output_article.txt", help="Path to the output article file.")
    parser.add_argument("--known_words", default="known_words.txt", help="Path to the known words list.")
    parser.add_argument("--target_words", default="target_words.txt", help="Path to the target words list.")
    parser.add_argument("--learned_words", default="learned_words.txt", help="Path to the learned words list (will be created or appended).")
    
    args = parser.parse_args()

    if args.gui:
        from gui import LexiLearnGUI
        app = LexiLearnGUI()
        app.mainloop()
    else:
        try:
            asyncio.run(main_async(args))
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
