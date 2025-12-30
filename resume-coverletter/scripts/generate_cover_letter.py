#!/usr/bin/env python3
"""
Generate professional cover letter from resume YAML and job details.

Usage:
    uv run scripts/generate_cover_letter.py <resume.yaml> --template <template> [options]

Examples:
    # Company-specific letter
    uv run scripts/generate_cover_letter.py resume.yaml \
      --template tech-modern-cover \
      --company "Acme Corp" \
      --position "Senior Manager" \
      --job-file job.txt \
      --output cover_letter.typ

    # Generic letter
    uv run scripts/generate_cover_letter.py resume.yaml \
      --template generic-cover \
      --output cover_generic.typ
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


def load_job_description(job_file: Path) -> str:
    """Load job description from text file."""
    if not job_file or not job_file.exists():
        return ""

    try:
        return job_file.read_text().strip()
    except Exception as e:
        print(f"Warning: Could not load job file: {e}", file=sys.stderr)
        return ""


def extract_top_achievements(resume_data: dict, limit: int = 5) -> list:
    """Extract top achievements from resume experience section."""
    achievements = []

    if 'experience' not in resume_data:
        return achievements

    for job in resume_data['experience'][:3]:  # Top 3 most recent jobs
        for position in job.get('positions', []):
            for achievement in position.get('achievements', [])[:2]:  # Top 2 per position
                achievements.append(achievement)
                if len(achievements) >= limit:
                    return achievements

    return achievements


def render_cover_letter(
    resume_data: dict,
    template_name: str,
    company: str = None,
    position: str = None,
    job_description: str = None,
    script_dir: Path = None
) -> str:
    """Render cover letter Typst from resume data using specified template."""
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError:
        print("Error: jinja2 not available. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    # Template directory
    template_dir = script_dir.parent / "assets" / "templates"

    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}", file=sys.stderr)
        sys.exit(1)

    template_file = f"{template_name}.typ.j2"
    template_path = template_dir / template_file

    if not template_path.exists():
        print(f"Error: Template not found: {template_file}", file=sys.stderr)
        available = [p.stem.replace('.typ', '') for p in template_dir.glob("*.typ.j2")]
        print(f"Available templates: {', '.join(available)}", file=sys.stderr)
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(template_dir))
    # Add Typst-safe filters
    env.filters["typst_escape"] = typst_escape
    env.filters["url_escape"] = url_escape

    # Extract key data from resume
    contact = resume_data.get('contact', {})
    summary = resume_data.get('summary', '')
    top_achievements = extract_top_achievements(resume_data, limit=5)

    # Prepare template context
    context = {
        'contact': contact,
        'company': company or 'the organization',
        'position': position or 'this opportunity',
        'summary': summary,
        'achievements': top_achievements,
        'job_description': job_description or '',
        'is_generic': not company,  # Flag for template to adjust language
    }

    template = env.get_template(template_file)
    return template.render(**context)


def typst_escape(text: str) -> str:
    r"""Escape special Typst characters in text."""
    if not isinstance(text, str):
        return str(text)

    # Order matters: backslash must be first
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
    r"""Escape special characters in URLs for Typst #link() calls."""
    if not isinstance(url, str):
        return str(url)

    replacements = [
        ("\\", "\\\\"),
        ('"', '\\"'),
    ]

    for old, new in replacements:
        url = url.replace(old, new)

    return url


def get_available_templates(script_dir: Path) -> list[str]:
    """Discover available templates from the templates directory."""
    template_dir = script_dir.parent / "assets" / "templates"
    if not template_dir.exists():
        return []
    return sorted([p.stem.replace('.typ', '') for p in template_dir.glob("*.typ.j2")])


def main():
    script_dir = Path(__file__).parent
    available_templates = get_available_templates(script_dir)

    parser = argparse.ArgumentParser(
        description="Generate professional cover letter from resume YAML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Company-specific letter
  uv run scripts/generate_cover_letter.py resume.yaml \\
    --template tech-modern-cover \\
    --company "Acme Corp" \\
    --position "Senior Manager" \\
    --job-file job.txt \\
    --output cover_letter.typ

  # Generic letter
  uv run scripts/generate_cover_letter.py resume.yaml \\
    --template generic-cover \\
    --output cover_generic.typ
        """
    )

    parser.add_argument("resume_yaml", type=Path, help="Path to resume YAML file")
    parser.add_argument(
        "-t", "--template",
        choices=available_templates if available_templates else None,
        required=True,
        help="Cover letter template to use"
    )
    parser.add_argument(
        "-c", "--company",
        type=str,
        help="Target company name (optional for generic letters)"
    )
    parser.add_argument(
        "-p", "--position",
        type=str,
        help="Target position/role (optional for generic letters)"
    )
    parser.add_argument(
        "-j", "--job-file",
        type=Path,
        help="Job description text file (optional)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output .typ file path (default: stdout)"
    )

    args = parser.parse_args()

    if not args.resume_yaml.exists():
        print(f"Error: Resume file not found: {args.resume_yaml}", file=sys.stderr)
        sys.exit(1)

    # Load data
    resume_data = load_yaml(args.resume_yaml)
    job_description = load_job_description(args.job_file) if args.job_file else None

    # Validate contact info exists
    if 'contact' not in resume_data:
        print("Error: Resume YAML missing 'contact' section", file=sys.stderr)
        sys.exit(1)

    # Generate cover letter
    cover_letter_output = render_cover_letter(
        resume_data=resume_data,
        template_name=args.template,
        company=args.company,
        position=args.position,
        job_description=job_description,
        script_dir=script_dir
    )

    # Write output
    if args.output:
        args.output.write_text(cover_letter_output)
        print(f"Cover letter written to: {args.output}", file=sys.stderr)
    else:
        print(cover_letter_output)


if __name__ == "__main__":
    main()
