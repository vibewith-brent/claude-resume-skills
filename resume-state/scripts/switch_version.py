#!/usr/bin/env python3
"""Switch the active version in a project."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (
    get_store_path,
    get_version_entry,
    get_version_path,
    load_project_state,
    resolve_project,
    save_project_state,
)


def switch_version(project: str, version_id: str) -> Path:
    """Switch to a different version.

    Returns:
        Path to the new active version's YAML
    """
    store_path = get_store_path()
    state = load_project_state(project, store_path)

    version_entry = get_version_entry(state, version_id)
    if not version_entry:
        raise ValueError(f"Version not found: {version_id}")

    state["active_version"] = version_id
    save_project_state(project, state, store_path)

    version_path = get_version_path(
        project, version_id, version_entry.get("tag"), store_path
    )
    return version_path / "resume.yaml"


def main():
    parser = argparse.ArgumentParser(description="Switch the active version")
    parser.add_argument("version", help="Version ID to switch to (e.g., v1, v2)")
    parser.add_argument(
        "--project", "-p",
        help="Project name (default: active project)",
    )
    args = parser.parse_args()

    try:
        project = resolve_project(args.project)
        yaml_path = switch_version(project, args.version)
        print(f"Switched to {args.version}")
        print(f"  YAML: {yaml_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
