---
name: resume-state
description: Use first when working with resumes. Initialize projects, import PDFs/DOCXs, create versions before changes. Manages multiple resume variants for different roles.
---

# Resume State Manager

## Overview

Manage resume versions across multiple projects/target roles. Each version preserves the complete YAML and generated artifacts, enabling rollback, A/B comparison, and organized multi-role job search workflows.

## Quick Start

### Initialize a Project

```bash
uv run scripts/init_project.py ml_engineer
```

### Import Existing Resume

```bash
uv run scripts/import_resume.py resume.pdf --project ml_engineer
```

Creates v1 with:
- Copied source PDF in `sources/`
- Extracted text in `versions/v1/extracted_text.txt`
- Placeholder YAML in `versions/v1/resume.yaml`

### Create New Version

```bash
uv run scripts/create_version.py --tag google --notes "Tailored for Google SWE"
```

Copies YAML from active version to new v2 (or v3, etc.).

### List Versions

```bash
uv run scripts/list_versions.py
```

Output:
```
ml_engineer versions:

  v1     [import]  2025-11-30  Imported from resume.pdf
* v2     [derived] 2025-11-30  google - Tailored for Google SWE
```

### Switch Active Version

```bash
uv run scripts/switch_version.py v1
```

### Get Active YAML Path

```bash
uv run scripts/get_active.py
# .resume_versions/projects/ml_engineer/versions/v2_google/resume.yaml
```

### Export for Submission

```bash
uv run scripts/export_version.py v2 ~/Desktop/applications/google/ --format pdf
```

### Compare Versions

```bash
uv run scripts/diff_versions.py v1 v2
```

## Storage Structure

```
.resume_versions/
├── config.json                    # Active project setting
└── projects/
    └── ml_engineer/
        ├── project.json           # Version history + metadata
        ├── sources/               # Original PDFs/DOCXs (immutable)
        ├── versions/
        │   ├── v1/
        │   │   ├── resume.yaml
        │   │   └── extracted_text.txt
        │   └── v2_google/
        │       ├── resume.yaml
        │       ├── resume.typ
        │       └── resume.pdf
        └── jobs/                  # Cached job postings
```

## Store Location

Scripts find `.resume_versions` using this search order:

1. **Environment variable**: `RESUME_VERSIONS_PATH` (if set)
2. **Upward search**: From current directory upward to root
3. **Global fallback**: `~/.resume_versions`

This allows:
- Running commands from any subdirectory of your project
- Using a global store for all projects (`~/.resume_versions`)
- Overriding location with `export RESUME_VERSIONS_PATH=/custom/path`

## Workflow Integration

State scripts provide path resolution for other skills:

```bash
# Get active YAML and pipe to formatter
YAML=$(uv run scripts/get_active.py)
uv run ../resume-formatter/scripts/yaml_to_typst.py "$YAML" executive -o "${YAML%.yaml}.typ"
uv run ../resume-formatter/scripts/compile_typst.py "${YAML%.yaml}.typ"
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `init_project.py <name>` | Create new project |
| `import_resume.py <file>` | Import PDF/DOCX as new version |
| `create_version.py` | Branch new version from active |
| `list_versions.py` | Show version history |
| `switch_version.py <id>` | Change active version |
| `get_active.py` | Print active YAML path |
| `export_version.py <id> <dir>` | Copy files to target |
| `diff_versions.py <a> <b>` | Compare YAML changes |

## Common Options

- `--project, -p`: Specify project (default: active project)
- `--tag, -t`: Version tag suffix (e.g., `google`, `shortened`)
- `--notes, -n`: Description of changes
