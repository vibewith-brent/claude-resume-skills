---
name: resume-extractor
description: Extract PDF/DOCX resumes to structured YAML format. Use when converting resume documents to YAML, importing existing resumes, or beginning resume workflows. Supports pdfplumber (PDF) and python-docx (DOCX).
license: MIT
metadata:
  version: 1.0.0
allowed-tools:
  - Bash(uv run:*)
  - Read
  - Write
---

# Resume Extractor

## Overview

Extract resume content from PDF or DOCX files and convert to structured YAML format for easy editing and manipulation. This skill provides the foundation for resume optimization and formatting workflows.

## Workflow

### 1. Extract Text from Resume

**For PDF resumes:**

Run the PDF extraction script to extract all text content:

```bash
uv run scripts/extract_pdf.py resume.pdf
```

Save extracted text to a file for further processing:

```bash
uv run scripts/extract_pdf.py resume.pdf --output extracted_text.txt
```

**For DOCX resumes:**

Run the DOCX extraction script:

```bash
uv run scripts/extract_docx.py resume.docx
```

Save extracted text:

```bash
uv run scripts/extract_docx.py resume.docx --output extracted_text.txt
```

### 2. Parse Extracted Text to YAML

After extracting text, parse it into structured YAML format following the resume schema. This step requires LLM assistance to understand the structure and map content to the appropriate YAML fields.

**Parsing instructions:**

1. Read the extracted text carefully
2. Identify major sections (contact, summary, experience, education, skills, etc.)
3. Map content to the YAML schema defined in `references/resume_schema.yaml`
4. Preserve all important information while organizing it logically
5. Use consistent formatting for dates, bullet points, and sections
6. Include metrics and quantifiable achievements exactly as written

**Schema reference:**

See `references/resume_schema.yaml` for the complete YAML structure including:
- Required fields (contact, summary, experience, education, skills)
- Optional fields (certifications, projects, publications, awards, languages, volunteer)
- Formatting guidelines and examples
- Best practices for YAML syntax

### 3. Validate and Refine

After creating the initial YAML:

1. Verify all sections from the original resume are captured
2. Check that contact information is complete and accurate
3. Ensure dates are in consistent format
4. Confirm achievement bullets start with action verbs
5. Validate YAML syntax (proper indentation, quotes, structure)

**Common validation checks:**

- Are company names, titles, and dates accurate?
- Are all technical skills captured in appropriate categories?
- Is the professional summary complete?
- Are there any missing sections from the original?
- Does the YAML parse without syntax errors?

### 4. Save YAML Resume

Save the parsed YAML to a file with a descriptive name:

```yaml
# Example filename: firstname_lastname_resume.yaml
```

## Tips for Quality Extraction

**Handling complex layouts:**
- PDF resumes with multi-column layouts may extract text in unexpected order
- Review extracted text carefully and reorganize during YAML parsing
- Tables in PDFs may require manual reconstruction

**Preserving formatting:**
- Bold, italic, and other formatting is lost during text extraction
- Focus on capturing content structure rather than visual styling
- Formatting will be reapplied during the Typst generation step

**Dealing with incomplete extraction:**
- If critical information is missing, read the original PDF/DOCX directly
- Some PDFs use images for text (not extractable) - may need manual entry
- Scanned PDFs require OCR preprocessing

**Date format normalization:**
- Original resumes may use inconsistent date formats
- Standardize to one format during YAML creation (e.g., "Jan 2020 - Dec 2022")
- Use "Present" for current positions

## Next Steps

After extracting resume to YAML:

1. **Edit and refine**: Use a text editor to make manual corrections to the YAML
2. **Optimize content**: Use the `resume-optimizer` skill to improve bullets, add metrics, and tailor for specific roles
3. **Format for output**: Use the `resume-formatter` skill to convert YAML to professionally formatted PDF
