# LexiLearn

LexiLearn 是一个智能英语阅读辅助工具，它能自动识别文章中的生词，提供实时翻译，并帮助你系统地积累词汇量。

## 特性

- 🚀 并行处理，快速翻译
- 🎯 智能识别专有名词，避免不必要的翻译
- 📚 自动维护个人词汇库
- 🔄 实时更新学习进度
- 📊 生成整洁的生词表
- 🌐 支持自定义 API 端点
- 💡 支持批量并发请求
- 🎨 优雅的进度显示
- 📝 自动记忆已学单词

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/LexiLearn.git
cd LexiLearn
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 首次使用需要下载NLTK数据（仅需执行一次）：
```bash
python setup.py
```

## 配置

1. 复制配置模板：
```bash
cp config.example.py config.py
```

2. 在 `config.py` 中填入你的配置：
```python
# API 配置
API_CONFIG = {
    "base_url": "https://your-api-endpoint/v1/chat/completions",
    "api_key": "your-api-key-here",
    "model": "gpt-3.5-turbo"
}

# 程序配置
APP_CONFIG = {
    "batch_size": 10,          # 并行处理的批量大小
    "connector_limit": 10,     # 并发连接数限制
    "sleep_time": 0.5,        # 批次间延迟时间（秒）
    "input_file": "input_article.txt",
    "output_file": "output_article.txt",
    "known_words_file": "known_words.txt"
}
```

## 使用方法

1. 准备文件：
   - 创建 `input_article.txt`，粘贴你要阅读的英文文章
   - （可选）创建 `known_words.txt`，每行一个已掌握的单词

2. 运行程序：
```bash
python main.py
```

3. 查看结果：
   - 程序会生成 `output_article.txt`
   - 文章中的生词会标注中文释义
   - 文末会附上本次学习的生词表
   - 新学习的单词会自动添加到词汇表中

## 输出示例

原文：
```text
The rapid advancement of artificial intelligence has transformed various sectors of our economy.
```

处理后：
```text
The rapid advancement(进展) of artificial(人工的) intelligence(智能) has transformed(改变) various(各种) sectors(部门) of our economy(经济).

==================================================
Word Bank
==================================================

advancement : 进展
artificial  : 人工的
economy     : 经济
intelligence: 智能
sectors     : 部门
transformed : 改变
various     : 各种
```

## 性能调优

你可以通过调整 `config.py` 中的以下参数来优化性能：

- `batch_size`：每批处理的句子数量
- `connector_limit`：并发连接数限制
- `sleep_time`：批次间延迟时间

根据你的 API 限制和网络条件调整这些参数。

## 项目结构

```
LexiLearn/
├── README.md
├── requirements.txt
├── setup.py           # NLTK数据下载脚本
├── config.example.py  # 配置文件模板
├── main.py           # 主程序
├── tests/            # 测试文件
└── examples/         # 示例文件
```

## 注意事项

1. 首次使用前请确保运行 `setup.py`
2. 确保 API 配置正确
3. 注意调整并发参数，避免触发 API 限制
4. 建议定期备份词汇表文件

## 贡献

欢迎提交 Pull Request 或创建 Issue！

## 待办事项

- [ ] 添加更多翻译 API 支持
- [ ] 支持导出学习报告
- [ ] 添加词形变化提示
- [ ] 支持自定义标注格式
- [ ] 添加图形用户界面
- [ ] 支持多种文本格式输入
- [ ] 添加学习进度统计
- [ ] 支持生词复习功能

## 许可证

MIT License

## 致谢

- NLTK 团队提供的自然语言处理工具
- OpenAI 提供的 API 服务
- 所有贡献者和用户
