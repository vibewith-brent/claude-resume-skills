#!/usr/bin/env python3
"""List versions in a project."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (
    get_active_project,
    list_projects,
    load_project_state,
    resolve_project,
)


def format_date(iso_date: str) -> str:
    """Format ISO date to short form."""
    return iso_date[:10] if iso_date else "N/A"


def list_versions(project: str, verbose: bool = False) -> None:
    """Print version list for a project."""
    state = load_project_state(project)
    active_version = state.get("active_version")
    versions = state.get("versions", [])

    if not versions:
        print(f"No versions in project: {project}")
        return

    print(f"{project} versions:")
    print()

    for v in versions:
        marker = "*" if v["id"] == active_version else " "
        source_type = v.get("source", {}).get("type", "unknown")
        tag_str = v.get("tag") or ""
        date_str = format_date(v.get("created_at", ""))
        notes = v.get("notes", "")

        # Format: * v1     [import]  2025-11-30  tag - notes
        tag_display = f"{tag_str} - " if tag_str else ""
        print(f"{marker} {v['id']:<6} [{source_type:<7}] {date_str}  {tag_display}{notes}")

        if verbose:
            parent = v.get("parent")
            if parent:
                print(f"         parent: {parent}")
            source = v.get("source", {})
            if source.get("file"):
                print(f"         file: {source['file']}")
            if source.get("operation"):
                print(f"         operation: {source['operation']}")
            print()


def main():
    parser = argparse.ArgumentParser(description="List versions in a project")
    parser.add_argument(
        "--project", "-p",
        help="Project name (default: active project)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed version info",
    )
    parser.add_argument(
        "--list-projects",
        action="store_true",
        help="List all projects instead of versions",
    )
    args = parser.parse_args()

    try:
        if args.list_projects:
            projects = list_projects()
            active = get_active_project()
            if not projects:
                print("No projects found")
                return
            print("Projects:")
            for p in projects:
                marker = "*" if p == active else " "
                print(f"{marker} {p}")
            return

        project = resolve_project(args.project)
        list_versions(project, verbose=args.verbose)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
