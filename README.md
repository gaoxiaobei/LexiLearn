# LexiLearn

LexiLearn 是一个智能英语阅读辅助工具，它能自动识别文章中的生词，提供实时翻译，并帮助你系统地积累词汇量。

## 特性

- 🚀 并行处理，快速翻译
- 🎯 智能识别专有名词，避免不必要的翻译
- 📚 自动维护个人词汇库
- 🔄 实时更新学习进度
- 📊 生成整洁的生词表
- 🌐 支持自定义 API 端点

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

## 配置

1. 复制配置模板：
```bash
cp config.example.py config.py
```

2. 在 `config.py` 中填入你的 API 配置：
```python
API_CONFIG = {
    "base_url": "你的API基础URL",
    "api_key": "你的API密钥",
    "model": "gpt-3.5-turbo"
}
```

## 使用方法

1. 准备文件：
   - 创建 `input_article.txt`，粘贴你要阅读的英文文章
   - 创建 `known_words.txt`，每行一个已掌握的单词（可选）

2. 运行程序：
```bash
python main.py
```

3. 查看结果：
   - 程序会生成 `output_article.txt`
   - 文章中的生词会标注中文释义
   - 文末会附上本次学习的生词表

## 输出示例

原文：
```
The cat sat on the mat and contemplated the enigmatic behavior of its owner.
```

处理后：
```
The cat sat on the mat and contemplated(思考) the enigmatic(神秘的) behavior of its owner.

==================================================
Word Bank
==================================================

contemplated : 思考
enigmatic   : 神秘的
```

## 高级配置

你可以通过修改以下参数来优化性能：

- `batch_size`：调整并行处理的批量大小
- `connector.limit`：调整并发连接数
- `sleep_time`：调整请求间隔

## 贡献

欢迎提交 Pull Request 或创建 Issue！

## 待办事项

- [ ] 添加更多翻译 API 支持
- [ ] 支持导出学习报告
- [ ] 添加词形变化提示
- [ ] 支持自定义标注格式
- [ ] 添加图形用户界面

## 许可证

MIT License

## 致谢

- NLTK 团队提供的自然语言处理工具
- OpenAI 提供的 API 服务
- 所有贡献者和用户
