# LexiLearn Makefile
# ==================
# This Makefile provides automation for development, testing, building, and releasing LexiLearn.
#
# Usage:
#   make help              - Show this help message
#   make install           - Install the package in development mode
#   make install-dev       - Install development dependencies
#   make install-test      - Install test dependencies
#   make test              - Run all tests
#   make test-unit         - Run unit tests
#   make test-integration  - Run integration tests
#   make test-e2e          - Run end-to-end tests
#   make coverage          - Run tests with coverage report
#   make lint              - Run code linting
#   make format            - Format code with black and isort
#   make check             - Run all code quality checks
#   make security          - Run security checks
#   make build             - Build source distribution and wheel
#   make clean             - Clean build artifacts
#   make distclean         - Clean all generated files
#   make release-test      - Test release to Test PyPI
#   make release           - Release to PyPI (requires proper checks)

# Variables
PYTHON ?= python3
PIP ?= pip
PYTEST ?= pytest
TWINE ?= twine
BUILD ?= python -m build

# Package information
PACKAGE_NAME = lexilearn
VERSION := $(shell $(PYTHON) -c "import tomllib; f=open('pyproject.toml', 'rb'); print(tomllib.load(f)['project']['version'])" 2>/dev/null || $(PYTHON) -c "import configparser; c=configparser.ConfigParser(); c.read('setup.cfg'); print(c['metadata']['version'])" 2>/dev/null || echo "unknown")

# Check if required files exist
ifeq ($(wildcard pyproject.toml),)
  ifeq ($(wildcard setup.cfg),)
    $(error Neither pyproject.toml nor setup.cfg found)
  endif
endif

# Directories
SRC_DIR = lexilearn
TEST_DIR = tests
DIST_DIR = dist
BUILD_DIR = build
DOCS_DIR = docs

# Default target
.DEFAULT_GOAL := help

# Help target
.PHONY: help
help: ## Show this help message
	@echo "LexiLearn Makefile"
	@echo "=================="
	@echo "Usage: make [target]"
	@echo ""
	@echo "Development targets:"
	@echo "  install           Install the package in development mode"
	@echo "  install-dev       Install development dependencies"
	@echo "  install-test      Install test dependencies"
	@echo ""
	@echo "Testing targets:"
	@echo "  test              Run all tests"
	@echo "  test-unit         Run unit tests"
	@echo "  test-integration  Run integration tests"
	@echo "  test-e2e          Run end-to-end tests"
	@echo "  coverage          Run tests with coverage report"
	@echo ""
	@echo "Code quality targets:"
	@echo "  lint              Run code linting"
	@echo "  format            Format code with black and isort"
	@echo "  check             Run all code quality checks"
	@echo "  security          Run security checks"
	@echo ""
	@echo "Build targets:"
	@echo "  build             Build source distribution and wheel"
	@echo "  clean             Clean build artifacts"
	@echo "  distclean         Clean all generated files"
	@echo ""
	@echo "Release targets:"
	@echo "  release-test      Test release to Test PyPI"
	@echo "  release           Release to PyPI (requires proper checks)"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development environment setup
.PHONY: install
install: ## Install the package in development mode
	$(PIP) install -e .

.PHONY: install-dev
install-dev: ## Install development dependencies
	$(PIP) install -e .[dev]

.PHONY: install-test
install-test: ## Install test dependencies
	$(PIP) install -e .[test]

# Testing targets
.PHONY: test
test: ## Run all tests
	@echo "Running all tests..."
	$(PYTEST) $(TEST_DIR) || (echo "Tests failed!"; exit 1)

.PHONY: test-unit
test-unit: ## Run unit tests
	@echo "Running unit tests..."
	$(PYTEST) $(TEST_DIR)/unit || (echo "Unit tests failed!"; exit 1)

.PHONY: test-integration
test-integration: ## Run integration tests
	@echo "Running integration tests..."
	$(PYTEST) $(TEST_DIR)/integration || (echo "Integration tests failed!"; exit 1)

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	@echo "Running end-to-end tests..."
	$(PYTEST) $(TEST_DIR)/e2e || (echo "End-to-end tests failed!"; exit 1)

.PHONY: coverage
coverage: ## Run tests with coverage report
	@echo "Running tests with coverage..."
	$(PYTEST) --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html || (echo "Coverage tests failed!"; exit 1)

# Code quality targets
.PHONY: lint
lint: ## Run code linting
	@echo "Running linting checks..."
	$(PYTHON) -m flake8 $(SRC_DIR) $(TEST_DIR) || (echo "Flake8 checks failed!"; exit 1)
	$(PYTHON) -m pylint $(SRC_DIR) || (echo "Pylint checks failed!"; exit 1)

.PHONY: format
format: ## Format code with black and isort
	@echo "Formatting code..."
	$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR) || (echo "Black formatting failed!"; exit 1)
	$(PYTHON) -m isort $(SRC_DIR) $(TEST_DIR) || (echo "ISort formatting failed!"; exit 1)

.PHONY: check
check: ## Run all code quality checks
	@echo "Running all code quality checks..."
	$(PYTHON) -m black --check $(SRC_DIR) $(TEST_DIR) || (echo "Black checks failed!"; exit 1)
	$(PYTHON) -m isort --check-only $(SRC_DIR) $(TEST_DIR) || (echo "ISort checks failed!"; exit 1)
	$(PYTHON) -m flake8 $(SRC_DIR) $(TEST_DIR) || (echo "Flake8 checks failed!"; exit 1)
	$(PYTHON) -m mypy $(SRC_DIR) || (echo "MyPy checks failed!"; exit 1)
	@echo "Running structure validation..."
	$(PYTHON) -m $(PACKAGE_NAME).validate_structure || (echo "Structure validation failed!"; exit 1)

.PHONY: security
security: ## Run security checks
	@echo "Running security checks..."
	$(PYTHON) -m bandit -r $(SRC_DIR) || (echo "Bandit security checks failed!"; exit 1)
	$(PYTHON) -m safety check || (echo "Safety dependency checks failed!"; exit 1)

# Build targets
.PHONY: build
build: clean ## Build source distribution and wheel
	@echo "Building $(PACKAGE_NAME) version $(VERSION)"
	$(BUILD) --sdist --wheel || (echo "Build failed!"; exit 1)
	$(TWINE) check $(DIST_DIR)/* || (echo "Twine check failed!"; exit 1)

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf $(DIST_DIR) $(BUILD_DIR) *.egg-info .pytest_cache .coverage htmlcov

.PHONY: distclean
distclean: clean ## Clean all generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache .pytest_cache .coverage htmlcov

# Release targets
.PHONY: release-test
release-test: build ## Test release to Test PyPI
	@echo "Testing release to Test PyPI"
	@echo "Version: $(VERSION)"
	@echo "Files to upload:"
	@ls -la $(DIST_DIR)/
	@echo ""
	@echo "To upload, run: twine upload --repository testpypi $(DIST_DIR)/*"
	@echo "This is a dry run. Uncomment the twine command to actually upload."

.PHONY: release
release: check test build ## Release to PyPI (requires proper checks)
	@echo "Preparing to release $(PACKAGE_NAME) version $(VERSION)"
	@echo ""
	@echo "Release checklist:"
	@echo "1. Ensure all tests pass: make test"
	@echo "2. Ensure code quality checks pass: make check"
	@echo "3. Ensure version is updated in pyproject.toml and setup.cfg"
	@echo "4. Ensure CHANGES.md is updated with release notes"
	@echo "5. Ensure git tag is created: git tag -a v$(VERSION) -m 'Release version $(VERSION)'"
	@echo ""
	@echo "Files to upload:"
	@ls -la $(DIST_DIR)/
	@echo ""
	@read -p "Are you sure you want to release version $(VERSION) to PyPI? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(TWINE) upload $(DIST_DIR)/*; \
		echo "Release completed!"; \
		echo "Next steps:"; \
		echo "1. Create a git tag: git tag -a v$(VERSION) -m 'Release version $(VERSION)'"; \
		echo "2. Push the tag: git push origin v$(VERSION)"; \
		echo "3. Create a GitHub release"; \
	else \
		echo "Release cancelled."; \
	fi