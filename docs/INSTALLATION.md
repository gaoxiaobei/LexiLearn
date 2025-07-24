# Installation and Setup Guide

This guide provides comprehensive instructions for installing and setting up LexiLearn on various platforms and environments.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space for installation
- **Network**: Internet connection for API calls and NLTK data

### Required Accounts
- **OpenAI Account**: Required for translation API
  - Sign up at [OpenAI](https://platform.openai.com)
  - Generate API key from [API Keys](https://platform.openai.com/api-keys)

## 🚀 Quick Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd lexilearn

# Run automated setup
python download_nltk_data.py

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key
```

### Option 2: Manual Installation

#### Step 1: Clone Repository
```bash
git clone <repository-url>
cd lexilearn
```

#### Step 2: Create Virtual Environment
```bash
# Using venv (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies
Using Makefile (recommended):
```bash
# Install development dependencies
make install-dev
```

Manual installation:
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest black flake8 mypy
```

#### Step 4: Download NLTK Data
```bash
# Download required NLTK corpora
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

#### Step 5: Configure Environment
```bash
# Copy configuration template
cp .env.example .env

# Edit .env with your settings
# Required: Set OPENAI_API_KEY
```

## 🔧 Platform-Specific Instructions

### Windows

#### Using Command Prompt
```cmd
# Install Python from python.org first
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python download_nltk_data.py
```

#### Using PowerShell
```powershell
# Install Python from Microsoft Store or python.org
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python download_nltk_data.py
```

#### Using Windows Subsystem for Linux (WSL)
```bash
# Install WSL from Microsoft Store
wsl
sudo apt update && sudo apt install python3 python3-pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python download_nltk_data.py
```

### macOS

#### Using Terminal
```bash
# Install Python via Homebrew (recommended)
brew install python

# Or use system Python (3.8+ required)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python download_nltk_data.py
```

#### Using Conda
```bash
# Create conda environment
conda create -n lexilearn python=3.9
conda activate lexilearn
pip install -r requirements.txt
python download_nltk_data.py
```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python download_nltk_data.py
```

### Linux (CentOS/RHEL)

```bash
# Install Python 3
sudo yum install python3 python3-pip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python download_nltk_data.py
```

## ⚙️ Configuration Setup

### Step 1: Get OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Create new secret key
5. Copy the key (starts with `sk-`)

### Step 2: Configure Environment
```bash
# Edit .env file
nano .env  # or use your preferred editor

# Required configuration
OPENAI_API_KEY=your-actual-api-key-here

# Optional customizations
API_MODEL=gpt-4o-mini
BATCH_SIZE=10
USE_TARGET_WORDS=true
```

### Step 3: Verify Configuration
```bash
# Test configuration
python test_setup.py

# Expected output:
# ✅ Configuration loaded successfully
# ✅ Vocabulary files initialized
# ✅ Text processing working
# ✅ Translation API accessible
```

## 📁 File Structure Setup

### Create Required Files
```bash
# Create vocabulary files
touch known_words.txt
touch target_words.txt
touch learned_words.txt

# Create sample article
cat > input_article.txt << EOF
The quick brown fox jumps over the lazy dog. This is a simple test article to verify that LexiLearn is working correctly. The ephemeral beauty of nature surrounds us every day.
EOF

# Create known words
cat > known_words.txt << EOF
the
a
is
to
of
and
this
that
EOF

# Create target words (optional)
cat > target_words.txt << EOF
ephemeral
surrounds
EOF
```

### Directory Structure
```
lexilearn/
├── .env                    # Your configuration
├── input_article.txt       # Article to process
├── known_words.txt         # Words you already know
├── target_words.txt        # Words to focus on (optional)
├── learned_words.txt       # Auto-updated learned words
├── output_article.txt      # Processed output
├── lexilearn.log          # Application logs
├── Makefile               # Build and release automation
├── scripts/
│   └── release.sh         # Release automation script
└── docs/
    └── RELEASE.md         # Release process documentation
```

## 🧪 Testing Installation

### Basic Test
```bash
# Run basic functionality test
python -c "from main import main; import asyncio; asyncio.run(main())"

# Or run test suite
python test_setup.py
```

### Verify Components
```bash
# Test configuration
python -c "from config import Config; c = Config(); c.validate(); print('✅ Config valid')"

# Test vocabulary
python -c "from vocabulary import VocabularyManager; import asyncio; v = VocabularyManager(); asyncio.run(v.initialize()); print('✅ Vocabulary loaded')"

# Test text processing
python -c "from text_processor import TextProcessor; t = TextProcessor(); print('✅ Text processor ready')"
```

## 🐳 Docker Installation (Alternative)

### Using Docker
```bash
# Build Docker image
docker build -t lexilearn .

# Run with environment variables
docker run -e OPENAI_API_KEY=your-key -v $(pwd):/app lexilearn

# Or use docker-compose
docker-compose up
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  lexilearn:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./input:/app/input
      - ./output:/app/output
      - ./vocabulary:/app/vocabulary
```

## 🚀 Production Deployment

### Systemd Service (Linux)
```ini
# /etc/systemd/system/lexilearn.service
[Unit]
Description=LexiLearn Article Processor
After=network.target

[Service]
Type=oneshot
User=lexilearn
WorkingDirectory=/opt/lexilearn
Environment=OPENAI_API_KEY=your-key
ExecStart=/opt/lexilearn/venv/bin/python main.py

[Install]
WantedBy=multi-user.target
```

### Windows Service
```powershell
# Using NSSM (Non-Sucking Service Manager)
nssm install LexiLearn "C:\lexilearn\venv\Scripts\python.exe" "C:\lexilearn\main.py"
nssm set LexiLearn Environment OPENAI_API_KEY=your-key
nssm start LexiLearn
```

## 🔍 Troubleshooting Installation

### Common Issues

#### Python Version Issues
```bash
# Check Python version
python --version  # Should be 3.8+
python3 --version

# If multiple Python versions
python3.9 -m venv venv
```

#### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### NLTK Data Download Issues
```bash
# Manual NLTK data download
python -c "import nltk; nltk.download('all')"

# Or specific packages
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

#### Permission Issues (Linux/macOS)
```bash
# Fix file permissions
chmod +x setup.py
chmod 644 *.txt
chmod 600 .env  # Secure API key
```

#### Windows Path Issues
```cmd
# Use forward slashes or raw strings
set INPUT_ARTICLE=articles\\my_article.txt
# or
set INPUT_ARTICLE=articles/my_article.txt
```

### Verification Script
```python
# save as verify_installation.py
import sys
import os
from pathlib import Path

def check_python_version():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    try:
        import nltk
        import aiohttp
        import aiosqlite
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def check_nltk_data():
    try:
        import nltk
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/wordnet')
        print("✅ NLTK data downloaded")
        return True
    except LookupError:
        print("❌ NLTK data missing")
        return False

def check_configuration():
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=your-openai-api-key-here' in content:
            print("❌ API key not configured")
            return False
    
    print("✅ Configuration file exists")
    return True

def main():
    print("LexiLearn Installation Verification")
    print("=" * 40)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_nltk_data(),
        check_configuration()
    ]
    
    if all(checks):
        print("\n🎉 Installation verified successfully!")
        print("Run: python main.py --article input_article.txt")
    else:
        print("\n❌ Installation issues found")
        print("Please check the troubleshooting section")

if __name__ == "__main__":
    main()
```

## 📊 Performance Optimization

### Memory Settings
```bash
# For large files, increase available memory
export PYTHONHASHSEED=0
export PYTHONMALLOC=malloc
```

### Network Optimization
```bash
# Increase connection limits
export CONNECTOR_LIMIT=20
export MAX_CONCURRENT_REQUESTS=10
```

## 🧰 Using the Makefile

LexiLearn includes a comprehensive Makefile that automates common development tasks. To see all available targets, run:

```bash
make help
```

### Common Makefile Targets

```bash
# Install the package in development mode
make install

# Install development dependencies
make install-dev

# Install test dependencies
make install-test

# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run end-to-end tests only
make test-e2e

# Run tests with coverage report
make coverage

# Format code with black and isort
make format

# Run code linting
make lint

# Run all code quality checks
make check

# Run security checks
make security

# Build source distribution and wheel
make build

# Clean build artifacts
make clean

# Clean all generated files
make distclean

# Test release to Test PyPI
make release-test

# Release to PyPI (requires proper checks)
make release
```

## 🔄 Update Instructions

### Updating LexiLearn
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Or using Makefile
make install-dev

# Verify installation
python verify_installation.py
```

### Updating NLTK Data
```bash
# Update NLTK corpora
python -c "import nltk; nltk.download('punkt', force=True); nltk.download('wordnet', force=True)"
```

## 📞 Support

If you encounter issues:
1. Check the [troubleshooting guide](TROUBLESHOOTING.md)
2. Run the verification script above
3. Check existing [issues](https://github.com/your-repo/lexilearn/issues)
4. Create a new issue with:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce