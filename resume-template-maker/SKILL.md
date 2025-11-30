# Resume Template Maker Skill

Create distinctive, professional Typst resume templates using structured design principles. Avoids generic "AI resume" patterns through multi-dimensional design guidance.

## When to Use

- User wants a custom template beyond the 4 built-in options
- User wants to modify an existing template significantly
- User describes a specific aesthetic ("minimalist with bold headers", "elegant serif")
- User wants industry-specific styling not covered by defaults
- User says "make it look like X" or "I want something more Y"

## Core Philosophy

**Problem**: Without guidance, generated templates converge toward safe, generic patterns—the resume equivalent of "Inter font with purple gradients."

**Solution**: Multi-dimensional design vectors that guide toward distinctive, professional output. Each template should have a clear design rationale, not just be "a resume."

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

### Step 1: Gather Requirements
```
- Target industry/role
- Aesthetic preferences (modern, traditional, creative, minimal)
- Content density (1 page strict, 2 page OK, flexible)
- Specific requests (sidebar, two-column, specific colors)
- Reference templates or designs they like
```

### Step 2: Design Template
Use `references/design_vectors.md` for typography, layout, whitespace, and color decisions.
Use `references/industry_themes.md` for industry-specific guidance.
Use `references/typst_patterns.md` for implementation patterns.

### Step 3: Create .typ.j2 Template
Output to `.claude/skills/resume-formatter/assets/templates/typst/[name].typ.j2`

Template must:
- Use Jinja2 syntax matching existing templates
- Include `typst_escape` filter on all user content
- Handle all YAML schema sections (required + optional)
- Compile with `typst compile`

### Step 4: Compile and Review
```bash
# Generate Typst
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py resume.yaml [template_name] -o test.typ

# Compile to PDF
uv run .claude/skills/resume-formatter/scripts/compile_typst.py test.typ -o test.pdf
```

Use **resume-reviewer** skill to evaluate output.

### Step 5: Iterate
Based on reviewer feedback:
1. Identify specific issues
2. Adjust template code
3. Recompile
4. Re-review

Continue until reviewer returns all PASS results.

## Quick Start Templates

For rapid customization, start from the closest existing template:

| Starting Point | Use When |
|----------------|----------|
| `modern.typ.j2` | Clean, contemporary, tech-adjacent |
| `classic.typ.j2` | Traditional, conservative, formal |
| `academic.typ.j2` | Research-focused, education-heavy |
| `creative.typ.j2` | Bold, visual, design-forward |

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

- [ ] Compiles without errors
- [ ] Handles all required YAML sections
- [ ] Handles optional sections gracefully (empty = no output)
- [ ] Special characters escaped properly
- [ ] Reviewer passes all categories
- [ ] Tested with actual resume content (not just sample)
- [ ] Consistent with stated design rationale
