---
name: resume-formatter
description: Convert resume YAML to professionally formatted PDF using Typst templates. Use when generating final resume PDFs, comparing template layouts, or creating print-ready documents.
---

# Resume Formatter

## Overview

Transform resume YAML files into professionally formatted PDF documents using Typst templates. Choose from 3 templates optimized for different use cases.

## Quick Start

```bash
# Step 1: Convert YAML to Typst
uv run scripts/yaml_to_typst.py resume.yaml executive --output resume.typ

# Step 2: Compile to PDF
uv run scripts/compile_typst.py resume.typ

# Result: resume.pdf
```

## Available Templates

### Template Selection Guide

```
Need?
├─ Professional default → Executive
├─ Extensive experience → Compact
└─ Clean/understated → Minimal
```

**Executive** (default)
- Best for: Most professional roles, senior positions
- Style: Clean hierarchy, navy/blue accents
- Font: Inter
- Features: Professional layout, good whitespace balance

**Compact**
- Best for: Extensive experience, dense content
- Style: Maximum density without sacrificing readability
- Font: Inter
- Features: Tight spacing, small section headers

**Minimal**
- Best for: Clean, understated presentation
- Style: Monochromatic with single blue accent
- Font: Inter
- Features: Generous whitespace, subtle hierarchy

## Workflow

### Convert YAML to Typst

```bash
uv run scripts/yaml_to_typst.py <yaml_file> <template> --output <output.typ>
```

**Templates:** `executive`, `compact`, `minimal`

**Examples:**
```bash
# Executive template (default)
uv run scripts/yaml_to_typst.py resume.yaml executive --output resume_executive.typ

# Compact template (dense)
uv run scripts/yaml_to_typst.py resume.yaml compact --output resume_compact.typ

# Minimal template (clean)
uv run scripts/yaml_to_typst.py resume.yaml minimal --output resume_minimal.typ
```

### Compile Typst to PDF

```bash
uv run scripts/compile_typst.py <typ_file> [--output <output.pdf>]
```

**Example:**
```bash
uv run scripts/compile_typst.py resume_executive.typ
# Creates: resume_executive.pdf

# Or specify custom output name:
uv run scripts/compile_typst.py resume_executive.typ --output brent_skoumal_resume.pdf
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

### Change Colors

Edit the color definitions at the top of the template:
```typst
#let primary = rgb("#1e3a5f")    // Header and section color
#let accent = rgb("#0369a1")     // Links, dates
```

### Change Font

All templates, near the top:
```typst
#set text(font: "Inter", size: 9pt)  // Change font name
```

Common alternatives: "Helvetica", "Arial", "Source Sans Pro", "Roboto"

### Change Margins

```typst
#set page(margin: (top: 0.4in, bottom: 0.35in, left: 0.5in, right: 0.5in))
```

## Tips for Best Results

**Content preparation:**
1. Optimize YAML using `resume-optimizer` skill first
2. Keep resume to 1-2 pages
3. Use consistent date formatting
4. Ensure all required YAML fields present

**Template selection:**
1. Executive for most cases
2. Compact if you have 10+ years of detailed experience
3. Minimal for creative/design-adjacent roles

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

# 1. Convert to Typst with executive template
uv run scripts/yaml_to_typst.py resume.yaml executive \
  --output resume_executive.typ

# 2. Compile to PDF
uv run scripts/compile_typst.py resume_executive.typ \
  --output final_resume.pdf

# 3. Review PDF
open final_resume.pdf  # macOS
# or
xdg-open final_resume.pdf  # Linux

# 4. (Optional) Generate alternative template for comparison
uv run scripts/yaml_to_typst.py resume.yaml compact \
  --output resume_compact.typ
uv run scripts/compile_typst.py resume_compact.typ \
  --output final_resume_compact.pdf
```

## Integration with Other Skills

**Complete resume workflow:**

1. **Extract:** Use `resume-extractor` to convert PDF/DOCX to YAML
2. **Optimize:** Use `resume-optimizer` to improve content and tailor for target role
3. **Format:** Use `resume-formatter` (this skill) to generate final PDF
4. **Iterate:** Make updates in YAML and regenerate

This workflow keeps resume data in editable YAML format while producing professional PDF output.
