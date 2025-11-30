#!/usr/bin/env python3
"""
Extract text and structure from PDF resumes.

Usage:
    uv run scripts/extract_pdf.py <pdf_path> [--output <output_file>]

Examples:
    uv run scripts/extract_pdf.py resume.pdf
    uv run scripts/extract_pdf.py resume.pdf --output extracted.txt
"""

import argparse
import sys
from pathlib import Path


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract all text from a PDF file."""
    try:
        import pdfplumber
    except ImportError:
        print("Error: pdfplumber not available. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    text_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                text_content.append(f"--- Page {page_num} ---\n{text}")

    return "\n\n".join(text_content)


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF resume")
    parser.add_argument("pdf_path", type=Path, help="Path to PDF resume file")
    parser.add_argument("-o", "--output", type=Path, help="Output file path (default: stdout)")

    args = parser.parse_args()

    if not args.pdf_path.exists():
        print(f"Error: File not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    if not args.pdf_path.suffix.lower() == '.pdf':
        print(f"Error: Not a PDF file: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    text = extract_pdf_text(args.pdf_path)

    if args.output:
        args.output.write_text(text)
        print(f"Extracted text written to: {args.output}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
