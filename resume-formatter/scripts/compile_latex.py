#!/usr/bin/env python3
"""
Compile LaTeX resume to PDF.

Usage:
    uv run scripts/compile_latex.py <tex_file> [--output <output_pdf>]

Examples:
    uv run scripts/compile_latex.py resume.tex
    uv run scripts/compile_latex.py resume.tex --output custom_resume.pdf

Requirements:
    - pdflatex must be installed on the system
    - On macOS: brew install --cask mactex-no-gui (or mactex for full)
    - On Linux: sudo apt-get install texlive-latex-base texlive-latex-extra
"""

import argparse
import subprocess
import sys
from pathlib import Path
import shutil


def check_pdflatex():
    """Check if pdflatex is available."""
    # On macOS, add common MacTeX paths if pdflatex not in PATH
    if not shutil.which("pdflatex"):
        import os
        mactex_paths = [
            "/Library/TeX/texbin",
            "/usr/local/texlive/2025/bin/universal-darwin",
            "/usr/local/texlive/2024/bin/universal-darwin",
        ]
        for path in mactex_paths:
            if Path(path).exists():
                os.environ["PATH"] = f"{path}:{os.environ.get('PATH', '')}"
                break

    if not shutil.which("pdflatex"):
        print("Error: pdflatex not found.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Install instructions:", file=sys.stderr)
        print("  macOS:  brew install --cask mactex-no-gui", file=sys.stderr)
        print("  Linux:  sudo apt-get install texlive-latex-base texlive-latex-extra", file=sys.stderr)
        sys.exit(1)


def compile_latex(tex_file: Path, output_pdf: Path = None) -> Path:
    """Compile LaTeX file to PDF."""
    if not tex_file.exists():
        print(f"Error: File not found: {tex_file}", file=sys.stderr)
        sys.exit(1)

    if not tex_file.suffix == '.tex':
        print(f"Error: Not a .tex file: {tex_file}", file=sys.stderr)
        sys.exit(1)

    # Run pdflatex twice for proper formatting (resolves references)
    print(f"Compiling {tex_file}...", file=sys.stderr)

    for run in [1, 2]:
        print(f"  Run {run}/2...", file=sys.stderr)
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", str(tex_file)],
            cwd=tex_file.parent,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error during compilation (run {run}):", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)

    # Default output PDF has same name as .tex file
    default_pdf = tex_file.with_suffix('.pdf')

    if output_pdf and output_pdf != default_pdf:
        shutil.move(str(default_pdf), str(output_pdf))
        result_pdf = output_pdf
    else:
        result_pdf = default_pdf

    # Clean up auxiliary files
    for ext in ['.aux', '.log', '.out']:
        aux_file = tex_file.with_suffix(ext)
        if aux_file.exists():
            aux_file.unlink()

    return result_pdf


def main():
    parser = argparse.ArgumentParser(description="Compile LaTeX resume to PDF")
    parser.add_argument("tex_file", type=Path, help="Path to .tex file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF path (default: same name as .tex)")

    args = parser.parse_args()

    check_pdflatex()
    output_pdf = compile_latex(args.tex_file, args.output)

    print(f"\n✓ Successfully compiled to: {output_pdf}", file=sys.stderr)


if __name__ == "__main__":
    main()
