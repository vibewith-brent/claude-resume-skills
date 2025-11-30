#!/usr/bin/env python3
"""Create a new version from an existing one."""

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (
    get_next_version_id,
    get_store_path,
    get_version_entry,
    get_version_path,
    load_project_state,
    now_iso,
    resolve_project,
    save_project_state,
)


def create_version(
    project: str,
    from_version: str | None = None,
    tag: str | None = None,
    notes: str = "",
    operation: str = "manual_edit",
) -> tuple[str, Path]:
    """Create a new version derived from an existing one.

    Args:
        project: Project name
        from_version: Version ID to copy from (default: active version)
        tag: Optional tag for the new version
        notes: Notes about this version
        operation: Operation type (manual_edit, optimize, tailor)

    Returns:
        Tuple of (version_id, version_path)
    """
    store_path = get_store_path()
    state = load_project_state(project, store_path)

    # Determine source version
    if from_version is None:
        from_version = state.get("active_version")
        if not from_version:
            raise ValueError("No active version to derive from")

    parent_entry = get_version_entry(state, from_version)
    if not parent_entry:
        raise ValueError(f"Version not found: {from_version}")

    # Get parent version path
    parent_path = get_version_path(
        project, from_version, parent_entry.get("tag"), store_path
    )
    parent_yaml = parent_path / "resume.yaml"
    if not parent_yaml.exists():
        raise ValueError(f"Parent YAML not found: {parent_yaml}")

    # Create new version
    version_id = get_next_version_id(state)
    version_path = get_version_path(project, version_id, tag, store_path)
    version_path.mkdir(parents=True, exist_ok=True)

    # Copy YAML from parent
    new_yaml = version_path / "resume.yaml"
    shutil.copy2(parent_yaml, new_yaml)

    # Update project state
    version_entry = {
        "id": version_id,
        "tag": tag,
        "created_at": now_iso(),
        "source": {
            "type": "derived",
            "operation": operation,
        },
        "parent": from_version,
        "notes": notes or f"Derived from {from_version}",
    }
    state["versions"].append(version_entry)
    state["active_version"] = version_id
    save_project_state(project, state, store_path)

    return version_id, version_path


def main():
    parser = argparse.ArgumentParser(description="Create a new version from existing")
    parser.add_argument(
        "--from", "-f",
        dest="from_version",
        help="Version ID to copy from (default: active version)",
    )
    parser.add_argument(
        "--project", "-p",
        help="Project name (default: active project)",
    )
    parser.add_argument(
        "--tag", "-t",
        help="Optional version tag (e.g., google_tailored)",
    )
    parser.add_argument(
        "--notes", "-n",
        default="",
        help="Notes about this version",
    )
    parser.add_argument(
        "--operation", "-o",
        default="manual_edit",
        choices=["manual_edit", "optimize", "tailor"],
        help="Type of operation (default: manual_edit)",
    )
    args = parser.parse_args()

    try:
        project = resolve_project(args.project)
        version_id, version_path = create_version(
            project,
            from_version=args.from_version,
            tag=args.tag,
            notes=args.notes,
            operation=args.operation,
        )
        print(f"Created {version_id} in project: {project}")
        print(f"  Parent: {args.from_version or 'active'}")
        print(f"  Path: {version_path}")
        print(f"  YAML: {version_path / 'resume.yaml'}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
