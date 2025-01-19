import asyncio
import aiohttp
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import re
from tqdm import tqdm
import time
from typing import Set, List, Tuple, Dict

try:
    from config import API_CONFIG, APP_CONFIG
except ImportError:
    print("请先复制 config.example.py 为 config.py 并进行配置")
    exit(1)

class VocabularyManager:
    def __init__(self, known_words_path: str):
        """初始化词汇管理器"""
        self.known_words_path = known_words_path
        self.known_words = self.load_known_words()
        
    def load_known_words(self) -> Set[str]:
        """加载已知词汇表"""
        try:
            with open(self.known_words_path, 'r', encoding='utf-8') as f:
                return set(word.strip().lower() for word in f.readlines())
        except FileNotFoundError:
            print(f"词汇表文件 {self.known_words_path} 不存在，将创建新文件。")
            return set()
    
    def add_words_batch(self, words: Set[str]) -> None:
        """批量添加新词到词汇表"""
        new_words = set(word.lower().strip() for word in words)
        new_words = new_words - self.known_words
        
        if new_words:
            self.known_words.update(new_words)
            with open(self.known_words_path, 'a', encoding='utf-8') as f:
                for word in sorted(new_words):
                    f.write(f"{word}\n")
    
    def is_known_word(self, word: str) -> bool:
        """检查词是否为已知词"""
        return word.lower() in self.known_words

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
        
        if not vocab_manager.is_known_word(base_form):
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
    # 先按段落分割
    paragraphs = article.split('\n\n')
    all_new_words = set()
    word_translations = {}
    processed_paragraphs = []

    # 处理每个段落
    for paragraph in paragraphs:
        if not paragraph.strip():  # 跳过空段落
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
        # 将处理后的句子重新组合成段落
        processed_paragraphs.append(' '.join(processed_sentences))
    
    # 使用原始的段落分隔符重新组合文章
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
    article_path = APP_CONFIG['input_file']
    known_words_path = APP_CONFIG['known_words_file']
    output_path = APP_CONFIG['output_file']
    
    print("开始处理文章...")
    print(f"正在加载已知词汇表: {known_words_path}")
    
    vocab_manager = VocabularyManager(known_words_path)
    
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
        print(f"本次新学习了 {len(new_words_to_add)} 个单词:")
        
        if word_bank_entries:
            print("\n新学习的单词列表:")
            for entry in word_bank_entries:
                print(f"- {entry}")
                
    except Exception as e:
        print(f"\n处理过程中出错: {e}")
        print("由于错误，新词未添加到词汇表")

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
