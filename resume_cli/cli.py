#!/usr/bin/env python3
"""Unified CLI for resume management.

Usage:
    resume <command> [options]

Commands:
    init        Initialize a new project
    import      Import PDF/DOCX resume
    extract     Extract text from PDF/DOCX
    format      Generate PDF from YAML
    review      Review PDF quality
    version     Manage versions (list, switch, diff, export)
    cover       Generate cover letter
    job         Fetch job posting
    status      Show current project and version status

Examples:
    resume init my_resume
    resume import resume.pdf
    resume format --template executive
    resume format --all-templates
    resume version list
    resume cover "Acme Corp" "Senior Engineer" --job job.txt
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Find the project root (where pyproject.toml lives)
def get_project_root() -> Path:
    """Find project root by looking for pyproject.toml."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path.cwd()


PROJECT_ROOT = get_project_root()


def run_script(skill: str, script: str, args: list[str], check: bool = True) -> int:
    """Run a skill script with uv."""
    script_path = PROJECT_ROOT / skill / "scripts" / script
    if not script_path.exists():
        print(f"Error: Script not found: {script_path}", file=sys.stderr)
        return 1

    cmd = ["uv", "run", str(script_path)] + args
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if check and result.returncode != 0:
        return result.returncode
    return result.returncode


def get_active_yaml() -> Optional[Path]:
    """Get the active resume YAML path."""
    result = subprocess.run(
        ["uv", "run", str(PROJECT_ROOT / "resume-state/scripts/get_active.py")],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    return None


# =============================================================================
# INIT COMMAND
# =============================================================================

def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a new project."""
    script_args = [args.name]
    return run_script("resume-state", "init_project.py", script_args)


# =============================================================================
# IMPORT COMMAND
# =============================================================================

def cmd_import(args: argparse.Namespace) -> int:
    """Import a resume file."""
    script_args = [str(args.file)]
    if args.project:
        script_args.extend(["--project", args.project])
    return run_script("resume-state", "import_resume.py", script_args)


# =============================================================================
# EXTRACT COMMAND
# =============================================================================

def cmd_extract(args: argparse.Namespace) -> int:
    """Extract text from PDF or DOCX."""
    file_path = Path(args.file)
    suffix = file_path.suffix.lower()

    script_args = [str(file_path)]
    if args.output:
        script_args.extend(["--output", str(args.output)])

    if suffix == ".pdf":
        return run_script("resume-extractor", "extract_pdf.py", script_args)
    elif suffix in (".docx", ".doc"):
        return run_script("resume-extractor", "extract_docx.py", script_args)
    else:
        print(f"Error: Unsupported file type: {suffix}", file=sys.stderr)
        return 1


# =============================================================================
# FORMAT COMMAND
# =============================================================================

TEMPLATES = ["executive", "tech-modern", "modern-dense", "compact", "minimal"]


def cmd_format(args: argparse.Namespace) -> int:
    """Format YAML to PDF."""
    # Determine YAML source
    yaml_path = args.yaml
    if yaml_path is None:
        yaml_path = get_active_yaml()
        if yaml_path is None:
            print("Error: No YAML file specified and no active version found.", file=sys.stderr)
            print("Use: resume format <file.yaml> or set an active project.", file=sys.stderr)
            return 1
        print(f"Using active version: {yaml_path}", file=sys.stderr)
    else:
        yaml_path = Path(yaml_path)

    if not yaml_path.exists():
        print(f"Error: YAML file not found: {yaml_path}", file=sys.stderr)
        return 1

    # Handle --all-templates
    if args.all_templates:
        print("Compiling with all templates...\n", file=sys.stderr)
        results = []
        for template in TEMPLATES:
            typ_path = yaml_path.with_suffix(f".{template}.typ")
            pdf_path = yaml_path.with_suffix(f".{template}.pdf")

            # YAML → Typst
            typst_args = [str(yaml_path), template, "-o", str(typ_path)]
            if args.skip_validation:
                typst_args.append("--skip-validation")
            ret = run_script("resume-formatter", "yaml_to_typst.py", typst_args, check=False)

            if ret == 0:
                # Typst → PDF
                ret = run_script("resume-formatter", "compile_typst.py",
                               [str(typ_path), "-o", str(pdf_path)], check=False)

            if ret == 0:
                # Get page count
                try:
                    import pdfplumber
                    with pdfplumber.open(pdf_path) as pdf:
                        pages = len(pdf.pages)
                except (ImportError, OSError, Exception) as e:
                    pages = "?"
                results.append((template, pdf_path, pages, "OK"))
            else:
                results.append((template, None, 0, "FAILED"))

        # Print summary
        print("\nTemplate Comparison:", file=sys.stderr)
        print("-" * 50, file=sys.stderr)
        for template, pdf, pages, status in results:
            if status == "OK":
                print(f"  {template:15} {pages} page(s)  → {pdf.name}", file=sys.stderr)
            else:
                print(f"  {template:15} FAILED", file=sys.stderr)
        return 0

    # Single template mode
    template = args.template or "executive"

    # Determine output paths
    if args.output:
        pdf_path = Path(args.output)
        typ_path = pdf_path.with_suffix(".typ")
    else:
        typ_path = yaml_path.with_suffix(".typ")
        pdf_path = yaml_path.with_suffix(".pdf")

    # YAML → Typst
    typst_args = [str(yaml_path), template, "-o", str(typ_path)]
    if args.skip_validation:
        typst_args.append("--skip-validation")

    ret = run_script("resume-formatter", "yaml_to_typst.py", typst_args)
    if ret != 0:
        return ret

    # Typst → PDF
    ret = run_script("resume-formatter", "compile_typst.py", [str(typ_path), "-o", str(pdf_path)])
    if ret != 0:
        return ret

    print(f"\nGenerated: {pdf_path}", file=sys.stderr)
    return 0


# =============================================================================
# REVIEW COMMAND
# =============================================================================

def cmd_review(args: argparse.Namespace) -> int:
    """Review a PDF."""
    script_args = [str(args.pdf)]

    if args.compare:
        script_args.extend(["--compare", str(args.compare)])
    elif args.quick:
        script_args.append("--quick")
    elif args.checklist:
        script_args.append("--checklist")
    elif args.json:
        script_args.append("--json")

    return run_script("resume-reviewer", "review_pdf.py", script_args)


# =============================================================================
# VERSION COMMAND
# =============================================================================

def cmd_version(args: argparse.Namespace) -> int:
    """Manage versions."""
    subcmd = args.version_cmd

    if subcmd == "list":
        script_args = []
        if args.project:
            script_args.extend(["--project", args.project])
        return run_script("resume-state", "list_versions.py", script_args)

    elif subcmd == "create":
        script_args = []
        if args.tag:
            script_args.extend(["--tag", args.tag])
        if args.notes:
            script_args.extend(["--notes", args.notes])
        if args.project:
            script_args.extend(["--project", args.project])
        return run_script("resume-state", "create_version.py", script_args)

    elif subcmd == "switch":
        script_args = [args.version_id]
        if args.project:
            script_args.extend(["--project", args.project])
        return run_script("resume-state", "switch_version.py", script_args)

    elif subcmd == "diff":
        script_args = [args.v1, args.v2]
        if args.project:
            script_args.extend(["--project", args.project])
        return run_script("resume-state", "diff_versions.py", script_args)

    elif subcmd == "export":
        script_args = [args.version_id, str(args.output_dir)]
        if args.project:
            script_args.extend(["--project", args.project])
        return run_script("resume-state", "export_version.py", script_args)

    elif subcmd == "active":
        return run_script("resume-state", "get_active.py", [])

    else:
        print(f"Unknown version subcommand: {subcmd}", file=sys.stderr)
        return 1


# =============================================================================
# COVER COMMAND
# =============================================================================

def cmd_cover(args: argparse.Namespace) -> int:
    """Generate cover letter."""
    # Determine YAML source
    yaml_path = args.yaml
    if yaml_path is None:
        yaml_path = get_active_yaml()
        if yaml_path is None:
            print("Error: No YAML file specified and no active version found.", file=sys.stderr)
            return 1
        print(f"Using active version: {yaml_path}", file=sys.stderr)
    else:
        yaml_path = Path(yaml_path)

    script_args = [str(yaml_path)]

    if args.template:
        script_args.extend(["--template", args.template])
    if args.company:
        script_args.extend(["--company", args.company])
    if args.position:
        script_args.extend(["--position", args.position])
    if args.job_file:
        script_args.extend(["--job-file", str(args.job_file)])

    # Determine output
    if args.output:
        typ_path = Path(args.output).with_suffix(".typ")
        pdf_path = Path(args.output).with_suffix(".pdf")
    else:
        typ_path = yaml_path.with_name("cover_letter.typ")
        pdf_path = yaml_path.with_name("cover_letter.pdf")

    script_args.extend(["--output", str(typ_path)])

    ret = run_script("resume-coverletter", "generate_cover_letter.py", script_args)
    if ret != 0:
        return ret

    # Compile to PDF
    ret = run_script("resume-coverletter", "compile_cover_letter.py",
                    [str(typ_path), "--output", str(pdf_path)])
    if ret != 0:
        return ret

    print(f"\nGenerated: {pdf_path}", file=sys.stderr)
    return 0


# =============================================================================
# JOB COMMAND
# =============================================================================

def cmd_job(args: argparse.Namespace) -> int:
    """Fetch job posting."""
    script_args = [args.url]

    if args.output:
        script_args.extend(["--output", str(args.output)])
    if args.cache_dir:
        script_args.extend(["--cache-dir", str(args.cache_dir)])

    return run_script("resume-optimizer", "fetch_job_posting.py", script_args)


# =============================================================================
# STATUS COMMAND
# =============================================================================

def cmd_status(args: argparse.Namespace) -> int:
    """Show current status."""
    # Import state utils to get status
    sys.path.insert(0, str(PROJECT_ROOT / "resume-state" / "scripts"))
    try:
        from state_utils import (
            get_store_path, load_config, get_active_project,
            load_project_state, get_active_version_path
        )
    except ImportError:
        print("Error: Could not load state utilities", file=sys.stderr)
        return 1

    store_path = get_store_path()
    print(f"Store: {store_path}")

    if not store_path.exists():
        print("\nNo resume store found. Run 'resume init <project>' to start.")
        return 0

    config = load_config(store_path)
    active_project = config.get("active_project")

    if not active_project:
        print("\nNo active project. Run 'resume init <project>' to start.")
        return 0

    print(f"Project: {active_project}")

    try:
        state = load_project_state(active_project, store_path)
        active_version = state.get("active_version")
        versions = state.get("versions", [])

        print(f"Active Version: {active_version}")
        print(f"Total Versions: {len(versions)}")

        # Get active YAML path
        try:
            yaml_path = get_active_version_path(active_project, store_path)
            print(f"Active YAML: {yaml_path}")
            if yaml_path.exists():
                print(f"  (exists, {yaml_path.stat().st_size} bytes)")
        except Exception as e:
            print(f"Active YAML: (error: {e})")

    except FileNotFoundError:
        print(f"Project '{active_project}' not found.")
        return 1

    return 0


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        prog="resume",
        description="Unified CLI for resume management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  resume init my_resume              # Start new project
  resume import resume.pdf           # Import existing resume
  resume format --template executive # Generate PDF
  resume format --all-templates      # Compare all templates
  resume version list                # List versions
  resume status                      # Show current status
        """,
    )
    parser.add_argument(
        "--version", action="version",
        version=f"%(prog)s 1.5.0"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # -------------------------------------------------------------------------
    # init
    # -------------------------------------------------------------------------
    p_init = subparsers.add_parser("init", help="Initialize a new project")
    p_init.add_argument("name", help="Project name")
    p_init.set_defaults(func=cmd_init)

    # -------------------------------------------------------------------------
    # import
    # -------------------------------------------------------------------------
    p_import = subparsers.add_parser("import", help="Import PDF/DOCX resume")
    p_import.add_argument("file", type=Path, help="Resume file (PDF or DOCX)")
    p_import.add_argument("-p", "--project", help="Project name (default: active)")
    p_import.set_defaults(func=cmd_import)

    # -------------------------------------------------------------------------
    # extract
    # -------------------------------------------------------------------------
    p_extract = subparsers.add_parser("extract", help="Extract text from PDF/DOCX")
    p_extract.add_argument("file", type=Path, help="File to extract")
    p_extract.add_argument("-o", "--output", type=Path, help="Output file")
    p_extract.set_defaults(func=cmd_extract)

    # -------------------------------------------------------------------------
    # format
    # -------------------------------------------------------------------------
    p_format = subparsers.add_parser("format", help="Generate PDF from YAML")
    p_format.add_argument("yaml", nargs="?", type=Path, help="YAML file (default: active version)")
    p_format.add_argument("-t", "--template", choices=TEMPLATES, help="Template name")
    p_format.add_argument("-o", "--output", type=Path, help="Output PDF path")
    p_format.add_argument("--all-templates", action="store_true",
                          help="Compile with all templates for comparison")
    p_format.add_argument("--skip-validation", action="store_true",
                          help="Skip YAML schema validation")
    p_format.set_defaults(func=cmd_format)

    # -------------------------------------------------------------------------
    # review
    # -------------------------------------------------------------------------
    p_review = subparsers.add_parser("review", help="Review PDF quality")
    p_review.add_argument("pdf", type=Path, help="PDF to review")
    p_review.add_argument("--compare", type=Path, help="Compare with another PDF")
    p_review.add_argument("--quick", action="store_true", help="Quick review template")
    p_review.add_argument("--checklist", action="store_true", help="Show full checklist")
    p_review.add_argument("--json", action="store_true", help="Output as JSON")
    p_review.set_defaults(func=cmd_review)

    # -------------------------------------------------------------------------
    # version
    # -------------------------------------------------------------------------
    p_version = subparsers.add_parser("version", help="Manage versions")
    version_sub = p_version.add_subparsers(dest="version_cmd", help="Version command")

    # version list
    v_list = version_sub.add_parser("list", help="List versions")
    v_list.add_argument("-p", "--project", help="Project name")

    # version create
    v_create = version_sub.add_parser("create", help="Create new version")
    v_create.add_argument("-t", "--tag", help="Version tag (e.g., 'google')")
    v_create.add_argument("-n", "--notes", help="Version notes")
    v_create.add_argument("-p", "--project", help="Project name")

    # version switch
    v_switch = version_sub.add_parser("switch", help="Switch active version")
    v_switch.add_argument("version_id", help="Version to switch to (e.g., v1, v2)")
    v_switch.add_argument("-p", "--project", help="Project name")

    # version diff
    v_diff = version_sub.add_parser("diff", help="Compare two versions")
    v_diff.add_argument("v1", help="First version")
    v_diff.add_argument("v2", help="Second version")
    v_diff.add_argument("-p", "--project", help="Project name")

    # version export
    v_export = version_sub.add_parser("export", help="Export version files")
    v_export.add_argument("version_id", help="Version to export")
    v_export.add_argument("output_dir", type=Path, help="Output directory")
    v_export.add_argument("-p", "--project", help="Project name")

    # version active
    v_active = version_sub.add_parser("active", help="Show active version path")

    p_version.set_defaults(func=cmd_version)

    # -------------------------------------------------------------------------
    # cover
    # -------------------------------------------------------------------------
    p_cover = subparsers.add_parser("cover", help="Generate cover letter")
    p_cover.add_argument("yaml", nargs="?", type=Path, help="Resume YAML (default: active)")
    p_cover.add_argument("-c", "--company", help="Company name")
    p_cover.add_argument("-p", "--position", help="Position/job title")
    p_cover.add_argument("-j", "--job-file", type=Path, help="Job description file")
    p_cover.add_argument("-t", "--template", help="Cover letter template")
    p_cover.add_argument("-o", "--output", type=Path, help="Output path")
    p_cover.set_defaults(func=cmd_cover)

    # -------------------------------------------------------------------------
    # job
    # -------------------------------------------------------------------------
    p_job = subparsers.add_parser("job", help="Fetch job posting")
    p_job.add_argument("url", help="Job posting URL")
    p_job.add_argument("-o", "--output", type=Path, help="Output file")
    p_job.add_argument("--cache-dir", type=Path, help="Cache directory")
    p_job.set_defaults(func=cmd_job)

    # -------------------------------------------------------------------------
    # status
    # -------------------------------------------------------------------------
    p_status = subparsers.add_parser("status", help="Show current status")
    p_status.set_defaults(func=cmd_status)

    # -------------------------------------------------------------------------
    # Parse and run
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
