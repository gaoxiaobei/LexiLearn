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
- 📄 完整保留原文格式

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/gaoxiaobei/LexiLearn.git
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
    "model": "gpt-4o-mini"
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
   - 支持多段落文本，会保留原文的段落格式

2. 运行程序：
```bash
python main.py
```

3. 查看结果：
   - 程序会生成 `output_article.txt`
   - 文章中的生词会标注中文释义
   - 保持原文的段落结构和格式
   - 文末会附上本次学习的生词表
   - 新学习的单词会自动添加到词汇表中

## 输出示例

原文：
```text
The rapid advancement of artificial intelligence has transformed various sectors of our economy. Companies worldwide are leveraging machine learning algorithms to optimize their operations and enhance customer experience.

Despite the unprecedented benefits, some experts caution about potential risks and ethical implications. The need for responsible development becomes increasingly apparent.

John, a renowned researcher at MIT, emphasizes the importance of responsible AI development. He argues that while innovation is crucial, we must ensure that technological progress aligns with human values and societal needs.
```

处理后：
```text
The rapid advancement(进展) of artificial(人工的) intelligence(智能) has transformed(改变) various(各种) sectors(部门) of our economy(经济). Companies(公司) worldwide(全球) are leveraging(利用) machine(机器) learning(学习) algorithms(算法) to optimize(优化) their operations(运营) and enhance(提高) customer(客户) experience(体验).

Despite(尽管) the unprecedented(空前的) benefits(好处), some experts(专家) caution(警告) about potential(潜在的) risks(风险) and ethical(伦理的) implications(影响). The need for responsible(负责任的) development(发展) becomes increasingly(日益) apparent(明显的).

John, a renowned(著名的) researcher(研究员) at MIT, emphasizes(强调) the importance(重要性) of responsible(负责任的) AI development(发展). He argues(论证) that while innovation(创新) is crucial(关键的), we must ensure(确保) that technological(技术的) progress(进步) aligns(符合) with human values(价值观) and societal(社会的) needs(需求).

==================================================
Word Bank
==================================================

advancement  : 进展
algorithms   : 算法
aligns       : 符合
apparent     : 明显的
artificial   : 人工的
benefits     : 好处
caution      : 警告
companies    : 公司
crucial      : 关键的
customer     : 客户
development  : 发展
enhance      : 提高
ensures      : 确保
ethical      : 伦理的
experience   : 体验
experts      : 专家
implications : 影响
importance   : 重要性
increasingly : 日益
innovation   : 创新
intelligence : 智能
leveraging   : 利用
machine      : 机器
needs        : 需求
operations   : 运营
optimize     : 优化
potential    : 潜在的
progress     : 进步
renowned     : 著名的
researcher   : 研究员
responsible  : 负责任的
risks        : 风险
sectors      : 部门
societal     : 社会的
technological: 技术的
transformed  : 改变
unprecedented: 空前的
values       : 价值观
various      : 各种
worldwide    : 全球
```

## 格式说明

- 原文的段落结构完全保留
- 每个生词后用括号标注中文含义
- 专有名词（如人名、地名）保持原样
- 词汇表按字母顺序排列
- 相同单词只在词汇表中出现一次
- 保持原文的标点符号和空格

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
