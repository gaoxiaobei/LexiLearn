# Troubleshooting Guide

Comprehensive troubleshooting guide for common issues and solutions in LexiLearn.

## 📋 Quick Diagnostic

Run the diagnostic script to identify common issues:
```bash
python test_setup.py
```

## 🔍 Common Issues

### 1. Installation Issues

#### Python Version Error
**Problem**: `Python 3.8+ required`
```bash
# Check Python version
python --version
python3 --version

# Install Python 3.8+
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.8 python3.8-venv

# macOS:
brew install python@3.8

# Windows:
# Download from python.org
```

#### Virtual Environment Issues
**Problem**: `venv` module not found or activation fails
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# If venv fails, try:
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

#### NLTK Data Download Issues
**Problem**: `Resource punkt not found`
```bash
# Manual NLTK download
python -c "import nltk; nltk.download('punkt')"
python -c "import nltk; nltk.download('wordnet')"
python -c "import nltk; nltk.download('averaged_perceptron_tagger')"

# If behind proxy:
python -c "import nltk; nltk.set_proxy('http://proxy.example.com:8080'); nltk.download('all')"
```

### 2. Configuration Issues

#### API Key Not Found
**Problem**: `OPENAI_API_KEY is required`
```bash
# Check if set
echo $OPENAI_API_KEY

# Set temporarily
export OPENAI_API_KEY="sk-your-key-here"

# Set in .env file
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Verify
python -c "from config import Config; Config().validate()"
```

#### Invalid Configuration Values
**Problem**: `BATCH_SIZE must be an integer`
```bash
# Check .env file
cat .env

# Fix integer values
sed -i 's/BATCH_SIZE="10"/BATCH_SIZE=10/g' .env

# Validate configuration
python -c "from config import Config; c=Config(); c.validate()"
```

### 3. File Issues

#### Input File Not Found
**Problem**: `FileNotFoundError: input_article.txt`
```bash
# Check file exists
ls -la input_article.txt

# Create sample file
cat > input_article.txt << EOF
The quick brown fox jumps over the lazy dog.
This is a sample article for testing LexiLearn.
EOF

# Use custom file
python main.py --article my_article.txt
```

#### Permission Denied
**Problem**: `PermissionError: [Errno 13] Permission denied`
```bash
# Fix file permissions
chmod 644 *.txt
chmod 755 .

# Check directory permissions
ls -la

# Run with sudo (not recommended)
sudo python main.py
```

#### Encoding Issues
**Problem**: `UnicodeDecodeError: 'utf-8' codec can't decode...`
```bash
# Check file encoding
file -i input_article.txt

# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 input_article.txt -o input_article_utf8.txt

# Use UTF-8 encoded file
python main.py --article input_article_utf8.txt
```

### 4. API Issues

#### Rate Limiting
**Problem**: `Rate limit exceeded` or `429 Too Many Requests`
```bash
# Reduce batch size
export BATCH_SIZE=5
export MAX_CONCURRENT_REQUESTS=3
export SLEEP_TIME=1.0

# Check API usage
# Visit OpenAI dashboard: https://platform.openai.com/usage
```

#### API Key Invalid
**Problem**: `401 Unauthorized` or `Invalid API key`
```bash
# Verify API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models

# Check key format (should start with sk-)
echo $OPENAI_API_KEY | grep "^sk-"

# Regenerate key if needed
# Visit: https://platform.openai.com/api-keys
```

#### API Timeout
**Problem**: `TimeoutError` or `Request timeout`
```bash
# Increase timeout
export API_TIMEOUT=60

# Check network connectivity
curl -I https://api.openai.com

# Use different model
export API_MODEL=gpt-4o-mini  # Faster than gpt-4
```

### 5. Processing Issues

#### Memory Issues
**Problem**: `MemoryError` or high memory usage
```bash
# Reduce batch size
export BATCH_SIZE=3

# Monitor memory
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# Use smaller articles
split -l 100 large_article.txt article_part_
```

#### Slow Processing
**Problem**: Processing takes too long
```bash
# Optimize settings
export BATCH_SIZE=15
export MAX_CONCURRENT_REQUESTS=10
export SLEEP_TIME=0.1

# Check system resources
htop  # or top on macOS/Linux
```

#### Translation Quality Issues
**Problem**: Poor translation quality
```bash
# Use better model
export API_MODEL=gpt-4

# Increase context
# Ensure context sentences are included

# Check target words
cat target_words.txt
```

### 6. Vocabulary Issues

#### Vocabulary Files Not Loading
**Problem**: Vocabulary files not being read
```bash
# Check file format
head -5 known_words.txt

# Ensure one word per line
cat > known_words.txt << EOF
hello
world
python
EOF

# Check file encoding
file -i known_words.txt
```

#### Duplicate Words
**Problem**: Duplicate entries in vocabulary
```bash
# Remove duplicates
sort known_words.txt | uniq > known_words_clean.txt
mv known_words_clean.txt known_words.txt

# Do the same for other files
sort target_words.txt | uniq > target_words_clean.txt
mv target_words_clean.txt target_words.txt
```

### 7. Logging Issues

#### No Log Output
**Problem**: No logs being generated
```bash
# Check log level
export LOG_LEVEL=DEBUG

# Check log file permissions
touch lexilearn.log
chmod 644 lexilearn.log

# Check disk space
df -h
```

#### Too Much Log Output
**Problem**: Excessive logging
```bash
# Reduce log level
export LOG_LEVEL=WARNING

# Disable file logging
export LOG_TO_FILE=false
```

## 🔧 Advanced Troubleshooting

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python main.py --article test.txt 2>&1 | tee debug.log

# Analyze debug output
grep ERROR debug.log
grep WARNING debug.log
```

### Network Diagnostics
```bash
# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"test"}]}' \
     https://api.openai.com/v1/chat/completions

# Check DNS resolution
nslookup api.openai.com

# Check SSL certificates
openssl s_client -connect api.openai.com:443
```

### Memory Profiling
```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler main.py

# Check for memory leaks
python -c "import gc; import psutil; print(f'Objects: {len(gc.get_objects())}')"
```

### Performance Profiling
```bash
# Install profiler
pip install py-spy

# Profile CPU usage
py-spy top --pid $(pgrep -f "python main.py")

# Generate flame graph
py-spy record -o profile.svg -- python main.py
```

## 🐳 Docker Troubleshooting

### Container Issues
```bash
# Check container logs
docker logs lexilearn-container

# Run with debug
docker run -e LOG_LEVEL=DEBUG lexilearn

# Interactive debugging
docker run -it --entrypoint /bin/bash lexilearn
```

### Volume Issues
```bash
# Check volume mounts
docker run -v $(pwd):/app --rm lexilearn ls -la /app

# Fix permissions
docker run -v $(pwd):/app --rm lexilearn chmod 644 /app/*.txt
```

## 🧪 Test Environment

### Create Test Environment
```bash
# Create test directory
mkdir test_env && cd test_env

# Copy essential files
cp ../.env.example .env
cp ../requirements.txt .
cp ../main.py .
cp ../config.py .
cp ../vocabulary.py .
cp ../text_processor.py .
cp ../translator.py .
cp ../article_processor.py .
cp ../logger.py .

# Create test files
echo "The quick brown fox jumps over the lazy dog." > input_article.txt
echo -e "the\nand\nor\nbut" > known_words.txt
echo -e "quick\nbrown\nlazy" > target_words.txt

# Test basic functionality
python main.py
```

### Automated Testing
```bash
# Create test script
cat > test_all.sh << 'EOF'
#!/bin/bash
set -e

echo "=== LexiLearn Diagnostic ==="
echo "Python version: $(python --version)"
echo "Virtual env: $VIRTUAL_ENV"

echo -e "\n=== Configuration Test ==="
python -c "from config import Config; Config().validate()" && echo "✅ Config valid"

echo -e "\n=== Vocabulary Test ==="
python -c "from vocabulary import VocabularyManager; import asyncio; v=VocabularyManager(); asyncio.run(v.initialize())" && echo "✅ Vocabulary loaded"

echo -e "\n=== Text Processing Test ==="
python -c "from text_processor import TextProcessor; t=TextProcessor(); print('✅ Text processor ready')"

echo -e "\n=== Translation Test ==="
python -c "from translator import Translator; import asyncio; async def test(): async with Translator() as tr: await tr.translate_word('test', 'This is a test'); print('✅ Translator working'); asyncio.run(test())"

echo -e "\n=== All tests passed! ==="
EOF

chmod +x test_all.sh
./test_all.sh
```

## 📊 Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `ModuleNotFoundError: No module named 'nltk'` | NLTK not installed | `pip install nltk` |
| `FileNotFoundError: input_article.txt` | Missing input file | Create or specify file |
| `ValueError: OPENAI_API_KEY is required` | Missing API key | Set OPENAI_API_KEY |
| `aiohttp.ClientError: Connection timeout` | Network issues | Check internet connection |
| `UnicodeDecodeError: 'utf-8'` | Wrong file encoding | Convert file to UTF-8 |
| `PermissionError: [Errno 13]` | File permissions | Fix file permissions |
| `RuntimeError: Event loop is closed` | Async issues | Use proper async context |

## 🆘 Getting Help

### Before Asking for Help
1. Run diagnostic script: `python test_setup.py`
2. Check this troubleshooting guide
3. Search existing issues
4. Check system requirements

### Information to Provide
When asking for help, include:
- **Error message**: Full error text
- **Environment**: OS, Python version, LexiLearn version
- **Configuration**: Relevant .env settings (remove API key)
- **Steps to reproduce**: What you did
- **Expected vs actual**: What should happen vs what happened

### Support Channels
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions
- **Email**: Security issues (maintainers@lexilearn.com)

## 🔍 Debug Tools

### System Information Script
```bash
cat > system_info.py << 'EOF'
#!/usr/bin/env python3
import sys
import platform
import subprocess

print("=== System Information ===")
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Architecture: {platform.architecture()}")

try:
    import nltk
    print(f"NLTK: {nltk.__version__}")
except ImportError:
    print("NLTK: Not installed")

try:
    import aiohttp
    print(f"aiohttp: {aiohttp.__version__}")
except ImportError:
    print("aiohttp: Not installed")

print("\n=== Environment Variables ===")
import os
for var in ['OPENAI_API_KEY', 'BATCH_SIZE', 'LOG_LEVEL']:
    value = os.getenv(var, 'Not set')
    if var == 'OPENAI_API_KEY' and value != 'Not set':
        value = '***' + value[-4:]  # Mask API key
    print(f"{var}: {value}")

print("\n=== File Check ===")
from pathlib import Path
files = ['input_article.txt', 'known_words.txt', 'target_words.txt', '.env']
for file in files:
    exists = Path(file).exists()
    print(f"{file}: {'✅' if exists else '❌'}")
EOF

python system_info.py
```

## 📝 Issue Resolution Log

### Issue #1: Windows Path Issues
**Problem**: Path separator issues on Windows
**Solution**: Use `pathlib.Path` for cross-platform compatibility

### Issue #2: Memory Leaks
**Problem**: Memory usage increasing over time
**Solution**: Added proper cleanup in async context managers

### Issue #3: Rate Limiting
**Problem**: Hitting OpenAI rate limits
**Solution**: Implemented exponential backoff and configurable delays