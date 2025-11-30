#!/usr/bin/env python3
"""Get the path to the active version's YAML file."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (
    get_active_version_path,
    resolve_project,
)


def main():
    parser = argparse.ArgumentParser(
        description="Print the path to the active version's YAML file"
    )
    parser.add_argument(
        "--project", "-p",
        help="Project name (default: active project)",
    )
    parser.add_argument(
        "--dir", "-d",
        action="store_true",
        help="Print version directory instead of YAML path",
    )
    args = parser.parse_args()

    try:
        project = resolve_project(args.project)
        yaml_path = get_active_version_path(project)

        if args.dir:
            print(yaml_path.parent)
        else:
            print(yaml_path)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
