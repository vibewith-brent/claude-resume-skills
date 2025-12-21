#!/usr/bin/env python3
"""Unified CLI for resume management skills.

Usage:
    resume state init <project>
    resume state import <file> [--project <name>]
    resume state version create [--tag <tag>] [--notes <notes>]
    resume state list
    resume state switch <version>
    resume state export <version> <output_dir>
    resume state diff <v1> <v2>
    resume state rollback <version>
    resume extract <file>
    resume validate <yaml_file> [--strict]
    resume format <yaml_file> [template] [-o output.pdf]
    resume format <yaml_file> --compare all [-o output_dir/]
    resume job fetch <url> [--output <file>]
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def get_skills_root() -> Path:
    """Get the root directory containing skills."""
    # Try relative to this file first (development)
    cli_path = Path(__file__).parent
    candidates = [
        cli_path.parent.parent,  # src/resume_cli -> repo root
        cli_path.parent.parent / ".claude" / "skills",  # symlinked skills
    ]

    for candidate in candidates:
        if (candidate / "resume-state").exists():
            return candidate
        if (candidate / "resume-state" / "scripts").exists():
            return candidate

    # Fallback: assume we're in repo root
    return Path.cwd()


def run_script(skill: str, script: str, args: list[str]) -> int:
    """Run a skill script with the given arguments."""
    root = get_skills_root()
    script_path = root / skill / "scripts" / script

    if not script_path.exists():
        # Try .claude/skills path
        script_path = root / ".claude" / "skills" / skill / "scripts" / script
        if not script_path.exists():
            print(f"Error: Script not found: {script_path}", file=sys.stderr)
            return 1

    cmd = ["uv", "run", str(script_path), *args]
    result = subprocess.run(cmd)
    return result.returncode


def cmd_state_init(args: argparse.Namespace) -> int:
    """Initialize a new project."""
    return run_script("resume-state", "init_project.py", [args.project])


def cmd_state_import(args: argparse.Namespace) -> int:
    """Import a PDF/DOCX resume."""
    script_args = [str(args.file)]
    if args.project:
        script_args.extend(["--project", args.project])
    if args.notes:
        script_args.extend(["--notes", args.notes])
    if args.tag:
        script_args.extend(["--tag", args.tag])
    if args.strict:
        script_args.append("--strict")
    return run_script("resume-state", "import_resume.py", script_args)


def cmd_state_version_create(args: argparse.Namespace) -> int:
    """Create a new version."""
    script_args = []
    if args.project:
        script_args.extend(["--project", args.project])
    if args.tag:
        script_args.extend(["--tag", args.tag])
    if args.notes:
        script_args.extend(["--notes", args.notes])
    return run_script("resume-state", "create_version.py", script_args)


def cmd_state_list(args: argparse.Namespace) -> int:
    """List versions."""
    script_args = []
    if args.project:
        script_args.extend(["--project", args.project])
    return run_script("resume-state", "list_versions.py", script_args)


def cmd_state_switch(args: argparse.Namespace) -> int:
    """Switch active version."""
    script_args = [args.version]
    if args.project:
        script_args.extend(["--project", args.project])
    return run_script("resume-state", "switch_version.py", script_args)


def cmd_state_export(args: argparse.Namespace) -> int:
    """Export a version."""
    script_args = [args.version, str(args.output_dir)]
    if args.project:
        script_args.extend(["--project", args.project])
    return run_script("resume-state", "export_version.py", script_args)


def cmd_state_diff(args: argparse.Namespace) -> int:
    """Diff two versions."""
    script_args = [args.v1, args.v2]
    if args.project:
        script_args.extend(["--project", args.project])
    return run_script("resume-state", "diff_versions.py", script_args)


def cmd_state_rollback(args: argparse.Namespace) -> int:
    """Rollback to a previous version by creating a new version from it."""
    # Get the YAML from the target version and create a new version
    script_args = ["--notes", f"Rollback to {args.version}"]
    if args.project:
        script_args.extend(["--project", args.project])

    # First switch to the version we want to rollback to
    switch_result = run_script("resume-state", "switch_version.py", [args.version])
    if switch_result != 0:
        return switch_result

    # Then create a new version from it
    return run_script("resume-state", "create_version.py", script_args)


def cmd_extract(args: argparse.Namespace) -> int:
    """Extract text from PDF/DOCX."""
    suffix = args.file.suffix.lower()
    if suffix == ".pdf":
        script = "extract_pdf.py"
    elif suffix in (".docx", ".doc"):
        script = "extract_docx.py"
    else:
        print(f"Error: Unsupported file type: {suffix}", file=sys.stderr)
        return 1

    script_args = [str(args.file)]
    if args.output:
        script_args.extend(["--output", str(args.output)])
    return run_script("resume-extractor", script, script_args)


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate resume YAML."""
    script_args = [str(args.file)]
    if args.strict:
        script_args.append("--strict")
    if args.json:
        script_args.append("--json")
    return run_script("resume-optimizer", "validate_yaml.py", script_args)


def cmd_format(args: argparse.Namespace) -> int:
    """Format resume YAML to PDF."""
    root = get_skills_root()
    yaml_to_typst = root / "resume-formatter" / "scripts" / "yaml_to_typst.py"
    compile_typst = root / "resume-formatter" / "scripts" / "compile_typst.py"

    # Fallback to .claude/skills
    if not yaml_to_typst.exists():
        yaml_to_typst = root / ".claude" / "skills" / "resume-formatter" / "scripts" / "yaml_to_typst.py"
        compile_typst = root / ".claude" / "skills" / "resume-formatter" / "scripts" / "compile_typst.py"

    if not yaml_to_typst.exists():
        print("Error: Formatter scripts not found", file=sys.stderr)
        return 1

    templates = args.template if isinstance(args.template, list) else [args.template]

    # Handle --compare all
    if args.compare:
        templates = ["executive", "compact", "minimal"]

    results = []
    for template in templates:
        with tempfile.NamedTemporaryFile(suffix=".typ", delete=False) as tmp:
            typ_path = Path(tmp.name)

        try:
            # Generate Typst
            result = subprocess.run(
                ["uv", "run", str(yaml_to_typst), str(args.file), template, "-o", str(typ_path)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"Error generating Typst for {template}: {result.stderr}", file=sys.stderr)
                return 1

            # Determine output path
            if args.output:
                if args.compare or len(templates) > 1:
                    # Multiple outputs go to directory
                    output_dir = Path(args.output)
                    output_dir.mkdir(parents=True, exist_ok=True)
                    pdf_path = output_dir / f"{template}.pdf"
                else:
                    pdf_path = Path(args.output)
            else:
                pdf_path = args.file.with_suffix(f".{template}.pdf")

            # Compile to PDF
            result = subprocess.run(
                ["uv", "run", str(compile_typst), str(typ_path), "-o", str(pdf_path)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"Error compiling {template}: {result.stderr}", file=sys.stderr)
                return 1

            results.append((template, pdf_path))
            print(f"Generated: {pdf_path}", file=sys.stderr)

        finally:
            typ_path.unlink(missing_ok=True)

    if len(results) > 1:
        print(f"\nGenerated {len(results)} PDFs:", file=sys.stderr)
        for template, path in results:
            print(f"  {template}: {path}", file=sys.stderr)

    return 0


def cmd_job_fetch(args: argparse.Namespace) -> int:
    """Fetch job posting from URL."""
    script_args = [args.url]
    if args.output:
        script_args.extend(["--output", str(args.output)])
    if args.cache_dir:
        script_args.extend(["--cache-dir", str(args.cache_dir)])
    return run_script("resume-optimizer", "fetch_job_posting.py", script_args)


def main():
    parser = argparse.ArgumentParser(
        prog="resume",
        description="Unified CLI for resume management skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.2.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ========== STATE COMMANDS ==========
    state_parser = subparsers.add_parser("state", help="Version and project management")
    state_subparsers = state_parser.add_subparsers(dest="state_command")

    # state init
    init_parser = state_subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("project", help="Project name")
    init_parser.set_defaults(func=cmd_state_init)

    # state import
    import_parser = state_subparsers.add_parser("import", help="Import a PDF/DOCX resume")
    import_parser.add_argument("file", type=Path, help="PDF or DOCX file to import")
    import_parser.add_argument("-p", "--project", help="Project name")
    import_parser.add_argument("-n", "--notes", help="Notes about import")
    import_parser.add_argument("-t", "--tag", help="Version tag")
    import_parser.add_argument("-s", "--strict", action="store_true", help="Fail on extraction errors")
    import_parser.set_defaults(func=cmd_state_import)

    # state version (subcommand group)
    version_parser = state_subparsers.add_parser("version", help="Version operations")
    version_subparsers = version_parser.add_subparsers(dest="version_command")

    # state version create
    create_parser = version_subparsers.add_parser("create", help="Create new version")
    create_parser.add_argument("-p", "--project", help="Project name")
    create_parser.add_argument("-t", "--tag", help="Version tag")
    create_parser.add_argument("-n", "--notes", help="Version notes")
    create_parser.set_defaults(func=cmd_state_version_create)

    # state list
    list_parser = state_subparsers.add_parser("list", help="List versions")
    list_parser.add_argument("-p", "--project", help="Project name")
    list_parser.set_defaults(func=cmd_state_list)

    # state switch
    switch_parser = state_subparsers.add_parser("switch", help="Switch active version")
    switch_parser.add_argument("version", help="Version ID (e.g., v1, v2)")
    switch_parser.add_argument("-p", "--project", help="Project name")
    switch_parser.set_defaults(func=cmd_state_switch)

    # state export
    export_parser = state_subparsers.add_parser("export", help="Export a version")
    export_parser.add_argument("version", help="Version ID")
    export_parser.add_argument("output_dir", type=Path, help="Output directory")
    export_parser.add_argument("-p", "--project", help="Project name")
    export_parser.set_defaults(func=cmd_state_export)

    # state diff
    diff_parser = state_subparsers.add_parser("diff", help="Diff two versions")
    diff_parser.add_argument("v1", help="First version ID")
    diff_parser.add_argument("v2", help="Second version ID")
    diff_parser.add_argument("-p", "--project", help="Project name")
    diff_parser.set_defaults(func=cmd_state_diff)

    # state rollback
    rollback_parser = state_subparsers.add_parser("rollback", help="Rollback to a version")
    rollback_parser.add_argument("version", help="Version to rollback to")
    rollback_parser.add_argument("-p", "--project", help="Project name")
    rollback_parser.set_defaults(func=cmd_state_rollback)

    # ========== EXTRACT COMMAND ==========
    extract_parser = subparsers.add_parser("extract", help="Extract text from PDF/DOCX")
    extract_parser.add_argument("file", type=Path, help="PDF or DOCX file")
    extract_parser.add_argument("-o", "--output", type=Path, help="Output file")
    extract_parser.set_defaults(func=cmd_extract)

    # ========== VALIDATE COMMAND ==========
    validate_parser = subparsers.add_parser("validate", help="Validate resume YAML")
    validate_parser.add_argument("file", type=Path, help="YAML file to validate")
    validate_parser.add_argument("-s", "--strict", action="store_true", help="Treat warnings as errors")
    validate_parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    validate_parser.set_defaults(func=cmd_validate)

    # ========== FORMAT COMMAND ==========
    format_parser = subparsers.add_parser("format", help="Format resume to PDF")
    format_parser.add_argument("file", type=Path, help="YAML file to format")
    format_parser.add_argument(
        "template",
        nargs="?",
        default="executive",
        choices=["executive", "compact", "minimal"],
        help="Template to use (default: executive)",
    )
    format_parser.add_argument("-o", "--output", type=Path, help="Output path (file or directory)")
    format_parser.add_argument(
        "--compare",
        action="store_true",
        help="Generate all templates for comparison",
    )
    format_parser.set_defaults(func=cmd_format)

    # ========== JOB COMMAND ==========
    job_parser = subparsers.add_parser("job", help="Job posting operations")
    job_subparsers = job_parser.add_subparsers(dest="job_command")

    # job fetch
    fetch_parser = job_subparsers.add_parser("fetch", help="Fetch job posting from URL")
    fetch_parser.add_argument("url", help="Job posting URL")
    fetch_parser.add_argument("-o", "--output", type=Path, help="Output file")
    fetch_parser.add_argument("--cache-dir", type=Path, help="Cache directory")
    fetch_parser.set_defaults(func=cmd_job_fetch)

    # Parse and execute
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Handle subcommands that need deeper nesting
    if args.command == "state" and not args.state_command:
        state_parser.print_help()
        return 1

    if args.command == "state" and args.state_command == "version" and not getattr(args, "version_command", None):
        version_parser.print_help()
        return 1

    if args.command == "job" and not args.job_command:
        job_parser.print_help()
        return 1

    if hasattr(args, "func"):
        return args.func(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
