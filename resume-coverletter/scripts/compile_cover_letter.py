#!/usr/bin/env python3
"""
Compile Typst cover letter to PDF.

Usage:
    uv run scripts/compile_cover_letter.py <cover_letter.typ> [--output <output.pdf>]

Examples:
    uv run scripts/compile_cover_letter.py cover_letter.typ
    uv run scripts/compile_cover_letter.py cover_letter.typ --output my_cover_letter.pdf

Requirements:
    - typst must be installed on the system
    - macOS: brew install typst
    - Linux: cargo install typst-cli (requires Rust)
    - Windows: winget install --id Typst.Typst
"""

import argparse
import subprocess
import sys
from pathlib import Path
import shutil


def find_typst() -> str:
    """Find typst executable, checking common installation paths."""
    # Check PATH first
    typst = shutil.which("typst")
    if typst:
        return typst

    # Check common installation locations
    common_paths = [
        # Homebrew on Apple Silicon
        "/opt/homebrew/bin/typst",
        # Homebrew on Intel Mac
        "/usr/local/bin/typst",
        # Cargo install location
        Path.home() / ".cargo" / "bin" / "typst",
    ]

    for path in common_paths:
        path = Path(path)
        if path.exists():
            return str(path)

    # Not found
    print("Error: typst not found.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Install instructions:", file=sys.stderr)
    print("  macOS:   brew install typst", file=sys.stderr)
    print("  Linux:   cargo install typst-cli", file=sys.stderr)
    print("  Windows: winget install --id Typst.Typst", file=sys.stderr)
    sys.exit(1)


def compile_typst(typ_file: Path, output_pdf: Path = None, typst_path: str = "typst") -> Path:
    """Compile Typst file to PDF."""
    if not typ_file.exists():
        print(f"Error: File not found: {typ_file}", file=sys.stderr)
        sys.exit(1)

    if not typ_file.suffix == '.typ':
        print(f"Error: Not a .typ file: {typ_file}", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if output_pdf:
        result_pdf = output_pdf
    else:
        result_pdf = typ_file.with_suffix('.pdf')

    # Typst compiles in a single pass
    print(f"Compiling {typ_file}...", file=sys.stderr)

    result = subprocess.run(
        [typst_path, "compile", str(typ_file), str(result_pdf)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error during compilation:", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        sys.exit(1)

    return result_pdf


def main():
    parser = argparse.ArgumentParser(description="Compile Typst cover letter to PDF")
    parser.add_argument("typ_file", type=Path, help="Path to .typ file")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output PDF path (default: same name as .typ)"
    )

    args = parser.parse_args()

    typst_path = find_typst()
    output_pdf = compile_typst(args.typ_file, args.output, typst_path)

    print(f"Compiled: {output_pdf}", file=sys.stderr)


if __name__ == "__main__":
    main()
