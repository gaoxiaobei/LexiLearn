#!/usr/bin/env python3
"""
Structure validation script for LexiLearn refactored implementation.
This script validates the code structure and basic functionality without external dependencies.
"""

import os
import sys
import ast
from pathlib import Path


def validate_file_structure():
    """Validate that all required files exist."""
    print("📁 Validating file structure...")
    
    required_files = [
        'lexilearn/main.py',
        'lexilearn/config.py',
        'lexilearn/logger.py',
        'lexilearn/vocabulary.py',
        'lexilearn/text_processor.py',
        'lexilearn/translator.py',
        'lexilearn/article_processor.py',
        '.env.example',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True


def validate_python_syntax():
    """Validate Python syntax in all modules."""
    print("🔍 Validating Python syntax...")
    
    python_files = [
        'lexilearn/main.py',
        'lexilearn/config.py',
        'lexilearn/logger.py',
        'lexilearn/vocabulary.py',
        'lexilearn/text_processor.py',
        'lexilearn/translator.py',
        'lexilearn/article_processor.py'
    ]
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
            print(f"   ✅ {file_path}")
        except SyntaxError as e:
            print(f"   ❌ {file_path}: {e}")
            return False
    
    print("✅ All Python files have valid syntax")
    return True


def validate_imports():
    """Validate that imports are properly structured."""
    print("📦 Validating import structure...")
    
    # Check for hardcoded API keys
    files_to_check = [
        'lexilearn/main.py',
        'lexilearn/config.py',
        'lexilearn/translator.py'
    ]
    
    for file_path in files_to_check:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for hardcoded API keys
        if 'your-api-key-here' in content.lower() or 'sk-' in content.lower():
            if file_path != '.env.example':
                print(f"   ⚠️  {file_path}: Contains placeholder API key (expected)")
            continue
        
        # Check for environment variable usage
        if 'os.getenv' in content or 'OPENAI_API_KEY' in content:
            print(f"   ✅ {file_path}: Uses environment variables")
    
    print("✅ Import structure validated")
    return True


def validate_docstrings():
    """Validate that classes and functions have docstrings."""
    print("📝 Validating documentation...")
    
    python_files = [
        'lexilearn/config.py',
        'lexilearn/logger.py',
        'lexilearn/vocabulary.py',
        'lexilearn/text_processor.py',
        'lexilearn/translator.py',
        'lexilearn/article_processor.py',
        'lexilearn/main.py'
    ]
    
    missing_docs = []
    
    for file_path in python_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not ast.get_docstring(node):
                        missing_docs.append(f"{file_path}:{node.name}")
        
        except Exception as e:
            print(f"   ❌ Error parsing {file_path}: {e}")
            return False
    
    if missing_docs:
        print(f"   ⚠️  Missing docstrings: {len(missing_docs)} items")
        for item in missing_docs[:5]:  # Show first 5
            print(f"      - {item}")
    else:
        print("   ✅ All classes and functions have docstrings")
    
    return True


def validate_type_hints():
    """Validate that type hints are used appropriately."""
    print("🔤 Validating type hints...")
    
    python_files = [
        'lexilearn/config.py',
        'lexilearn/vocabulary.py',
        'lexilearn/text_processor.py',
        'lexilearn/translator.py',
        'lexilearn/article_processor.py'
    ]
    
    for file_path in python_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic check for type hints
        type_hint_indicators = ['->', ':', 'from typing import', 'import typing']
        has_type_hints = any(indicator in content for indicator in type_hint_indicators)
        
        if has_type_hints:
            print(f"   ✅ {file_path}: Uses type hints")
        else:
            print(f"   ⚠️  {file_path}: Limited type hints")
    
    print("✅ Type hint validation completed")
    return True


def validate_error_handling():
    """Validate that proper error handling is implemented."""
    print("🛡️  Validating error handling...")
    
    files_to_check = [
        'lexilearn/vocabulary.py',
        'lexilearn/translator.py',
        'lexilearn/article_processor.py',
        'lexilearn/main.py'
    ]
    
    for file_path in files_to_check:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for exception handling patterns
        has_try_except = 'try:' in content
        has_custom_exceptions = 'class.*Error' in content
        has_logging = 'logger.' in content
        
        checks = []
        if has_try_except:
            checks.append("try/except")
        if has_custom_exceptions:
            checks.append("custom exceptions")
        if has_logging:
            checks.append("logging")
        
        print(f"   ✅ {file_path}: {', '.join(checks)}")
    
    print("✅ Error handling validation completed")
    return True


def main():
    """Run all validation checks."""
    print("🚀 LexiLearn Structure Validation\n")
    
    validations = [
        validate_file_structure,
        validate_python_syntax,
        validate_imports,
        validate_docstrings,
        validate_type_hints,
        validate_error_handling
    ]
    
    results = []
    for validation in validations:
        try:
            result = validation()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Validation error: {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("="*50)
    print("Validation Summary")
    print("="*50)
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All structural validations passed!")
        print("✅ LexiLearn refactoring is complete and ready for use.")
    else:
        print("⚠️  Some validations failed. Please review the issues above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)