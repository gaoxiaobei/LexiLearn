import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import asyncio
import threading
import queue
import os
from core import (
    API_CONFIG,
    VocabularyManager,
    process_article_async,
    format_word_bank,
    download_nltk_data,
)

class WordManagementWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Words")
        self.geometry("600x400")
        self.parent = parent

        self.create_widgets()
        self.load_words()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Known words
        known_frame = ttk.LabelFrame(main_frame, text="Known Words", padding="5")
        known_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.known_list = tk.Listbox(known_frame)
        self.known_list.pack(fill=tk.BOTH, expand=True)
        
        known_entry_frame = ttk.Frame(known_frame)
        known_entry_frame.pack(fill=tk.X, pady=5)
        self.known_entry = ttk.Entry(known_entry_frame)
        self.known_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(known_entry_frame, text="Add", command=lambda: self.add_word(self.known_list, self.known_entry)).pack(side=tk.LEFT, padx=5)
        ttk.Button(known_frame, text="Remove Selected", command=lambda: self.remove_word(self.known_list)).pack(fill=tk.X)

        # Target words
        target_frame = ttk.LabelFrame(main_frame, text="Target Words", padding="5")
        target_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.target_list = tk.Listbox(target_frame)
        self.target_list.pack(fill=tk.BOTH, expand=True)

        target_entry_frame = ttk.Frame(target_frame)
        target_entry_frame.pack(fill=tk.X, pady=5)
        self.target_entry = ttk.Entry(target_entry_frame)
        self.target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(target_entry_frame, text="Add", command=lambda: self.add_word(self.target_list, self.target_entry)).pack(side=tk.LEFT, padx=5)
        ttk.Button(target_frame, text="Remove Selected", command=lambda: self.remove_word(self.target_list)).pack(fill=tk.X)

        # Bottom buttons
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        ttk.Button(button_frame, text="Save and Close", command=self.save_and_close).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=10)

    def load_words(self):
        self.load_word_list("known_words.txt", self.known_list)
        self.load_word_list("target_words.txt", self.target_list)

    def load_word_list(self, filename, listbox):
        listbox.delete(0, tk.END)
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    listbox.insert(tk.END, line.strip())

    def add_word(self, listbox, entry):
        word = entry.get().strip()
        if word:
            listbox.insert(tk.END, word)
            entry.delete(0, tk.END)

    def remove_word(self, listbox):
        selected_indices = listbox.curselection()
        for i in reversed(selected_indices):
            listbox.delete(i)

    def save_and_close(self):
        self.save_word_list("known_words.txt", self.known_list)
        self.save_word_list("target_words.txt", self.target_list)
        self.destroy()

    def save_word_list(self, filename, listbox):
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(listbox.size()):
                f.write(listbox.get(i) + '\n')

class LexiLearnGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LexiLearn")
        self.geometry("800x600")

        self.result_queue = queue.Queue()
        self.create_widgets()
        self.check_queue()

        # Download NLTK data in a separate thread
        threading.Thread(target=download_nltk_data, daemon=True).start()


    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input and Output Panes
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Input Frame
        input_frame = ttk.LabelFrame(paned_window, text="Input Article", padding="5")
        self.input_text = tk.Text(input_frame, wrap="word", height=15)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        paned_window.add(input_frame, weight=1)

        # Output Frame
        output_frame = ttk.LabelFrame(paned_window, text="Processed Article", padding="5")
        self.output_text = tk.Text(output_frame, wrap="word", height=15, state="disabled")
        self.output_text.pack(fill=tk.BOTH, expand=True)
        paned_window.add(output_frame, weight=1)

        # Button Frame
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.pack(fill=tk.X)

        self.load_button = ttk.Button(button_frame, text="Load File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.process_button = ttk.Button(button_frame, text="Process", command=self.start_processing)
        self.process_button.pack(side=tk.LEFT, padx=5)

        self.manage_words_button = ttk.Button(button_frame, text="Manage Words", command=self.manage_words)
        self.manage_words_button.pack(side=tk.LEFT, padx=5)
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=5)

        # Status Bar
        self.status_label = ttk.Label(self, text="Ready", padding="5", anchor="w")
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an article file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*" ))
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, f.read())
                self.status_label.config(text=f"Loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def start_processing(self):
        if not API_CONFIG['api_key']:
            messagebox.showerror("Error", "API_KEY environment variable not set.")
            return
            
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Warning", "Input article is empty.")
            return

        self.process_button.config(state="disabled")
        self.load_button.config(state="disabled")
        self.status_label.config(text="Processing...")
        self.progress_bar.start()

        # Run async processing in a separate thread
        threading.Thread(target=self.run_async_processing, args=(input_text,), daemon=True).start()

    def run_async_processing(self, article_text):
        asyncio.run(self.processing_coroutine(article_text))

    async def processing_coroutine(self, article_text):
        try:
            vocab_manager = VocabularyManager(
                "known_words.txt",
                "target_words.txt",
                "learned_words.txt"
            )
            
            def progress_callback(progress):
                self.result_queue.put(("progress", progress))

            processed_article, new_words, word_bank_entries = await process_article_async(
                article_text,
                vocab_manager,
                progress_callback
            )
            
            word_bank = format_word_bank(word_bank_entries)
            result_text = processed_article + word_bank
            
            self.result_queue.put(("success", result_text))

        except Exception as e:
            self.result_queue.put(("error", str(e)))

    def check_queue(self):
        try:
            message_type, data = self.result_queue.get_nowait()
            if message_type == "progress":
                self.progress_bar.config(value=data)
                self.status_label.config(text=f"Processing... {data:.0f}%")
            elif message_type == "success":
                self.output_text.config(state="normal")
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, data)
                self.output_text.config(state="disabled")
                self.status_label.config(text="Processing complete!")
                self.progress_bar.stop()
                self.progress_bar.config(value=100)
                self.process_button.config(state="normal")
                self.load_button.config(state="normal")
            elif message_type == "error":
                messagebox.showerror("Error", f"An error occurred: {data}")
                self.status_label.config(text="Error during processing.")
                self.progress_bar.stop()
                self.process_button.config(state="normal")
                self.load_button.config(state="normal")
        except queue.Empty:
            pass
        finally:
            self.after(100, self.check_queue)

    def manage_words(self):
        WordManagementWindow(self)

if __name__ == "__main__":
    app = LexiLearnGUI()
    app.mainloop()
