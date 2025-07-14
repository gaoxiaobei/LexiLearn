# LexiLearn

LexiLearn is an intelligent English reading assistant that helps you systematically build your vocabulary by providing real-time translations for unknown words in an article, based on your learning goals.

## Features

- 🎯 **Targeted Learning**: Translates only the words from your target list, or all unknown words.
- 🚀 **Optimized for Speed**: Uses asynchronous processing and batch API requests to translate words quickly.
- 📚 **Vocabulary Management**: Maintains separate lists for known, target, and learned words.
- 🔄 **Progress Tracking**: Automatically updates your learned words list, so you only learn new words once.
- 📊 **Clean Output**: Generates a clean, annotated article and a word bank of newly learned words.
- ⚙️ **Configurable**: Easily configure file paths and processing parameters through command-line arguments.
- 🔐 **Secure**: Keeps your API key safe by loading it from an environment variable.

## Installation

1.  **Clone the repository or download the source code.**

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **NLTK Data**: The first time you run the script, it will automatically download the necessary data models from NLTK (`punkt`, `averaged_perceptron_tagger`, `wordnet`).

## Configuration

1.  **Set the API Key**: Before running the script, you need to set your API key as an environment variable named `API_KEY`.

    -   **On Windows:**
        ```powershell
        $env:API_KEY="your-api-key-here"
        ```
        *Note: This sets the variable for the current session. For a permanent setting, use the System Properties dialog.*

    -   **On macOS/Linux:**
        ```bash
        export API_KEY="your-api-key-here"
        ```
        *Note: Add this line to your `~/.bashrc` or `~/.zshrc` file for it to persist across sessions.*

2.  **API Endpoint**: If you need to use a different API endpoint, you can modify it in the `main.py` script:
    ```python
    API_CONFIG = {
        "base_url": "https://your-api-endpoint/v1/chat/completions",
        # ...
    }
    ```

## Usage

1.  **Prepare your files**:
    -   `input_article.txt`: The English article you want to process. A sample file is provided.
    -   `known_words.txt`: A list of words you already know (one word per line). A sample file is provided.
    -   `target_words.txt`: A list of words you want to learn. If this file is empty or doesn't exist, the script will operate in "Full Word List" mode, identifying all unknown words. A sample file is provided.
    -   `learned_words.txt`: This file is automatically created and updated by the script to track the words you've learned.

2.  **Run the script from your terminal**:
    ```bash
    python main.py [input_file] [options]
    ```

    **Examples:**

    -   **To process the default `input_article.txt`:**
        ```bash
        python main.py
        ```

    -   **To specify a different input file and output file:**
        ```bash
        python main.py my_article.txt -o my_annotated_article.txt
        ```

    -   **To use different word lists:**
        ```bash
        python main.py --known_words my_known_words.txt --target_words my_targets.txt
        ```

    For a full list of options, run:
    ```bash
    python main.py --help
    ```

3.  **Check the output**:
    -   The processed article will be saved to `output_article.txt` (or the file you specified with `-o`).
    -   Unknown words will be annotated with their translations (e.g., `word(translation)`).
    -   A "Word Bank" will be appended to the end of the output file, listing the new words you've learned in this session.
    -   The `learned_words.txt` file will be updated with the new words.

## How It Works

LexiLearn processes the article paragraph by paragraph. For each paragraph, it:
1.  Identifies all the words.
2.  Uses NLTK for Part-of-Speech (POS) tagging to understand the role of each word (noun, verb, etc.).
3.  Determines the base form (lemma) of each word.
4.  Checks if the base form is a word that needs to be translated based on your word lists.
5.  Groups all the words that need translation and sends them to the API in a single **batch request**.
6.  Receives the translations and annotates the article.
7.  At the end of the process, it updates your `learned_words.txt` file.

This batching approach significantly reduces the number of API calls, making the process faster and more efficient.

## License

MIT License