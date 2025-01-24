import asyncio
import aiohttp
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import re
from tqdm import tqdm
from typing import Set, List, Tuple, Dict

# API配置
API_CONFIG = {
    "base_url": "你的API基础URL",
    "api_key": "你的API密钥",
    "model": "gpt-3.5-turbo"
}

# 程序配置
APP_CONFIG = {
    "batch_size": 10,          # 并行处理的批量大小
    "connector_limit": 10,     # 并发连接数限制
    "sleep_time": 0.5,        # 批次间延迟时间（秒）
}

class VocabularyManager:
    def __init__(self, known_words_path: str, target_words_path: str, learned_words_path: str):
        """初始化词汇管理器"""
        self.known_words_path = known_words_path
        self.target_words_path = target_words_path
        self.learned_words_path = learned_words_path
        self.known_words = self.load_words(known_words_path)
        self.target_words = self.load_words(target_words_path)
        self.learned_words = self.load_words(learned_words_path)
        
    def load_words(self, file_path: str) -> Set[str]:
        """加载词汇表"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return set(word.strip().lower() for word in f.readlines())
        except FileNotFoundError:
            print(f"词汇表文件 {file_path} 不存在，将创建新文件。")
            return set()
    
    def should_translate(self, word: str) -> bool:
        """判断单词是否需要翻译"""
        word = word.lower()
        return (word in self.target_words and 
                word not in self.known_words and 
                word not in self.learned_words)
    
    def add_words_batch(self, words: Set[str]) -> None:
        """批量添加新学习的单词"""
        new_words = {word.lower().strip() for word in words} - self.learned_words
        if new_words:
            self.learned_words.update(new_words)
            with open(self.learned_words_path, 'a', encoding='utf-8') as f:
                for word in sorted(new_words):
                    f.write(f"{word}\n")

def get_word_base_form(word: str) -> str:
    """获取单词的基本形式"""
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(
        lemmatizer.lemmatize(
            lemmatizer.lemmatize(word.lower(), pos='v'),
            pos='n'
        ),
        pos='a'
    )

def is_proper_noun(word: str, context: str) -> bool:
    """判断单词是否为专有名词"""
    words = word_tokenize(context)
    tagged = pos_tag(words)
    
    for w, tag in tagged:
        if w == word:
            return tag in ['NNP', 'NNPS']
    
    return False

async def get_translation_async(
    session: aiohttp.ClientSession,
    word: str,
    context: str
) -> Tuple[str, bool]:
    """异步获取翻译"""
    if is_proper_noun(word, context):
        return word, True

    headers = {
        "Authorization": f"Bearer {API_CONFIG['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": API_CONFIG['model'],
        "messages": [
            {
                "role": "system",
                "content": "你是一个翻译助手，请根据上下文提供准确的中文翻译。对于人名、地名等专有名词，请保留原文。"
            },
            {
                "role": "user",
                "content": f"在以下句子中，请给出单词'{word}'最准确的中文含义（只需要给出翻译，无需解释）：\n{context}"
            }
        ]
    }
    
    try:
        async with session.post(API_CONFIG['base_url'], headers=headers, json=data) as response:
            result = await response.json()
            translation = result['choices'][0]['message']['content'].strip()
            return translation, True
    except Exception as e:
        print(f"\n翻译出错 {word}: {e}")
        return "翻译失败", False

async def process_sentence_async(
    sentence: str,
    vocab_manager: VocabularyManager,
    session: aiohttp.ClientSession,
    pbar: tqdm,
    word_translations: Dict[str, str]
) -> Tuple[str, Set[str]]:
    """异步处理单个句子"""
    words = word_tokenize(sentence)
    processed_words = []
    new_words = set()
    translation_tasks = []
    words_to_translate = []

    for word in words:
        if not re.match(r'^[a-zA-Z]+$', word):
            processed_words.append((word, None))
            continue
            
        if is_proper_noun(word, sentence):
            processed_words.append((word, None))
            continue
            
        base_form = get_word_base_form(word)
        
        if vocab_manager.should_translate(base_form):
            if base_form not in word_translations:
                words_to_translate.append((word, base_form))
                processed_words.append((word, len(translation_tasks)))
                translation_tasks.append(get_translation_async(session, word, sentence))
            else:
                processed_words.append((word, -1, word_translations[base_form]))
        else:
            processed_words.append((word, None))

    if translation_tasks:
        translations = await asyncio.gather(*translation_tasks)
        
        for i, ((word, base_form), (translation, success)) in enumerate(zip(words_to_translate, translations)):
            if success:
                new_words.add(base_form)
                if base_form not in word_translations:
                    word_translations[base_form] = translation

    result_words = []
    for word_info in processed_words:
        if len(word_info) == 3:  # 使用已有翻译
            word, _, translation = word_info
            result_words.append(f"{word}({translation})")
        elif len(word_info) == 2:  # word, trans_idx
            word, trans_idx = word_info
            if trans_idx is not None:
                translation, _ = translations[trans_idx]
                result_words.append(f"{word}({translation})")
            else:
                result_words.append(word)

    pbar.update(1)
    return ' '.join(result_words), new_words

async def process_article_async(
    article_path: str,
    vocab_manager: VocabularyManager
) -> Tuple[str, Set[str], List[str]]:
    """异步处理文章"""
    with open(article_path, 'r', encoding='utf-8') as f:
        article = f.read()

    print("正在分析文章...")
    paragraphs = article.split('\n\n')
    all_new_words = set()
    word_translations = {}
    processed_paragraphs = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            processed_paragraphs.append('')
            continue

        sentences = nltk.sent_tokenize(paragraph)
        processed_sentences = []

        pbar = tqdm(total=len(sentences), desc="处理进度", unit="句")

        connector = aiohttp.TCPConnector(limit=APP_CONFIG['connector_limit'])
        async with aiohttp.ClientSession(connector=connector) as session:
            for i in range(0, len(sentences), APP_CONFIG['batch_size']):
                batch = sentences[i:i + APP_CONFIG['batch_size']]
                tasks = [
                    process_sentence_async(
                        sentence,
                        vocab_manager,
                        session,
                        pbar,
                        word_translations
                    ) for sentence in batch
                ]
                results = await asyncio.gather(*tasks)
                
                for processed_sentence, new_words in results:
                    processed_sentences.append(processed_sentence)
                    all_new_words.update(new_words)
                
                await asyncio.sleep(APP_CONFIG['sleep_time'])

        pbar.close()
        processed_paragraphs.append(' '.join(processed_sentences))
    
    processed_article = '\n\n'.join(processed_paragraphs)
    
    word_bank_entries = sorted(
        [f"{word}: {translation}" for word, translation in word_translations.items()],
        key=lambda x: x.split(':')[0].strip().lower()
    )
    
    return processed_article, all_new_words, word_bank_entries

def format_word_bank(word_bank_entries: List[str]) -> str:
    """格式化词汇表"""
    if not word_bank_entries:
        return "\n\n=== Word Bank ===\n无新词汇"
    
    max_word_length = max(len(entry.split(':')[0].strip()) for entry in word_bank_entries)
    
    word_bank = "\n\n" + "="*50 + "\n"
    word_bank += "Word Bank\n"
    word_bank += "="*50 + "\n\n"
    
    for entry in word_bank_entries:
        word, translation = entry.split(':')
        word = word.strip()
        translation = translation.strip()
        word_bank += f"{word:<{max_word_length}} : {translation}\n"
    
    return word_bank

async def main_async():
    """主程序异步实现"""
    article_path = 'input_article.txt'
    known_words_path = 'known_words.txt'
    target_words_path = 'target_words.txt'
    learned_words_path = 'learned_words.txt'
    output_path = 'output_article.txt'
    
    print("开始处理文章...")
    print(f"正在加载词汇表...")
    
    vocab_manager = VocabularyManager(
        known_words_path,
        target_words_path,
        learned_words_path
    )
    
    try:
        processed_article, new_words_to_add, word_bank_entries = await process_article_async(
            article_path,
            vocab_manager
        )
        
        word_bank = format_word_bank(word_bank_entries)
        
        print("\n保存处理结果...")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_article)
            f.write(word_bank)
        
        vocab_manager.add_words_batch(new_words_to_add)
        
        print(f"\n处理完成！结果已保存到 {output_path}")
        print(f"本次新学习了 {len(new_words_to_add)} 个单词")
        print(f"目标词汇表中还有 {len(vocab_manager.target_words - vocab_manager.known_words - vocab_manager.learned_words)} 个单词未学习")
        
        if word_bank_entries:
            print("\n新学习的单词列表:")
            for entry in word_bank_entries:
                print(f"- {entry}")
                
    except Exception as e:
        print(f"\n处理过程中出错: {e}")
        print("由于错误，新词未添加到已学词表")

def main():
    """主程序入口"""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序执行出错: {e}")

if __name__ == "__main__":
    main()
