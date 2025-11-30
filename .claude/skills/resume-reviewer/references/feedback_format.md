# Feedback Format for Resume Review

Structured templates for providing actionable feedback during resume review and template iteration.

---

## Quick Review Format

For rapid assessment when user asks "does this look good?":

```
## Quick Review: [filename.pdf]

**Overall**: [READY / NEEDS WORK / REVISE]

**Strengths**:
- [What works well]
- [Another positive]

**Issues**:
- [Most critical issue]
- [Second issue if any]

**Recommendation**: [One sentence on next action]
```

---

## Full Review Format

Comprehensive evaluation for detailed feedback:

```
## Full Review: [filename.pdf]

### Summary
[2-3 sentences on overall impression and readiness]

### Category Scores

| Category | Status | Notes |
|----------|--------|-------|
| Layout | PASS/WARN/FAIL | [Brief note] |
| Typography | PASS/WARN/FAIL | [Brief note] |
| Whitespace | PASS/WARN/FAIL | [Brief note] |
| Alignment | PASS/WARN/FAIL | [Brief note] |
| Color | PASS/WARN/FAIL | [Brief note] |
| ATS | PASS/WARN/FAIL | [Brief note] |

### Issues Found

**Critical** (must fix):
1. [Issue]: [Location] — [Impact]

**Recommended** (should fix):
1. [Issue]: [Location] — [Impact]

**Minor** (nice to fix):
1. [Issue]: [Location] — [Impact]

### Recommended Actions
1. [Specific action to address critical issue]
2. [Next action]

### Verdict
[READY TO SUBMIT / NEEDS [X] FIXES / MAJOR REVISION NEEDED]
```

---

## Iteration Feedback Format

For template-maker iteration loops (machine-readable structure):

```
## Iteration Review: Round [N]

### Status: [CONTINUE / COMPLETE]

### Pass/Fail Summary
- Layout: [PASS/FAIL]
- Typography: [PASS/FAIL]
- Whitespace: [PASS/FAIL]
- Alignment: [PASS/FAIL]
- Color: [PASS/FAIL]
- ATS: [PASS/FAIL]

### Failures Requiring Adjustment

#### Issue 1: [Name]
- **Location**: [Where in document]
- **Problem**: [What's wrong]
- **Fix**: [Specific LaTeX adjustment]
```latex
% Suggested change
[code snippet]
```

#### Issue 2: [Name]
- **Location**: [Where in document]
- **Problem**: [What's wrong]
- **Fix**: [Specific LaTeX adjustment]

### Iteration Instruction
[If CONTINUE: "Adjust template with fixes above and recompile"]
[If COMPLETE: "Template passes all checks, ready for use"]
```

---

## Comparison Format

When reviewing multiple versions or templates:

```
## Template Comparison

### Versions Reviewed
1. [template1.pdf] - [description]
2. [template2.pdf] - [description]

### Side-by-Side Evaluation

| Aspect | Template 1 | Template 2 | Winner |
|--------|-----------|-----------|--------|
| Readability | [score] | [score] | [1/2/tie] |
| Visual Appeal | [score] | [score] | [1/2/tie] |
| Space Usage | [score] | [score] | [1/2/tie] |
| Industry Fit | [score] | [score] | [1/2/tie] |
| ATS Compat | [score] | [score] | [1/2/tie] |

### Recommendation
**Best for [use case]**: Template [N]
**Reasoning**: [Why this template wins for the stated purpose]

### Issues by Template

**Template 1**:
- [Issue if any]

**Template 2**:
- [Issue if any]
```

---

## Specific Issue Callouts

Use these formats when highlighting specific problems:

### Overflow Issue
```
**OVERFLOW DETECTED**
- Page: [N]
- Section: [Experience/Skills/etc.]
- Content cut: [What's missing]
- Fix: [Reduce content / Adjust spacing / Change format]
```

### Alignment Issue
```
**ALIGNMENT ISSUE**
- Element: [Dates/Bullets/Headers]
- Location: [Section or throughout]
- Expected: [Right-aligned/Left-aligned/Consistent]
- Actual: [What's happening]
- Fix: [Use hfill/tabular/etc.]
```

### Spacing Issue
```
**SPACING INCONSISTENCY**
- Between: [Sections/Items/Elements]
- Observed: [X pt here, Y pt there]
- Fix: [Standardize to Z pt / Use consistent command]
```

### Typography Issue
```
**TYPOGRAPHY PROBLEM**
- Element: [Name/Headers/Body/etc.]
- Issue: [Too small/Inconsistent/Wrong font]
- Current: [What it is]
- Recommended: [What it should be]
```

---

## Feedback Principles

1. **Be specific** — "Date on line 3 of Experience misaligned" not "dates look off"
2. **Be actionable** — Include how to fix, not just what's wrong
3. **Prioritize** — Critical issues first, minor issues last
4. **Be quantitative** — "12pt gap" not "big gap"
5. **Reference location** — Section, page, or line where issue occurs
6. **Suggest code** — Include LaTeX snippets for fixes when relevant

---

## Status Definitions

### Overall Verdicts
- **READY**: No critical or recommended fixes needed, safe to submit
- **NEEDS WORK**: Has recommended fixes, functional but could be better
- **REVISE**: Has critical issues, should not be submitted as-is

### Category Statuses
- **PASS**: Meets all criteria, no issues
- **WARN**: Minor issues, acceptable but not ideal
- **FAIL**: Critical issues that impact usability or appearance

### Iteration Statuses
- **CONTINUE**: Template needs more adjustments
- **COMPLETE**: Template meets all quality criteria
