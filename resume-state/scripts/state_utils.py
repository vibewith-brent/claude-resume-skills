"""Shared utilities for resume state management."""

import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Regex pattern for valid version IDs (v1, v2, v3, ...)
VERSION_ID_PATTERN = re.compile(r"^v(\d+)$")

STORE_DIR = ".resume_versions"
CONFIG_FILE = "config.json"
PROJECT_FILE = "project.json"

CONFIG_SCHEMA_VERSION = "1.0.0"
PROJECT_SCHEMA_VERSION = "1.0.0"


def get_store_path(start_path: Optional[Path] = None) -> Path:
    """Find .resume_versions store by searching upward within git repo, then global fallback.

    Search order:
    1. RESUME_VERSIONS_PATH environment variable
    2. If in git repo: search upward within repo boundaries for .resume_versions
       - If found, use it
       - If not found, use repo root .resume_versions
    3. Otherwise: search upward from current directory for .resume_versions
    4. Fall back to global ~/.resume_versions

    Returns existing store path, or appropriate path for creation.
    """
    # Check environment variable
    env_path = os.environ.get("RESUME_VERSIONS_PATH")
    if env_path:
        return Path(env_path).expanduser()

    # Start from current directory
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()
    git_root = None

    # First pass: find git root
    temp = current
    while True:
        if (temp / ".git").exists():
            git_root = temp
            break
        parent = temp.parent
        if parent == temp:
            break
        temp = parent

    # If in a git repo, search only within repo boundaries
    if git_root:
        current = start_path.resolve()
        while True:
            candidate = current / STORE_DIR
            if candidate.exists() and candidate.is_dir():
                return candidate

            # Stop at git root
            if current == git_root:
                return git_root / STORE_DIR

            current = current.parent
    else:
        # Not in git repo: search upward normally
        while True:
            candidate = current / STORE_DIR
            if candidate.exists() and candidate.is_dir():
                return candidate

            # Check if we've reached root
            parent = current.parent
            if parent == current:
                break
            current = parent

        # Fall back to global location
        return Path.home() / STORE_DIR


def ensure_store_exists(store_path: Optional[Path] = None) -> Path:
    """Ensure the store directory exists."""
    if store_path is None:
        store_path = get_store_path()
    store_path.mkdir(parents=True, exist_ok=True)
    return store_path


def load_config(store_path: Optional[Path] = None) -> dict:
    """Load global config or return default."""
    if store_path is None:
        store_path = get_store_path()
    config_path = store_path / CONFIG_FILE
    if config_path.exists():
        return json.loads(config_path.read_text())
    return {"version": CONFIG_SCHEMA_VERSION, "active_project": None}


def save_config(config: dict, store_path: Optional[Path] = None) -> None:
    """Save global config."""
    if store_path is None:
        store_path = get_store_path()
    ensure_store_exists(store_path)
    config_path = store_path / CONFIG_FILE
    fd, tmp_path = tempfile.mkstemp(dir=store_path, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(config, f, indent=2)
        Path(tmp_path).replace(config_path)
    except:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def get_project_path(project: str, store_path: Optional[Path] = None) -> Path:
    """Get path to a project directory."""
    if store_path is None:
        store_path = get_store_path()
    return store_path / "projects" / project


def list_projects(store_path: Optional[Path] = None) -> list[str]:
    """List all project names."""
    if store_path is None:
        store_path = get_store_path()
    projects_dir = store_path / "projects"
    if not projects_dir.exists():
        return []
    return sorted([p.name for p in projects_dir.iterdir() if p.is_dir()])


def load_project_state(project: str, store_path: Optional[Path] = None) -> dict:
    """Load project state from project.json."""
    project_path = get_project_path(project, store_path)
    state_file = project_path / PROJECT_FILE
    if not state_file.exists():
        raise FileNotFoundError(f"Project not found: {project}")
    return json.loads(state_file.read_text())


def save_project_state(
    project: str, state: dict, store_path: Optional[Path] = None
) -> None:
    """Save project state to project.json."""
    project_path = get_project_path(project, store_path)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_file = project_path / PROJECT_FILE
    fd, tmp_path = tempfile.mkstemp(dir=project_path, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(state, f, indent=2)
        Path(tmp_path).replace(state_file)
    except:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def get_active_project(store_path: Optional[Path] = None) -> Optional[str]:
    """Get the currently active project name."""
    config = load_config(store_path)
    return config.get("active_project")


def set_active_project(project: str, store_path: Optional[Path] = None) -> None:
    """Set the active project."""
    config = load_config(store_path)
    config["active_project"] = project
    save_config(config, store_path)


def resolve_project(project: Optional[str], store_path: Optional[Path] = None) -> str:
    """Resolve project name from argument or active project."""
    if project:
        return project
    active = get_active_project(store_path)
    if not active:
        raise ValueError("No project specified and no active project set")
    return active


def parse_version_id(version_id: str) -> int:
    """Parse a version ID and return its numeric component.

    Args:
        version_id: Version ID string (e.g., 'v1', 'v2')

    Returns:
        The numeric part of the version ID

    Raises:
        ValueError: If the version ID format is invalid
    """
    match = VERSION_ID_PATTERN.match(version_id)
    if not match:
        raise ValueError(
            f"Invalid version ID format: '{version_id}'. "
            f"Expected format: v1, v2, v3, ..."
        )
    return int(match.group(1))


def validate_version_id(version_id: str) -> bool:
    """Check if a version ID is valid.

    Args:
        version_id: Version ID string to validate

    Returns:
        True if valid, False otherwise
    """
    return VERSION_ID_PATTERN.match(version_id) is not None


def get_next_version_id(state: dict) -> str:
    """Get the next version ID (v1, v2, v3, ...).

    Args:
        state: Project state dictionary

    Returns:
        Next version ID string

    Raises:
        ValueError: If existing version IDs have invalid format
    """
    versions = state.get("versions", [])
    if not versions:
        return "v1"

    max_num = 0
    for v in versions:
        vid = v.get("id", "")
        try:
            num = parse_version_id(vid)
            max_num = max(max_num, num)
        except ValueError:
            # Skip malformed version IDs but log warning
            import sys

            print(f"Warning: Skipping malformed version ID: {vid}", file=sys.stderr)

    return f"v{max_num + 1}"


def get_version_entry(state: dict, version_id: str) -> Optional[dict]:
    """Get version entry by ID."""
    for v in state.get("versions", []):
        if v["id"] == version_id:
            return v
    return None


def get_version_dir_name(version_id: str, tag: Optional[str] = None) -> str:
    """Get directory name for a version."""
    if tag:
        return f"{version_id}_{tag}"
    return version_id


def get_version_path(
    project: str,
    version_id: str,
    tag: Optional[str] = None,
    store_path: Optional[Path] = None,
) -> Path:
    """Get path to a version directory."""
    project_path = get_project_path(project, store_path)
    dirname = get_version_dir_name(version_id, tag)
    return project_path / "versions" / dirname


def get_active_version_path(project: str, store_path: Optional[Path] = None) -> Path:
    """Get path to the active version's YAML file."""
    state = load_project_state(project, store_path)
    active_id = state.get("active_version")
    if not active_id:
        raise ValueError(f"No active version set for project: {project}")
    version = get_version_entry(state, active_id)
    if not version:
        raise ValueError(f"Active version not found: {active_id}")
    version_dir = get_version_path(project, active_id, version.get("tag"), store_path)
    return version_dir / "resume.yaml"


def copy_file(src: Path, dst: Path) -> None:
    """Copy a file, creating parent directories if needed."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def now_iso() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


# Coaching session constants
COACHING_DIR = "coaching"
COACHING_SESSION_SCHEMA_VERSION = "1.0.0"


def get_coaching_dir(
    project: str,
    version_id: str,
    tag: Optional[str] = None,
    store_path: Optional[Path] = None,
) -> Path:
    """Get path to coaching directory for a version.

    Args:
        project: Project name
        version_id: Version ID (e.g., 'v1', 'v2')
        tag: Optional version tag
        store_path: Optional store path override

    Returns:
        Path to the coaching directory within the version
    """
    version_path = get_version_path(project, version_id, tag, store_path)
    return version_path / COACHING_DIR


def generate_session_id() -> str:
    """Generate a unique session ID with timestamp."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"session_{timestamp}"


def save_coaching_session(
    project: str,
    version_id: str,
    session: dict,
    tag: Optional[str] = None,
    store_path: Optional[Path] = None,
) -> Path:
    """Save a coaching session to the version's coaching directory.

    Args:
        project: Project name
        version_id: Version ID (e.g., 'v1', 'v2')
        session: Session data dictionary
        tag: Optional version tag
        store_path: Optional store path override

    Returns:
        Path to the saved session file
    """
    coaching_dir = get_coaching_dir(project, version_id, tag, store_path)
    coaching_dir.mkdir(parents=True, exist_ok=True)

    # Ensure session has required fields
    if "id" not in session:
        session["id"] = generate_session_id()
    if "version" not in session:
        session["version"] = COACHING_SESSION_SCHEMA_VERSION
    if "created_at" not in session:
        session["created_at"] = now_iso()
    session["updated_at"] = now_iso()

    session_file = coaching_dir / f"{session['id']}.json"

    # Atomic write
    fd, tmp_path = tempfile.mkstemp(dir=coaching_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(session, f, indent=2)
        Path(tmp_path).replace(session_file)
    except:
        Path(tmp_path).unlink(missing_ok=True)
        raise

    return session_file


def load_coaching_session(
    project: str,
    version_id: str,
    session_id: str,
    tag: Optional[str] = None,
    store_path: Optional[Path] = None,
) -> dict:
    """Load a specific coaching session by ID.

    Args:
        project: Project name
        version_id: Version ID (e.g., 'v1', 'v2')
        session_id: Session ID to load
        tag: Optional version tag
        store_path: Optional store path override

    Returns:
        Session data dictionary

    Raises:
        FileNotFoundError: If session file does not exist
    """
    coaching_dir = get_coaching_dir(project, version_id, tag, store_path)
    session_file = coaching_dir / f"{session_id}.json"

    if not session_file.exists():
        raise FileNotFoundError(f"Coaching session not found: {session_id}")

    return json.loads(session_file.read_text())


def list_coaching_sessions(
    project: str,
    version_id: Optional[str] = None,
    tag: Optional[str] = None,
    store_path: Optional[Path] = None,
) -> list[dict]:
    """List all coaching sessions for a version.

    Args:
        project: Project name
        version_id: Version ID (e.g., 'v1', 'v2'). If None, uses active version.
        tag: Optional version tag
        store_path: Optional store path override

    Returns:
        List of session metadata dicts (id, created_at, status, focus areas)
    """
    # Resolve version if not provided
    if version_id is None:
        state = load_project_state(project, store_path)
        version_id = state.get("active_version")
        if not version_id:
            return []
        version_entry = get_version_entry(state, version_id)
        tag = version_entry.get("tag") if version_entry else None

    coaching_dir = get_coaching_dir(project, version_id, tag, store_path)
    if not coaching_dir.exists():
        return []

    sessions = []
    for session_file in sorted(coaching_dir.glob("session_*.json")):
        try:
            data = json.loads(session_file.read_text())
            sessions.append(
                {
                    "id": data.get("id", session_file.stem),
                    "created_at": data.get("created_at"),
                    "updated_at": data.get("updated_at"),
                    "status": data.get("status", "unknown"),
                    "focus_areas": data.get("focus", {}).get("areas", []),
                }
            )
        except (json.JSONDecodeError, KeyError):
            # Skip malformed session files
            continue

    return sessions


def get_latest_session(
    project: str,
    version_id: Optional[str] = None,
    tag: Optional[str] = None,
    store_path: Optional[Path] = None,
    status_filter: Optional[str] = None,
) -> Optional[dict]:
    """Get the most recent coaching session.

    Args:
        project: Project name
        version_id: Version ID. If None, uses active version.
        tag: Optional version tag
        store_path: Optional store path override
        status_filter: Optional status to filter by (e.g., 'active', 'paused')

    Returns:
        Full session data dict, or None if no sessions exist
    """
    # Resolve version if not provided
    if version_id is None:
        state = load_project_state(project, store_path)
        version_id = state.get("active_version")
        if not version_id:
            return None
        version_entry = get_version_entry(state, version_id)
        tag = version_entry.get("tag") if version_entry else None

    coaching_dir = get_coaching_dir(project, version_id, tag, store_path)
    if not coaching_dir.exists():
        return None

    # Find most recent session file
    session_files = sorted(coaching_dir.glob("session_*.json"), reverse=True)

    for session_file in session_files:
        try:
            data = json.loads(session_file.read_text())
            if status_filter is None or data.get("status") == status_filter:
                return data
        except (json.JSONDecodeError, KeyError):
            continue

    return None
