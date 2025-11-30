#!/usr/bin/env python3
"""Export version files to a target directory."""

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (
    get_store_path,
    get_version_entry,
    get_version_path,
    load_project_state,
    resolve_project,
)


def export_version(
    project: str,
    version_id: str,
    output_dir: Path,
    format: str = "all",
) -> list[Path]:
    """Export version files to a target directory.

    Args:
        project: Project name
        version_id: Version to export
        output_dir: Target directory
        format: What to export (pdf, yaml, all)

    Returns:
        List of exported file paths
    """
    store_path = get_store_path()
    state = load_project_state(project, store_path)

    version_entry = get_version_entry(state, version_id)
    if not version_entry:
        raise ValueError(f"Version not found: {version_id}")

    version_path = get_version_path(
        project, version_id, version_entry.get("tag"), store_path
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    exported = []

    # Map format to file extensions
    extensions = {
        "pdf": [".pdf"],
        "yaml": [".yaml", ".yml"],
        "all": [".pdf", ".yaml", ".yml", ".tex"],
    }
    allowed = extensions.get(format, extensions["all"])

    # Copy matching files
    for f in version_path.iterdir():
        if f.is_file() and f.suffix.lower() in allowed:
            dest = output_dir / f.name
            shutil.copy2(f, dest)
            exported.append(dest)

    return exported


def main():
    parser = argparse.ArgumentParser(description="Export version files to a directory")
    parser.add_argument("version", help="Version ID to export (e.g., v1, v2)")
    parser.add_argument("output", type=Path, help="Target directory")
    parser.add_argument(
        "--project", "-p",
        help="Project name (default: active project)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["pdf", "yaml", "all"],
        default="all",
        help="What to export (default: all)",
    )
    args = parser.parse_args()

    try:
        project = resolve_project(args.project)
        exported = export_version(
            project,
            args.version,
            args.output,
            format=args.format,
        )

        if exported:
            print(f"Exported {len(exported)} file(s) to {args.output}:")
            for f in exported:
                print(f"  {f.name}")
        else:
            print(f"No matching files found in {args.version}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
