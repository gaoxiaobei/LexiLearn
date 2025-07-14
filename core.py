import asyncio
import aiohttp
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import re
from tqdm import tqdm
from typing import Set, List, Tuple, Dict
from nltk.tokenize.treebank import TreebankWordDetokenizer
import os
import json

def load_settings(settings_path: str) -> Tuple[Dict, Dict, Dict]:
    """从JSON文件加载配置"""
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            api_config = settings.get("api_config", {})
            app_config = settings.get("app_config", {})
            file_paths = settings.get("file_paths", {})
            
            # 验证关键配置是否存在
            if not all(k in api_config for k in ["base_url", "api_key", "model"]):
                raise ValueError("API配置不完整")
            if not all(k in app_config for k in ["batch_size", "connector_limit", "sleep_time"]):
                raise ValueError("APP配置不完整")
            if not all(k in file_paths for k in ["known_words", "target_words", "learned_words"]):
                raise ValueError("文件路径配置不完整")
                
            return api_config, app_config, file_paths
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"错误：无法加载或解析 {settings_path}: {e}")
        print("请确保 settings.json 文件存在且格式正确。")
        exit(1)

# 加载配置
API_CONFIG, APP_CONFIG, FILE_PATHS = load_settings("settings.json")


def download_nltk_data():
    """下载NLTK所需数据"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK 'punkt' model...")
        nltk.download('punkt')
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Downloading NLTK 'punkt_tab' model...")
        nltk.download('punkt_tab')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        print("Downloading NLTK 'averaged_perceptron_tagger' model...")
        nltk.download('averaged_perceptron_tagger')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger_eng')
    except LookupError:
        print("Downloading NLTK 'averaged_perceptron_tagger_eng' model...")
        nltk.download('averaged_perceptron_tagger_eng')
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading NLTK 'wordnet' model...")
        nltk.download('wordnet')

class VocabularyManager:
    def __init__(self):
        self.known_words_path = FILE_PATHS['known_words']
        self.target_words_path = FILE_PATHS['target_words']
        self.learned_words_path = FILE_PATHS['learned_words']
        self.known_words = self.load_words(self.known_words_path)
        self.learned_words = self.load_words(self.learned_words_path)
        try:
            self.target_words = self.load_words(self.target_words_path)
            if not self.target_words:
                APP_CONFIG["use_target_words"] = False
        except FileNotFoundError:
            self.target_words = set()
            APP_CONFIG["use_target_words"] = False
            print(f"目标词表文件 {self.target_words_path} 不存在，将使用全词表模式。")

    def load_words(self, file_path: str) -> Set[str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return set(word.strip().lower() for word in f)
        except FileNotFoundError:
            return set()

    def should_translate(self, word: str) -> bool:
        word = word.lower()
        if APP_CONFIG["use_target_words"]:
            return (word in self.target_words and
                    word not in self.known_words and
                    word not in self.learned_words)
        else:
            return (word not in self.known_words and
                    word not in self.learned_words)

    def add_words_batch(self, words: Set[str]):
        new_words = {word.lower().strip() for word in words} - self.learned_words
        if new_words:
            self.learned_words.update(new_words)
            with open(self.learned_words_path, 'a', encoding='utf-8') as f:
                for word in sorted(new_words):
                    f.write(f"{word}\n")

def get_wordnet_pos(treebank_tag: str) -> str:
    """将Treebank POS标签转换为WordNet POS标签"""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

lemmatizer = WordNetLemmatizer()

def get_word_base_form(word: str, pos_tag: str) -> str:
    """使用POS标签获取单词的基本形式"""
    pos = get_wordnet_pos(pos_tag)
    return lemmatizer.lemmatize(word.lower(), pos)

async def get_batch_translations_async(
    session: aiohttp.ClientSession,
    words_to_translate: List[Dict[str, str]]
) -> Dict[str, str]:
    """批量异步获取翻译"""
    if not words_to_translate:
        return {}

    headers = {
        "Authorization": f"Bearer {API_CONFIG['api_key']}",
        "Content-Type": "application/json"
    }
    
    # 创建一个JSON友好的单词列表
    word_list_json = json.dumps([item['word'] for item in words_to_translate])

    prompt = (
        "You are a translation assistant. Provide accurate Chinese translations for the following list of English words. "
        "For each word, consider its context in the sentence provided. "
        "For proper nouns (like names, places), return the original word. "
        "Your response should be a JSON object mapping each original word to its translation.\n"
        f"Words to translate: {word_list_json}\n\n"
        "Contexts:\n"
    )

    for item in words_to_translate:
        prompt += f"- Word: '{item['word']}', Context: '{item['context']}'\n"

    data = {
        "model": API_CONFIG['model'],
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Please provide the translations in a single JSON object."}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        async with session.post(API_CONFIG['base_url'], headers=headers, json=data) as response:
            response.raise_for_status()
            result = await response.json()
            translations_text = result['choices'][0]['message']['content'].strip()
            return json.loads(translations_text)
    except Exception as e:
        print(f"\nError in batch translation: {e}")
        return {item['word']: "翻译失败" for item in words_to_translate}


async def process_paragraph_async(
    paragraph: str,
    vocab_manager: VocabularyManager,
    session: aiohttp.ClientSession,
    pbar: tqdm = None
) -> Tuple[str, Set[str], Dict[str, str]]:
    """异步处理单个段落"""
    if not paragraph.strip():
        if pbar:
            pbar.update(len(sent_tokenize(paragraph)))
        return "", set(), {}

    sentences = sent_tokenize(paragraph)
    words_to_translate_info = []
    
    # 1. 收集所有需要翻译的单词
    for sentence in sentences:
        words_and_tags = pos_tag(word_tokenize(sentence))
        for word, tag in words_and_tags:
            if not re.match(r'^[a-zA-Z\']+$', word) or tag in ['NNP', 'NNPS']:
                continue
            
            base_form = get_word_base_form(word, tag)
            if vocab_manager.should_translate(base_form):
                words_to_translate_info.append({"word": word, "base_form": base_form, "context": sentence})

    # 2. 批量获取翻译
    unique_words_to_translate = {v['word']:v for v in words_to_translate_info}.values()
    translations = await get_batch_translations_async(session, list(unique_words_to_translate))

    # 3. 构建注释后的句子
    processed_sentences = []
    new_words = set()
    word_translations_map = {}

    word_to_base_form = {item['word']: item['base_form'] for item in unique_words_to_translate}
    detokenizer = TreebankWordDetokenizer()

    for sentence in sentences:
        words = word_tokenize(sentence)
        annotated_words = []
        for word in words:
            if word in translations and translations[word] != "翻译失败" and translations[word] != word:
                annotated_words.append(f"{word}({translations[word]})")
                
                # 找到对应的base_form
                base_form = word_to_base_form.get(word)
                if base_form:
                    new_words.add(base_form)
                    word_translations_map[base_form] = translations[word]
            else:
                annotated_words.append(word)
        
        processed_sentences.append(detokenizer.detokenize(annotated_words))

    if pbar:
        pbar.update(len(sentences))
    return ' '.join(processed_sentences), new_words, word_translations_map


async def process_article_async(
    article_text: str,
    vocab_manager: VocabularyManager,
    progress_callback=None
) -> Tuple[str, Set[str], List[str]]:
    """异步处理文章"""
    print("Analyzing article...")

    article = article_text.replace("’", "'").replace("‘", "'").replace("`", "'").replace("“", '"').replace("”", '"')
    
    paragraphs = article.split('\n\n')
    all_new_words = set()
    word_translations = {}
    processed_paragraphs = []

    total_sentences = sum(len(sent_tokenize(p)) for p in paragraphs if p.strip())
    
    connector = aiohttp.TCPConnector(limit=APP_CONFIG['connector_limit'])
    async with aiohttp.ClientSession(connector=connector) as session:
        processed_sentences = 0
        for i in range(0, len(paragraphs), APP_CONFIG['batch_size']):
            batch = paragraphs[i:i + APP_CONFIG['batch_size']]
            tasks = [
                process_paragraph_async(
                    p,
                    vocab_manager,
                    session
                ) for p in batch
            ]
            results = await asyncio.gather(*tasks)
            for processed_paragraph, new_words, translations in results:
                processed_paragraphs.append(processed_paragraph)
                all_new_words.update(new_words)
                word_translations.update(translations)
            
            if progress_callback:
                # This is a simplification. A more accurate progress would be based on sentences.
                progress = (i + len(batch)) / len(paragraphs) * 100
                progress_callback(progress)

            if i + APP_CONFIG['batch_size'] < len(paragraphs):
                await asyncio.sleep(APP_CONFIG['sleep_time'])

    vocab_manager.add_words_batch(all_new_words)
    processed_article = '\n\n'.join(processed_paragraphs)
    
    word_bank_entries = sorted(
        [f"{word}: {translation}" for word, translation in word_translations.items()],
        key=lambda x: x.split(':')[0].strip().lower()
    )
    
    return processed_article, all_new_words, word_bank_entries

def format_word_bank(word_bank_entries: List[str]) -> str:
    """格式化词汇表"""
    if not word_bank_entries:
        return "\n\n==================================================\nWord Bank\n==================================================\nNo new words."
    
    max_word_len = max((len(entry.split(':')[0].strip()) for entry in word_bank_entries), default=0)
    
    bank = "\n\n" + "="*50 + "\n"
    bank += "Word Bank\n"
    bank += "="*50 + "\n\n"
    
    for entry in word_bank_entries:
        word, translation = entry.split(':', 1)
        bank += f"{word.strip():<{max_word_len}} : {translation.strip()}\n"
        
    return bank
