#!/usr/bin/env python3
"""Compare YAML content between two versions."""

import argparse
import difflib
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


def diff_versions(
    project: str,
    version_a: str,
    version_b: str,
    context_lines: int = 3,
) -> str:
    """Generate a diff between two versions' YAML files.

    Returns:
        Unified diff string
    """
    store_path = get_store_path()
    state = load_project_state(project, store_path)

    # Get version entries
    entry_a = get_version_entry(state, version_a)
    entry_b = get_version_entry(state, version_b)

    if not entry_a:
        raise ValueError(f"Version not found: {version_a}")
    if not entry_b:
        raise ValueError(f"Version not found: {version_b}")

    # Get YAML paths
    path_a = get_version_path(project, version_a, entry_a.get("tag"), store_path)
    path_b = get_version_path(project, version_b, entry_b.get("tag"), store_path)

    yaml_a = path_a / "resume.yaml"
    yaml_b = path_b / "resume.yaml"

    if not yaml_a.exists():
        raise ValueError(f"YAML not found for {version_a}: {yaml_a}")
    if not yaml_b.exists():
        raise ValueError(f"YAML not found for {version_b}: {yaml_b}")

    # Read files
    lines_a = yaml_a.read_text().splitlines(keepends=True)
    lines_b = yaml_b.read_text().splitlines(keepends=True)

    # Generate diff
    diff = difflib.unified_diff(
        lines_a,
        lines_b,
        fromfile=f"{version_a}/resume.yaml",
        tofile=f"{version_b}/resume.yaml",
        n=context_lines,
    )

    return "".join(diff)


def main():
    parser = argparse.ArgumentParser(description="Compare YAML between two versions")
    parser.add_argument("version_a", help="First version ID (e.g., v1)")
    parser.add_argument("version_b", help="Second version ID (e.g., v2)")
    parser.add_argument(
        "--project", "-p",
        help="Project name (default: active project)",
    )
    parser.add_argument(
        "--context", "-c",
        type=int,
        default=3,
        help="Number of context lines (default: 3)",
    )
    args = parser.parse_args()

    try:
        project = resolve_project(args.project)
        diff_output = diff_versions(
            project,
            args.version_a,
            args.version_b,
            context_lines=args.context,
        )

        if diff_output:
            print(diff_output)
        else:
            print(f"No differences between {args.version_a} and {args.version_b}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
