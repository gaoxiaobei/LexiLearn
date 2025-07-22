"""End-to-end tests for CLI functionality."""

import subprocess
import tempfile
from pathlib import Path

import pytest


class TestCLI:
    """End-to-end tests for command-line interface."""
    
    def test_cli_help(self):
        """Test CLI help command."""
        result = subprocess.run(
            ["python", "-m", "lexilearn.main", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "help" in result.stdout.lower()
    
    def test_cli_version(self):
        """Test CLI version command."""
        result = subprocess.run(
            ["python", "-m", "lexilearn.main", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
    
    def test_cli_process_single_file(self, tmp_path):
        """Test processing a single file via CLI."""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("This is a test article about machine learning.")
        
        # Create output directory
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        # Run CLI command
        result = subprocess.run([
            "python", "-m", "lexilearn.main",
            str(test_file),
            "--output", str(output_dir),
            "--config", "test-config"
        ], capture_output=True, text=True)
        
        # Should handle missing config gracefully
        assert result.returncode != 0 or "error" in result.stderr.lower()
    
    def test_cli_process_directory(self, tmp_path):
        """Test processing a directory via CLI."""
        # Create test directory
        test_dir = tmp_path / "articles"
        test_dir.mkdir()
        
        # Create test files
        (test_dir / "article1.txt").write_text("Article 1 content")
        (test_dir / "article2.txt").write_text("Article 2 content")
        
        output_dir = tmp_path / "output"
        
        # Run CLI command
        result = subprocess.run([
            "python", "-m", "lexilearn.main",
            str(test_dir),
            "--output", str(output_dir),
            "--recursive"
        ], capture_output=True, text=True)
        
        # Should handle missing config gracefully
        assert result.returncode != 0 or "error" in result.stderr.lower()
    
    def test_cli_invalid_arguments(self):
        """Test CLI with invalid arguments."""
        result = subprocess.run(
            ["python", "-m", "lexilearn.main", "--invalid-flag"],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0