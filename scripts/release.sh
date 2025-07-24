#!/bin/bash

# LexiLearn Release Script
# ========================
# This script automates the release process for LexiLearn

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if we're in the right directory
check_project_root() {
    if [ ! -f "pyproject.toml" ] && [ ! -f "setup.cfg" ]; then
        print_error "This script must be run from the project root directory"
        exit 1
    fi
}

# Function to get current version
get_version() {
    if [ -f "pyproject.toml" ]; then
        python3 -c "import tomllib; f=open('pyproject.toml', 'rb'); print(tomllib.load(f)['project']['version'])" 2>/dev/null || echo "unknown"
    elif [ -f "setup.cfg" ]; then
        python3 -c "import configparser; c=configparser.ConfigParser(); c.read('setup.cfg'); print(c['metadata']['version'])" 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# Function to validate release checklist
validate_checklist() {
    print_info "Validating release checklist..."
    
    # Check if CHANGES.md is updated
    if [ ! -f "CHANGES.md" ]; then
        print_warning "CHANGES.md not found"
    else
        print_success "CHANGES.md found"
    fi
    
    # Check if version is updated
    VERSION=$(get_version)
    if [ "$VERSION" = "unknown" ]; then
        print_warning "Could not determine package version"
    else
        print_success "Package version: $VERSION"
    fi
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "There are uncommitted changes in the repository"
    else
        print_success "No uncommitted changes"
    fi
}

# Function to run pre-release checks
pre_release_checks() {
    print_info "Running pre-release checks..."
    
    # Run tests
    print_info "Running tests..."
    if make test; then
        print_success "All tests passed"
    else
        print_error "Tests failed"
        exit 1
    fi
    
    # Run code quality checks
    print_info "Running code quality checks..."
    if make check; then
        print_success "All code quality checks passed"
    else
        print_error "Code quality checks failed"
        exit 1
    fi
    
    # Run security checks
    print_info "Running security checks..."
    if make security; then
        print_success "Security checks passed"
    else
        print_warning "Security checks had issues (continuing anyway)"
    fi
}

# Function to build package
build_package() {
    print_info "Building package..."
    if make build; then
        print_success "Package built successfully"
    else
        print_error "Package build failed"
        exit 1
    fi
}

# Function to test installation
test_installation() {
    print_info "Testing package installation..."
    
    # Create a temporary virtual environment
    TEMP_VENV=$(mktemp -d)
    python3 -m venv "$TEMP_VENV"
    
    # Activate virtual environment
    source "$TEMP_VENV/bin/activate"
    
    # Install package
    pip install dist/*.whl
    
    # Test basic commands
    if lexilearn --help >/dev/null 2>&1; then
        print_success "lexilearn command works"
    else
        print_error "lexilearn command failed"
        deactivate
        rm -rf "$TEMP_VENV"
        exit 1
    fi
    
    # Deactivate and clean up
    deactivate
    rm -rf "$TEMP_VENV"
    print_success "Installation test completed"
}

# Function to publish to Test PyPI
publish_test_pypi() {
    print_info "Publishing to Test PyPI..."
    
    if command_exists twine; then
        twine upload --repository testpypi dist/*
        print_success "Published to Test PyPI"
    else
        print_error "Twine not found. Please install it with: pip install twine"
        exit 1
    fi
}

# Function to publish to PyPI
publish_pypi() {
    print_info "Publishing to PyPI..."
    
    if command_exists twine; then
        twine upload dist/*
        print_success "Published to PyPI"
    else
        print_error "Twine not found. Please install it with: pip install twine"
        exit 1
    fi
}

# Function to create git tag
create_git_tag() {
    VERSION=$(get_version)
    if [ "$VERSION" = "unknown" ]; then
        print_error "Could not determine version for git tag"
        exit 1
    fi
    
    TAG="v$VERSION"
    if git tag -a "$TAG" -m "Release version $VERSION"; then
        print_success "Created git tag: $TAG"
    else
        print_error "Failed to create git tag"
        exit 1
    fi
}

# Function to push git tag
push_git_tag() {
    VERSION=$(get_version)
    TAG="v$VERSION"
    
    if git push origin "$TAG"; then
        print_success "Pushed git tag: $TAG"
    else
        print_error "Failed to push git tag"
        exit 1
    fi
}

# Main function
main() {
    print_info "LexiLearn Release Script"
    print_info "========================"
    
    # Parse command line arguments
    ACTION="help"
    if [ $# -gt 0 ]; then
        ACTION="$1"
    fi
    
    case "$ACTION" in
        "validate")
            check_project_root
            validate_checklist
            ;;
        "pre-checks")
            check_project_root
            pre_release_checks
            ;;
        "build")
            check_project_root
            build_package
            ;;
        "test-install")
            check_project_root
            test_installation
            ;;
        "test-release")
            check_project_root
            validate_checklist
            pre_release_checks
            build_package
            test_installation
            publish_test_pypi
            ;;
        "release")
            check_project_root
            validate_checklist
            pre_release_checks
            build_package
            test_installation
            publish_pypi
            create_git_tag
            push_git_tag
            ;;
        "help"|*)
            echo "Usage: $0 [ACTION]"
            echo ""
            echo "Actions:"
            echo "  validate      Validate release checklist"
            echo "  pre-checks    Run pre-release checks (tests, linting, etc.)"
            echo "  build         Build the package"
            echo "  test-install  Test package installation in a virtual environment"
            echo "  test-release  Full test release process (validate, build, test, publish to Test PyPI)"
            echo "  release       Full release process (validate, build, test, publish to PyPI, git tag)"
            echo "  help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 validate"
            echo "  $0 release"
            ;;
    esac
}

# Run main function
main "$@"