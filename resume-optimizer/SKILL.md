---
name: resume-optimizer
description: Optimize resume content for target roles with ATS optimization, impact quantification, and keyword alignment. Use when tailoring for job postings or adding metrics.
---

# Resume Optimizer

## Overview

Improve resume content through ATS optimization, impact quantification, keyword alignment, and content critique. Tailor resumes for specific target roles by analyzing job descriptions and recommending strategic improvements.

## Quick Start

### For Job-Specific Tailoring

1. Fetch or paste job description
2. Analyze requirements and identify keyword gaps
3. Tailor resume content to match job requirements
4. Apply ATS optimization and quantify impact

**See:** [Job Tailoring Guide](references/job-tailoring.md)

### For General Optimization

1. Run content quality review on all bullets
2. Add metrics and quantifiable results
3. Strengthen action verbs and remove weak language
4. Apply ATS optimization guidelines

**See:** [General Optimization Guide](references/general-optimization.md)

## Workflow Decision Tree

```
Start with resume YAML file
    ↓
Do you have a target job description?
    ↓
    ├─ YES → Job-Specific Tailoring
    │         ↓
    │         1. Analyze job posting
    │         2. Keyword gap analysis
    │         3. Tailor content (summary, bullets, skills)
    │         4. ATS optimization
    │         5. Quantify impact
    │
    └─ NO → General Optimization
              ↓
              1. Content quality review
              2. ATS optimization
              3. Quantify impact
              4. Strengthen language
```

## Job-Specific Tailoring

### 1. Analyze Job Posting

**Fetch from URL:**
```bash
uv run scripts/fetch_job_posting.py "<job_url>" --output job_description.txt
```

**Or use pasted text:**
Save directly to `job_description.txt`

**Extract:**
- Required qualifications (must-have skills, experience, education)
- Preferred qualifications (nice-to-have)
- Key responsibilities and deliverables
- Priority keywords (mentioned multiple times or in title)

**Detailed guide:** [Job Tailoring Guide](references/job-tailoring.md)

### 2. Keyword Gap Analysis

Compare resume against job description:

- **Critical gaps:** Required qualifications you have but didn't mention
- **Easy additions:** Skills you have matching preferred qualifications
- **Terminology mismatches:** Same skill, different wording (e.g., "ML" vs "Machine Learning")
- **True gaps:** Required qualifications you don't have (note but don't fabricate)

Prioritize adding critical keywords to Skills section and integrating into achievement bullets.

### 3. Tailor Content

**Professional Summary:**
- Mirror language from job description
- Highlight most relevant experience
- Include target job title or similar phrasing
- Feature 2-3 top required skills

**Experience Bullets:**
- Reorder to prioritize most relevant achievements first
- Rewrite to incorporate job description keywords
- Emphasize experiences matching target role responsibilities

**Skills Section:**
- Promote required skills to top of categories
- Add missing keywords (if you have the skill)
- Group similar technologies mentioned in job

**Examples:** [Optimization Examples](references/examples.md)

## ATS Optimization

### Quick ATS Checklist

**Section headers:**
- [ ] Use standard headers (Experience, Education, Skills, Summary)
- [ ] Avoid creative or unusual section names

**Keywords:**
- [ ] Include exact phrases from job description
- [ ] List acronyms AND spelled-out versions (e.g., "Natural Language Processing (NLP)")
- [ ] Feature high-priority skills in Skills section
- [ ] Integrate keywords naturally in achievement bullets

**Formatting:**
- [ ] Simple, clean structure (no tables, columns, text boxes)
- [ ] Standard fonts
- [ ] Contact info at top (not in header/footer)
- [ ] Consistent date formatting
- [ ] Plain bullet points (•, -, or ◦)

**Content structure:**
- [ ] Reverse chronological experience
- [ ] Clear company names, job titles, dates
- [ ] Action verbs starting each bullet
- [ ] Quantified achievements

**Comprehensive guide:** [ATS Guidelines](references/ats_guidelines.md)

### Keyword Integration Tiers

**Tier 1 (required skills):**
- Add to Skills section if missing
- Mention in Professional Summary
- Incorporate into 2-3 achievement bullets

**Tier 2 (preferred skills):**
- Add to Skills section if missing
- Mention in at least 1 achievement bullet

**Tier 3 (nice-to-have):**
- Add to Skills section if relevant

## Quantify Impact

### Impact Formula

```
[Action Verb] + [What You Did] + [How You Did It] + [Measurable Result]
```

### Metric Categories

Add at least one metric from these categories to each bullet:

- **Time/Speed:** Reduced X from [time] to [time], improved by X%
- **Cost/Revenue:** Saved $X, generated $X revenue, reduced costs by X%
- **Scale/Volume:** Processed X items, scaled to X requests, served X users
- **Quality/Accuracy:** Improved accuracy from X% to Y%, reduced errors by X%
- **Team/Adoption:** Led team of X, adopted by X teams, onboarded X users
- **Efficiency:** Automated X% of process, eliminated X hours of manual work

**If exact metrics unavailable:**
- Estimate based on scope: "~500K users", "10M+ requests"
- Compare to baseline: "3x faster than previous approach"
- Describe scale: "across 15+ microservices"

**Detailed patterns:** [Impact Patterns](references/impact_patterns.md)

## Action Verb Strengthening

Replace weak verbs:
- "Helped" → "Enabled", "Facilitated"
- "Worked on" → "Developed", "Built", "Implemented"
- "Responsible for" → "Owned", "Managed", "Led"
- "Participated in" → "Contributed to", "Collaborated on"

**Full list:** [Action Verbs](references/action_verbs.yaml)

## General Content Review

### Quality Checklist

**For each experience bullet:**
- [ ] Starts with strong action verb
- [ ] Includes what you did AND how you did it
- [ ] Contains at least one metric or quantifiable result
- [ ] Is specific (not vague)
- [ ] Is concise (1-2 lines maximum)
- [ ] Demonstrates impact (not just activities)

**For Professional Summary:**
- [ ] 2-4 sentences
- [ ] Highlights years of experience and seniority level
- [ ] Mentions 3-5 core competencies
- [ ] Includes industry/domain context

**For Skills section:**
- [ ] Organized by logical categories
- [ ] Most important skills listed first
- [ ] Specific (not "Programming" but "Python, Java, Go")
- [ ] No outdated technologies

**Detailed guide:** [General Optimization](references/general-optimization.md)

### Common Issues

**Weak bullets (activity-focused):**
❌ "Worked on machine learning models"
✅ "Developed GBM churn model achieving 0.84 AUC, reducing churn by 15% and retaining $5M ARR"

**Vague impact:**
❌ "Improved system performance"
✅ "Reduced API response time from 800ms to 120ms through Redis caching"

**Missing context:**
❌ "Built data pipeline"
✅ "Built PySpark ETL pipeline processing 50M+ daily transactions with 99.9% data quality"

**More examples:** [Optimization Examples](references/examples.md)

## Resume Length Guidelines

- **Early career (0-5 years):** 1 page
- **Mid-career (5-10 years):** 1-2 pages
- **Senior/Staff (10+ years):** 2 pages
- **Executive:** 2-3 pages

**Bullet count per role:**
- Current role: 4-6 bullets
- Recent roles (last 5 years): 3-5 bullets
- Older roles (5-10 years ago): 2-3 bullets
- Very old roles (10+ years ago): 1-2 bullets or consolidate

## Final Optimization Checklist

**Content:**
- [ ] All bullets start with strong action verbs
- [ ] Every bullet includes measurable impact when possible
- [ ] Professional summary is tailored and compelling
- [ ] Skills section highlights most relevant capabilities
- [ ] No weak, vague, or passive language
- [ ] Appropriate length for experience level

**ATS Optimization:**
- [ ] Standard section headers throughout
- [ ] Keywords from job description integrated naturally
- [ ] Simple, clean formatting
- [ ] Contact info at top
- [ ] Consistent formatting

**Target Role Alignment (if applicable):**
- [ ] Keywords from job description present in resume
- [ ] Professional summary mirrors job requirements
- [ ] Most relevant experience highlighted first
- [ ] Skills section prioritizes target role requirements
- [ ] Language and terminology matches job description

## Output

Provide optimized YAML resume file with:
1. Updated professional summary
2. Reordered and rewritten experience bullets
3. Enhanced skills section
4. Added metrics and impact quantification
5. ATS-optimized formatting
6. Summary of changes made and rationale

## Reference Documentation

- [Job Tailoring Guide](references/job-tailoring.md) - Detailed job-specific optimization
- [General Optimization Guide](references/general-optimization.md) - Content quality and best practices
- [ATS Guidelines](references/ats_guidelines.md) - Comprehensive ATS requirements
- [Impact Patterns](references/impact_patterns.md) - Templates for quantifying achievements
- [Action Verbs](references/action_verbs.yaml) - Strong verbs categorized by impact type
- [Optimization Examples](references/examples.md) - Before/after transformations
