#!/usr/bin/env python3
"""Scaffold a new Typst resume template.

This script creates a new template file with proper structure, escaping,
and all required sections. Supports starting from scratch or extending
an existing template.

Usage:
    uv run scripts/scaffold_template.py <template_name> [OPTIONS]
    uv run scripts/scaffold_template.py creative --font "Playfair Display"
    uv run scripts/scaffold_template.py modern --base minimal --accent "#2563eb"

Examples:
    uv run scripts/scaffold_template.py startup
    uv run scripts/scaffold_template.py academic --layout two-column
    uv run scripts/scaffold_template.py creative --base executive --font "Playfair Display"
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from textwrap import dedent


# Standard template output location
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "resume-formatter" / "assets" / "templates" / "typst"

# Available base templates
BASE_TEMPLATES = ["executive", "compact", "minimal"]

# Design presets for quick scaffolding
DESIGN_PRESETS = {
    "modern-serif": {
        "font": "New Computer Modern",
        "accent": "#2563eb",
        "layout": "single",
        "description": "Elegant serif typography with modern blue accents",
    },
    "tech-minimal": {
        "font": "JetBrains Mono",
        "accent": "#10b981",
        "layout": "single",
        "description": "Monospace font with tech-forward green accent",
    },
    "executive-classic": {
        "font": "Times New Roman",
        "accent": "#1e3a5f",
        "layout": "single",
        "description": "Traditional serif with navy blue accents",
    },
    "creative": {
        "font": "Playfair Display",
        "accent": "#7c3aed",
        "layout": "single",
        "description": "Display font with creative purple accent",
    },
    "dense": {
        "font": "Inter",
        "accent": "#374151",
        "layout": "single",
        "description": "Maximum content density with subtle styling",
    },
}

# Template skeleton with all sections
TEMPLATE_SKELETON = '''\
// {name} Resume Template
// Design: {description}
// Font: {font}
// Layout: {layout}
// Generated with scaffold_template.py

#set page(
  paper: "us-letter",
  margin: (top: {margin_top}, bottom: {margin_bottom}, left: {margin_lr}, right: {margin_lr}),
)

#set text(font: "{font}", size: {body_size}, fill: rgb("#262626"))
#set par(justify: false, leading: {leading})

// Colors
#let black = rgb("#171717")
#let dark = rgb("#404040")
#let medium = rgb("#737373")
#let light = rgb("#a3a3a3")
#let border = rgb("#e5e5e5")
#let accent = rgb("{accent}")

// Spacing constants
#let xs = 2pt
#let sm = 4pt
#let md = 6pt
#let lg = 10pt
#let xl = 14pt

// Section header helper
#let section(title) = {{
  v(lg)
  grid(
    columns: (auto, 1fr),
    column-gutter: md,
    text(size: {section_size}, weight: "bold", fill: black, tracking: 0.5pt)[#upper(title)],
    align(horizon, line(length: 100%, stroke: 0.4pt + border))
  )
  v(sm)
}}

// Job entry helper
#let job(title, company, location: none, dates) = {{
  grid(
    columns: (1fr, auto),
    [
      #text(size: {title_size}, weight: "semibold", fill: black)[#title]
      #v(-2pt)
      #text(size: {subtitle_size}, fill: medium)[#company#if location != none [, #location]]
    ],
    align(right + top, text(size: {date_size}, weight: "medium", fill: accent)[#dates])
  )
  v(xs)
}}

// Education entry helper
#let edu(degree, school, year) = {{
  grid(
    columns: (1fr, auto),
    [#text(weight: "semibold", fill: black)[#degree] #text(fill: light)[—] #text(fill: medium)[#school]],
    text(size: {date_size}, weight: "medium", fill: accent)[#year]
  )
}}

// Bullet list helper
#let bullets(items) = {{
  set list(
    marker: text(fill: light, size: 5pt)[●],
    indent: 0pt,
    body-indent: md,
    spacing: xs,
  )
  set text(size: {bullet_size}, fill: dark)
  for item in items [- #item]
}}

// Link styling
#show link: it => text(fill: accent)[#it]

// ============================================================================
// HEADER
// ============================================================================

#align({name_align})[
  #text(size: {name_size}, weight: "bold", fill: black, tracking: 0.8pt)[{{{{ contact.name | typst_escape | upper }}}}]
  {{% if contact.title %}}
  #v(xs)
  #text(size: {title_size}, weight: "regular", fill: medium)[{{{{ contact.title | typst_escape }}}}]
  {{% endif %}}
]

#v(md)

#align(center)[
  #set text(size: {contact_size}, fill: medium)
  {{% if contact.location %}}{{{{ contact.location | typst_escape }}}}{{% endif %}}
  {{% if contact.phone %}}#h(lg) {{{{ contact.phone | typst_escape }}}}{{% endif %}}
  {{% if contact.email %}}#h(lg) #link("mailto:{{{{ contact.email | url_escape }}}}")[#text(fill: accent)[{{{{ contact.email | typst_escape }}}}]]{{% endif %}}
  {{% if contact.linkedin %}}#h(lg) #link("https://{{{{ contact.linkedin | url_escape }}}}")[#text(fill: accent)[{{{{ contact.linkedin | typst_escape }}}}]]{{% endif %}}
  {{% if contact.github %}}#h(lg) #link("https://{{{{ contact.github | url_escape }}}}")[#text(fill: accent)[{{{{ contact.github | typst_escape }}}}]]{{% endif %}}
]

// ============================================================================
// SUMMARY
// ============================================================================

{{% if summary %}}
#section("Summary")
#text(size: {bullet_size}, fill: dark)[{{{{ summary | typst_escape }}}}]
{{% endif %}}

// ============================================================================
// EXPERIENCE
// ============================================================================

{{% if experience %}}
#section("Experience")
{{% for exp in experience %}}
{{% for position in exp.positions %}}
#job(
  [{{{{ position.title | typst_escape }}}}],
  [{{{{ exp.company | typst_escape }}}}],
  {{% if exp.location %}}location: [{{{{ exp.location | typst_escape }}}}],{{% endif %}}
  [{{{{ position.dates | typst_escape }}}}],
)
{{% if position.achievements %}}
#bullets((
  {{% for a in position.achievements %}}
  [{{{{ a | typst_escape }}}}],
  {{% endfor %}}
))
{{% endif %}}
#v(md)
{{% endfor %}}
{{% endfor %}}
{{% endif %}}

// ============================================================================
// SKILLS
// ============================================================================

{{% if skills %}}
#section("Skills")
#set text(size: {skill_size})
{{% for category, items in skills.items() %}}
#text(weight: "semibold", fill: black)[{{{{ category | typst_escape }}}}]#h(sm){{% if items is iterable and items is not string %}}#text(fill: dark)[{{{{ items | join(' · ') | typst_escape }}}}]{{% else %}}#text(fill: dark)[{{{{ items | typst_escape }}}}]{{% endif %}}
#v(sm)
{{% endfor %}}
{{% endif %}}

// ============================================================================
// EDUCATION
// ============================================================================

{{% if education %}}
#section("Education")
{{% for e in education %}}
#edu([{{{{ e.degree | typst_escape }}}}], [{{{{ e.institution | typst_escape }}}}], [{{{{ e.graduation_year }}}}])
{{% if e.gpa or e.honors %}}
#v(xs)
#text(size: {bullet_size}, fill: medium)[
  {{% if e.gpa %}}GPA: {{{{ e.gpa | typst_escape }}}}{{% endif %}}
  {{% if e.gpa and e.honors %}} | {{% endif %}}
  {{% if e.honors %}}{{{{ e.honors | typst_escape }}}}{{% endif %}}
]
{{% endif %}}
{{% if not loop.last %}}#v(xs){{% endif %}}
{{% endfor %}}
{{% endif %}}

// ============================================================================
// CERTIFICATIONS (Optional)
// ============================================================================

{{% if certifications %}}
#section("Certifications")
{{% for cert in certifications %}}
#grid(
  columns: (1fr, auto),
  [#text(weight: "semibold", fill: black)[{{{{ cert.name | typst_escape }}}}] #text(fill: light)[—] #text(fill: medium)[{{{{ cert.issuer | typst_escape }}}}]],
  text(size: {date_size}, weight: "medium", fill: accent)[{{{{ cert.date | typst_escape }}}}]
)
{{% if not loop.last %}}#v(xs){{% endif %}}
{{% endfor %}}
{{% endif %}}

// ============================================================================
// PROJECTS (Optional)
// ============================================================================

{{% if projects %}}
#section("Projects")
{{% for project in projects %}}
#grid(
  columns: (1fr, auto),
  [
    #text(weight: "semibold", fill: black)[{{{{ project.name | typst_escape }}}}]
    {{% if project.technologies %}}#h(sm)#text(size: 7.5pt, fill: light)[{{{{ project.technologies | join(' · ') | typst_escape }}}}]{{% endif %}}
  ],
  text(size: {date_size}, weight: "medium", fill: accent)[{{{{ project.dates | typst_escape }}}}]
)
{{% if project.description or project.achievements %}}
#v(xs)
#bullets((
  {{% if project.description %}}[{{{{ project.description | typst_escape }}}}],{{% endif %}}
  {{% if project.achievements %}}{{% for a in project.achievements %}}[{{{{ a | typst_escape }}}}],{{% endfor %}}{{% endif %}}
))
{{% endif %}}
{{% if not loop.last %}}#v(md){{% endif %}}
{{% endfor %}}
{{% endif %}}

// ============================================================================
// PUBLICATIONS (Optional)
// ============================================================================

{{% if publications %}}
#section("Publications")
{{% for pub in publications %}}
#text(fill: dark)[{{{{ pub.authors | typst_escape }}}}.] #emph[{{{{ pub.title | typst_escape }}}}.] #text(fill: medium)[{{{{ pub.venue | typst_escape }}}}, {{{{ pub.date | typst_escape }}}}.] {{% if pub.url %}}#link("{{{{ pub.url | url_escape }}}}")[#text(fill: accent, size: {date_size})[↗]]{{% endif %}}
{{% if not loop.last %}}#v(xs){{% endif %}}
{{% endfor %}}
{{% endif %}}

// ============================================================================
// AWARDS (Optional)
// ============================================================================

{{% if awards %}}
#section("Awards")
{{% for award in awards %}}
#grid(
  columns: (1fr, auto),
  [#text(weight: "semibold", fill: black)[{{{{ award.name | typst_escape }}}}] #text(fill: light)[—] #text(fill: medium)[{{{{ award.issuer | typst_escape }}}}]],
  text(size: {date_size}, weight: "medium", fill: accent)[{{{{ award.date | typst_escape }}}}]
)
{{% if not loop.last %}}#v(xs){{% endif %}}
{{% endfor %}}
{{% endif %}}

// ============================================================================
// LANGUAGES (Optional)
// ============================================================================

{{% if languages %}}
#section("Languages")
{{% for lang in languages %}}#text(weight: "medium", fill: black)[{{{{ lang.language | typst_escape }}}}] #text(fill: light)[({{{{ lang.proficiency | typst_escape }}}})]{{{% if not loop.last %}}#h(lg){{% endif %}}{{% endfor %}}
{{% endif %}}

// ============================================================================
// VOLUNTEER (Optional)
// ============================================================================

{{% if volunteer %}}
#section("Volunteer")
{{% for vol in volunteer %}}
#job(
  [{{{{ vol.role | typst_escape }}}}],
  [{{{{ vol.organization | typst_escape }}}}],
  [{{{{ vol.dates | typst_escape }}}}],
)
{{% if vol.achievements %}}
#bullets((
  {{% for a in vol.achievements %}}
  [{{{{ a | typst_escape }}}}],
  {{% endfor %}}
))
{{% endif %}}
{{% if not loop.last %}}#v(md){{% endif %}}
{{% endfor %}}
{{% endif %}}
'''


def validate_template_name(name: str) -> bool:
    """Validate template name."""
    if not re.match(r"^[a-z][a-z0-9_-]*$", name):
        return False
    if name in BASE_TEMPLATES:
        return False  # Don't overwrite built-in templates
    return True


def get_size_scale(density: str) -> dict:
    """Get font sizes based on density setting."""
    scales = {
        "normal": {
            "name_size": "18pt",
            "title_size": "9.5pt",
            "section_size": "8.5pt",
            "subtitle_size": "8.5pt",
            "body_size": "9pt",
            "bullet_size": "8.5pt",
            "skill_size": "8pt",
            "date_size": "8pt",
            "contact_size": "8pt",
            "leading": "0.5em",
            "margin_top": "0.4in",
            "margin_bottom": "0.35in",
            "margin_lr": "0.5in",
        },
        "compact": {
            "name_size": "16pt",
            "title_size": "9pt",
            "section_size": "8pt",
            "subtitle_size": "8pt",
            "body_size": "8.5pt",
            "bullet_size": "8pt",
            "skill_size": "7.5pt",
            "date_size": "7.5pt",
            "contact_size": "7.5pt",
            "leading": "0.45em",
            "margin_top": "0.35in",
            "margin_bottom": "0.3in",
            "margin_lr": "0.45in",
        },
        "spacious": {
            "name_size": "22pt",
            "title_size": "10.5pt",
            "section_size": "9.5pt",
            "subtitle_size": "9pt",
            "body_size": "10pt",
            "bullet_size": "9.5pt",
            "skill_size": "9pt",
            "date_size": "8.5pt",
            "contact_size": "8.5pt",
            "leading": "0.6em",
            "margin_top": "0.6in",
            "margin_bottom": "0.5in",
            "margin_lr": "0.65in",
        },
    }
    return scales.get(density, scales["normal"])


def scaffold_template(
    name: str,
    font: str = "Inter",
    accent: str = "#2563eb",
    layout: str = "single",
    density: str = "normal",
    description: str = "",
    name_align: str = "center",
    output_dir: Path | None = None,
) -> Path:
    """Generate a new template file."""
    if output_dir is None:
        output_dir = TEMPLATES_DIR

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{name}.typ.j2"

    # Get size scale
    sizes = get_size_scale(density)

    # Build description if not provided
    if not description:
        description = f"Custom template with {font} font"

    # Format template
    content = TEMPLATE_SKELETON.format(
        name=name.replace("-", " ").title(),
        font=font,
        accent=accent,
        layout=layout,
        description=description,
        name_align=name_align,
        **sizes,
    )

    output_path.write_text(content)
    return output_path


def copy_and_rename_template(base: str, name: str, output_dir: Path | None = None) -> Path:
    """Copy an existing template and rename it."""
    if output_dir is None:
        output_dir = TEMPLATES_DIR

    base_path = output_dir / f"{base}.typ.j2"
    if not base_path.exists():
        raise FileNotFoundError(f"Base template not found: {base_path}")

    output_path = output_dir / f"{name}.typ.j2"
    shutil.copy(base_path, output_path)

    # Update the comment at the top
    content = output_path.read_text()
    content = re.sub(
        r"^// .+ Resume Template",
        f"// {name.replace('-', ' ').title()} Resume Template (based on {base})",
        content,
        count=1,
    )
    output_path.write_text(content)

    return output_path


def list_presets() -> None:
    """Print available design presets."""
    print("\nAvailable Design Presets:\n")
    for preset_name, preset in DESIGN_PRESETS.items():
        print(f"  {preset_name}:")
        print(f"    Font: {preset['font']}")
        print(f"    Accent: {preset['accent']}")
        print(f"    Description: {preset['description']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new Typst resume template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create from scratch with defaults
  uv run scripts/scaffold_template.py creative

  # Create with custom font and color
  uv run scripts/scaffold_template.py modern-serif --font "New Computer Modern" --accent "#1e3a5f"

  # Create by copying existing template
  uv run scripts/scaffold_template.py startup --base minimal

  # Use a preset
  uv run scripts/scaffold_template.py tech-resume --preset tech-minimal

  # List available presets
  uv run scripts/scaffold_template.py --list-presets

Available base templates: executive, compact, minimal
Density options: compact, normal, spacious
        """,
    )
    parser.add_argument("name", nargs="?", help="Template name (lowercase, alphanumeric, hyphens)")
    parser.add_argument("--base", choices=BASE_TEMPLATES, help="Base template to copy from")
    parser.add_argument("--font", default="Inter", help="Primary font family (default: Inter)")
    parser.add_argument("--accent", default="#2563eb", help="Accent color hex (default: #2563eb)")
    parser.add_argument(
        "--layout",
        choices=["single", "two-column", "sidebar"],
        default="single",
        help="Layout type (default: single)",
    )
    parser.add_argument(
        "--density",
        choices=["compact", "normal", "spacious"],
        default="normal",
        help="Content density (default: normal)",
    )
    parser.add_argument(
        "--name-align",
        choices=["left", "center"],
        default="center",
        help="Name alignment (default: center)",
    )
    parser.add_argument("--preset", choices=list(DESIGN_PRESETS.keys()), help="Use a design preset")
    parser.add_argument("--output-dir", type=Path, help="Output directory (default: formatter templates)")
    parser.add_argument("--list-presets", action="store_true", help="List available design presets")
    parser.add_argument("--description", default="", help="Template description comment")

    args = parser.parse_args()

    # Handle --list-presets
    if args.list_presets:
        list_presets()
        return

    # Require name for all other operations
    if not args.name:
        parser.print_help()
        print("\nError: Template name is required", file=sys.stderr)
        sys.exit(1)

    # Validate name
    if not validate_template_name(args.name):
        print(
            f"Error: Invalid template name '{args.name}'.\n"
            "Must be lowercase, start with letter, contain only a-z, 0-9, -, _\n"
            f"Cannot be one of: {', '.join(BASE_TEMPLATES)}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        # Apply preset if specified
        if args.preset:
            preset = DESIGN_PRESETS[args.preset]
            args.font = preset["font"]
            args.accent = preset["accent"]
            args.layout = preset["layout"]
            if not args.description:
                args.description = preset["description"]

        # Copy from base or scaffold new
        if args.base:
            output_path = copy_and_rename_template(
                args.base,
                args.name,
                output_dir=args.output_dir,
            )
            print(f"Created {output_path} (based on {args.base})")
        else:
            output_path = scaffold_template(
                name=args.name,
                font=args.font,
                accent=args.accent,
                layout=args.layout,
                density=args.density,
                description=args.description,
                name_align=args.name_align,
                output_dir=args.output_dir,
            )
            print(f"Created {output_path}")

        print("\nNext steps:")
        print(f"  1. Edit the template: {output_path}")
        print(f"  2. Test with: uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py resume.yaml {args.name} -o test.typ")
        print(f"  3. Compile: uv run .claude/skills/resume-formatter/scripts/compile_typst.py test.typ -o test.pdf")
        print("  4. Review with resume-reviewer skill")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
