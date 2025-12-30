---
name: resume-template-maker
description: Create custom Typst resume templates tailored to specific content and page requirements. Use for any resume project that needs to fit content precisely.
---

# Resume Template Maker Skill

Create personalized Typst resume templates that fit each person's unique content. The built-in templates are starting points—most resume projects need a custom template to fit their content on the desired number of pages.

## When to Use

**Always consider customization when:**
- Resume content doesn't fit cleanly on target page count
- Content overflows onto a partial second page (or leaves awkward whitespace)
- User has significantly more or less experience than template was designed for
- Spacing feels too tight or too loose with built-in templates
- User wants to emphasize different sections than template prioritizes

**Also use for:**
- Industry-specific styling (finance, creative, tech, academic)
- Aesthetic preferences ("minimalist", "bold headers", "elegant serif")
- Major layout changes (sidebar, two-column, skills-forward)

## Core Philosophy

**Reality**: Each person's resume content is different. A template designed for 15 years of experience won't work for a new grad. A 1-page template won't work for someone with 25 achievements. Fitting content well requires tuning line spacing, margins, section gaps, and font sizes.

**Approach**: Start from the closest built-in template, then adjust parameters to fit the specific content. Use design vectors for aesthetic decisions, but focus first on making content fit the target page count cleanly.

## Content Fitting (Do This First)

Before aesthetic decisions, ensure content fits the target page count:

### Quick Tuning Parameters

| Too Much Content | Parameter | Too Little Content |
|------------------|-----------|-------------------|
| Reduce to 0.5in | **Margins** | Increase to 0.75in |
| Reduce to 9pt | **Body font** | Increase to 10.5pt |
| Reduce to 0.5em | **Line height** (`leading`) | Increase to 0.7em |
| Reduce to 6pt | **Section gap** | Increase to 12pt |
| Reduce to 2pt | **List spacing** | Increase to 4pt |
| Reduce to 18pt | **Name size** | Increase to 24pt |

### Content Reduction (When Still Too Long)

If parameter tuning isn't enough:
1. Reduce bullets per role (4-5 instead of 6-8)
2. Combine or remove older/less relevant positions
3. Condense skills into inline format vs. grouped
4. Shorten summary to 2-3 lines
5. Remove optional sections (volunteer, languages, publications)

### Whitespace Addition (When Too Short)

If content doesn't fill the page well:
1. Add a summary section if missing
2. Expand skills into categorized groups
3. Add a Projects section for side work
4. Include certifications, awards, or volunteer work
5. Increase spacing parameters (generous margins, larger section gaps)

### Page Break Decisions

For 2-page resumes:
- Break after a complete job entry, never mid-bullets
- Keep related content together (don't split one job across pages)
- Aim for roughly equal page density

## Design Vector Framework

Every template decision maps to four vectors:

### 1. Typography
- Font families (Inter, Source Sans, Roboto, etc.)
- Weight contrasts (name vs. body)
- Size hierarchy (5-level scale)
- Character: authoritative, approachable, creative, traditional

### 2. Layout
- Single column vs. multi-column vs. sidebar
- Section order and grouping
- Information density
- Visual flow pattern (F-pattern, Z-pattern)

### 3. Whitespace
- Margin philosophy (generous vs. efficient)
- Section rhythm (breathing room vs. compact)
- Internal spacing consistency
- Balance and distribution

### 4. Color
- Palette size (1-3 colors)
- Usage pattern (headers only, accents, backgrounds)
- Industry appropriateness
- Print considerations

## Workflow

### Step 1: Assess Content and Requirements
```
- How much content? (count: jobs, bullets, skills, education entries)
- Target page count? (strict 1-page, prefer 1, flexible 2-page)
- Industry/role context? (affects font choice, formality)
- Any specific aesthetic preferences?
```

### Step 2: Choose Starting Template
Pick the closest match based on content volume:

| Content | Recommended Start |
|---------|-------------------|
| Light (new grad, 1-2 jobs) | `minimal` or `executive` with increased spacing |
| Medium (5-10 years) | `executive` or `tech-modern` |
| Heavy (15+ years, many roles) | `modern-dense` or `compact` |

### Step 3: Compile with Actual Content
```bash
# Generate with chosen template
uv run resume-formatter/scripts/yaml_to_typst.py resume.yaml <template> -o test.typ
uv run resume-formatter/scripts/compile_typst.py test.typ -o test.pdf
```

### Step 4: Evaluate Fit
Check the PDF:
- Does content fit target page count?
- Any orphan lines (single line on new page)?
- Awkward whitespace at bottom of pages?
- Sections feel too cramped or too sparse?

### Step 5: Create Custom Template
```bash
# Copy and customize
cp resume-formatter/assets/templates/typst/<base>.typ.j2 \
   resume-formatter/assets/templates/typst/<user>-custom.typ.j2
```

Adjust parameters per "Content Fitting" section above.

### Step 6: Apply Design Vectors (If Needed)
For aesthetic changes beyond spacing:
- Use `references/design_vectors.md` for typography, layout, color decisions
- Use `references/industry_themes.md` for industry-specific guidance
- Use `references/typst_patterns.md` for implementation patterns

### Step 7: Iterate
Use **resume-reviewer** skill to evaluate:
1. Content fit (primary concern)
2. Visual hierarchy
3. Readability
4. Professional appearance

Continue until content fits well and reviewer passes all checks.

## Quick Start Templates

Start from the template closest to your needs:

| Template | Content Volume | Page Target | Style |
|----------|---------------|-------------|-------|
| `executive.typ.j2` | Medium | 1-2 pages | Professional, balanced |
| `tech-modern.typ.j2` | Medium | 1 page | Modern, creative |
| `modern-dense.typ.j2` | Heavy | 1-2 pages | Maximum density |
| `compact.typ.j2` | Heavy | 1 page strict | Minimal spacing |
| `minimal.typ.j2` | Light-Medium | 1 page | Understated, clean |

## References

- `references/design_vectors.md` — Detailed guidance on typography, layout, whitespace, color
- `references/industry_themes.md` — Industry-specific design recommendations
- `references/typst_patterns.md` — Code patterns for common template features
- `references/iteration_workflow.md` — Detailed iteration process

## Integration with Reviewer

The template-maker and reviewer form an iteration loop:

```
[Design] → [Create .typ.j2] → [Compile PDF] → [Review] → [Adjust] → ...
                                    ↑                         ↓
                                    └─────────────────────────┘
```

The reviewer provides structured feedback that maps directly to template adjustments. Iteration continues until the reviewer passes all quality checks.

## Output Checklist

Before considering a template complete:

**Content Fit (Primary)**
- [ ] Content fits target page count without overflow
- [ ] No orphan lines or awkward page breaks
- [ ] No excessive whitespace at page bottoms
- [ ] Spacing feels balanced throughout

**Technical**
- [ ] Compiles without errors
- [ ] Handles all required YAML sections
- [ ] Handles optional sections gracefully (empty = no output)
- [ ] Special characters escaped properly

**Quality**
- [ ] Tested with actual resume content (not sample data)
- [ ] Reviewer passes all categories
- [ ] Consistent with stated design rationale
