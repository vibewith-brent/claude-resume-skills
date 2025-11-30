# Job-Specific Resume Tailoring Guide

## Table of Contents
- [Job Description Analysis](#job-description-analysis)
- [Keyword Gap Analysis](#keyword-gap-analysis)
- [Tailoring Resume Content](#tailoring-resume-content)
- [Integration Strategy](#integration-strategy)

## Job Description Analysis

### From URL

Fetch job posting content from URL (LinkedIn, Indeed, company career pages):

```bash
uv run scripts/fetch_job_posting.py "<job_url>" --output job_description.txt
```

Review the extracted content to ensure it captured the job description (not just navigation/boilerplate).

### From Pasted Text

If user provides job description text directly:
1. Save to file: `job_description.txt`
2. Proceed to analysis

### Analysis Tasks

Extract and document:

**1. Required qualifications:**
- Years of experience
- Must-have technical skills and tools
- Required education/certifications
- Domain expertise requirements

**2. Preferred qualifications:**
- Nice-to-have skills
- Bonus technologies
- Preferred experience areas

**3. Key responsibilities:**
- Primary job functions
- Day-to-day activities
- Major deliverables

**4. Company/team context:**
- Team size and structure
- Tech stack
- Industry/domain
- Company stage and culture

**5. Priority keywords:**
- Skills mentioned multiple times (highest priority)
- Skills in job title or first paragraph (high priority)
- Specific tools/technologies/frameworks
- Industry-specific terminology

## Keyword Gap Analysis

Compare resume content against job description:

**1. Identify keyword gaps:**
- Required skills missing from resume
- Important technologies not mentioned
- Relevant experience not highlighted
- Industry terms not used

**2. Categorize gaps:**
- **Critical gaps:** Required qualifications you have but didn't mention
- **Easy additions:** Skills you have that match preferred qualifications
- **Terminology mismatches:** Same skill, different wording (e.g., "ML" vs "Machine Learning")
- **True gaps:** Required qualifications you don't have (note but don't fabricate)

**3. Prioritize additions:**
- Add critical missing keywords to Skills section
- Incorporate important terms into existing achievement bullets
- Update Professional Summary to echo job description language
- Consider adding relevant projects if they demonstrate key skills

## Tailoring Resume Content

### Professional Summary Tailoring

Rewrite summary to:
- Mirror language from job description
- Highlight most relevant experience for this role
- Include target job title or similar phrasing
- Feature 2-3 top required skills
- Maintain 2-4 sentence length

**Example transformation:**

*Original:*
> Senior Data Scientist with 8 years of experience in ML and analytics across various industries.

*Tailored for Staff AI Engineer role:*
> Staff-level AI Systems Engineer with 8+ years architecting production ML and GenAI systems including agentic workflows, RAG, and multi-agent orchestration. Proven expertise deploying LLMs at scale with robust observability, safety filters, and governance while driving cross-functional stakeholder alignment in gaming and FinTech.

### Experience Bullets Tailoring

For each relevant role:
1. Reorder bullets to prioritize most relevant achievements first
2. Rewrite bullets to incorporate job description keywords
3. Emphasize experiences matching target role responsibilities
4. De-emphasize or remove bullets less relevant to target role

**Example transformation:**

*Original bullet:*
> Built ML models for customer segmentation

*Tailored for GenAI Engineer role:*
> Architected multi-agent GenAI workflow with retrieval-augmented generation and tool-calling patterns to automate customer segmentation, reducing manual analysis time by 70%

### Skills Section Tailoring

Reorganize skills to:
- Promote required skills to top of relevant categories
- Add missing keywords (if you have the skill)
- Group similar technologies mentioned in job description
- Remove or de-emphasize less relevant skills

## Integration Strategy

### Keyword Integration by Tier

**Tier 1 keywords (required skills):**
- Add to Skills section if missing
- Mention in Professional Summary
- Incorporate into 2-3 achievement bullets

**Tier 2 keywords (preferred skills):**
- Add to Skills section if missing
- Mention in at least 1 achievement bullet

**Tier 3 keywords (nice-to-have):**
- Add to Skills section if relevant and you have experience

### Integration Examples

*Job requires: "Experience with LangChain, vector databases, and prompt engineering"*

- Skills section: Add "LangChain, LlamaIndex, Pydantic AI Agents" and "Vector stores (FAISS, Pinecone, Weaviate)"
- Summary: "Experienced in architecting RAG systems with LangChain and vector databases"
- Bullet: "Built RAG pipeline using LangChain and Pinecone vector store, implementing prompt engineering techniques to improve response accuracy by 30%"
