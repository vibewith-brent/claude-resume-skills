# State Management Reference

Technical reference for the resume-state version management system.

---

## Store Structure

```
.resume_versions/
├── config.json                 # Global configuration
└── projects/
    └── <project_name>/
        ├── project.json        # Project metadata and version history
        ├── sources/            # Original imported files
        │   └── original.pdf
        ├── versions/
        │   ├── v1/
        │   │   └── resume.yaml
        │   ├── v2_tailored/    # With tag
        │   │   └── resume.yaml
        │   └── v3/
        │       └── resume.yaml
        └── jobs/               # Cached job postings (optional)
            └── company_abc123.json
```

---

## Store Location

The store is located by searching in this order:

1. **Environment variable**: `RESUME_VERSIONS_PATH` (if set)
2. **Upward search**: Starting from current directory, search parent directories for `.resume_versions/`
3. **Global fallback**: `~/.resume_versions/`

This allows:
- Per-project stores (`.resume_versions/` in repo root)
- User-wide store (`~/.resume_versions/`)
- Custom locations via environment variable

---

## Configuration Files

### config.json (Schema v1.0.0)

Global configuration at store root.

```json
{
  "version": "1.0.0",
  "active_project": "john-doe"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version (currently "1.0.0") |
| `active_project` | string\|null | Currently active project name |

### project.json (Schema v1.0.0)

Per-project metadata.

```json
{
  "name": "john-doe",
  "schema_version": "1.0.0",
  "created_at": "2024-01-15T10:30:00.000000+00:00",
  "updated_at": "2024-01-15T14:22:00.000000+00:00",
  "active_version": "v2",
  "versions": [
    {
      "id": "v1",
      "tag": null,
      "notes": "Initial import",
      "created_at": "2024-01-15T10:30:00.000000+00:00",
      "source_file": "original.pdf"
    },
    {
      "id": "v2",
      "tag": "tailored",
      "notes": "Tailored for SRE role",
      "created_at": "2024-01-15T14:22:00.000000+00:00"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Project name |
| `schema_version` | string | Schema version (currently "1.0.0") |
| `created_at` | ISO datetime | Project creation timestamp |
| `updated_at` | ISO datetime | Last modification timestamp |
| `active_version` | string | Currently active version ID (e.g., "v2") |
| `versions` | array | Version history entries |

#### Version Entry

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Version ID (v1, v2, ...) |
| `tag` | string\|null | Optional short tag (e.g., "tailored", "sre") |
| `notes` | string\|null | Free-form description |
| `created_at` | ISO datetime | Version creation timestamp |
| `source_file` | string\|null | Original imported file (v1 only typically) |

---

## Version IDs

Version IDs follow the pattern `v<number>`:
- Valid: `v1`, `v2`, `v10`, `v999`
- Invalid: `1`, `V1`, `v1.0`, `version1`, `v-1`

The regex pattern: `^v(\d+)$`

Version directories can include a tag:
- `v1/` (no tag)
- `v2_tailored/` (with tag "tailored")

---

## Scripts Reference

All scripts support `--project`/`-p` flag. If not provided, uses the active project.

### Project Management

```bash
# Initialize new project
uv run resume-state/scripts/init_project.py <name>

# List all projects
uv run resume-state/scripts/list_versions.py  # Shows active project's versions

# Get active version's YAML path
uv run resume-state/scripts/get_active.py
```

### Version Management

```bash
# Import PDF/DOCX (creates v1 if new project)
uv run resume-state/scripts/import_resume.py <file.pdf> [--project name]

# Create new version from active
uv run resume-state/scripts/create_version.py [--tag tag] [--notes "..."]

# Switch active version
uv run resume-state/scripts/switch_version.py v2

# Export version to directory
uv run resume-state/scripts/export_version.py v1 /path/to/output/

# Compare two versions
uv run resume-state/scripts/diff_versions.py v1 v2
```

---

## Error Patterns

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "No project specified and no active project set" | No `-p` flag and no active project | Run `init_project.py` first or specify `-p` |
| "Project not found: X" | Project doesn't exist | Check name spelling, run `list_versions.py` |
| "Active version not found: vN" | Corrupt state | Check `project.json`, ensure version directory exists |
| "Invalid version ID format" | Malformed version ID | Use format: v1, v2, v3, ... |

### State Corruption Recovery

If state becomes corrupt:

1. **Backup**: Copy `.resume_versions/projects/<name>/` to safe location
2. **Check `project.json`**: Validate JSON syntax, ensure `active_version` exists in `versions`
3. **Check directories**: Verify each version in `versions/` has a `resume.yaml`
4. **Manual fix**: Edit `project.json` to remove invalid entries or add missing ones

---

## Python API

```python
from state_utils import (
    get_store_path,
    load_config,
    load_project_state,
    get_active_project,
    resolve_project,
    get_active_version_path,
    get_next_version_id,
    parse_version_id,
    validate_version_id,
)

# Get store location
store = get_store_path()  # Path to .resume_versions/

# Get active project
project = get_active_project()  # Returns str or None

# Resolve project (from arg or active)
project = resolve_project(args.project)  # Raises if none available

# Load project state
state = load_project_state("john-doe")

# Get active YAML path
yaml_path = get_active_version_path("john-doe")

# Get next version ID
next_id = get_next_version_id(state)  # "v3" if v2 is highest

# Validate version ID format
is_valid = validate_version_id("v1")  # True
is_valid = validate_version_id("1")   # False

# Parse version ID
num = parse_version_id("v5")  # Returns 5
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `RESUME_VERSIONS_PATH` | Override store location | `/custom/path/.resume_versions` |
| `RESUME_EXTRACTOR_PATH` | Path to extractor scripts | `/path/to/resume-extractor/scripts` |

---

## Integration with Other Skills

### resume-extractor

- `import_resume.py` calls extractor scripts to convert PDF/DOCX to YAML
- Extracted YAML is stored as version's `resume.yaml`

### resume-formatter

- Reads YAML from active version via `get_active_version_path()`
- `yaml_to_typst.py` + `compile_typst.py` generate PDF

### resume-optimizer

- Works on active version's YAML
- `validate_yaml.py` checks schema compliance
- After optimization, create new version to preserve history

### Workflow Pattern

```
init_project → import_resume (v1) → optimize → create_version (v2) → format PDF
                                         ↓
                              tailor for job → create_version (v3_tailored)
```

---

## Schema Validation

JSON schemas for validation are in `resume-state/schemas/`:

- `config_schema.json` — Validates `config.json`
- `project_schema.json` — Validates `project.json`

```bash
# Validate with any JSON Schema tool
npx ajv validate -s schemas/project_schema.json -d project.json
```
