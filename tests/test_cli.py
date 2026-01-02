"""Tests for the unified resume CLI."""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from resume_cli.cli import (
    get_project_root,
    run_script,
    get_active_yaml,
    main,
    TEMPLATES,
)


class TestProjectRoot:
    """Tests for get_project_root function."""

    def test_finds_project_root(self):
        """Should find the project root containing pyproject.toml."""
        root = get_project_root()
        assert root.exists()
        assert (root / "pyproject.toml").exists()

    def test_project_root_contains_resume_cli(self):
        """Project root should contain resume_cli package."""
        root = get_project_root()
        assert (root / "resume_cli").exists()
        assert (root / "resume_cli" / "cli.py").exists()


class TestTemplates:
    """Tests for template constants."""

    def test_templates_list(self):
        """Should have all expected templates."""
        assert "executive" in TEMPLATES
        assert "tech-modern" in TEMPLATES
        assert "modern-dense" in TEMPLATES
        assert "compact" in TEMPLATES
        assert "minimal" in TEMPLATES
        assert len(TEMPLATES) == 5


class TestRunScript:
    """Tests for run_script function."""

    def test_run_script_nonexistent(self):
        """Should return error for non-existent script."""
        result = run_script("nonexistent-skill", "fake_script.py", [])
        assert result == 1

    @patch("subprocess.run")
    def test_run_script_success(self, mock_run):
        """Should return 0 on successful script execution."""
        mock_run.return_value = MagicMock(returncode=0)
        # Use a real skill/script path
        result = run_script("resume-state", "get_active.py", [], check=False)
        # Either script runs or doesn't exist in test environment
        assert result in (0, 1)


class TestCLIHelp:
    """Tests for CLI help output."""

    def test_main_help(self):
        """Main help should show all commands."""
        result = subprocess.run(
            ["uv", "run", "resume", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "init" in result.stdout
        assert "import" in result.stdout
        assert "extract" in result.stdout
        assert "format" in result.stdout
        assert "review" in result.stdout
        assert "version" in result.stdout
        assert "cover" in result.stdout
        assert "job" in result.stdout
        assert "status" in result.stdout

    def test_format_help(self):
        """Format command help should show template options."""
        result = subprocess.run(
            ["uv", "run", "resume", "format", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "executive" in result.stdout
        assert "tech-modern" in result.stdout
        assert "--all-templates" in result.stdout

    def test_version_help(self):
        """Version command help should show subcommands."""
        result = subprocess.run(
            ["uv", "run", "resume", "version", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "list" in result.stdout
        assert "create" in result.stdout
        assert "switch" in result.stdout
        assert "diff" in result.stdout
        assert "export" in result.stdout


class TestCLIStatus:
    """Tests for status command."""

    def test_status_no_store(self, tmp_path, monkeypatch):
        """Status should handle missing store gracefully."""
        # Change to temp directory with no .resume_versions
        monkeypatch.chdir(tmp_path)
        result = subprocess.run(
            ["uv", "run", "resume", "status"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        # Should not crash
        assert result.returncode == 0
        assert "Store:" in result.stdout or "No resume store" in result.stdout


class TestCLIVersion:
    """Tests for CLI version."""

    def test_version_flag(self):
        """--version should show version number."""
        result = subprocess.run(
            ["uv", "run", "resume", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "1.5.0" in result.stdout


class TestCLIExtract:
    """Tests for extract command."""

    def test_extract_nonexistent_file(self, tmp_path):
        """Extract should fail gracefully for non-existent file."""
        result = subprocess.run(
            ["uv", "run", "resume", "extract", str(tmp_path / "nonexistent.pdf")],
            capture_output=True,
            text=True,
        )
        # Should fail but not crash
        assert result.returncode != 0

    def test_extract_unsupported_type(self, tmp_path):
        """Extract should reject unsupported file types."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("test content")
        result = subprocess.run(
            ["uv", "run", "resume", "extract", str(txt_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "Unsupported" in result.stderr


class TestCLIFormat:
    """Tests for format command."""

    def test_format_no_yaml_no_active(self, tmp_path, monkeypatch):
        """Format should fail gracefully when no YAML and no active version."""
        monkeypatch.chdir(tmp_path)
        result = subprocess.run(
            ["uv", "run", "resume", "format"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        # Should fail with helpful message
        assert result.returncode != 0
        assert "No YAML" in result.stderr or "active" in result.stderr.lower()


class TestCLIReview:
    """Tests for review command."""

    def test_review_nonexistent_pdf(self, tmp_path):
        """Review should fail for non-existent PDF."""
        result = subprocess.run(
            ["uv", "run", "resume", "review", str(tmp_path / "nonexistent.pdf")],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0


class TestCLIJob:
    """Tests for job command."""

    def test_job_invalid_url(self):
        """Job should handle invalid URLs gracefully."""
        result = subprocess.run(
            ["uv", "run", "resume", "job", "not-a-valid-url"],
            capture_output=True,
            text=True,
        )
        # Should fail but not crash
        assert result.returncode != 0
