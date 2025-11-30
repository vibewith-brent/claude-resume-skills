# Resume Formatter Examples

## Table of Contents
- [Complete Workflow Examples](#complete-workflow-examples)
- [Template Comparison](#template-comparison)
- [Customization Examples](#customization-examples)
- [Common Use Cases](#common-use-cases)

## Complete Workflow Examples

### Example 1: Basic Single-Template Workflow

**Starting point:** `brent_resume.yaml`

**Goal:** Generate modern-template PDF

```bash
# Step 1: Convert YAML to LaTeX
uv run scripts/yaml_to_latex.py brent_resume.yaml modern \
  --output brent_resume_modern.tex

# Step 2: Compile to PDF
uv run scripts/compile_latex.py brent_resume_modern.tex \
  --output brent_skoumal_resume.pdf

# Step 3: Review
open brent_skoumal_resume.pdf  # macOS
# or
xdg-open brent_skoumal_resume.pdf  # Linux

# Result: brent_skoumal_resume.pdf
```

### Example 2: Multi-Template Comparison

**Goal:** Generate PDFs with all 4 templates to compare

```bash
# Generate modern template
uv run scripts/yaml_to_latex.py resume.yaml modern \
  --output resume_modern.tex
uv run scripts/compile_latex.py resume_modern.tex \
  --output resume_modern.pdf

# Generate classic template
uv run scripts/yaml_to_latex.py resume.yaml classic \
  --output resume_classic.tex
uv run scripts/compile_latex.py resume_classic.tex \
  --output resume_classic.pdf

# Generate academic template
uv run scripts/yaml_to_latex.py resume.yaml academic \
  --output resume_academic.tex
uv run scripts/compile_latex.py resume_academic.tex \
  --output resume_academic.pdf

# Generate creative template
uv run scripts/yaml_to_latex.py resume.yaml creative \
  --output resume_creative.tex
uv run scripts/compile_latex.py resume_creative.tex \
  --output resume_creative.pdf

# Review all
ls -lh resume_*.pdf
```

### Example 3: Job-Specific Resume Generation

**Scenario:** Tailored resume for specific job posting

```bash
# Assume you've already optimized resume for target role
# Input: brent_resume_staff_ai_engineer.yaml

# Step 1: Generate PDF with modern template (for tech role)
uv run scripts/yaml_to_latex.py \
  brent_resume_staff_ai_engineer.yaml modern \
  --output brent_resume_staff_ai.tex

# Step 2: Compile
uv run scripts/compile_latex.py brent_resume_staff_ai.tex \
  --output brent_skoumal_staff_ai_engineer.pdf

# Step 3: Verify ATS compatibility
pdftotext brent_skoumal_staff_ai_engineer.pdf - | head -50

# Result: brent_skoumal_staff_ai_engineer.pdf
```

### Example 4: Iterative Refinement

**Scenario:** Edit content and regenerate

```bash
# Initial generation
uv run scripts/yaml_to_latex.py resume.yaml modern \
  --output resume.tex
uv run scripts/compile_latex.py resume.tex

# Review PDF, decide to make changes
# Edit resume.yaml (add metrics, improve bullets, etc.)

# Regenerate from updated YAML
uv run scripts/yaml_to_latex.py resume.yaml modern \
  --output resume.tex
uv run scripts/compile_latex.py resume.tex

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
uv run scripts/yaml_to_latex.py \
  resume_optimized.yaml modern --output resume.tex
uv run scripts/compile_latex.py resume.tex \
  --output final_resume.pdf

# Final result: final_resume.pdf
```

## Template Comparison

### Visual Comparison Table

| Feature | Modern | Classic | Academic | Creative |
|---------|--------|---------|----------|----------|
| **Color scheme** | Blue accents | Black/white | Minimal color | Bold header color |
| **Icons** | Yes (contact) | No | No | Yes (contact) |
| **Best for** | Tech, startups | Finance, law | Research, academia | Design, marketing |
| **ATS-friendly** | High | Very High | High | Medium |
| **Print-friendly** | High | Very High | High | Medium |
| **Page density** | Medium | High | Medium | Low |
| **Multi-page** | Good | Excellent | Excellent | Good |

### When to Use Each Template

**Modern Template:**
```bash
# Use for: Software Engineer, Data Scientist, Product Manager, Tech roles
uv run scripts/yaml_to_latex.py resume.yaml modern --output resume.tex
```

**Best features:**
- Clean, professional appearance
- ATS-compatible while visually appealing
- Blue accent color is professional but not boring
- Icons make contact info easy to spot

**Classic Template:**
```bash
# Use for: Finance, Consulting, Law, Government, Traditional industries
uv run scripts/yaml_to_latex.py resume.yaml classic --output resume.tex
```

**Best features:**
- Maximum ATS compatibility
- Conservative appearance for traditional industries
- Highest content density (fits more info)
- Excellent print quality in grayscale

**Academic Template:**
```bash
# Use for: Research positions, Postdocs, Faculty, Scientific roles
uv run scripts/yaml_to_latex.py resume.yaml academic --output resume.tex
```

**Best features:**
- Emphasis on publications and education
- Multi-page layout works well
- Numbered publication lists
- Research interests section

**Creative Template:**
```bash
# Use for: Design, UX, Marketing, Creative industries
uv run scripts/yaml_to_latex.py resume.yaml creative --output resume.tex
```

**Best features:**
- Visually distinctive
- Modern typography
- Colored header stands out
- Hyperlinked contact info

## Customization Examples

### Example 1: Change Color (Modern Template)

**Edit:** `assets/templates/latex/modern.tex.j2` lines 15-18

```latex
% Before (default blue theme)
\definecolor{headerblue}{RGB}{0,102,204}
\definecolor{dateblue}{RGB}{0,102,204}
\definecolor{subtextgray}{RGB}{120,120,120}

% After (try different accent colors)
\definecolor{headerblue}{RGB}{0,153,76}    % Green accents
\definecolor{dateblue}{RGB}{0,153,76}
% Or
\definecolor{headerblue}{RGB}{102,51,153}  % Purple accents
\definecolor{dateblue}{RGB}{102,51,153}
```

### Example 2: Change Color (Creative Template)

**Edit:** `assets/templates/latex/creative.tex.j2` lines 15-17

```latex
% Before
\definecolor{primarycolor}{RGB}{0,102,204}    % Blue
\definecolor{accentcolor}{RGB}{51,51,51}       % Dark grey

% After - Professional purple
\definecolor{primarycolor}{RGB}{102,51,153}    % Purple
\definecolor{accentcolor}{RGB}{51,51,51}       % Dark grey

% Or - Tech green
\definecolor{primarycolor}{RGB}{0,153,76}      % Green
\definecolor{accentcolor}{RGB}{51,51,51}       % Dark grey
```

### Example 3: Adjust Font Size

**Edit:** Any template, first line

```latex
% Before (11pt - default)
\documentclass[11pt,letterpaper]{article}

% After (10pt - smaller, fits more content)
\documentclass[10pt,letterpaper]{article}

% Or (12pt - larger, more readable)
\documentclass[12pt,letterpaper]{article}
```

**Result:** Regenerate PDF to see changes
```bash
uv run scripts/compile_latex.py resume.tex
```

### Example 4: Adjust Margins

**Modern template** - Edit geometry scale:

```latex
% Before
\usepackage[scale=0.85]{geometry}

% After (wider margins)
\usepackage[scale=0.80]{geometry}

% Or (narrower margins, more content)
\usepackage[scale=0.90]{geometry}
```

**Other templates** - Edit margin size:

```latex
% Before
\usepackage[margin=0.75in]{geometry}

% After (wider margins)
\usepackage[margin=1.0in]{geometry}

% Or (narrower margins)
\usepackage[margin=0.5in]{geometry}
```

### Example 5: Custom Template Workflow

**Goal:** Create custom template based on modern

```bash
# Step 1: Copy modern template
cp assets/templates/latex/modern.tex.j2 \
   assets/templates/latex/custom.tex.j2

# Step 2: Edit custom.tex.j2
# - Change colors
# - Adjust margins
# - Modify fonts

# Step 3: Generate PDF with custom template
uv run scripts/yaml_to_latex.py \
  resume.yaml custom --output resume_custom.tex
uv run scripts/compile_latex.py resume_custom.tex

# Step 4: Iterate
```

## Common Use Cases

### Use Case 1: Tech Startup Application

**Profile:** Software Engineer, 5 years experience, applying to startup

**Template choice:** Modern

**Why:** Clean, professional, tech-friendly, ATS-compatible

```bash
uv run scripts/yaml_to_latex.py \
  resume.yaml modern --output resume.tex
uv run scripts/compile_latex.py resume.tex \
  --output john_doe_software_engineer.pdf
```

### Use Case 2: Finance/Consulting Application

**Profile:** Data Analyst, 3 years experience, applying to McKinsey

**Template choice:** Classic

**Why:** Conservative, traditional, maximum ATS compatibility

```bash
uv run scripts/yaml_to_latex.py \
  resume.yaml classic --output resume.tex
uv run scripts/compile_latex.py resume.tex \
  --output jane_smith_analyst.pdf
```

### Use Case 3: Academic Position

**Profile:** PhD, 10 publications, applying for postdoc

**Template choice:** Academic

**Why:** Emphasis on publications, research-focused

```bash
uv run scripts/yaml_to_latex.py \
  cv.yaml academic --output cv.tex
uv run scripts/compile_latex.py cv.tex \
  --output robert_johnson_cv.pdf
```

### Use Case 4: Design/Creative Role

**Profile:** UX Designer, 4 years experience, applying to design agency

**Template choice:** Creative

**Why:** Visually distinctive, shows design sensibility

```bash
uv run scripts/yaml_to_latex.py \
  resume.yaml creative --output resume.tex
uv run scripts/compile_latex.py resume.tex \
  --output sarah_williams_ux_designer.pdf
```

### Use Case 5: Multiple Applications

**Scenario:** Applying to different types of companies

```bash
# For tech companies - modern template
uv run scripts/yaml_to_latex.py \
  resume_tech_focused.yaml modern \
  --output resume_tech.tex
uv run scripts/compile_latex.py resume_tech.tex \
  --output resume_tech_companies.pdf

# For consulting - classic template
uv run scripts/yaml_to_latex.py \
  resume_consulting_focused.yaml classic \
  --output resume_consulting.tex
uv run scripts/compile_latex.py resume_consulting.tex \
  --output resume_consulting.pdf

# Maintain multiple YAML versions tailored for different roles
```

### Use Case 6: ATS Testing

**Goal:** Ensure resume passes ATS systems

```bash
# Generate with classic template (best ATS compatibility)
uv run scripts/yaml_to_latex.py \
  resume.yaml classic --output resume_ats.tex
uv run scripts/compile_latex.py resume_ats.tex \
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
brent_skoumal_resume.pdf

# With target company
firstname_lastname_company.pdf
jane_smith_google.pdf

# With role
firstname_lastname_role.pdf
john_doe_senior_engineer.pdf

# With date (for tracking versions)
firstname_lastname_resume_2024.pdf
```

### Poor Naming Examples

```bash
# Avoid these
resume.pdf                    # Too generic
resume_final.pdf              # Not specific
cv_final_v3_FINAL.pdf        # Confusing
my_resume_updated.pdf         # Unprofessional
JohnDoeRESUME.pdf            # Inconsistent case
```

## Quick Reference Commands

```bash
# Generate modern template
uv run scripts/yaml_to_latex.py RESUME.yaml modern -o out.tex && \
uv run scripts/compile_latex.py out.tex

# Generate classic template
uv run scripts/yaml_to_latex.py RESUME.yaml classic -o out.tex && \
uv run scripts/compile_latex.py out.tex

# Generate academic template
uv run scripts/yaml_to_latex.py RESUME.yaml academic -o out.tex && \
uv run scripts/compile_latex.py out.tex

# Generate creative template
uv run scripts/yaml_to_latex.py RESUME.yaml creative -o out.tex && \
uv run scripts/compile_latex.py out.tex

# Test ATS compatibility
pdftotext output.pdf - | less
```
