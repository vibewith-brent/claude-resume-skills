# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Resume management skills suite for Claude Code: extract PDF/DOCX → optimize content → format to PDF → review and iterate. Six skills auto-load from `.claude/skills/` and are invoked via natural language.

## Workflow Priority

**IMPORTANT**: When a user provides a resume (PDF/DOCX) or starts working on a resume:
1. **First**: Initialize a project with `resume-state` if none exists
2. **Then**: Import the resume file to track the original
3. **Then**: Use other skills (extract, optimize, format)
4. **Before changes**: Create a new version to preserve history

This ensures all resume work is tracked and versioned.

## Common Commands

Run `uv sync` first if dependencies aren't installed.

### Testing Skills

```bash
# Verify all skills are loaded (should list 6 skills)
ls -la .claude/skills/

# Test extraction
uv run .claude/skills/resume-extractor/scripts/extract_pdf.py test.pdf

# Validate YAML structure
uv run .claude/skills/resume-optimizer/scripts/validate_yaml.py resume.yaml

# Test PDF generation pipeline
uv run .claude/skills/resume-formatter/scripts/yaml_to_latex.py resume.yaml modern -o test.tex
uv run .claude/skills/resume-formatter/scripts/compile_latex.py test.tex -o test.pdf
```

### Version Management (USE FIRST)
```bash
# Initialize a project (do this first when starting)
uv run .claude/skills/resume-state/scripts/init_project.py ml_engineer

# Import resume (copies source, extracts text) - do this before extraction
uv run .claude/skills/resume-state/scripts/import_resume.py resume.pdf

# Create new version before making changes
uv run .claude/skills/resume-state/scripts/create_version.py --tag google --notes "Tailored for Google"

# List versions
uv run .claude/skills/resume-state/scripts/list_versions.py

# Switch active version
uv run .claude/skills/resume-state/scripts/switch_version.py v1

# Get active YAML path (use this path for other commands)
uv run .claude/skills/resume-state/scripts/get_active.py

# Export version to directory
uv run .claude/skills/resume-state/scripts/export_version.py v2 ~/Desktop/applications/

# Compare versions
uv run .claude/skills/resume-state/scripts/diff_versions.py v1 v2
```

### PDF Extraction
```bash
uv run .claude/skills/resume-extractor/scripts/extract_pdf.py resume.pdf
```

### DOCX Extraction
```bash
uv run .claude/skills/resume-extractor/scripts/extract_docx.py resume.docx
```

### YAML Validation
```bash
uv run .claude/skills/resume-optimizer/scripts/validate_yaml.py resume.yaml
```

### YAML → LaTeX → PDF (two-step)
```bash
# Step 1: Convert to LaTeX (templates: modern, classic, academic, creative)
uv run .claude/skills/resume-formatter/scripts/yaml_to_latex.py resume.yaml modern -o resume.tex

# Step 2: Compile to PDF (runs pdflatex twice, cleans aux files)
uv run .claude/skills/resume-formatter/scripts/compile_latex.py resume.tex -o resume.pdf
```

### One-liner PDF generation
```bash
uv run .claude/skills/resume-formatter/scripts/yaml_to_latex.py resume.yaml modern -o resume.tex && \
uv run .claude/skills/resume-formatter/scripts/compile_latex.py resume.tex -o resume.pdf
```

### Fetch Job Posting
```bash
uv run .claude/skills/resume-optimizer/scripts/fetch_job_posting.py "<url>" --output job.txt
```

## Architecture

```
resume-*/                 # Canonical skill sources
├── resume-extractor/     # PDF/DOCX → text extraction
├── resume-optimizer/     # Content improvement, ATS, tailoring
├── resume-formatter/     # YAML → LaTeX → PDF
│   └── assets/templates/latex/  # Jinja2 templates (.tex.j2)
├── resume-reviewer/      # Visual QA for compiled PDFs
├── resume-template-maker/ # Create custom LaTeX templates
└── resume-state/         # Version and project management

.claude/skills/           # Symlinks to resume-*/ (auto-loaded by Claude Code)

.resume_versions/         # Version store (created on init)
├── config.json           # Active project setting
└── projects/<name>/
    ├── project.json      # Version history
    ├── sources/          # Original PDFs/DOCXs
    ├── versions/v1/      # Version snapshots
    └── jobs/             # Cached job postings
```

Single source of truth: edit `resume-*/` directories; `.claude/skills/` contains symlinks.

### Skill Workflow

```
[State] → [Extract] → [Optimize] → [Format] → [Review] ←→ [Template Maker]
   ↓          ↓            ↓            ↓          ↓              ↓
Project    PDF/DOCX      YAML       YAML→PDF   Visual QA    Custom .tex.j2
Versions
```

- **resume-state**: Manages projects and versions; tracks YAML iterations and original sources
- **resume-reviewer**: Evaluates compiled PDFs against visual QA checklist, provides structured feedback
- **resume-template-maker**: Creates custom templates using design vectors (typography, layout, whitespace, color)

## Key Files

- **State Schema**: `.resume_versions/projects/<name>/project.json` — version history and metadata
- **Global Config**: `.resume_versions/config.json` — active project setting
- **State Utils**: `resume-state/scripts/state_utils.py` — shared utilities for version management (schema v1.0.0)
- **YAML Schema**: `.claude/skills/resume-extractor/references/resume_schema.yaml` — canonical structure for resume data
- **LaTeX Templates**: `.claude/skills/resume-formatter/assets/templates/latex/*.tex.j2` — Jinja2 templates with `latex_escape` filter
- **Visual QA Checklist**: `.claude/skills/resume-reviewer/references/visual_qa_checklist.md` — structured evaluation criteria
- **Design Vectors**: `.claude/skills/resume-template-maker/references/design_vectors.md` — typography, layout, whitespace, color guidance
- **Industry Themes**: `.claude/skills/resume-template-maker/references/industry_themes.md` — industry-specific design recommendations
- **Reference Docs**: `references/` dirs contain ATS guidelines, action verbs, impact patterns, examples

## LaTeX Dependency

Requires MacTeX:
```bash
brew install --cask mactex
# or minimal: brew install --cask mactex-no-gui
```

If `pdflatex` not found after install:
```bash
export PATH="/Library/TeX/texbin:$PATH"
```

## YAML Resume Structure

Required sections: `contact`, `summary`, `experience`, `skills`, `education`

Optional: `certifications`, `projects`, `publications`, `awards`, `languages`, `volunteer`

Experience uses nested positions to handle multiple roles at same company:
```yaml
experience:
  - company: "Company Name"
    positions:
      - title: "Role"
        dates: "Jan 2020 - Present"
        achievements:
          - "Bullet starting with action verb"
```

## Template Selection

| Template | Use Case |
|----------|----------|
| modern | Tech, startups, general |
| classic | Finance, law, consulting |
| academic | Research, academia |
| creative | Design, marketing, UX |

## Template Creation Workflow

For custom templates, the template-maker and reviewer work in an iteration loop:

1. **Design** — Define typography, layout, whitespace, color based on industry theme
2. **Create** — Generate `.tex.j2` template in `assets/templates/latex/`
3. **Compile** — Convert to PDF using existing formatter scripts
4. **Review** — Evaluate with resume-reviewer skill
5. **Adjust** — Fix issues identified by reviewer
6. **Repeat** — Continue until all visual QA checks pass

Design vectors prevent generic "AI resume" patterns by providing mid-altitude guidance on fonts, spacing, and color choices tailored to industry expectations.

## Versioned Workflow

For multi-role job searches, use state management to track iterations:

```bash
# 1. Initialize project for target role
uv run .claude/skills/resume-state/scripts/init_project.py ml_engineer

# 2. Import existing resume
uv run .claude/skills/resume-state/scripts/import_resume.py current_resume.pdf

# 3. Parse extracted text into YAML (edit versions/v1/resume.yaml)

# 4. Create optimized version
uv run .claude/skills/resume-state/scripts/create_version.py --tag optimized --notes "Added metrics"

# 5. Work with active version using get_active.py
YAML=$(uv run .claude/skills/resume-state/scripts/get_active.py)
uv run .claude/skills/resume-formatter/scripts/yaml_to_latex.py "$YAML" modern -o "${YAML%.yaml}.tex"
uv run .claude/skills/resume-formatter/scripts/compile_latex.py "${YAML%.yaml}.tex"

# 6. Create role-specific versions
uv run .claude/skills/resume-state/scripts/create_version.py --tag google --notes "Tailored for Google SWE"

# 7. Export for submission
uv run .claude/skills/resume-state/scripts/export_version.py v3 ~/Desktop/applications/google/
```

Version history is preserved in `.resume_versions/projects/<name>/project.json`.

## Development Notes

### Python Environment

- Managed with `uv` (auto-installed by Claude Code)
- Requires Python >=3.10
- Dependencies in `pyproject.toml`: pdfplumber, python-docx, pyyaml, jinja2, requests, beautifulsoup4

### Skill Architecture

- **Source of Truth**: Edit `resume-*/` directories directly
- **Symlinks**: `.claude/skills/` contains symlinks to `resume-*/` for auto-loading
- **Scripts**: All utility scripts use `uv run` and are callable from skill directories
- **State Management**: Centralized in `state_utils.py` with functions for config/project loading, version resolution, path handling

### Version Store Structure

```
.resume_versions/
├── config.json              # {"version": "1.0.0", "active_project": "ml_engineer"}
└── projects/<name>/
    ├── project.json         # {"version": "1.0.0", "active_version": "v2", "versions": [...]}
    ├── sources/             # Immutable original files
    ├── versions/v1/         # YAML snapshots + artifacts
    └── jobs/                # Cached job postings
```

### Store Location Resolution

Scripts find `.resume_versions` using this search order:

1. **Environment variable**: `RESUME_VERSIONS_PATH` (if set)
2. **Upward search**: From current directory to root (like `.git`)
3. **Global fallback**: `~/.resume_versions`

This enables:
- Running commands from any subdirectory within the project
- Using a global store for all resume projects
- Custom location via `export RESUME_VERSIONS_PATH=/path/to/store`

### Adding New Scripts

When adding scripts to `resume-state/scripts/`:
1. Import from `state_utils.py` for consistency
2. Use `resolve_project()` to handle --project/-p flags
3. Follow pattern: load state → modify → save state
4. Update `resume-state/SKILL.md` commands reference
