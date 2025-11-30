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

## Quick Reference

Run `uv sync` first if dependencies aren't installed.

```bash
# Version management (USE FIRST)
uv run .claude/skills/resume-state/scripts/init_project.py <project_name>
uv run .claude/skills/resume-state/scripts/import_resume.py <file.pdf|docx>
uv run .claude/skills/resume-state/scripts/create_version.py --tag <tag> --notes "description"
uv run .claude/skills/resume-state/scripts/list_versions.py
uv run .claude/skills/resume-state/scripts/switch_version.py <v1|v2|...>
uv run .claude/skills/resume-state/scripts/get_active.py  # prints active YAML path

# Extraction
uv run .claude/skills/resume-extractor/scripts/extract_pdf.py <file.pdf>
uv run .claude/skills/resume-extractor/scripts/extract_docx.py <file.docx>

# Validation
uv run .claude/skills/resume-optimizer/scripts/validate_yaml.py <resume.yaml>

# PDF generation (templates: modern, modern-tech, classic, academic, creative)
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py <resume.yaml> <template> -o <out.typ>
uv run .claude/skills/resume-formatter/scripts/compile_typst.py <file.typ> -o <out.pdf>

# One-liner PDF
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py resume.yaml modern -o resume.typ && \
uv run .claude/skills/resume-formatter/scripts/compile_typst.py resume.typ -o resume.pdf

# Job tailoring
uv run .claude/skills/resume-optimizer/scripts/fetch_job_posting.py "<url>" --output job.txt

# Export and compare
uv run .claude/skills/resume-state/scripts/export_version.py <v1> <output_dir>/
uv run .claude/skills/resume-state/scripts/diff_versions.py <v1> <v2>
```

## Architecture

```
resume-*/                 # Canonical skill sources
├── resume-extractor/     # PDF/DOCX → text extraction
├── resume-optimizer/     # Content improvement, ATS, tailoring
├── resume-formatter/     # YAML → Typst → PDF
│   └── assets/templates/typst/  # Jinja2 templates (.typ.j2)
├── resume-reviewer/      # Visual QA for compiled PDFs
├── resume-template-maker/ # Create custom Typst templates
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
Project    PDF/DOCX      YAML       YAML→PDF   Visual QA    Custom .typ.j2
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
- **Typst Templates**: `.claude/skills/resume-formatter/assets/templates/typst/*.typ.j2` — Jinja2 templates with `typst_escape` filter
- **Visual QA Checklist**: `.claude/skills/resume-reviewer/references/visual_qa_checklist.md` — structured evaluation criteria
- **Design Vectors**: `.claude/skills/resume-template-maker/references/design_vectors.md` — typography, layout, whitespace, color guidance
- **Industry Themes**: `.claude/skills/resume-template-maker/references/industry_themes.md` — industry-specific design recommendations
- **Reference Docs**: `references/` dirs contain ATS guidelines, action verbs, impact patterns, examples

## Typst Dependency

Requires Typst (~20MB, much lighter than MacTeX):
```bash
brew install typst
```

Verify installation:
```bash
typst --version
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
| modern-tech | Tech with teal accents, side-line headers |
| classic | Finance, law, consulting |
| academic | Research, academia |
| creative | Design, marketing, UX |

## Template Creation Workflow

For custom templates, the template-maker and reviewer work in an iteration loop:

1. **Design** — Define typography, layout, whitespace, color based on industry theme
2. **Create** — Generate `.typ.j2` template in `assets/templates/typst/`
3. **Compile** — Convert to PDF using existing formatter scripts
4. **Review** — Evaluate with resume-reviewer skill
5. **Adjust** — Fix issues identified by reviewer
6. **Repeat** — Continue until all visual QA checks pass

Design vectors prevent generic "AI resume" patterns by providing mid-altitude guidance on fonts, spacing, and color choices tailored to industry expectations.

## Versioned Workflow Example

```bash
# 1. Initialize → 2. Import → 3. Edit YAML → 4. Create versions → 5. Generate PDF → 6. Export
uv run .claude/skills/resume-state/scripts/init_project.py ml_engineer
uv run .claude/skills/resume-state/scripts/import_resume.py current_resume.pdf
# Edit versions/v1/resume.yaml with content from extracted_text.txt
uv run .claude/skills/resume-state/scripts/create_version.py --tag google --notes "Tailored for Google"

YAML=$(uv run .claude/skills/resume-state/scripts/get_active.py)
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py "$YAML" modern -o "${YAML%.yaml}.typ"
uv run .claude/skills/resume-formatter/scripts/compile_typst.py "${YAML%.yaml}.typ"

uv run .claude/skills/resume-state/scripts/export_version.py v2 ~/Desktop/applications/google/
```

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

### Packaging Skills for Distribution

Package skills as ZIP files per Anthropic's format:
```bash
uv run scripts/package_skills.py           # All skills → dist/*.zip
uv run scripts/package_skills.py resume-formatter  # Single skill
```

ZIP structure: `skill-name.zip` containing `skill-name/` folder at root.
