#!/usr/bin/env python3
"""
Package skills as distributable ZIP files per Anthropic's requirements.

Creates ZIP files with correct structure:
    skill-name.zip
    └── skill-name/
        ├── SKILL.md
        └── (other files)

Usage:
    uv run scripts/package_skills.py              # Package all skills
    uv run scripts/package_skills.py resume-formatter  # Package one skill
    uv run scripts/package_skills.py --output dist/    # Custom output directory
"""

import argparse
import zipfile
from pathlib import Path

SKILL_DIRS = [
    "resume-extractor",
    "resume-formatter",
    "resume-optimizer",
    "resume-reviewer",
    "resume-state",
    "resume-template-maker",
]

EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    ".DS_Store",
    "*.pdf",
    "*.typ",
    "*.tex",
]


def should_exclude(path: Path) -> bool:
    """Check if path should be excluded from packaging."""
    name = path.name
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            if name.endswith(pattern[1:]):
                return True
        elif name == pattern:
            return True
    return False


def package_skill(skill_dir: Path, output_dir: Path) -> Path:
    """Package a single skill as a ZIP file."""
    if not skill_dir.exists():
        raise FileNotFoundError(f"Skill directory not found: {skill_dir}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / f"{skill_dir.name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_dir.rglob("*"):
            if file_path.is_file() and not should_exclude(file_path):
                # Archive path: skill-name/relative/path
                arcname = f"{skill_dir.name}/{file_path.relative_to(skill_dir)}"
                zf.write(file_path, arcname)

    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Package skills as ZIP files")
    parser.add_argument("skills", nargs="*", help="Skill names to package (default: all)")
    parser.add_argument("-o", "--output", type=Path, default=Path("dist"),
                        help="Output directory for ZIP files (default: dist/)")
    parser.add_argument("--list", action="store_true", help="List available skills")

    args = parser.parse_args()

    if args.list:
        print("Available skills:")
        for skill in SKILL_DIRS:
            print(f"  - {skill}")
        return

    # Determine project root (parent of scripts/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    skills_to_package = args.skills if args.skills else SKILL_DIRS
    output_dir = args.output if args.output.is_absolute() else project_root / args.output

    print(f"Packaging skills to: {output_dir}/")
    print()

    for skill_name in skills_to_package:
        skill_dir = project_root / skill_name
        try:
            zip_path = package_skill(skill_dir, output_dir)
            # Get file count and size
            with zipfile.ZipFile(zip_path, 'r') as zf:
                file_count = len(zf.namelist())
            size_kb = zip_path.stat().st_size / 1024
            print(f"✓ {skill_name}.zip ({file_count} files, {size_kb:.1f} KB)")
        except FileNotFoundError as e:
            print(f"✗ {skill_name}: {e}")
        except Exception as e:
            print(f"✗ {skill_name}: {e}")

    print()
    print(f"Done. ZIP files ready in {output_dir}/")


if __name__ == "__main__":
    main()
