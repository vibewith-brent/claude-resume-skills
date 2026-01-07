#!/usr/bin/env python3
"""Manage coaching session persistence.

This script handles I/O operations for coaching sessions. Claude drives
the actual coaching conversation via SKILL.md; this script just persists
and retrieves session state.

Commands:
    save    Save session state to version's coaching directory
    load    Load a specific session by ID
    list    List sessions for current version
    resume  Load latest incomplete session (status: active or paused)

Usage:
    uv run resume-coach/scripts/session_manager.py save < session.json
    uv run resume-coach/scripts/session_manager.py load --id session_20250107_143022
    uv run resume-coach/scripts/session_manager.py list
    uv run resume-coach/scripts/session_manager.py resume
"""

import argparse
import json
import sys
from pathlib import Path

# Add resume-state scripts to path
sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "resume-state" / "scripts")
)

from state_utils import (
    resolve_project,
    load_project_state,
    get_version_entry,
    save_coaching_session,
    load_coaching_session,
    list_coaching_sessions,
    get_latest_session,
)


def cmd_save(args):
    """Save session from stdin."""
    project = resolve_project(args.project)
    state = load_project_state(project)

    version_id = args.version or state.get("active_version")
    if not version_id:
        print("Error: No version specified and no active version set", file=sys.stderr)
        sys.exit(1)

    version_entry = get_version_entry(state, version_id)
    tag = version_entry.get("tag") if version_entry else None

    # Read session data from stdin or file
    if args.file:
        session_data = json.loads(Path(args.file).read_text())
    else:
        session_data = json.load(sys.stdin)

    path = save_coaching_session(project, version_id, session_data, tag)
    print(
        json.dumps(
            {
                "status": "saved",
                "session_id": session_data.get("id"),
                "path": str(path),
            }
        )
    )


def cmd_load(args):
    """Load session by ID."""
    project = resolve_project(args.project)
    state = load_project_state(project)

    version_id = args.version or state.get("active_version")
    if not version_id:
        print("Error: No version specified and no active version set", file=sys.stderr)
        sys.exit(1)

    version_entry = get_version_entry(state, version_id)
    tag = version_entry.get("tag") if version_entry else None

    try:
        session = load_coaching_session(project, version_id, args.id, tag)
        print(json.dumps(session, indent=2))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    """List sessions for version."""
    project = resolve_project(args.project)

    sessions = list_coaching_sessions(
        project,
        version_id=args.version,
    )

    if args.format == "json":
        print(json.dumps(sessions, indent=2))
    else:
        if not sessions:
            print("No coaching sessions found.")
            return

        print(f"{'ID':<30} {'Status':<10} {'Created':<25} Focus Areas")
        print("-" * 80)
        for s in sessions:
            focus = ", ".join(s.get("focus_areas", [])[:3]) or "-"
            created = s.get("created_at", "-")[:19] if s.get("created_at") else "-"
            print(f"{s['id']:<30} {s.get('status', '-'):<10} {created:<25} {focus}")


def cmd_resume(args):
    """Load latest incomplete session."""
    project = resolve_project(args.project)

    # Look for active or paused sessions
    for status in ["active", "paused"]:
        session = get_latest_session(
            project,
            version_id=args.version,
            status_filter=status,
        )
        if session:
            print(json.dumps(session, indent=2))
            return

    # No incomplete sessions
    print(
        json.dumps({"status": "no_session", "message": "No incomplete sessions found"})
    )


def main():
    parser = argparse.ArgumentParser(
        description="Manage coaching session persistence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "-p",
        "--project",
        help="Project name (uses active project if not specified)",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Version ID (uses active version if not specified)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # save command
    save_parser = subparsers.add_parser(
        "save", help="Save session to coaching directory"
    )
    save_parser.add_argument(
        "-f",
        "--file",
        help="Read session from file instead of stdin",
    )

    # load command
    load_parser = subparsers.add_parser("load", help="Load session by ID")
    load_parser.add_argument(
        "--id",
        required=True,
        help="Session ID to load",
    )

    # list command
    list_parser = subparsers.add_parser("list", help="List sessions for version")
    list_parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="Output format",
    )

    # resume command
    subparsers.add_parser("resume", help="Load latest incomplete session")

    args = parser.parse_args()

    commands = {
        "save": cmd_save,
        "load": cmd_load,
        "list": cmd_list,
        "resume": cmd_resume,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
