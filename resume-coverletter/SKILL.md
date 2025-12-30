---
name: resume-coverletter
description: Generate professional cover letters matching resume templates. Use when creating cover letters for job applications, matching resume styling and branding.
---

# Resume Cover Letter Generator

## Overview

Generate professional cover letters that match your resume's design language. Choose from templates that align with resume styles (executive, tech-modern, generic) or create custom letters for specific companies and roles.

## Quick Start

```bash
# Generate cover letter from resume YAML + job description
uv run scripts/generate_cover_letter.py resume.yaml \
  --template tech-modern-cover \
  --company "Block" \
  --position "Outsourcing Program Manager" \
  --job-file job_description.txt \
  --output cover_letter.typ

# Compile to PDF
uv run scripts/compile_cover_letter.py cover_letter.typ --output cover_letter.pdf
```

## Available Templates

**tech-modern-cover**
- Best for: Modern tech/creative roles
- Style: Deep lavender palette, Carlito font
- Matches: tech-modern resume template
- Features: Contemporary professional aesthetic

**executive-cover**
- Best for: Professional/executive roles
- Style: Navy/blue accents, Inter font
- Matches: executive resume template
- Features: Clean, traditional professional layout

**generic-cover**
- Best for: Reusable letters, industry-agnostic
- Style: Neutral, adaptable design
- Matches: Any resume template
- Features: Flexible content structure

## Workflow

### 1. Generate Cover Letter

```bash
uv run scripts/generate_cover_letter.py <resume.yaml> \
  --template <template_name> \
  --company "Company Name" \
  --position "Job Title" \
  [--job-file job_description.txt] \
  [--output cover_letter.typ]
```

**Parameters:**
- `resume.yaml`: Source resume data (uses contact info, experience, skills)
- `--template`: Cover letter template (tech-modern-cover, executive-cover, generic-cover)
- `--company`: Target company name (optional for generic)
- `--position`: Job title/position (optional for generic)
- `--job-file`: Job description text file for context (optional)
- `--output`: Output .typ file path (default: stdout)

**Examples:**

```bash
# Company-specific letter with job description
uv run scripts/generate_cover_letter.py resume.yaml \
  --template executive-cover \
  --company "Acme Corp" \
  --position "Senior Manager" \
  --job-file job_acme.txt \
  --output cover_acme.typ

# Generic letter (no specific company)
uv run scripts/generate_cover_letter.py resume.yaml \
  --template generic-cover \
  --output cover_generic.typ

# Tech role with job URL (fetch job description first)
uv run .claude/skills/resume-optimizer/scripts/fetch_job_posting.py \
  "https://jobs.company.com/123" --output job.txt
uv run scripts/generate_cover_letter.py resume.yaml \
  --template tech-modern-cover \
  --company "Tech Startup" \
  --position "Engineering Manager" \
  --job-file job.txt \
  --output cover_tech.typ
```

### 2. Compile to PDF

```bash
uv run scripts/compile_cover_letter.py <cover_letter.typ> [--output <output.pdf>]
```

**Example:**
```bash
uv run scripts/compile_cover_letter.py cover_acme.typ --output cover_acme.pdf
```

### 3. Review and Iterate

After compilation:
1. Review PDF for layout, spacing, content flow
2. Check contact info matches resume exactly
3. Verify company-specific details are accurate
4. Ensure single-page format
5. Test text extraction (copy-paste from PDF)

To revise:
1. Regenerate .typ with adjusted parameters
2. Recompile to PDF
3. Review again

## Content Strategy

### Opening Paragraph
- Express specific interest in the role/company
- Briefly state years of experience and core expertise
- Connect your background to the role's requirements

### Body Paragraphs (2-3)
- Highlight 3-5 key achievements from resume
- Use metrics and quantifiable impact
- Map your experience to job requirements
- Show cross-functional collaboration
- Demonstrate industry knowledge

### Closing Paragraph
- Reinforce enthusiasm for the opportunity
- Summarize unique value proposition
- Call to action (discuss further, interview request)
- Thank the reader

### Best Practices
- Keep to one page (600-800 words max)
- Use active voice and strong action verbs
- Mirror language from job description
- Balance confidence with humility
- Avoid generic phrases ("I am writing to apply...")
- Customize for each company/role

## Template Selection Guide

| Resume Template | Matching Cover Letter |
|----------------|---------------------|
| executive | executive-cover |
| tech-modern | tech-modern-cover |
| modern-dense | executive-cover or tech-modern-cover |
| compact | executive-cover |
| minimal | executive-cover or generic-cover |

**Auto-detection**: Script will detect resume template from YAML metadata (if present) and suggest matching cover letter template.

## Prerequisites

**Typst Installation:**
```bash
# macOS
brew install typst

# Linux
cargo install typst-cli

# Windows
winget install --id Typst.Typst
```

**Verify:**
```bash
typst --version
```

## Integration with Other Skills

**Complete application workflow:**

1. **State**: Use `resume-state` to manage resume versions
2. **Extract**: Use `resume-extractor` to convert resume to YAML
3. **Optimize**: Use `resume-optimizer` to tailor resume for target role
4. **Format**: Use `resume-formatter` to generate resume PDF
5. **Cover Letter**: Use `resume-coverletter` (this skill) to generate matching cover letter
6. **Review**: Review both documents together for consistency

**Job application package:**
```bash
# Optimize resume for role
uv run .claude/skills/resume-optimizer/scripts/fetch_job_posting.py \
  "<job_url>" --output job.txt

# Generate resume PDF
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py \
  resume.yaml tech-modern --output resume.typ
uv run .claude/skills/resume-formatter/scripts/compile_typst.py \
  resume.typ --output resume.pdf

# Generate matching cover letter
uv run scripts/generate_cover_letter.py resume.yaml \
  --template tech-modern-cover \
  --company "Target Company" \
  --position "Target Role" \
  --job-file job.txt \
  --output cover_letter.typ
uv run scripts/compile_cover_letter.py \
  cover_letter.typ --output cover_letter.pdf
```

## Tips for Best Results

**Content:**
1. Extract top 3-5 achievements from resume
2. Quantify impact with metrics
3. Use job description keywords naturally
4. Show understanding of company/industry
5. Be specific about why this role/company

**Formatting:**
1. Match cover letter template to resume template
2. Ensure contact info is identical to resume
3. Keep to single page
4. Use consistent date formats
5. Test PDF text extraction

**Customization:**
1. Research company before writing
2. Reference specific company initiatives/values
3. Tailor achievements to role requirements
4. Adjust tone for industry (formal vs. creative)
5. Proofread for company-specific details

## Troubleshooting

**Template not found:** Check available templates with `ls assets/templates/` or use one of: tech-modern-cover, executive-cover, generic-cover

**Contact info mismatch:** Ensure resume YAML has complete contact section matching your actual resume

**Content overflow:** Reduce achievements to 3-5 key points; aim for 600-800 words total

**Typst compile errors:** Check `typst --version`; escape special characters in YAML

**Generic vs. specific:** Use generic template for reusable letters; use company-specific for targeted applications
