---
name: resume-formatter
description: Convert resume YAML to professionally formatted PDF using Typst templates. Use when generating final resume PDFs, comparing template layouts, or creating print-ready documents. Includes 4 templates optimized for different industries.
license: MIT
metadata:
  version: 2.0.0
allowed-tools:
  - Bash(uv run:*)
  - Bash(typst:*)
  - Read
  - Write
---

# Resume Formatter

## Overview

Transform resume YAML files into professionally formatted PDF documents using Typst templates. Choose from 4 theme options optimized for different industries and personal styles.

## Quick Start

```bash
# Step 1: Convert YAML to Typst
uv run scripts/yaml_to_typst.py resume.yaml modern --output resume.typ

# Step 2: Compile to PDF
uv run scripts/compile_typst.py resume.typ

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
- Font: Inter
- Features: Professional icons, compact layout

**Classic**
- Best for: Finance, consulting, law, traditional industries
- Style: Conservative, minimal formatting, black/white
- Font: New Computer Modern (serif)
- Features: Maximum ATS compatibility, no graphics

**Academic**
- Best for: Research positions, academia, scientific roles
- Style: Formal, publication-focused
- Font: New Computer Modern (serif)
- Features: Numbered publications, multi-page with page numbers

**Creative**
- Best for: Design, marketing, UX, creative industries
- Style: Bold, modern, visually distinctive
- Font: Inter
- Features: Colored header bar, modern typography

**Detailed comparison:** [Theme Guide](references/theme_guide.md)

## Workflow

### Convert YAML to Typst

```bash
uv run scripts/yaml_to_typst.py <yaml_file> <template> --output <output.typ>
```

**Templates:** `modern`, `classic`, `academic`, `creative`

**Examples:**
```bash
# Modern template (tech/startup)
uv run scripts/yaml_to_typst.py resume.yaml modern --output resume_modern.typ

# Classic template (finance/consulting)
uv run scripts/yaml_to_typst.py resume.yaml classic --output resume_classic.typ

# Academic template (research)
uv run scripts/yaml_to_typst.py resume.yaml academic --output resume_academic.typ

# Creative template (design)
uv run scripts/yaml_to_typst.py resume.yaml creative --output resume_creative.typ
```

### Compile Typst to PDF

```bash
uv run scripts/compile_typst.py <typ_file> [--output <output.pdf>]
```

**Example:**
```bash
uv run scripts/compile_typst.py resume_modern.typ
# Creates: resume_modern.pdf

# Or specify custom output name:
uv run scripts/compile_typst.py resume_modern.typ --output brent_skoumal_resume.pdf
```

Typst compiles in a single pass with no auxiliary files to clean up.

### Review PDF

After compilation:
1. **Visual review:** Check formatting, layout, spacing
2. **Content review:** Verify all sections rendered correctly
3. **ATS test:** Copy-paste text to ensure proper extraction
4. **Print test:** View in grayscale for B&W readability

### Iterate if Needed

1. Edit the YAML source (not Typst)
2. Regenerate Typst from updated YAML
3. Recompile to PDF
4. Review again

**Why edit YAML instead of Typst:**
- Easier to maintain and update
- Can regenerate with different templates
- Works with resume-optimizer skill

## Prerequisites

### Typst Installation

**macOS:**
```bash
brew install typst
```

**Linux:**
```bash
# Via cargo (requires Rust)
cargo install typst-cli

# Or via package manager (check availability)
```

**Windows:**
```bash
winget install --id Typst.Typst
```

**Verify:**
```bash
typst --version
```

## Quick Customization

### Change Colors (Modern/Creative)

Edit the color definitions at the top of the template:
```typst
#let headerblue = rgb("#0066cc")    // Header and section color
#let subtextgray = rgb("#787878")   // Subtext color
```

### Change Font

All templates, near the top:
```typst
#set text(font: "Inter", size: 10pt)  // Change font name
```

Common alternatives: "Helvetica", "Arial", "Source Sans Pro", "Roboto"

### Change Margins

```typst
#set page(margin: (top: 0.5in, bottom: 0.5in, left: 0.6in, right: 0.6in))
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

# 1. Convert to Typst with modern template
uv run scripts/yaml_to_typst.py resume.yaml modern \
  --output resume_modern.typ

# 2. Compile to PDF
uv run scripts/compile_typst.py resume_modern.typ \
  --output final_resume.pdf

# 3. Review PDF
open final_resume.pdf  # macOS
# or
xdg-open final_resume.pdf  # Linux

# 4. (Optional) Generate alternative template for comparison
uv run scripts/yaml_to_typst.py resume.yaml classic \
  --output resume_classic.typ
uv run scripts/compile_typst.py resume_classic.typ \
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
