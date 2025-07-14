# LexiLearn

LexiLearn is an intelligent English reading assistant with a graphical user interface (GUI) that helps you systematically build your vocabulary. It provides real-time translations for unknown words in an article, based on your learning goals, and allows you to manage all settings through a user-friendly interface.

## Features

-  GUI-First: A simple and intuitive GUI for a smooth user experience.
- 🎯 **Targeted Learning**: Translates only the words from your target list, or all unknown words.
- 🚀 **Optimized for Speed**: Uses asynchronous processing and batch API requests to translate words quickly.
- 📚 **Vocabulary Management**: Easily manage your known and target word lists through the GUI.
- 🔄 **Progress Tracking**: Automatically updates your learned words list, so you only learn new words once.
- 📊 **Clean Output**: Generates a clean, annotated article and a word bank of newly learned words.
- ⚙️ **Centralized Configuration**: All settings, including API keys and file paths, are managed in a single `settings.json` file, editable through the GUI.
- 🔐 **Secure**: Keeps your API key safe by storing it in a configuration file, not in the code.

## Installation

1.  **Clone the repository or download the source code.**

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **NLTK Data**: The first time you run the application, it will automatically download the necessary data models from NLTK in the background.

## Configuration

All configuration is now managed through the `settings.json` file. You can edit this file directly or use the in-app **Settings** window.

1.  **Launch the application**:
    ```bash
    python gui.py
    ```

2.  **Open the Settings Window**: Click on the "Settings" button to open the configuration panel.

3.  **Set Your API Key**: In the Settings window, enter your API key in the "Api Key" field. Without a valid key, the translation service will not work.

4.  **Customize Paths and Parameters (Optional)**:
    -   **API Configuration**: Change the `base_url` or `model` if needed.
    -   **Application Configuration**: Adjust `batch_size`, `connector_limit`, or `sleep_time` to fine-tune performance.
    -   **File Paths**: Modify the default file paths for your word lists (`known_words`, `target_words`, `learned_words`).

5.  **Save and Restart**: Click "Save" to apply your changes. A restart is required for the new settings to take effect.

## Usage

1.  **Run the application**:
    ```bash
    python gui.py
    ```

2.  **Manage Word Lists (Optional)**:
    -   Click the "Manage Words" button to add or remove words from your `known_words.txt` and `target_words.txt` lists.
    -   Click "Save and Close" when you are finished.

3.  **Process an Article**:
    -   **Load an article**: Click "Load File" to select a `.txt` file or paste your text directly into the "Input Article" panel.
    -   **Start processing**: Click the "Process" button. The application will analyze the text and display the annotated version in the "Processed Article" panel.
    -   The status bar and progress bar will show the real-time progress.

4.  **View the Results**:
    -   The processed article with inline translations will appear on the right.
    -   A "Word Bank" with all the newly learned words and their translations will be at the end.
    -   Your `learned_words.txt` file will be automatically updated.

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
