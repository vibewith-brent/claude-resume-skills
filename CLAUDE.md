# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Resume management skills suite for Claude Code: extract PDF/DOCX → optimize content → format to PDF. Three skills auto-load from `.claude/skills/` and are invoked via natural language.

## Common Commands

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

### Fetch Job Posting
```bash
uv run .claude/skills/resume-optimizer/scripts/fetch_job_posting.py "<url>" --output job.txt
```

## Architecture

```
.claude/skills/           # Active skills (auto-loaded by Claude Code)
├── resume-extractor/     # PDF/DOCX → text extraction
├── resume-optimizer/     # Content improvement, ATS, tailoring
└── resume-formatter/     # YAML → LaTeX → PDF
    └── assets/templates/latex/  # Jinja2 templates (.tex.j2)

resume-*/                 # Source copies (packaged to .skill ZIP files)
```

Skills are duplicated: `.claude/skills/` for runtime, `resume-*/` for development/packaging.

## Key Files

- **YAML Schema**: `.claude/skills/resume-extractor/references/resume_schema.yaml` — canonical structure for resume data
- **LaTeX Templates**: `.claude/skills/resume-formatter/assets/templates/latex/*.tex.j2` — Jinja2 templates with `latex_escape` filter
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
