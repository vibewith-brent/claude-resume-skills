# Resume Formatter Theme Guide

## Overview

The resume-formatter skill includes 4 professionally designed LaTeX templates, each optimized for different industries and personal styles.

## Available Themes

### 1. Modern (`modern`)

**Best for:** Tech, startups, creative industries
**Style:** Clean, professional, uses moderncv package
**Features:**
- Banking-style layout (clean, compact)
- Blue accent color
- Professional section headers
- Compact bullet lists
- Contact icons

**Pros:**
- Most ATS-friendly template
- Professional yet contemporary
- Great for tech roles
- Compact (fits more content)

**Cons:**
- Requires `texlive-latex-extra` for moderncv package
- Less customization without LaTeX knowledge

**Recommended for:**
- Software Engineers
- Data Scientists
- Product Managers
- Tech industry roles

---

### 2. Classic (`classic`)

**Best for:** Finance, consulting, law, traditional industries
**Style:** Traditional, conservative, minimal formatting
**Features:**
- Simple article-based layout
- No colors or graphics
- Traditional section headers with horizontal rules
- Maximum readability
- Standard fonts

**Pros:**
- Works with minimal LaTeX packages
- Maximum ATS compatibility
- Professional and conservative
- Easy to customize

**Cons:**
- Less visually distinctive
- May appear bland for creative roles

**Recommended for:**
- Finance roles
- Consulting positions
- Legal professions
- Government/military
- Traditional corporate environments

---

### 3. Academic (`academic`)

**Best for:** Research, academia, scientific roles
**Style:** Formal, publication-focused
**Features:**
- Emphasis on education and publications sections
- Numbered publication lists
- Research interests section
- Page numbers
- Subsections for positions

**Pros:**
- Designed for academic conventions
- Highlights research and publications
- Multi-page friendly with page numbers
- Clear hierarchy

**Cons:**
- Too formal for most industry roles
- Not optimized for brevity

**Recommended for:**
- Academic positions (faculty, postdoc)
- Research scientist roles
- PhD candidates
- Roles emphasizing publications

---

### 4. Creative (`creative`)

**Best for:** Design, marketing, creative industries
**Style:** Bold, modern, color-accented
**Features:**
- Colored header bar
- Blue and gray color scheme
- Visual section separators
- Modern typography
- Hyperlinked contact info

**Pros:**
- Visually distinctive
- Shows design sensibility
- Modern and engaging
- Good for portfolio roles

**Cons:**
- Colors may not print well in B&W
- Some ATS systems struggle with graphics
- Less conservative

**Recommended for:**
- UX/UI Designers
- Marketing roles
- Creative positions
- Startups
- Roles emphasizing visual design

## Choosing the Right Template

**Decision tree:**

```
Are you applying to academia or research roles?
  └─ YES → Use Academic
  └─ NO  → Continue

Is the industry traditional/conservative (finance, law, consulting)?
  └─ YES → Use Classic
  └─ NO  → Continue

Is the role creative (design, marketing, UX)?
  └─ YES → Use Creative
  └─ NO  → Use Modern (default for tech/general)
```

## Customization

### Color Changes

**Modern template:**
Edit line 6 in `modern.tex.j2`:
```latex
\moderncvcolor{blue}  % Options: blue, orange, green, red, purple, grey, black
```

**Creative template:**
Edit lines 15-17 in `creative.tex.j2`:
```latex
\definecolor{primarycolor}{RGB}{0,102,204}    % Main accent color
\definecolor{accentcolor}{RGB}{51,51,51}       % Secondary color
\definecolor{lightgray}{RGB}{240,240,240}      % Background accents
```

### Font Changes

**All templates:**
Change font size in `\documentclass` line:
```latex
\documentclass[11pt,a4paper]{...}  % Change 11pt to 10pt, 12pt, etc.
```

For Classic/Academic/Creative templates, add font package:
```latex
\usepackage{times}      % Times New Roman
\usepackage{helvet}     % Helvetica
\usepackage{palatino}   % Palatino
```

### Margin Adjustments

**Modern template:**
```latex
\usepackage[scale=0.85]{geometry}  % Increase scale for wider margins
```

**Other templates:**
```latex
\usepackage[margin=0.75in]{geometry}  % Adjust margin size
```

### Section Order

Templates render sections in this order (if present in YAML):
1. Professional Summary / Profile / Research Interests
2. Professional Experience / Experience
3. Skills / Core Competencies / Technical Skills
4. Education
5. Certifications (if present)
6. Projects / Research Projects (if present)
7. Publications (if present)
8. Awards & Honors (if present)
9. Languages (if present)

To change order, edit the template file section blocks.

## LaTeX Installation

### macOS

**Full installation (3.9 GB):**
```bash
brew install --cask mactex
```

**Minimal installation (100 MB):**
```bash
brew install --cask mactex-no-gui
```

### Linux (Ubuntu/Debian)

**Full installation:**
```bash
sudo apt-get install texlive-full
```

**Minimal installation:**
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra
```

### Windows

Download and install MiKTeX or TeX Live:
- MiKTeX: https://miktex.org/download
- TeX Live: https://www.tug.org/texlive/

## Troubleshooting

### Missing Package Errors

If you get errors like `! LaTeX Error: File 'moderncv.cls' not found`:

**macOS:**
```bash
sudo tlmgr update --self
sudo tlmgr install moderncv
```

**Linux:**
```bash
sudo apt-get install texlive-latex-extra
```

### Compilation Errors

**Symptom:** Special characters causing errors
**Solution:** The yaml_to_latex.py script escapes special LaTeX characters automatically. If you see errors, check for unescaped `&`, `%`, `$`, `#`, `_`, `{`, `}` in your YAML.

**Symptom:** "! Undefined control sequence"
**Solution:** Template uses undefined command. Install missing packages or use different template.

**Symptom:** Content cut off or overlapping
**Solution:** Reduce content length, decrease font size, or adjust margins.

### PDF Generation Issues

**Symptom:** PDF not generated but no errors
**Solution:** Run pdflatex twice (compile_latex.py does this automatically).

**Symptom:** Fonts look wrong
**Solution:** Ensure proper LaTeX installation with font packages.

## Best Practices

1. **Preview before applying:** Generate PDF and review carefully
2. **Test in B&W:** Print or convert to grayscale to ensure readability
3. **Check PDF text:** Copy-paste text from PDF to verify proper extraction (ATS test)
4. **Stay under 2 pages:** Most roles expect 1-2 pages maximum
5. **Proofread:** LaTeX doesn't check spelling - review final PDF carefully
6. **Keep YAML source:** Easier to update than editing LaTeX directly

## Template Comparison Matrix

| Feature | Modern | Classic | Academic | Creative |
|---------|--------|---------|----------|----------|
| ATS-Friendly | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| Visual Appeal | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★★ |
| Conservative | ★★★☆☆ | ★★★★★ | ★★★★★ | ★☆☆☆☆ |
| Content Density | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★★★☆ |
| Easy Customization | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| Package Requirements | High | Low | Medium | Medium |
| Print Quality | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ |
| Digital Quality | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ |

## Advanced Customization

For more extensive template modifications, see LaTeX documentation:
- moderncv: https://ctan.org/pkg/moderncv
- titlesec: https://ctan.org/pkg/titlesec
- geometry: https://ctan.org/pkg/geometry
- color/xcolor: https://ctan.org/pkg/xcolor
