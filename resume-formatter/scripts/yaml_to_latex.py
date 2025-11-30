#!/usr/bin/env python3
"""
Convert resume YAML to LaTeX format using specified template.

Usage:
    uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py <yaml_file> <template> [--output <output_file>]

Templates:
    modern    - Clean, modern professional template
    classic   - Traditional conservative template
    academic  - Academic/research-focused template
    creative  - Bold, design-forward template

Examples:
    uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml modern
    uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml modern --output resume.tex
"""

import argparse
import sys
from pathlib import Path


def load_yaml(yaml_path: Path) -> dict:
    """Load and parse YAML resume file."""
    try:
        import yaml
    except ImportError:
        print("Error: pyyaml not available. Run with: uv run --with pyyaml,jinja2", file=sys.stderr)
        sys.exit(1)

    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML: {e}", file=sys.stderr)
        sys.exit(1)


def render_latex(resume_data: dict, template_name: str, script_dir: Path) -> str:
    """Render LaTeX from resume data using specified template."""
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError:
        print("Error: jinja2 not available. Run with: uv run --with pyyaml,jinja2", file=sys.stderr)
        sys.exit(1)

    # Template directory is ../assets/templates/latex/ relative to script
    template_dir = script_dir.parent / "assets" / "templates" / "latex"

    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}", file=sys.stderr)
        sys.exit(1)

    template_file = f"{template_name}.tex.j2"
    template_path = template_dir / template_file

    if not template_path.exists():
        print(f"Error: Template not found: {template_file}", file=sys.stderr)
        print(f"Available templates: modern (modern_custom), classic, academic, creative", file=sys.stderr)
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(template_dir))
    # Add LaTeX-safe filter
    env.filters['latex_escape'] = latex_escape

    template = env.get_template(template_file)
    return template.render(**resume_data)


def latex_escape(text: str) -> str:
    """Escape special LaTeX characters in text."""
    if not isinstance(text, str):
        return str(text)

    # IMPORTANT: Backslash must be escaped FIRST, before other characters
    # that introduce backslashes in their replacements
    text = text.replace('\\', r'\textbackslash{}')

    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def main():
    parser = argparse.ArgumentParser(description="Convert resume YAML to LaTeX")
    parser.add_argument("yaml_file", type=Path, help="Path to YAML resume file")
    parser.add_argument("template", choices=["modern", "classic", "academic", "creative"],
                        help="LaTeX template to use")
    parser.add_argument("-o", "--output", type=Path, help="Output .tex file path (default: stdout)")

    args = parser.parse_args()

    if not args.yaml_file.exists():
        print(f"Error: File not found: {args.yaml_file}", file=sys.stderr)
        sys.exit(1)

    # Get script directory for finding templates
    script_dir = Path(__file__).parent

    resume_data = load_yaml(args.yaml_file)

    # Map modern to modern_custom (the improved custom template)
    template_name = "modern_custom" if args.template == "modern" else args.template

    latex_output = render_latex(resume_data, template_name, script_dir)

    if args.output:
        args.output.write_text(latex_output)
        print(f"LaTeX written to: {args.output}", file=sys.stderr)
    else:
        print(latex_output)


if __name__ == "__main__":
    main()
