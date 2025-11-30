#!/usr/bin/env python3
"""Initialize a new resume project."""

import argparse
import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (
    PROJECT_SCHEMA_VERSION,
    ensure_store_exists,
    get_active_project,
    get_project_path,
    get_store_path,
    now_iso,
    save_config,
    load_config,
    save_project_state,
)


def init_project(name: str, set_active: bool = True) -> Path:
    """Initialize a new project with directory structure."""
    store_path = get_store_path()
    ensure_store_exists(store_path)

    project_path = get_project_path(name, store_path)
    if project_path.exists():
        raise FileExistsError(f"Project already exists: {name}")

    # Create directory structure
    (project_path / "sources").mkdir(parents=True)
    (project_path / "versions").mkdir(parents=True)
    (project_path / "jobs").mkdir(parents=True)

    # Initialize project state
    state = {
        "version": PROJECT_SCHEMA_VERSION,
        "name": name,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "active_version": None,
        "versions": [],
        "metadata": {},
    }
    save_project_state(name, state, store_path)

    # Set as active project if first or requested
    if set_active or get_active_project(store_path) is None:
        config = load_config(store_path)
        config["active_project"] = name
        save_config(config, store_path)

    return project_path


def main():
    parser = argparse.ArgumentParser(description="Initialize a new resume project")
    parser.add_argument("name", help="Project name (e.g., ml_engineer, product_manager)")
    parser.add_argument(
        "--no-activate",
        action="store_true",
        help="Don't set as active project",
    )
    args = parser.parse_args()

    try:
        project_path = init_project(args.name, set_active=not args.no_activate)
        print(f"Created project: {args.name}")
        print(f"  Path: {project_path}")
        if not args.no_activate:
            print(f"  Set as active project")
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
