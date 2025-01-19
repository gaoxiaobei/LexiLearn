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
