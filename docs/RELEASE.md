# LexiLearn Release Process

This document describes the release process for LexiLearn, including automated tools to streamline releases.

## 🚀 Automated Release Process

LexiLearn provides two automated tools to simplify the release process:

1. **Makefile**: Contains targets for building, testing, and publishing
2. **Release Script**: A comprehensive bash script for full release automation

### Using the Makefile

The Makefile provides granular control over the release process:

```bash
# Build the package
make build

# Test the release to Test PyPI
make release-test

# Release to PyPI (with confirmation prompts)
make release
```

For a full list of available targets, run:
```bash
make help
```

### Using the Release Script

The release script (`scripts/release.sh`) provides a more guided approach to releases:

```bash
# Validate release checklist
./scripts/release.sh validate

# Run all pre-release checks
./scripts/release.sh pre-checks

# Build the package
./scripts/release.sh build

# Test package installation
./scripts/release.sh test-install

# Perform a test release to Test PyPI
./scripts/release.sh test-release

# Perform a full release to PyPI
./scripts/release.sh release
```

## 📋 Manual Release Process

If you prefer to perform the release manually, follow these steps:

### 1. Pre-Release Preparation

- [ ] Update version number in `pyproject.toml`
- [ ] Update version number in `setup.cfg` (if applicable)
- [ ] Update `CHANGES.md` with release notes
- [ ] Run all tests: `make test`
- [ ] Run code quality checks: `make check`
- [ ] Run security checks: `make security`

### 2. Build Process

```bash
# Clean previous builds
make clean

# Build source distribution and wheel
make build
```

### 3. Local Installation Test

Create a fresh virtual environment and test the installation:

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate

# Install from built package
pip install dist/lexilearn-*.whl

# Test console scripts
lexilearn --help
lexilearn-setup
lexilearn-validate

# Clean up
deactivate
rm -rf test_env
```

### 4. Publish to Test PyPI

First, test the release on Test PyPI:

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ lexilearn
```

### 5. Publish to PyPI

After verifying the Test PyPI release:

```bash
# Upload to PyPI
twine upload dist/*
```

### 6. Git Tagging

Create and push a git tag for the release:

```bash
# Get version
VERSION=$(python -c "import tomllib; f=open('pyproject.toml', 'rb'); print(tomllib.load(f)['project']['version'])")

# Create tag
git tag -a "v$VERSION" -m "Release version $VERSION"

# Push tag
git push origin "v$VERSION"
```

## 🔧 Release Tools

### Makefile Targets

| Target | Description |
|--------|-------------|
| `build` | Build source distribution and wheel |
| `release-test` | Test release to Test PyPI |
| `release` | Release to PyPI (with confirmation prompts) |
| `clean` | Clean build artifacts |
| `distclean` | Clean all generated files |

### Release Script Actions

| Action | Description |
|--------|-------------|
| `validate` | Validate release checklist |
| `pre-checks` | Run pre-release checks (tests, linting, etc.) |
| `build` | Build the package |
| `test-install` | Test package installation in a virtual environment |
| `test-release` | Full test release process |
| `release` | Full release process |

## 🛡️ Safety Checks

The automated release process includes several safety checks:

1. **Version Consistency**: Ensures version numbers match across all files
2. **Test Validation**: Runs all test suites before release
3. **Code Quality**: Verifies code quality standards
4. **Security Scanning**: Checks for known vulnerabilities
5. **Interactive Confirmation**: Requires explicit confirmation before PyPI upload
6. **Git Tagging**: Automatically creates and pushes git tags

## 🚨 Rollback Plan

If issues are discovered after release:

1. Immediately assess severity of issue
2. If critical, yank release from PyPI: `twine remove dist/lexilearn-*`
3. Create issue tracking the problem
4. Develop fix in separate branch
5. Plan hotfix release

## 📞 Support

For issues with the release process:

1. Check the [troubleshooting guide](TROUBLESHOOTING.md)
2. Review the [release checklist](../RELEASE_CHECKLIST.md)
3. Create a new issue with:
   - Error messages
   - Steps to reproduce
   - Environment information