#!/usr/bin/env python3
"""Import a PDF/DOCX resume as a new version."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (
    copy_file,
    get_next_version_id,
    get_project_path,
    get_store_path,
    get_version_path,
    load_project_state,
    now_iso,
    resolve_project,
    save_project_state,
)


def find_extractor_scripts() -> Path:
    """Find the resume-extractor scripts directory.

    Search order:
    1. RESUME_EXTRACTOR_PATH environment variable
    2. Sibling directory: ../resume-extractor/scripts (for development)
    3. Symlinked skills: ../.claude/skills/resume-extractor/scripts
    4. Parent directories: search upward for resume-extractor
    5. Fallback: ../../resume-extractor/scripts (legacy path)

    Returns:
        Path to the extractor scripts directory

    Raises:
        FileNotFoundError: If extractor scripts cannot be found
    """
    # Check environment variable first
    env_path = os.environ.get("RESUME_EXTRACTOR_PATH")
    if env_path:
        path = Path(env_path).expanduser()
        if path.exists():
            return path

    script_dir = Path(__file__).parent
    candidates = [
        # Sibling skill directory (common in development)
        script_dir.parent.parent / "resume-extractor" / "scripts",
        # Symlinked via .claude/skills
        script_dir.parent.parent / ".claude" / "skills" / "resume-extractor" / "scripts",
        # Legacy hardcoded path (grandparent / resume-extractor)
        script_dir.parent.parent.parent / "resume-extractor" / "scripts",
    ]

    for candidate in candidates:
        if candidate.exists() and (candidate / "extract_pdf.py").exists():
            return candidate

    # Search upward for resume-extractor
    current = script_dir
    for _ in range(10):  # Limit search depth
        parent = current.parent
        if parent == current:
            break
        candidate = parent / "resume-extractor" / "scripts"
        if candidate.exists() and (candidate / "extract_pdf.py").exists():
            return candidate
        current = parent

    raise FileNotFoundError(
        "Could not find resume-extractor scripts. "
        "Set RESUME_EXTRACTOR_PATH environment variable or ensure "
        "resume-extractor is a sibling directory."
    )


def import_resume(
    file_path: Path,
    project: str,
    notes: str = "",
    tag: str | None = None,
    strict: bool = False,
) -> tuple[str, Path]:
    """Import a resume file as a new version.

    Args:
        file_path: Path to PDF or DOCX file
        project: Project name
        notes: Optional notes about this import
        tag: Optional version tag
        strict: If True, fail on extraction errors instead of warning

    Returns:
        Tuple of (version_id, version_path)

    Raises:
        RuntimeError: If strict=True and extraction fails
    """
    store_path = get_store_path()
    state = load_project_state(project, store_path)

    # Find extractor scripts
    extractor_scripts = find_extractor_scripts()

    # Determine version ID
    version_id = get_next_version_id(state)

    # Copy source file
    project_path = get_project_path(project, store_path)
    source_filename = f"{version_id}_{file_path.name}"
    source_dest = project_path / "sources" / source_filename
    copy_file(file_path, source_dest)

    # Create version directory
    version_path = get_version_path(project, version_id, tag, store_path)
    version_path.mkdir(parents=True, exist_ok=True)

    # Extract text using appropriate extractor
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        extractor = extractor_scripts / "extract_pdf.py"
    elif suffix in (".docx", ".doc"):
        extractor = extractor_scripts / "extract_docx.py"
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    extracted_text_path = version_path / "extracted_text.txt"
    result = subprocess.run(
        ["uv", "run", str(extractor), str(file_path), "-o", str(extracted_text_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        error_msg = f"Extraction failed: {result.stderr}"
        if strict:
            raise RuntimeError(error_msg)
        print(f"Warning: {error_msg}", file=sys.stderr)
        print("Continuing with import. You may need to manually extract text.", file=sys.stderr)

    # Create placeholder YAML
    yaml_path = version_path / "resume.yaml"
    yaml_content = f"""# Resume extracted from: {file_path.name}
# Version: {version_id}
# Created: {now_iso()}
#
# TODO: Parse extracted_text.txt into structured YAML format
# See references/resume_schema.yaml for the expected structure

contact:
  name: ""
  email: ""
  phone: ""
  location: ""

summary: ""

experience: []

education: []

skills: []
"""
    yaml_path.write_text(yaml_content)

    # Update project state
    version_entry = {
        "id": version_id,
        "tag": tag,
        "created_at": now_iso(),
        "source": {
            "type": "import",
            "file": source_filename,
            "original_name": file_path.name,
        },
        "parent": None,
        "notes": notes or f"Imported from {file_path.name}",
    }
    state["versions"].append(version_entry)
    state["active_version"] = version_id
    save_project_state(project, state, store_path)

    return version_id, version_path


def main():
    parser = argparse.ArgumentParser(description="Import a PDF/DOCX resume as a new version")
    parser.add_argument("file", type=Path, help="Path to PDF or DOCX file")
    parser.add_argument(
        "--project", "-p",
        help="Project name (default: active project)",
    )
    parser.add_argument(
        "--notes", "-n",
        default="",
        help="Notes about this import",
    )
    parser.add_argument(
        "--tag", "-t",
        help="Optional version tag",
    )
    parser.add_argument(
        "--strict", "-s",
        action="store_true",
        help="Fail on extraction errors instead of warning",
    )
    args = parser.parse_args()

    try:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)

        project = resolve_project(args.project)
        version_id, version_path = import_resume(
            args.file,
            project,
            notes=args.notes,
            tag=args.tag,
            strict=args.strict,
        )
        print(f"Imported as {version_id} in project: {project}")
        print(f"  Source: {args.file.name}")
        print(f"  Version path: {version_path}")
        print(f"  YAML: {version_path / 'resume.yaml'}")
        print(f"  Extracted text: {version_path / 'extracted_text.txt'}")
        print()
        print("Next: Parse extracted_text.txt into resume.yaml")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
