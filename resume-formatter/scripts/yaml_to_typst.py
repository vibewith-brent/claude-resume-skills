#!/usr/bin/env python3
"""
Convert resume YAML to Typst format using specified template.

Usage:
    uv run scripts/yaml_to_typst.py <yaml_file> <template> [--output <output_file>]

Templates are discovered from assets/templates/typst/*.typ.j2

Examples:
    uv run scripts/yaml_to_typst.py resume.yaml modern
    uv run scripts/yaml_to_typst.py resume.yaml modern-tech --output resume.typ
"""

import argparse
import sys
from pathlib import Path


def load_yaml(yaml_path: Path) -> dict:
    """Load and parse YAML resume file."""
    try:
        import yaml
    except ImportError:
        print("Error: pyyaml not available. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML: {e}", file=sys.stderr)
        sys.exit(1)


def render_typst(resume_data: dict, template_name: str, script_dir: Path) -> str:
    """Render Typst from resume data using specified template."""
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError:
        print("Error: jinja2 not available. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    # Template directory is ../assets/templates/typst/ relative to script
    template_dir = script_dir.parent / "assets" / "templates" / "typst"

    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}", file=sys.stderr)
        sys.exit(1)

    template_file = f"{template_name}.typ.j2"
    template_path = template_dir / template_file

    if not template_path.exists():
        print(f"Error: Template not found: {template_file}", file=sys.stderr)
        print(f"Available templates: modern, classic, academic, creative", file=sys.stderr)
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(template_dir))
    # Add Typst-safe filters
    env.filters["typst_escape"] = typst_escape
    env.filters["url_escape"] = url_escape

    template = env.get_template(template_file)
    return template.render(**resume_data)


def typst_escape(text: str) -> str:
    r"""Escape special Typst characters in text.

    Typst special characters that need escaping:
    - \ is escape character (must be first)
    - # starts function calls
    - $ starts math mode
    - @ starts references
    - < > for raw blocks
    - _ for subscript
    - * for bold/emphasis
    - ` for raw/code
    - ~ for non-breaking space
    - ^ for superscript
    """
    if not isinstance(text, str):
        return str(text)

    # Order matters: backslash must be first to avoid double-escaping
    replacements = [
        ("\\", "\\\\"),
        ("#", "\\#"),
        ("$", "\\$"),
        ("@", "\\@"),
        ("<", "\\<"),
        (">", "\\>"),
        ("_", "\\_"),
        ("*", "\\*"),
        ("`", "\\`"),
        ("~", "\\~"),
        ("^", "\\^"),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    return text


def url_escape(url: str) -> str:
    r"""Escape special characters in URLs for Typst #link() calls.

    URLs need fewer escapes than regular text since they're inside quotes,
    but certain characters can still break Typst syntax.
    """
    if not isinstance(url, str):
        return str(url)

    # URLs inside #link("...") need these escaped
    replacements = [
        ("\\", "\\\\"),
        ('"', '\\"'),  # Quotes break the string literal
    ]

    for old, new in replacements:
        url = url.replace(old, new)

    return url


def get_available_templates(script_dir: Path) -> list[str]:
    """Discover available templates from the templates directory."""
    template_dir = script_dir.parent / "assets" / "templates" / "typst"
    if not template_dir.exists():
        return []
    return sorted([p.stem.replace('.typ', '') for p in template_dir.glob("*.typ.j2")])


def main():
    script_dir = Path(__file__).parent
    available_templates = get_available_templates(script_dir)

    parser = argparse.ArgumentParser(description="Convert resume YAML to Typst")
    parser.add_argument("yaml_file", type=Path, help="Path to YAML resume file")
    parser.add_argument("template", choices=available_templates,
                        help="Typst template to use")
    parser.add_argument("-o", "--output", type=Path, help="Output .typ file path (default: stdout)")

    args = parser.parse_args()

    if not args.yaml_file.exists():
        print(f"Error: File not found: {args.yaml_file}", file=sys.stderr)
        sys.exit(1)

    resume_data = load_yaml(args.yaml_file)
    typst_output = render_typst(resume_data, args.template, script_dir)

    if args.output:
        args.output.write_text(typst_output)
        print(f"Typst written to: {args.output}", file=sys.stderr)
    else:
        print(typst_output)


if __name__ == "__main__":
    main()
