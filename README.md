# LexiLearn

LexiLearn 是一个智能英语阅读辅助工具，它能根据你的目标词汇表标注文章中的生词，提供实时翻译，并帮助你系统地积累词汇量。

## 特性

- 🎯 只翻译目标词汇表中的单词
- 🚀 并行处理，快速翻译
- 📚 分离的词汇管理系统
- 🔄 实时更新学习进度
- 📊 生成整洁的生词表
- 🌐 支持自定义 API 端点
- 💡 支持批量并发请求
- 📄 完整保留原文格式

## 安装

1. 安装依赖：
```bash
pip install aiohttp nltk tqdm
```

## 配置

1. 在 `main.py` 中填入你的 API 配置：
```python
API_CONFIG = {
    "base_url": "你的API基础URL",
    "api_key": "你的API密钥",
    "model": "gpt-3.5-turbo"
}
```

## 使用方法

1. 准备文件：
   - `input_article.txt`：待处理的英文文章
   - `known_words.txt`：已掌握的单词列表（每行一个）
   - `target_words.txt`：想要学习的目标单词列表（每行一个）
   - `learned_words.txt`：将自动记录新学会的单词（程序自动创建）

2. 运行程序：
```bash
python main.py
```

3. 查看结果：
   - 程序生成 `output_article.txt`
   - 只标注目标词汇表中的生词
   - 保持原文的段落结构
   - 文末附上本次学习的生词表
   - 新学习的单词自动添加到 learned_words.txt

## 词汇管理说明

- `known_words.txt`：已掌握的词汇，不会被修改
- `target_words.txt`：学习目标词汇
- `learned_words.txt`：通过本程序学习的新词

## 输出示例

原文：
```text
The rapid advancement of artificial intelligence has transformed various sectors of our economy.
```

target_words.txt 内容：
```text
advancement
artificial
intelligence
transform
sector
economy
```

输出：
```text
The rapid advancement(进展) of artificial(人工的) intelligence(智能) has transformed(改变) various sectors(部门) of our economy(经济).

==================================================
Word Bank
==================================================

advancement : 进展
artificial  : 人工的
economy     : 经济
intelligence: 智能
sectors     : 部门
transformed : 改变
```

## 注意事项

1. 确保 API 配置正确
2. 目标词汇表使用单词原形
3. 专有名词（人名、地名）会自动跳过
4. 同一个单词只会在词汇表中出现一次
5. 已学习的单词会自动记录，下次不再标注

## 性能调优

可以在代码中调整以下参数：
```python
APP_CONFIG = {
    "batch_size": 10,          # 并行处理的批量大小
    "connector_limit": 10,     # 并发连接数限制
    "sleep_time": 0.5,        # 批次间延迟时间（秒）
}
```

## 许可证

MIT License
