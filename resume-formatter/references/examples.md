# Resume Formatter Examples

## Complete Workflow Examples

### Example 1: Basic Single-Template Workflow

**Starting point:** `resume.yaml`

**Goal:** Generate PDF with executive template

```bash
# Step 1: Convert YAML to Typst
uv run scripts/yaml_to_typst.py resume.yaml executive \
  --output resume.typ

# Step 2: Compile to PDF
uv run scripts/compile_typst.py resume.typ \
  --output firstname_lastname_resume.pdf

# Step 3: Review
open firstname_lastname_resume.pdf  # macOS
```

### Example 2: Multi-Template Comparison

**Goal:** Generate PDFs with all 3 templates to compare

```bash
# Generate executive template
uv run scripts/yaml_to_typst.py resume.yaml executive \
  --output resume_executive.typ
uv run scripts/compile_typst.py resume_executive.typ \
  --output resume_executive.pdf

# Generate compact template
uv run scripts/yaml_to_typst.py resume.yaml compact \
  --output resume_compact.typ
uv run scripts/compile_typst.py resume_compact.typ \
  --output resume_compact.pdf

# Generate minimal template
uv run scripts/yaml_to_typst.py resume.yaml minimal \
  --output resume_minimal.typ
uv run scripts/compile_typst.py resume_minimal.typ \
  --output resume_minimal.pdf

# Review all
ls -lh resume_*.pdf
```

### Example 3: Job-Specific Resume Generation

**Scenario:** Tailored resume for specific job posting

```bash
# Assume you've already optimized resume for target role
# Input: resume_staff_ai_engineer.yaml

# Step 1: Generate PDF with executive template (for tech role)
uv run scripts/yaml_to_typst.py \
  resume_staff_ai_engineer.yaml executive \
  --output resume_staff_ai.typ

# Step 2: Compile
uv run scripts/compile_typst.py resume_staff_ai.typ \
  --output brent_skoumal_staff_ai_engineer.pdf

# Step 3: Verify ATS compatibility
pdftotext brent_skoumal_staff_ai_engineer.pdf - | head -50
```

### Example 4: Iterative Refinement

**Scenario:** Edit content and regenerate

```bash
# Initial generation
uv run scripts/yaml_to_typst.py resume.yaml executive \
  --output resume.typ
uv run scripts/compile_typst.py resume.typ

# Review PDF, decide to make changes
# Edit resume.yaml (add metrics, improve bullets, etc.)

# Regenerate from updated YAML
uv run scripts/yaml_to_typst.py resume.yaml executive \
  --output resume.typ
uv run scripts/compile_typst.py resume.typ

# Repeat until satisfied
```

### Example 5: Complete End-to-End Pipeline

**Scenario:** Extract → Optimize → Format complete workflow

```bash
# Step 1: Extract from PDF
uv run scripts/extract_pdf.py original_resume.pdf \
  --output extracted_text.txt

# (Manual: Parse extracted text to YAML)
# Result: resume_initial.yaml

# Step 2: Optimize (using resume-optimizer skill)
# (Manual: Run optimization, add metrics, tailor for role)
# Result: resume_optimized.yaml

# Step 3: Format to PDF
uv run scripts/yaml_to_typst.py \
  resume_optimized.yaml executive --output resume.typ
uv run scripts/compile_typst.py resume.typ \
  --output final_resume.pdf
```

## Template Comparison

### Visual Comparison Table

| Feature | Executive | Compact | Minimal |
|---------|-----------|---------|---------|
| **Color scheme** | Navy/blue accents | Blue/gray | Monochrome + blue |
| **Best for** | Most roles | Dense experience | Clean look |
| **ATS-friendly** | High | High | High |
| **Page density** | Medium | High | Low-Medium |
| **Font size** | 9pt | 8-8.5pt | 9pt |

### When to Use Each Template

**Executive Template:**
```bash
# Use for: Most professional roles
uv run scripts/yaml_to_typst.py resume.yaml executive --output resume.typ
```

**Best features:**
- Professional and contemporary
- Good balance of content and whitespace
- Works for most industries

**Compact Template:**
```bash
# Use for: Extensive experience (10+ years)
uv run scripts/yaml_to_typst.py resume.yaml compact --output resume.typ
```

**Best features:**
- Maximum content density
- Fits more on 2 pages
- Great for comprehensive skill lists

**Minimal Template:**
```bash
# Use for: Clean, understated presentation
uv run scripts/yaml_to_typst.py resume.yaml minimal --output resume.typ
```

**Best features:**
- Clean and easy to read
- Subtle design shows restraint
- Works well printed in B&W

## Customization Examples

### Example 1: Change Colors

**Edit:** `assets/templates/typst/executive.typ.j2` color definitions

```typst
// Before (navy theme)
#let primary = rgb("#1e3a5f")
#let accent = rgb("#0369a1")

// After (teal theme)
#let primary = rgb("#0f766e")
#let accent = rgb("#14b8a6")
```

### Example 2: Adjust Font Size

**Edit:** Any template, text settings

```typst
// Before (9pt - default)
#set text(font: "Inter", size: 9pt)

// After (8.5pt - smaller, fits more content)
#set text(font: "Inter", size: 8.5pt)
```

### Example 3: Adjust Margins

**All templates** - Edit page settings:

```typst
// Before
#set page(margin: (top: 0.4in, bottom: 0.35in, left: 0.5in, right: 0.5in))

// After (tighter margins)
#set page(margin: (top: 0.35in, bottom: 0.3in, left: 0.45in, right: 0.45in))
```

### Example 4: Custom Template Workflow

**Goal:** Create custom template based on executive

```bash
# Step 1: Copy executive template
cp assets/templates/typst/executive.typ.j2 \
   assets/templates/typst/custom.typ.j2

# Step 2: Edit custom.typ.j2
# - Change colors
# - Adjust margins
# - Modify fonts

# Step 3: Generate PDF with custom template
uv run scripts/yaml_to_typst.py \
  resume.yaml custom --output resume_custom.typ
uv run scripts/compile_typst.py resume_custom.typ

# Step 4: Iterate
```

## Common Use Cases

### Use Case 1: Tech Role Application

**Profile:** Software Engineer, 5 years experience

**Template choice:** Executive

```bash
uv run scripts/yaml_to_typst.py \
  resume.yaml executive --output resume.typ
uv run scripts/compile_typst.py resume.typ \
  --output john_doe_software_engineer.pdf
```

### Use Case 2: Senior Role with Extensive History

**Profile:** Staff Engineer, 12 years experience, many roles

**Template choice:** Compact

```bash
uv run scripts/yaml_to_typst.py \
  resume.yaml compact --output resume.typ
uv run scripts/compile_typst.py resume.typ \
  --output jane_smith_staff_engineer.pdf
```

### Use Case 3: Design-Adjacent Role

**Profile:** Technical PM, wants clean presentation

**Template choice:** Minimal

```bash
uv run scripts/yaml_to_typst.py \
  resume.yaml minimal --output resume.typ
uv run scripts/compile_typst.py resume.typ \
  --output bob_jones_pm.pdf
```

### Use Case 4: ATS Testing

**Goal:** Ensure resume passes ATS systems

```bash
# Generate PDF
uv run scripts/yaml_to_typst.py \
  resume.yaml executive --output resume.typ
uv run scripts/compile_typst.py resume.typ \
  --output resume_ats_test.pdf

# Test text extraction
pdftotext resume_ats_test.pdf extracted.txt

# Review extracted text
cat extracted.txt

# Check for:
# - All content present
# - Proper ordering
# - No garbled characters
# - Section headers clear
```

## File Naming Best Practices

### Good Naming Examples

```bash
# Professional, clear
firstname_lastname_resume.pdf

# With target company
firstname_lastname_google.pdf

# With role
firstname_lastname_senior_engineer.pdf
```

### Poor Naming Examples

```bash
# Avoid these
resume.pdf                    # Too generic
resume_final.pdf              # Not specific
cv_final_v3_FINAL.pdf        # Confusing
```

## Quick Reference Commands

```bash
# Generate executive template
uv run scripts/yaml_to_typst.py RESUME.yaml executive -o out.typ && \
uv run scripts/compile_typst.py out.typ

# Generate compact template
uv run scripts/yaml_to_typst.py RESUME.yaml compact -o out.typ && \
uv run scripts/compile_typst.py out.typ

# Generate minimal template
uv run scripts/yaml_to_typst.py RESUME.yaml minimal -o out.typ && \
uv run scripts/compile_typst.py out.typ

# Test ATS compatibility
pdftotext output.pdf - | less
```
