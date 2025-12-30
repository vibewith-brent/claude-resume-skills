# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Resume management skills suite for Claude Code: extract PDF/DOCX → optimize content → format to PDF → review and iterate. Seven skills distributed via plugin marketplace.

## Installation

Install skills via plugin marketplace:

```bash
# Add this repo as a plugin marketplace
/plugin marketplace add https://github.com/vibewith-brent/claude-resume-skills

# Install the resume skills plugin
/plugin install resume-skills@resume-helper-skills

# Or update if already installed
/plugin update resume-skills@resume-helper-skills
```

After installation, skills are invoked via natural language (e.g., "extract my resume", "optimize for this job posting", "format as PDF").

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
uv run resume-state/scripts/init_project.py <project_name>
uv run resume-state/scripts/import_resume.py <file.pdf|docx>
uv run resume-state/scripts/create_version.py --tag <tag> --notes "description"
uv run resume-state/scripts/list_versions.py
uv run resume-state/scripts/switch_version.py <v1|v2|...>
uv run resume-state/scripts/get_active.py  # prints active YAML path

# Extraction
uv run resume-extractor/scripts/extract_pdf.py <file.pdf>
uv run resume-extractor/scripts/extract_docx.py <file.docx>

# Validation
uv run resume-optimizer/scripts/validate_yaml.py <resume.yaml>

# PDF generation (templates: executive, tech-modern, modern-dense, compact, minimal)
uv run resume-formatter/scripts/yaml_to_typst.py <resume.yaml> <template> -o <out.typ>
uv run resume-formatter/scripts/yaml_to_typst.py <resume.yaml> <template> --skip-validation -o <out.typ>  # legacy YAML
uv run resume-formatter/scripts/compile_typst.py <file.typ> -o <out.pdf>

# One-liner PDF
uv run resume-formatter/scripts/yaml_to_typst.py resume.yaml executive -o resume.typ && \
uv run resume-formatter/scripts/compile_typst.py resume.typ -o resume.pdf

# Job tailoring
uv run resume-optimizer/scripts/fetch_job_posting.py "<url>" --output job.txt

# Export and compare
uv run resume-state/scripts/export_version.py <v1> <output_dir>/
uv run resume-state/scripts/diff_versions.py <v1> <v2>

# Testing
uv sync --extra dev           # Install test dependencies
uv run pytest tests/ -v       # Run tests
```

## Architecture

```
resume-*/                 # Skill directories (plugin source)
├── resume-extractor/     # PDF/DOCX → text extraction
├── resume-optimizer/     # Content improvement, ATS, tailoring
├── resume-formatter/     # YAML → Typst → PDF
│   └── assets/templates/typst/  # Jinja2 templates (.typ.j2)
├── resume-reviewer/      # Visual QA for compiled PDFs
├── resume-template-maker/ # Create custom Typst templates
├── resume-coverletter/   # Generate matching cover letters
└── resume-state/         # Version and project management

.claude-plugin/           # Plugin marketplace configuration
└── marketplace.json      # Defines plugin entry points

.resume_versions/         # Version store (created on init)
├── config.json           # Active project setting
└── projects/<name>/
    ├── project.json      # Version history
    ├── sources/          # Original PDFs/DOCXs
    ├── versions/v1/      # Version snapshots
    └── jobs/             # Cached job postings
```

### Skill Workflow

```
[State] → [Extract] → [Optimize] → [Format] → [Review] ←→ [Template Maker]
   ↓          ↓            ↓            ↓          ↓              ↓
Project    PDF/DOCX      YAML       YAML→PDF   Visual QA    Custom .typ.j2
                                       ↓
                               [Cover Letter]
```

- **resume-state**: Manages projects and versions; tracks YAML iterations and original sources
- **resume-reviewer**: Generates review templates; Claude views the PDF and fills in the visual QA checklist
- **resume-template-maker**: Creates custom templates using design vectors (typography, layout, whitespace, color)
- **resume-coverletter**: Generates cover letters matching resume template styling

## Key Files

- **State Schema**: `.resume_versions/projects/<name>/project.json` — version history and metadata
- **Global Config**: `.resume_versions/config.json` — active project setting
- **State Utils**: `resume-state/scripts/state_utils.py` — shared utilities for version management (schema v1.0.0)
- **YAML Schema**: `resume-extractor/references/resume_schema.yaml` — canonical structure for resume data
- **Typst Templates**: `resume-formatter/assets/templates/typst/*.typ.j2` — Jinja2 templates with `typst_escape` filter
- **Visual QA Checklist**: `resume-reviewer/references/visual_qa_checklist.md` — structured evaluation criteria
- **Design Vectors**: `resume-template-maker/references/design_vectors.md` — typography, layout, whitespace, color guidance
- **Industry Themes**: `resume-template-maker/references/industry_themes.md` — industry-specific design recommendations
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

Required: `contact`. Recommended: `summary`, `experience`, `skills`, `education`

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
| executive | Professional, clean hierarchy, navy accents (default) |
| tech-modern | Modern/creative with deep lavender palette, pill-style skills, Carlito font, single-page optimized |
| modern-dense | Maximum density with categorized inline skills, strategic spacing, ~20-25 bullets |
| compact | Maximum density for extensive experience |
| minimal | Clean, understated, monochromatic |

### Custom Template Creation

For custom templates, the template-maker and reviewer work in an iteration loop:

1. **Design** — Define typography, layout, whitespace, color based on industry theme
2. **Create** — Generate `.typ.j2` template in `assets/templates/typst/`
3. **Compile** — Convert to PDF using existing formatter scripts
4. **Review** — Evaluate with resume-reviewer skill
5. **Adjust** — Fix issues identified by reviewer
6. **Repeat** — Continue until all visual QA checks pass

Design vectors prevent generic "AI resume" patterns by providing mid-altitude guidance on fonts, spacing, and color choices tailored to industry expectations.

## Common Pitfalls

- **YAML escaping**: Quotes containing colons or special chars need proper YAML escaping
- **Template names**: Lowercase only (`modern-tech` not `Modern-Tech`)
- **Version IDs**: Format is `v1`, `v2` (lowercase v + number)
- **Skill invocation**: Use natural language after plugin installation

## Troubleshooting

**Skills not loading:** Verify plugin is installed with `/plugin list`. Re-install with `/plugin install resume-skills@resume-helper-skills`.

**Typst compile errors:** Check `typst --version`. Escape special chars in YAML (colons, quotes).

**Content overflow:** Reduce achievements to 4-6 per role. Use optimizer to condense bullets.

**State not found:** Run `get_active.py` to verify project exists. If no `.resume_versions/`, run `init_project.py`.

**Store location:** Scripts search upward for `.resume_versions/`. If in a git repo, prefer repo-local `.resume_versions/`. Otherwise fall back to `~/.resume_versions`. Override with `RESUME_VERSIONS_PATH` env var.

## Development Notes

### Python Environment

- Managed with `uv`; run `uv sync` to install dependencies
- Python >=3.10 required
- Dependencies: pdfplumber, python-docx, pyyaml, jinja2, requests, beautifulsoup4, pydantic

### Skill Architecture

- **Source of Truth**: `resume-*/` directories
- **Plugin Config**: `.claude-plugin/marketplace.json` defines plugin entry points
- **State Management**: `state_utils.py` provides config/project loading, version resolution, path handling
- **New scripts**: Import from `state_utils.py`, use `resolve_project()` for `--project/-p` flags

### Local Development

For local development/testing, you can either:
1. Install via plugin marketplace (recommended — tests real distribution)
2. Create symlinks in `.claude/skills/` pointing to `resume-*/` directories
