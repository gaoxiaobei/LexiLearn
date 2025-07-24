# LexiLearn Release Notes

## Version 1.0.0 (2025-07-24)

### Summary

This is the first official release of LexiLearn as a properly packaged Python application. This release focuses on restructuring the project into a modern, installable package with improved packaging configuration and console script entry points.

### Major Changes

- **Project Restructuring**: The entire codebase has been reorganized into a proper `lexilearn` package structure
- **Modern Packaging**: Implemented modern Python packaging with `pyproject.toml` configuration
- **Console Scripts**: Added convenient command-line entry points for all major functionalities

### New Features

- **Proper Package Structure**: Code is now organized in a standard Python package layout
- **Console Scripts**:
  - `lexilearn`: Main application entry point for processing articles
  - `lexilearn-setup`: Utility to download required NLTK data
  - `lexilearn-validate`: Structure validation tool
- **Improved Installation**: Package can now be installed via pip with all dependencies automatically handled
- **Enhanced Documentation**: Updated documentation reflecting the new package structure

### Fixes

- **Packaging Issues**: Resolved previous issues with package distribution and installation
- **Dependency Management**: Standardized dependency specification in `pyproject.toml`
- **Entry Point Configuration**: Fixed console script entry points for better usability

### Breaking Changes

- **Installation Method**: Users now need to install the package via pip rather than running directly from source
- **Module Imports**: Direct imports from the old flat structure will no longer work; all imports should use the `lexilearn` package namespace
- **File Structure**: Project files have been reorganized into the `lexilearn` package directory

### Migration Guide

For users upgrading from the previous version:

1. Install the package using pip:
   ```bash
   pip install lexilearn
   ```

2. Use the new console scripts instead of direct Python execution:
   ```bash
   # Old way
   python main.py
   
   # New way
   lexilearn
   ```

3. Ensure all custom scripts update their imports to use the `lexilearn` package namespace.

### Known Issues

- None at this time

---

For previous changes, please see the commit history.