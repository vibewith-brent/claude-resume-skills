#!/usr/bin/env python3
"""Import a PDF/DOCX resume as a new version."""

import argparse
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

# Path to extractor scripts (relative to project root)
EXTRACTOR_SCRIPTS = Path(__file__).parent.parent.parent / "resume-extractor" / "scripts"


def import_resume(
    file_path: Path,
    project: str,
    notes: str = "",
    tag: str | None = None,
) -> tuple[str, Path]:
    """Import a resume file as a new version.

    Returns:
        Tuple of (version_id, version_path)
    """
    store_path = get_store_path()
    state = load_project_state(project, store_path)

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
        extractor = EXTRACTOR_SCRIPTS / "extract_pdf.py"
    elif suffix in (".docx", ".doc"):
        extractor = EXTRACTOR_SCRIPTS / "extract_docx.py"
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    extracted_text_path = version_path / "extracted_text.txt"
    result = subprocess.run(
        ["uv", "run", str(extractor), str(file_path), "-o", str(extracted_text_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Warning: Extraction failed: {result.stderr}", file=sys.stderr)

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
