"""
Validation script entry point for LexiLearn.
This script provides a command-line interface to run structure validation.
"""

from .validate_structure import main

# Expose the main function for the entry point
main = main

if __name__ == "__main__":
    main()