#!/usr/bin/env python3
"""
Fetch and extract job posting content from URLs.

Usage:
    uv run scripts/fetch_job_posting.py <url> [--output <output_file>]

Examples:
    uv run scripts/fetch_job_posting.py "https://linkedin.com/jobs/view/12345"
    uv run scripts/fetch_job_posting.py "https://indeed.com/..." --output job_desc.txt
"""

import argparse
import sys
from pathlib import Path


def fetch_job_posting(url: str) -> str:
    """Fetch job posting content from a URL."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Error: Required packages not available. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing content: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Fetch job posting from URL")
    parser.add_argument("url", help="Job posting URL")
    parser.add_argument("-o", "--output", type=Path, help="Output file path (default: stdout)")

    args = parser.parse_args()

    content = fetch_job_posting(args.url)

    if args.output:
        args.output.write_text(content)
        print(f"Job posting content written to: {args.output}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
