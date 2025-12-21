#!/usr/bin/env python3
"""Review a resume PDF against the visual QA checklist.

This script provides structured output for resume PDF review, supporting both
human-readable and JSON formats for iteration with template-maker.

Usage:
    uv run scripts/review_pdf.py <resume.pdf> [--json] [--checklist]
    uv run scripts/review_pdf.py <resume.pdf> --compare <other.pdf>

Examples:
    uv run scripts/review_pdf.py resume.pdf
    uv run scripts/review_pdf.py resume.pdf --json > review.json
    uv run scripts/review_pdf.py resume.pdf --checklist
    uv run scripts/review_pdf.py template1.pdf --compare template2.pdf
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any


class Status(str, Enum):
    """Review status levels."""
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class Verdict(str, Enum):
    """Overall verdict levels."""
    READY = "READY"
    NEEDS_WORK = "NEEDS_WORK"
    REVISE = "REVISE"


class IterationStatus(str, Enum):
    """Iteration loop status."""
    CONTINUE = "CONTINUE"
    COMPLETE = "COMPLETE"


@dataclass
class Issue:
    """A specific issue found during review."""
    category: str
    severity: str  # critical, recommended, minor
    location: str
    problem: str
    fix: str = ""
    code_snippet: str = ""


@dataclass
class CategoryScore:
    """Score for a review category."""
    name: str
    status: Status
    notes: str = ""


@dataclass
class ReviewResult:
    """Complete review result."""
    pdf_path: str
    page_count: int = 0
    categories: list[CategoryScore] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    verdict: Verdict = Verdict.NEEDS_WORK
    iteration_status: IterationStatus = IterationStatus.CONTINUE
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "pdf_path": self.pdf_path,
            "page_count": self.page_count,
            "categories": [
                {"name": c.name, "status": c.status.value, "notes": c.notes}
                for c in self.categories
            ],
            "issues": [asdict(i) for i in self.issues],
            "verdict": self.verdict.value,
            "iteration_status": self.iteration_status.value,
            "summary": self.summary,
        }


def get_pdf_info(pdf_path: Path) -> dict[str, Any]:
    """Get basic info about a PDF file."""
    try:
        import pdfplumber
    except ImportError:
        print("Warning: pdfplumber not available, skipping PDF analysis", file=sys.stderr)
        return {"exists": pdf_path.exists(), "size_kb": 0, "pages": 0}

    if not pdf_path.exists():
        return {"exists": False, "size_kb": 0, "pages": 0}

    size_kb = pdf_path.stat().st_size / 1024

    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = len(pdf.pages)
            # Get first page dimensions
            if pages > 0:
                page = pdf.pages[0]
                width = page.width
                height = page.height
            else:
                width = height = 0

            return {
                "exists": True,
                "size_kb": round(size_kb, 1),
                "pages": pages,
                "width_pt": round(width, 1),
                "height_pt": round(height, 1),
            }
    except Exception as e:
        print(f"Warning: Could not read PDF: {e}", file=sys.stderr)
        return {"exists": True, "size_kb": round(size_kb, 1), "pages": 0}


def print_checklist() -> None:
    """Print the visual QA checklist for manual review."""
    checklist = """
## Visual QA Checklist

Use this checklist to evaluate the PDF manually:

### 1. Page Layout & Overflow
- [ ] Content fits within expected page count (1-2 pages)
- [ ] No text cut off at page edges
- [ ] No content overflowing into margins
- [ ] No orphaned section headers (header at bottom, content on next page)
- [ ] Page breaks occur at logical points

### 2. Typography & Readability
- [ ] Name is most prominent element
- [ ] Section headers clearly distinguished from body
- [ ] Body text is readable (minimum ~10pt)
- [ ] Line spacing aids readability
- [ ] Special characters render correctly (bullets, dashes)

### 3. Whitespace & Visual Balance
- [ ] Margins are consistent on all sides
- [ ] Consistent gaps between sections
- [ ] Bullet points have consistent indentation
- [ ] No random large gaps mid-page

### 4. Alignment & Structure
- [ ] Dates aligned consistently (all right-aligned, or all inline)
- [ ] Bullet points start at same indent level
- [ ] Same pattern used for all job entries
- [ ] Same pattern used for all education entries

### 5. Color & Contrast
- [ ] Text has sufficient contrast against background
- [ ] Color palette is cohesive (2-3 colors max)
- [ ] Would print acceptably in black and white

### 6. ATS Compatibility
- [ ] All text is selectable (not rendered as images)
- [ ] Copy-paste produces readable text
- [ ] Standard section headers (Experience, Education, Skills)
- [ ] Simple, parseable layout

### Scoring
For each category, assign:
- PASS: All critical checks pass
- WARN: Minor issues that should be addressed
- FAIL: Critical issues that must be fixed

### Overall Verdict
- READY: All PASS, ready to submit
- NEEDS_WORK: Has WARN items, review recommended
- REVISE: Has FAIL items, must fix before use
"""
    print(checklist)


def print_quick_review_template(pdf_path: Path, pdf_info: dict) -> None:
    """Print template for quick review."""
    template = f"""
## Quick Review: {pdf_path.name}

**PDF Info**: {pdf_info['pages']} page(s), {pdf_info['size_kb']} KB

**Overall**: [READY / NEEDS_WORK / REVISE]

**Strengths**:
- [What works well]
- [Another positive]

**Issues**:
- [Most critical issue]
- [Second issue if any]

**Recommendation**: [One sentence on next action]
"""
    print(template)


def print_full_review_template(pdf_path: Path, pdf_info: dict) -> None:
    """Print template for full review."""
    template = f"""
## Full Review: {pdf_path.name}

**PDF Info**: {pdf_info['pages']} page(s), {pdf_info['size_kb']} KB, {pdf_info.get('width_pt', 0)}x{pdf_info.get('height_pt', 0)} pt

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
[READY / NEEDS_WORK / REVISE]
"""
    print(template)


def print_iteration_template(pdf_path: Path, pdf_info: dict, round_num: int = 1) -> None:
    """Print template for iteration feedback."""
    template = f"""
## Iteration Review: Round {round_num}

**PDF**: {pdf_path.name} ({pdf_info['pages']} pages)

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
- **Fix**: [Specific Typst adjustment]
```typst
// Suggested change
[code snippet]
```

### Iteration Instruction
[If CONTINUE: "Adjust template with fixes above and recompile"]
[If COMPLETE: "Template passes all checks, ready for use"]
"""
    print(template)


def print_comparison_template(pdf1: Path, pdf2: Path, info1: dict, info2: dict) -> None:
    """Print template for comparing two PDFs."""
    template = f"""
## Template Comparison

### Versions Reviewed
1. {pdf1.name} - {info1['pages']} page(s), {info1['size_kb']} KB
2. {pdf2.name} - {info2['pages']} page(s), {info2['size_kb']} KB

### Side-by-Side Evaluation

| Aspect | {pdf1.stem} | {pdf2.stem} | Winner |
|--------|-----------|-----------|--------|
| Readability | [1-5] | [1-5] | [1/2/tie] |
| Visual Appeal | [1-5] | [1-5] | [1/2/tie] |
| Space Usage | [1-5] | [1-5] | [1/2/tie] |
| Industry Fit | [1-5] | [1-5] | [1/2/tie] |
| ATS Compat | [1-5] | [1-5] | [1/2/tie] |

### Recommendation
**Best for [use case]**: [Template name]
**Reasoning**: [Why this template wins]

### Issues by Template

**{pdf1.stem}**:
- [Issue if any]

**{pdf2.stem}**:
- [Issue if any]
"""
    print(template)


def create_empty_result(pdf_path: Path, pdf_info: dict) -> ReviewResult:
    """Create an empty review result with default categories."""
    categories = [
        CategoryScore("Layout", Status.WARN, "Pending review"),
        CategoryScore("Typography", Status.WARN, "Pending review"),
        CategoryScore("Whitespace", Status.WARN, "Pending review"),
        CategoryScore("Alignment", Status.WARN, "Pending review"),
        CategoryScore("Color", Status.WARN, "Pending review"),
        CategoryScore("ATS", Status.WARN, "Pending review"),
    ]

    return ReviewResult(
        pdf_path=str(pdf_path),
        page_count=pdf_info.get("pages", 0),
        categories=categories,
        issues=[],
        verdict=Verdict.NEEDS_WORK,
        iteration_status=IterationStatus.CONTINUE,
        summary="Review pending - fill in category scores and issues",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Review resume PDF against visual QA checklist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Output Formats:
  Default     Print full review template for manual completion
  --quick     Print quick review template
  --iteration Print iteration template for template-maker loop
  --json      Print empty JSON structure to fill in
  --checklist Print the complete visual QA checklist

Examples:
  uv run scripts/review_pdf.py resume.pdf
  uv run scripts/review_pdf.py resume.pdf --quick
  uv run scripts/review_pdf.py resume.pdf --iteration --round 2
  uv run scripts/review_pdf.py resume.pdf --json
  uv run scripts/review_pdf.py a.pdf --compare b.pdf
        """,
    )
    parser.add_argument("pdf", type=Path, help="PDF file to review")
    parser.add_argument(
        "--compare",
        type=Path,
        help="Compare with another PDF",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Print quick review template",
    )
    parser.add_argument(
        "--iteration",
        action="store_true",
        help="Print iteration template for template-maker",
    )
    parser.add_argument(
        "--round",
        type=int,
        default=1,
        help="Iteration round number (default: 1)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON structure",
    )
    parser.add_argument(
        "--checklist",
        action="store_true",
        help="Print the visual QA checklist",
    )

    args = parser.parse_args()

    # Validate PDF exists
    if not args.pdf.exists():
        print(f"Error: PDF not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    if not args.pdf.suffix.lower() == ".pdf":
        print(f"Error: Not a PDF file: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    # Get PDF info
    pdf_info = get_pdf_info(args.pdf)

    # Handle comparison mode
    if args.compare:
        if not args.compare.exists():
            print(f"Error: Comparison PDF not found: {args.compare}", file=sys.stderr)
            sys.exit(1)
        compare_info = get_pdf_info(args.compare)
        print_comparison_template(args.pdf, args.compare, pdf_info, compare_info)
        return

    # Handle checklist mode
    if args.checklist:
        print_checklist()
        return

    # Handle JSON output
    if args.json:
        result = create_empty_result(args.pdf, pdf_info)
        print(json.dumps(result.to_dict(), indent=2))
        return

    # Handle iteration mode
    if args.iteration:
        print_iteration_template(args.pdf, pdf_info, args.round)
        return

    # Handle quick mode
    if args.quick:
        print_quick_review_template(args.pdf, pdf_info)
        return

    # Default: full review template
    print_full_review_template(args.pdf, pdf_info)


if __name__ == "__main__":
    main()
