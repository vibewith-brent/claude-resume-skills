"""Shared utilities for resume state management."""

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

STORE_DIR = ".resume_versions"
CONFIG_FILE = "config.json"
PROJECT_FILE = "project.json"

CONFIG_SCHEMA_VERSION = "1.0.0"
PROJECT_SCHEMA_VERSION = "1.0.0"


def get_store_path(start_path: Optional[Path] = None) -> Path:
    """Find or create the .resume_versions store in the project root."""
    if start_path is None:
        start_path = Path.cwd()
    return start_path / STORE_DIR


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
    config_path.write_text(json.dumps(config, indent=2))


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


def save_project_state(project: str, state: dict, store_path: Optional[Path] = None) -> None:
    """Save project state to project.json."""
    project_path = get_project_path(project, store_path)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_file = project_path / PROJECT_FILE
    state_file.write_text(json.dumps(state, indent=2))


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


def get_next_version_id(state: dict) -> str:
    """Get the next version ID (v1, v2, v3, ...)."""
    versions = state.get("versions", [])
    if not versions:
        return "v1"
    max_num = max(int(v["id"][1:]) for v in versions)
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
