---
name: resume-reviewer
description: Visual QA for compiled resume PDFs. Evaluate layout, typography, spacing. Use after compiling a PDF to check for issues before finalizing.
version: 1.0.0
---

# Resume Reviewer Skill

Visual QA and critique for compiled resume PDFs. Provides structured evaluation to drive iterative improvement.

## When to Use

- After compiling a resume PDF to check for layout issues
- When a user asks "does this look good?" or "check my resume"
- As the feedback loop in template creation/customization
- Before finalizing a resume for submission

## Workflow

1. **View the PDF** — Use the Read tool on the compiled PDF file
2. **Run the checklist** — Evaluate against `references/visual_qa_checklist.md`
3. **Identify issues** — Cross-reference with `references/common_issues.md`
4. **Provide feedback** — Use the format in `references/feedback_format.md`

## Quick Evaluation

For rapid assessment, check these critical items first:

1. **Page overflow** — Does content fit on expected pages (1-2)?
2. **Readability** — Is text large enough, spacing adequate?
3. **Visual balance** — Is whitespace well-distributed?
4. **Hierarchy** — Is the name most prominent, sections clear?
5. **Alignment** — Are dates, bullets, sections aligned consistently?

## Feedback for Iteration

When reviewing for template-maker iteration:

```
## Visual QA Results

### Pass/Fail Summary
- Layout: [PASS/FAIL]
- Typography: [PASS/FAIL]
- Whitespace: [PASS/FAIL]
- Alignment: [PASS/FAIL]
- Overall: [PASS/FAIL]

### Issues Found
1. [Specific issue with location]
2. [Another issue]

### Recommended Adjustments
1. [Specific Typst adjustment to fix issue 1]
2. [Adjustment for issue 2]
```

## References

- `references/visual_qa_checklist.md` — Complete evaluation checklist
- `references/common_issues.md` — Known Typst resume failure patterns
- `references/feedback_format.md` — Structured feedback templates

## Integration with Template Maker

This skill is the inner loop of the template-maker workflow:

```
template-maker generates → compile to PDF → reviewer evaluates → template-maker adjusts
                                ↑                                        ↓
                                └────────────────────────────────────────┘
```

Continue iteration until reviewer returns all PASS results.
