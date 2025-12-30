"""Tests for resume-formatter/scripts/yaml_to_typst.py"""

import sys
from pathlib import Path

# Add the yaml_to_typst module to path
sys.path.insert(0, str(Path(__file__).parent.parent / "resume-formatter" / "scripts"))

from yaml_to_typst import typst_escape, url_escape


class TestTypstEscape:
    """Tests for typst_escape()"""

    def test_hash(self):
        assert typst_escape("#heading") == "\\#heading"

    def test_dollar(self):
        assert typst_escape("$100") == "\\$100"

    def test_at(self):
        assert typst_escape("@reference") == "\\@reference"

    def test_angle_brackets(self):
        assert typst_escape("<tag>") == "\\<tag\\>"

    def test_underscore(self):
        assert typst_escape("snake_case") == "snake\\_case"

    def test_asterisk(self):
        assert typst_escape("*bold*") == "\\*bold\\*"

    def test_backtick(self):
        assert typst_escape("`code`") == "\\`code\\`"

    def test_tilde(self):
        assert typst_escape("a~b") == "a\\~b"

    def test_caret(self):
        assert typst_escape("x^2") == "x\\^2"

    def test_backslash(self):
        # Backslash must be escaped first to avoid double-escaping
        assert typst_escape("path\\to\\file") == "path\\\\to\\\\file"

    def test_multiple_special_chars(self):
        assert typst_escape("#$@") == "\\#\\$\\@"

    def test_plain_text(self):
        assert typst_escape("hello world") == "hello world"

    def test_empty_string(self):
        assert typst_escape("") == ""

    def test_non_string_input(self):
        assert typst_escape(123) == "123"


class TestUrlEscape:
    """Tests for url_escape()"""

    def test_backslash(self):
        assert url_escape("path\\file") == "path\\\\file"

    def test_double_quote(self):
        assert url_escape('query="value"') == 'query=\\"value\\"'

    def test_normal_url(self):
        url = "https://example.com/path?q=test"
        assert url_escape(url) == url

    def test_empty_string(self):
        assert url_escape("") == ""

    def test_non_string_input(self):
        assert url_escape(123) == "123"
