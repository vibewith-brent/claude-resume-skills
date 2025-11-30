---
name: resume-formatter
description: Convert resume YAML to professionally formatted PDF using LaTeX templates. Use when generating final resume PDFs, comparing template layouts, or creating print-ready documents. Includes 4 templates optimized for different industries.
license: MIT
version: 1.0.0
allowed-tools:
  - Bash(uv run:*)
  - Bash(/Library/TeX/texbin/pdflatex:*)
  - Read
  - Write
---

# Resume Formatter

## Overview

Transform resume YAML files into professionally formatted PDF documents using LaTeX templates. Choose from 4 theme options optimized for different industries and personal styles.

## Quick Start

```bash
# Step 1: Convert YAML to LaTeX
uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml modern --output resume.tex

# Step 2: Compile to PDF
uv run scripts/compile_latex.py resume.tex

# Result: resume.pdf
```

## Available Templates

### Template Selection Guide

```
Role type?
├─ Academia/Research → Use Academic
├─ Finance/Law/Consulting → Use Classic
├─ Design/Marketing/UX → Use Creative
└─ Tech/General → Use Modern (default)
```

**Modern** (default)
- Best for: Tech, startups, general professional roles
- Style: Clean, professional, blue accents, ATS-friendly
- Features: Professional icons, compact layout

**Classic**
- Best for: Finance, consulting, law, traditional industries
- Style: Conservative, minimal formatting, black/white
- Features: Maximum ATS compatibility, no graphics

**Academic**
- Best for: Research positions, academia, scientific roles
- Style: Formal, publication-focused
- Features: Numbered publications, multi-page friendly

**Creative**
- Best for: Design, marketing, UX, creative industries
- Style: Bold, modern, visually distinctive
- Features: Colored header, modern typography, hyperlinked contact

**Detailed comparison:** [Theme Guide](references/theme_guide.md)

## Workflow

### Convert YAML to LaTeX

```bash
uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py <yaml_file> <template> --output <output.tex>
```

**Templates:** `modern`, `classic`, `academic`, `creative`

**Examples:**
```bash
# Modern template (tech/startup)
uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml modern --output resume_modern.tex

# Classic template (finance/consulting)
uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml classic --output resume_classic.tex

# Academic template (research)
uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml academic --output resume_academic.tex

# Creative template (design)
uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml creative --output resume_creative.tex
```

### Compile LaTeX to PDF

```bash
uv run scripts/compile_latex.py <tex_file> [--output <output.pdf>]
```

**Example:**
```bash
uv run scripts/compile_latex.py resume_modern.tex
# Creates: resume_modern.pdf

# Or specify custom output name:
uv run scripts/compile_latex.py resume_modern.tex --output brent_skoumal_resume.pdf
```

The script runs pdflatex twice (for proper formatting) and cleans up auxiliary files (.aux, .log, .out).

### Review PDF

After compilation:
1. **Visual review:** Check formatting, layout, spacing
2. **Content review:** Verify all sections rendered correctly
3. **ATS test:** Copy-paste text to ensure proper extraction
4. **Print test:** View in grayscale for B&W readability

### Iterate if Needed

1. Edit the YAML source (not LaTeX)
2. Regenerate LaTeX from updated YAML
3. Recompile to PDF
4. Review again

**Why edit YAML instead of LaTeX:**
- Easier to maintain and update
- Can regenerate with different templates
- Works with resume-optimizer skill

## Prerequisites

### LaTeX Installation

**macOS:**
```bash
# Full installation (3.9 GB)
brew install --cask mactex

# OR minimal installation (100 MB)
brew install --cask mactex-no-gui
```

**Linux (Ubuntu/Debian):**
```bash
# Full installation
sudo apt-get install texlive-full

# OR minimal installation
sudo apt-get install texlive-latex-base texlive-latex-extra
```

**Verify:**
```bash
pdflatex --version
```

## Quick Customization

### Change Colors (Modern)

Edit template line 6:
```latex
\moderncvcolor{blue}  % Options: blue, orange, green, red, purple, grey, black
```

### Change Colors (Creative)

Edit RGB definitions (lines 15-17):
```latex
\definecolor{primarycolor}{RGB}{0,102,204}    % Main accent
\definecolor{accentcolor}{RGB}{51,51,51}       % Secondary
```

### Change Font Size

All templates, line 1:
```latex
\documentclass[11pt,a4paper]{...}  % Try 10pt, 11pt, or 12pt
```

### Change Margins

**Modern:**
```latex
\usepackage[scale=0.85]{geometry}  % Increase for wider margins
```

**Other templates:**
```latex
\usepackage[margin=0.75in]{geometry}  % Adjust as needed
```

**Detailed customization:** [Theme Guide](references/theme_guide.md)

## Tips for Best Results

**Content preparation:**
1. Optimize YAML using `resume-optimizer` skill first
2. Keep resume to 1-2 pages
3. Use consistent date formatting
4. Ensure all required YAML fields present

**Template selection:**
1. Match template to industry norms
2. When in doubt, choose Modern or Classic
3. Test ATS compatibility for target companies
4. Generate PDFs with multiple templates to compare

**PDF generation:**
1. Always review PDF before submitting
2. Test text extraction (copy-paste from PDF)
3. Check both screen and print appearance
4. Keep source YAML for easy updates

**File naming:**
```
Good: firstname_lastname_resume.pdf
Good: firstname_lastname_companyname.pdf
Avoid: resume.pdf, cv_final_v3.pdf
```

## Complete Example

```bash
# Starting from YAML resume:

# 1. Convert to LaTeX with modern template
uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml modern \
  --output resume_modern.tex

# 2. Compile to PDF
uv run scripts/compile_latex.py resume_modern.tex \
  --output final_resume.pdf

# 3. Review PDF
open final_resume.pdf  # macOS
# or
xdg-open final_resume.pdf  # Linux

# 4. (Optional) Generate alternative template for comparison
uv run --with pyyaml,jinja2 scripts/yaml_to_latex.py resume.yaml classic \
  --output resume_classic.tex
uv run scripts/compile_latex.py resume_classic.tex \
  --output final_resume_classic.pdf
```

## Integration with Other Skills

**Complete resume workflow:**

1. **Extract:** Use `resume-extractor` to convert PDF/DOCX to YAML
2. **Optimize:** Use `resume-optimizer` to improve content and tailor for target role
3. **Format:** Use `resume-formatter` (this skill) to generate final PDF
4. **Iterate:** Make updates in YAML and regenerate

This workflow keeps resume data in editable YAML format while producing professional PDF output.

## Reference Documentation

- [Theme Guide](references/theme_guide.md) - Template comparison and customization
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
- [Examples](references/examples.md) - Complete workflow examples and use cases
