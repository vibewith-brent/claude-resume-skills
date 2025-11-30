# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Resume management skills suite for Claude Code: extract PDF/DOCX → optimize content → format to PDF → review and iterate. Five skills auto-load from `.claude/skills/` and are invoked via natural language.

## Common Commands

Run `uv sync` first if dependencies aren't installed.

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
.claude/skills/           # Active skills (auto-loaded by Claude Code)
├── resume-extractor/     # PDF/DOCX → text extraction
├── resume-optimizer/     # Content improvement, ATS, tailoring
├── resume-formatter/     # YAML → LaTeX → PDF
│   └── assets/templates/latex/  # Jinja2 templates (.tex.j2)
├── resume-reviewer/      # Visual QA for compiled PDFs
└── resume-template-maker/ # Create custom LaTeX templates

resume-*/                 # Source copies (packaged to .skill ZIP files)
```

Skills are duplicated: `.claude/skills/` for runtime, `resume-*/` for development/packaging.

### Skill Workflow

```
[Extract] → [Optimize] → [Format] → [Review] ←→ [Template Maker]
   ↓            ↓            ↓          ↓              ↓
 PDF/DOCX    YAML       YAML→PDF    Visual QA    Custom .tex.j2
```

- **resume-reviewer**: Evaluates compiled PDFs against visual QA checklist, provides structured feedback
- **resume-template-maker**: Creates custom templates using design vectors (typography, layout, whitespace, color)

## Key Files

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
