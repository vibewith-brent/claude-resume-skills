# Template Iteration Workflow

Detailed process for creating and refining resume templates through iterative design-compile-review cycles.

---

## Overview

Template creation is iterative:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  [Gather Requirements] → [Design] → [Create Template]   │
│                                           ↓             │
│                         ┌─────────────────┴───────────┐ │
│                         │      ITERATION LOOP         │ │
│                         │                             │ │
│                         │   [Compile] → [Review]      │ │
│                         │       ↑           ↓         │ │
│                         │       └── [Adjust] ←┘       │ │
│                         │                             │ │
│                         │   Exit when: All PASS       │ │
│                         └─────────────────────────────┘ │
│                                           ↓             │
│                              [Finalize Template]        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Requirements Gathering

### Questions to Ask

1. **Target Role/Industry**
   - What industry? (Tech, finance, creative, etc.)
   - What level? (Entry, mid, senior, executive)
   - Any specific companies? (Affects conservative vs. modern choice)

2. **Aesthetic Preferences**
   - Modern or traditional?
   - Minimal or detailed?
   - Any templates they like? (Show examples if needed)
   - Personal brand colors?

3. **Content Constraints**
   - Must fit on 1 page? 2 pages OK?
   - How many jobs/bullets to include?
   - Any sections to emphasize or de-emphasize?

4. **Technical Requirements**
   - Will submit to ATS? (Affects layout complexity)
   - Print or digital primarily?
   - Any specific formats needed?

### Deliverable

Document requirements before designing:

```
## Template Requirements

- Industry: [X]
- Level: [X]
- Aesthetic: [X]
- Page limit: [X]
- Key sections: [X]
- Color preferences: [X]
- Special requests: [X]
```

---

## Phase 2: Design

### Process

1. **Select Industry Theme**
   - Consult `industry_themes.md`
   - Note recommended fonts, colors, layout

2. **Define Design Vectors**
   - Typography: [Font family, sizes, weights]
   - Layout: [Single column / sidebar / two-column]
   - Whitespace: [Margins, section spacing]
   - Color: [Palette, usage pattern]

3. **Sketch Structure**
   ```
   [Header: Name centered, contact inline]
   [Summary: 2-3 lines]
   [Experience: Reverse chron, bullets]
   [Skills: Inline by category]
   [Education: Compact]
   ```

4. **Select Base Patterns**
   - Consult `latex_patterns.md`
   - Identify code snippets needed

### Deliverable

Design specification:

```
## Template Design: [name]

### Typography
- Font: TeX Gyre Heros
- Name: 24pt bold
- Headers: 12pt bold
- Body: 11pt regular

### Layout
- Single column
- Standard section order
- Skills inline

### Whitespace
- Margins: 0.7in
- Section gap: 14pt
- Item gap: 2pt

### Color
- Primary: #005293 (headers)
- Body: black
- Accents: primary for links
```

---

## Phase 3: Create Template

### File Location
```
.claude/skills/resume-formatter/assets/templates/latex/[name].tex.j2
```

### Template Checklist

Before first compile:
- [ ] Jinja2 syntax correct
- [ ] All user content uses `| latex_escape`
- [ ] All required sections handled (contact, summary, experience, skills, education)
- [ ] Optional sections have `{% if ... %}` guards
- [ ] No hardcoded content (all from YAML)
- [ ] Consistent spacing commands

### Initial Template

Start with minimal working version:
1. Copy closest existing template
2. Modify to match design spec
3. Ensure it compiles without errors
4. Then refine

---

## Phase 4: Compile

### Commands

```bash
# Convert YAML to LaTeX
uv run .claude/skills/resume-formatter/scripts/yaml_to_latex.py \
    [resume.yaml] [template_name] -o output.tex

# Compile LaTeX to PDF
uv run .claude/skills/resume-formatter/scripts/compile_latex.py \
    output.tex -o output.pdf
```

### Handle Compilation Errors

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Missing package or typo | Add `\usepackage{}` or fix typo |
| `Missing $ inserted` | Unescaped special char | Use `| latex_escape` filter |
| `Font not found` | Font not installed | Use different font or install MacTeX full |
| `Dimension too large` | Spacing calculation error | Check spacing values |
| `Emergency stop` | Syntax error | Check for missing `}` or `\end{}` |

### Verify Output

After successful compile:
1. Open PDF to verify it rendered
2. Check all sections appear
3. Look for obvious issues before formal review

---

## Phase 5: Review

### Invoke Reviewer

Use the **resume-reviewer** skill to evaluate the compiled PDF.

### Review Process

1. Read the PDF file
2. Apply visual QA checklist
3. Generate structured feedback

### Expected Output

```
## Iteration Review: Round 1

### Status: CONTINUE

### Pass/Fail Summary
- Layout: PASS
- Typography: PASS
- Whitespace: FAIL
- Alignment: WARN
- Color: PASS
- ATS: PASS

### Failures Requiring Adjustment

#### Issue 1: Inconsistent section spacing
- Location: Between Experience and Skills sections
- Problem: 20pt gap vs 12pt elsewhere
- Fix: Use consistent \sectionspace command

#### Issue 2: Date alignment
- Location: Experience section
- Problem: Dates not right-aligned consistently
- Fix: Use tabular with @{\extracolsep{\fill}}
```

---

## Phase 6: Adjust

### Process

1. **Parse Feedback**
   - Identify FAIL and WARN items
   - Prioritize: FAIL first, then WARN

2. **Locate in Template**
   - Find the relevant code section
   - Understand current implementation

3. **Apply Fix**
   - Make minimal change to address issue
   - Don't introduce new changes beyond fix

4. **Verify Fix**
   - Ensure change compiles
   - Doesn't break other areas

### Common Adjustments

**Spacing Issues**
```latex
% Before: inconsistent
\vspace{12pt}
...
\vspace{20pt}

% After: consistent
\sectionspace  % Defined as 12pt in preamble
...
\sectionspace
```

**Alignment Issues**
```latex
% Before: hfill not working
\textbf{Company} \hfill Location

% After: tabular alignment
\begin{tabular*}{\textwidth}{@{}l@{\extracolsep{\fill}}r@{}}
\textbf{Company} & Location \\
\end{tabular*}
```

**Overflow Issues**
```latex
% Option 1: Reduce margins
\usepackage[margin=0.6in]{geometry}

% Option 2: Reduce font size
\documentclass[10pt,letterpaper]{article}

% Option 3: Reduce spacing
\setlist[itemize]{topsep=0pt, itemsep=0pt}
```

---

## Phase 7: Iterate

### Loop Until Pass

```
Round 1: Initial template
  → Review: 2 FAIL, 1 WARN
  → Fix FAIL issues

Round 2: Fixed spacing and alignment
  → Review: 0 FAIL, 1 WARN
  → Fix WARN issue

Round 3: Fixed typography warning
  → Review: All PASS
  → Exit loop
```

### Iteration Limits

- Typical: 2-4 rounds
- If >5 rounds: Reconsider design approach
- If stuck: Simplify template, address systematically

### Track Changes

Document each iteration:

```
## Iteration Log

### Round 1
- Created initial template from modern base
- Issues: Section spacing inconsistent, dates misaligned

### Round 2
- Fixed: Added consistent \sectionspace command
- Fixed: Changed to tabular date alignment
- Issues: Font hierarchy unclear

### Round 3
- Fixed: Increased name size to 26pt
- All PASS
```

---

## Phase 8: Finalize

### Final Checks

- [ ] Template compiles cleanly (no warnings)
- [ ] All YAML sections handled correctly
- [ ] Empty optional sections produce no output
- [ ] Tested with actual resume (not just sample)
- [ ] Tested with minimal content (doesn't break)
- [ ] Tested with maximum content (doesn't overflow)
- [ ] ATS extraction works (`pdftotext output.pdf -`)

### Documentation

Add template to formatter's options:

```markdown
| Template | Use Case |
|----------|----------|
| modern | Tech, startups |
| classic | Finance, law |
| academic | Research |
| creative | Design, marketing |
| [new] | [description] |  ← Add entry
```

### User Handoff

Provide:
1. Template name for future use
2. Any special considerations
3. Recommended use cases

```
Template "[name]" created and ready.

Use with:
  uv run .../yaml_to_latex.py resume.yaml [name] -o resume.tex
  uv run .../compile_latex.py resume.tex -o resume.pdf

Best for: [industry/role]
Notes: [any special considerations]
```

---

## Troubleshooting

### Template Won't Compile

1. Check for Jinja2 syntax errors (missing `%}`, `}}`)
2. Check for LaTeX syntax errors (missing `}`, `\end{}`)
3. Compile with verbose output to find line number
4. Isolate: Comment out sections until it compiles

### Review Keeps Finding Issues

1. Step back: Is the design fundamentally flawed?
2. Simplify: Remove complex features, add back one at a time
3. Compare: Look at working templates for patterns
4. Reset: Start fresh from a known-working template

### Content Doesn't Fit

1. Reduce margins (min 0.5in)
2. Reduce font sizes (min 9pt body)
3. Reduce spacing (tighten lists, sections)
4. Change layout (sidebar can be more efficient)
5. If still won't fit: Content needs editing, not template

### ATS Extraction Fails

1. Remove complex layouts (multi-column, sidebars)
2. Use single-column design
3. Avoid tables for content structure
4. Test: `pdftotext resume.pdf -` should be readable

---

## Quick Reference

### File Paths
```
Template: .claude/skills/resume-formatter/assets/templates/latex/[name].tex.j2
Output:   [anywhere user specifies, typically ./resume.tex → ./resume.pdf]
```

### Commands
```bash
# Compile pipeline
uv run .../yaml_to_latex.py resume.yaml [template] -o out.tex
uv run .../compile_latex.py out.tex -o out.pdf

# Test ATS extraction
pdftotext out.pdf -
```

### Iteration States
- **CONTINUE**: More fixes needed
- **COMPLETE**: All checks pass
