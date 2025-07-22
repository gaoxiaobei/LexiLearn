# Configuration Documentation

Comprehensive guide to all configuration options available in LexiLearn.

## 📋 Overview

LexiLearn uses a hierarchical configuration system with environment variable support. All configuration is validated at startup with helpful error messages.

## 🎯 Quick Configuration

### Essential Configuration
```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Recommended
BATCH_SIZE=10
USE_TARGET_WORDS=true
```

### Complete Configuration Template
```bash
# Copy from .env.example
cp .env.example .env

# Edit with your settings
nano .env
```

## 🔧 Configuration Categories

### API Configuration

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `OPENAI_API_KEY` | - | **Required** OpenAI API key | `sk-abc123...` |
| `API_BASE_URL` | `https://api.openai.com/v1/chat/completions` | OpenAI API endpoint | `https://api.openai.com/v1/chat/completions` |
| `API_MODEL` | `gpt-4o-mini` | OpenAI model to use | `gpt-4`, `gpt-4o-mini`, `gpt-3.5-turbo` |
| `API_MAX_RETRIES` | `3` | Max retry attempts for failed requests | `5` |
| `API_TIMEOUT` | `30` | Request timeout in seconds | `60` |

### Processing Configuration

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `BATCH_SIZE` | `10` | Sentences per processing batch | `5`, `15`, `20` |
| `CONNECTOR_LIMIT` | `10` | Max concurrent HTTP connections | `20` |
| `SLEEP_TIME` | `0.5` | Delay between batches (seconds) | `1.0`, `0.1` |
| `USE_TARGET_WORDS` | `true` | Filter translations by target words | `true`, `false` |
| `MAX_CONCURRENT_REQUESTS` | `5` | Max concurrent API requests | `10` |

### File Configuration

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `INPUT_ARTICLE` | `input_article.txt` | Default article file | `my_article.txt` |
| `KNOWN_WORDS_FILE` | `known_words.txt` | Known vocabulary file | `vocabulary/known.txt` |
| `TARGET_WORDS_FILE` | `target_words.txt` | Target vocabulary file | `vocabulary/target.txt` |
| `LEARNED_WORDS_FILE` | `learned_words.txt` | Learned words file | `vocabulary/learned.txt` |
| `OUTPUT_ARTICLE` | `output_article.txt` | Processed output file | `results/processed.txt` |
| `LOG_FILE` | `lexilearn.log` | Log file location | `logs/app.log` |

### Logging Configuration

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `LOG_LEVEL` | `INFO` | Logging level | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `LOG_TO_FILE` | `true` | Enable file logging | `true`, `false` |
| `LOG_TO_CONSOLE` | `true` | Enable console logging | `true`, `false` |

## 📝 Configuration Examples

### Development Configuration
```bash
# .env.development
OPENAI_API_KEY=sk-dev-key
API_MODEL=gpt-4o-mini
BATCH_SIZE=5
LOG_LEVEL=DEBUG
USE_TARGET_WORDS=true
```

### Production Configuration
```bash
# .env.production
OPENAI_API_KEY=sk-prod-key
API_MODEL=gpt-4
BATCH_SIZE=15
LOG_LEVEL=INFO
USE_TARGET_WORDS=false
MAX_CONCURRENT_REQUESTS=10
```

### Testing Configuration
```bash
# .env.test
OPENAI_API_KEY=sk-test-key
API_MODEL=gpt-4o-mini
BATCH_SIZE=2
LOG_LEVEL=DEBUG
USE_TARGET_WORDS=true
SLEEP_TIME=0.1
```

## 🔍 Advanced Configuration

### Rate Limiting Configuration
```bash
# Conservative settings for rate-limited APIs
BATCH_SIZE=5
MAX_CONCURRENT_REQUESTS=3
SLEEP_TIME=1.0
API_MAX_RETRIES=5
```

### Performance Configuration
```bash
# Aggressive settings for fast processing
BATCH_SIZE=20
MAX_CONCURRENT_REQUESTS=10
SLEEP_TIME=0.1
CONNECTOR_LIMIT=20
```

### Memory-Conscious Configuration
```bash
# Settings for memory-constrained environments
BATCH_SIZE=3
MAX_CONCURRENT_REQUESTS=2
LOG_LEVEL=WARNING
```

## 🛠️ Configuration Methods

### Method 1: Environment Variables
```bash
# Temporary (current session)
export OPENAI_API_KEY="sk-abc123"
export BATCH_SIZE=10
python main.py

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export OPENAI_API_KEY="sk-abc123"' >> ~/.bashrc
source ~/.bashrc
```

### Method 2: .env File
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-abc123
BATCH_SIZE=10
USE_TARGET_WORDS=true
LOG_LEVEL=INFO
EOF

# Use with python-dotenv (automatically loaded)
python main.py
```

### Method 3: Programmatic Configuration
```python
import os
from config import Config

# Set environment variables programmatically
os.environ['OPENAI_API_KEY'] = 'sk-abc123'
os.environ['BATCH_SIZE'] = '15'

# Load configuration
config = Config()
print(f"Using batch size: {config.processing.batch_size}")
```

### Method 4: Configuration Files
```python
# config.json
{
    "api": {
        "api_key": "sk-abc123",
        "model": "gpt-4o-mini",
        "max_retries": 3
    },
    "processing": {
        "batch_size": 10,
        "use_target_words": true
    }
}

# Load from JSON
import json
with open('config.json') as f:
    config_data = json.load(f)
```

## 🎯 Configuration Templates

### Template 1: Beginner Setup
```bash
# .env.beginner
OPENAI_API_KEY=your-key-here
BATCH_SIZE=5
USE_TARGET_WORDS=true
LOG_LEVEL=INFO
```

### Template 2: Advanced User
```bash
# .env.advanced
OPENAI_API_KEY=your-key-here
API_MODEL=gpt-4
BATCH_SIZE=15
CONNECTOR_LIMIT=20
MAX_CONCURRENT_REQUESTS=10
SLEEP_TIME=0.2
USE_TARGET_WORDS=false
LOG_LEVEL=DEBUG
```

### Template 3: Enterprise Setup
```bash
# .env.enterprise
OPENAI_API_KEY=your-key-here
API_BASE_URL=https://your-enterprise-endpoint.com/v1/chat/completions
API_MODEL=gpt-4
API_TIMEOUT=60
API_MAX_RETRIES=5
BATCH_SIZE=20
CONNECTOR_LIMIT=50
MAX_CONCURRENT_REQUESTS=20
SLEEP_TIME=0.1
USE_TARGET_WORDS=false
LOG_LEVEL=WARNING
LOG_FILE=/var/log/lexilearn.log
```

## 🔐 Security Best Practices

### API Key Management
```bash
# Never commit API keys to version control
echo ".env" >> .gitignore

# Use environment-specific files
echo ".env.local" >> .gitignore
echo ".env.production" >> .gitignore

# Use secrets management in production
# AWS Secrets Manager, Azure Key Vault, etc.
```

### File Permissions
```bash
# Secure .env file
chmod 600 .env

# Secure log files
chmod 644 lexilearn.log
```

## 🧪 Configuration Validation

### Built-in Validation
```python
from config import Config

try:
    config = Config()
    config.validate()
    print("✅ Configuration is valid")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
```

### Custom Validation Script
```python
#!/usr/bin/env python3
import os
from config import Config

def validate_config():
    """Validate configuration and provide helpful messages."""
    
    required_vars = ['OPENAI_API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"❌ Missing required variables: {', '.join(missing)}")
        return False
    
    try:
        config = Config()
        config.validate()
        print("✅ All configuration valid")
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    validate_config()
```

## 🚀 Environment-Specific Configurations

### Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Use environment variables
ENV OPENAI_API_KEY=""
ENV BATCH_SIZE=10
ENV LOG_LEVEL=INFO

CMD ["python", "main.py"]
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
      - BATCH_SIZE=10
      - USE_TARGET_WORDS=true
    volumes:
      - ./articles:/app/articles
      - ./vocabulary:/app/vocabulary
      - ./output:/app/output
    env_file:
      - .env
```

### Kubernetes Configuration
```yaml
# k8s-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: lexilearn-config
data:
  BATCH_SIZE: "10"
  USE_TARGET_WORDS: "true"
  LOG_LEVEL: "INFO"
---
apiVersion: v1
kind: Secret
metadata:
  name: lexilearn-secrets
type: Opaque
stringData:
  OPENAI_API_KEY: "sk-abc123"
```

## 📊 Configuration Monitoring

### Health Check Configuration
```python
# health_check.py
import os
from config import Config

def check_configuration():
    """Check if configuration is healthy."""
    
    checks = {
        'api_key_set': bool(os.getenv('OPENAI_API_KEY')),
        'config_valid': False,
        'files_accessible': False
    }
    
    try:
        config = Config()
        config.validate()
        checks['config_valid'] = True
        
        # Check file accessibility
        from pathlib import Path
        files_to_check = [
            config.file.known_words_file,
            config.file.target_words_file,
            config.file.learned_words_file
        ]
        
        checks['files_accessible'] = all(
            Path(f).parent.exists() for f in files_to_check
        )
        
    except Exception:
        pass
    
    return checks

# Usage
if __name__ == "__main__":
    health = check_configuration()
    print("Configuration Health:", health)
```

## 🔄 Configuration Migration

### Version 1.x to 2.x Migration
```bash
# Old configuration (v1.x)
export API_KEY=sk-abc123
export BATCH=10

# New configuration (v2.x)
export OPENAI_API_KEY=sk-abc123
export BATCH_SIZE=10
```

### Migration Script
```python
# migrate_config.py
import os
import json

def migrate_v1_to_v2():
    """Migrate from v1.x to v2.x configuration."""
    
    old_to_new = {
        'API_KEY': 'OPENAI_API_KEY',
        'BATCH': 'BATCH_SIZE',
        'TARGET_FILTER': 'USE_TARGET_WORDS'
    }
    
    # Read old .env
    old_config = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    old_config[key] = value
    
    # Create new .env
    new_config = {}
    for old_key, value in old_config.items():
        new_key = old_to_new.get(old_key, old_key)
        new_config[new_key] = value
    
    # Write new .env
    with open('.env.new', 'w') as f:
        for key, value in new_config.items():
            f.write(f"{key}={value}\n")
    
    print("Migration complete. Check .env.new")

if __name__ == "__main__":
    migrate_v1_to_v2()
```

## 🎨 Custom Configuration Schemes

### Color-coded Logging
```bash
# Enable colored logs
export LOG_COLORS=true
export LOG_LEVEL_COLORS='{"DEBUG":"blue","INFO":"green","WARNING":"yellow","ERROR":"red"}'
```

### Custom File Formats
```bash
# Support for different file formats
export INPUT_FORMAT=txt
export OUTPUT_FORMAT=md
export VOCABULARY_FORMAT=csv
```

## 📋 Configuration Checklist

Before running LexiLearn:

- [ ] **Required**: Set `OPENAI_API_KEY`
- [ ] **Recommended**: Configure `BATCH_SIZE` based on API limits
- [ ] **Optional**: Set up target words filtering
- [ ] **Optional**: Configure logging level
- [ ] **Optional**: Customize file paths
- [ ] **Optional**: Set up rate limiting
- [ ] **Optional**: Configure for production use

## 🆘 Troubleshooting Configuration

### Common Issues

1. **"OPENAI_API_KEY not found"**
   ```bash
   # Check if set
   echo $OPENAI_API_KEY
   
   # Set temporarily
   export OPENAI_API_KEY="your-key"
   ```

2. **"Invalid batch size"**
   ```bash
   # Must be integer
   export BATCH_SIZE=10  # ✅
   export BATCH_SIZE="10"  # ✅
   export BATCH_SIZE=ten  # ❌
   ```

3. **"File not found"**
   ```bash
   # Check file paths
   ls -la known_words.txt
   mkdir -p vocabulary/
   touch vocabulary/known.txt
   ```

4. **"Permission denied"**
   ```bash
   # Fix permissions
   chmod 644 .env
   chmod 755 .
   ```

### Debug Configuration
```bash
# Print all configuration
python -c "from config import Config; c=Config(); print(c.to_dict())"

# Test specific values
python -c "from config import Config; print(Config().api.model)"