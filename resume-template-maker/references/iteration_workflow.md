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
   - Consult `typst_patterns.md`
   - Identify code snippets needed

### Deliverable

Design specification:

```
## Template Design: [name]

### Typography
- Font: Inter
- Name: 24pt bold
- Headers: 12pt bold
- Body: 10pt regular

### Layout
- Single column
- Standard section order
- Skills inline

### Whitespace
- Margins: 0.5in
- Section gap: 0.8em
- Item gap: 0.3em

### Color
- Primary: #005293 (headers)
- Body: black
- Accents: primary for links
```

---

## Phase 3: Create Template

### File Location
```
.claude/skills/resume-formatter/assets/templates/typst/[name].typ.j2
```

### Template Checklist

Before first compile:
- [ ] Jinja2 syntax correct
- [ ] All user content uses `| typst_escape`
- [ ] All required sections handled (contact, summary, experience, skills, education)
- [ ] Optional sections have `{% if ... %}` guards
- [ ] No hardcoded content (all from YAML)
- [ ] Consistent spacing values

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
# Convert YAML to Typst
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py \
    [resume.yaml] [template_name] -o output.typ

# Compile Typst to PDF
uv run .claude/skills/resume-formatter/scripts/compile_typst.py \
    output.typ -o output.pdf
```

### Handle Compilation Errors

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `expected ... found ...` | Syntax error | Check brackets, content/code mode |
| Unescaped `#` or `@` | Special char in content | Use `| typst_escape` filter |
| `font not found` | Font not installed | Use different font or install font |
| Page overflow | Too much content | Reduce margins/font or content |

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
- Problem: 1em gap vs 0.5em elsewhere
- Fix: Use consistent #v(section-gap) command

#### Issue 2: Date alignment
- Location: Experience section
- Problem: Dates not right-aligned consistently
- Fix: Use grid with (1fr, auto) columns
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
```typst
// Before: inconsistent
#v(0.8em)
...
#v(1.2em)

// After: consistent
#v(section-gap)  // Defined as 0.8em at top
...
#v(section-gap)
```

**Alignment Issues**
```typst
// Before: h(1fr) not working
*Company* #h(1fr) Location

// After: grid alignment
#grid(
  columns: (1fr, auto),
  [*Company*], [Location]
)
```

**Overflow Issues**
```typst
// Option 1: Reduce margins
#set page(margin: (x: 0.5in, y: 0.4in))

// Option 2: Reduce font size
#set text(size: 9pt)

// Option 3: Reduce spacing
#set list(spacing: 0.3em, tight: true)
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
- Created initial template from executive base
- Issues: Section spacing inconsistent, dates misaligned

### Round 2
- Fixed: Added consistent section-gap variable
- Fixed: Changed to grid date alignment
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
| executive | Most roles, professional |
| compact | Dense experience, 10+ years |
| minimal | Clean, understated |
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
  uv run .../yaml_to_typst.py resume.yaml [name] -o resume.typ
  uv run .../compile_typst.py resume.typ -o resume.pdf

Best for: [industry/role]
Notes: [any special considerations]
```

---

## Troubleshooting

### Template Won't Compile

1. Check for Jinja2 syntax errors (missing `%}`, `}}`)
2. Check for Typst syntax errors (unclosed brackets, wrong mode)
3. Compile directly with `typst compile` for detailed errors
4. Isolate: Comment out sections until it compiles

### Review Keeps Finding Issues

1. Step back: Is the design fundamentally flawed?
2. Simplify: Remove complex features, add back one at a time
3. Compare: Look at working templates for patterns
4. Reset: Start fresh from a known-working template

### Content Doesn't Fit

1. Reduce margins (min 0.4in)
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
Template: .claude/skills/resume-formatter/assets/templates/typst/[name].typ.j2
Output:   [anywhere user specifies, typically ./resume.typ → ./resume.pdf]
```

### Commands
```bash
# Compile pipeline
uv run .../yaml_to_typst.py resume.yaml [template] -o out.typ
uv run .../compile_typst.py out.typ -o out.pdf

# Test ATS extraction
pdftotext out.pdf -
```

### Iteration States
- **CONTINUE**: More fixes needed
- **COMPLETE**: All checks pass
