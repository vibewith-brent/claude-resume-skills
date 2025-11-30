# Resume Helper Skills for Claude Code

Three professional skills for extracting, optimizing, and formatting resumes with Claude Code on macOS.

## Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/yourusername/resume_helper.git
cd resume_helper

# 2. Install prerequisites (one-time setup)
brew install --cask mactex

# 3. Open Claude Code in this directory
# Skills are automatically loaded and ready to use!
```

## What This Does

- **Extract** PDF/DOCX resumes to editable YAML format
- **Optimize** content with ATS compatibility, metrics, and keyword alignment
- **Format** professional PDFs with 4 designer templates

## Prerequisites (macOS)

### Required

1. **Claude Code** - Download from [claude.ai/claude-code](https://claude.ai/claude-code)
2. **uv** (Python package manager) - Automatically installed by Claude Code
3. **MacTeX** (for PDF generation):
   ```bash
   brew install --cask mactex
   ```

   After installation, verify:
   ```bash
   pdflatex --version
   ```

   > **Note:** MacTeX is ~4GB. For minimal install (100MB): `brew install --cask mactex-no-gui`

### Auto-Installed

These Python packages install automatically when you use the skills:
- `pdfplumber`, `python-docx` (extractor)
- `pyyaml`, `requests`, `beautifulsoup4` (optimizer)
- `jinja2`, `pyyaml` (formatter)

## Installation

### Option 1: Install via Plugin Marketplace (Easiest)

Register this repository as a Claude Code plugin marketplace:

```
/plugin marketplace add yourusername/resume_helper
```

Then install the resume skills:

```
/plugin install resume-skills
```

All three skills (extractor, optimizer, formatter) will be available globally in any Claude Code project.

### Option 2: Clone and Use Locally

```bash
git clone https://github.com/yourusername/resume_helper.git
cd resume_helper
```

Open Claude Code in this directory. Skills load automatically from `.claude/skills/`.

### Option 3: Install Globally (Manual)

To use these skills in any Claude Code project:

```bash
# Unzip skills to Claude's global directory
unzip resume-extractor.skill -d ~/Library/Application\ Support/Claude/skills/resume-extractor
unzip resume-optimizer.skill -d ~/Library/Application\ Support/Claude/skills/resume-optimizer
unzip resume-formatter.skill -d ~/Library/Application\ Support/Claude/skills/resume-formatter
```

## How to Use

Just talk to Claude Code in natural language. The skills activate automatically based on your request.

### Extract Resume from PDF

```
"Extract my resume from resume.pdf to YAML format"
```

Claude will:
1. Extract text from your PDF
2. Parse into structured YAML
3. Save as `firstname_lastname_resume.yaml`

### Optimize Resume

```
"Optimize my resume: add metrics, strengthen bullets, ensure ATS compatibility"
```

Claude will:
1. Review bullets for weak verbs
2. Add quantifiable metrics
3. Apply ATS guidelines
4. Update professional summary
5. Provide improved YAML

### Tailor for Job

```
"Tailor my resume for this job: [paste job URL]"
```

Claude will:
1. Analyze job requirements
2. Identify keyword gaps
3. Reorder and rewrite bullets
4. Integrate relevant keywords
5. Provide job-specific YAML

### Generate PDF

```
"Convert my resume YAML to PDF using the modern template"
```

Claude will:
1. Convert YAML to LaTeX
2. Compile to PDF
3. Provide polished resume

## Available Templates

| Template | Best For | Style |
|----------|----------|-------|
| **modern** | Tech, AI/ML, Software | Clean sans-serif, blue accents, minimalist |
| **creative** | Design, Marketing, Startups | Bold blue header, colorful sections |
| **classic** | Finance, Law, Consulting | Traditional serif, conservative |
| **academic** | Research, Academia, Science | Education-first, publication-focused |

### Template Examples

```
# Generate single template
"Generate PDF with modern template"

# Compare all templates
"Generate PDFs with all 4 templates so I can compare"

# Get recommendation
"Which template is best for AI engineering roles at tech companies?"
```

## Complete Workflow Example

Start with a PDF resume and create a tailored version:

```
1. "Extract my resume from old_resume.pdf"
   → Creates old_resume.yaml

2. "Optimize this resume for better ATS compatibility and add metrics"
   → Provides optimized_resume.yaml

3. "Tailor my resume for this Senior AI Engineer role at Google: [job URL]"
   → Provides google_resume.yaml

4. "Generate PDF with modern template"
   → Creates google_resume.pdf
```

## Direct Command Reference

If you prefer running commands directly:

### Extract PDF to YAML
```bash
uv run --with pdfplumber resume-extractor/scripts/extract_pdf.py your_resume.pdf
```

### Extract DOCX to YAML
```bash
uv run --with python-docx resume-extractor/scripts/extract_docx.py your_resume.docx
```

### Validate YAML Structure
```bash
uv run --with pyyaml resume-optimizer/scripts/validate_yaml.py resume.yaml
```

### Generate PDF from YAML
```bash
# Step 1: Convert YAML to LaTeX
uv run --with jinja2 --with pyyaml \
  resume-formatter/scripts/yaml_to_latex.py \
  resume.yaml \
  modern \
  -o resume.tex

# Step 2: Compile LaTeX to PDF
uv run resume-formatter/scripts/compile_latex.py \
  resume.tex \
  -o resume.pdf
```

### One-Liner PDF Generation
```bash
uv run --with jinja2 --with pyyaml resume-formatter/scripts/yaml_to_latex.py resume.yaml modern -o resume.tex && uv run resume-formatter/scripts/compile_latex.py resume.tex -o resume.pdf
```

## File Structure

```
resume_helper/
├── README.md                          # This file
├── brent_skoumal_resume.yaml          # Example resume in YAML format
│
├── resume-extractor.skill             # Packaged skill (ZIP)
├── resume-optimizer.skill             # Packaged skill (ZIP)
├── resume-formatter.skill             # Packaged skill (ZIP)
│
├── resume-extractor/
│   ├── SKILL.md                       # Skill instructions
│   ├── scripts/
│   │   ├── extract_pdf.py
│   │   └── extract_docx.py
│   └── references/
│       └── resume_schema.yaml
│
├── resume-optimizer/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── validate_yaml.py
│   │   └── fetch_job_posting.py
│   └── references/
│       ├── ats_guidelines.md
│       ├── impact_patterns.md
│       ├── action_verbs.yaml
│       ├── job-tailoring.md
│       ├── general-optimization.md
│       └── examples.md
│
└── resume-formatter/
    ├── SKILL.md
    ├── scripts/
    │   ├── yaml_to_latex.py
    │   └── compile_latex.py
    ├── references/
    │   ├── theme_guide.md
    │   ├── troubleshooting.md
    │   └── examples.md
    └── assets/
        └── templates/
            └── latex/
                ├── modern_custom.tex.j2      # Modern with Source Sans Pro
                ├── creative.tex.j2           # Bold blue header design
                ├── classic.tex.j2            # Traditional layout
                └── academic.tex.j2           # Research-focused
```

## Troubleshooting

### Skills Not Loading

1. **Verify you're in the correct directory:**
   ```bash
   pwd  # Should show /path/to/resume_helper
   ls .claude/skills/  # Should show three skill directories
   ```

2. **Restart Claude Code:**
   - Close Claude Code completely
   - Navigate to `resume_helper` directory in Terminal
   - Open Claude Code from here

3. **Ask Claude Code:**
   ```
   "What skills do you have available?"
   ```

### pdflatex Not Found

If you see "pdflatex not found" error:

1. **Install MacTeX:**
   ```bash
   brew install --cask mactex
   ```

2. **Verify installation:**
   ```bash
   pdflatex --version
   ```

3. **If still not found, add to PATH:**
   ```bash
   export PATH="/Library/TeX/texbin:$PATH"
   ```

### LaTeX Compilation Errors

Common issues and solutions:

**Missing packages:**
```bash
# Reinstall with full LaTeX
brew uninstall --cask mactex-no-gui
brew install --cask mactex
```

**Content too long:**
- Use resume-optimizer to condense content
- Aim for 1-2 pages maximum
- Remove older or less relevant positions

**Font issues:**
- Source Sans Pro is included with MacTeX
- If errors persist, use `classic` template (uses standard fonts)

### YAML Validation Errors

Validate your YAML structure:

```bash
uv run --with pyyaml resume-optimizer/scripts/validate_yaml.py resume.yaml
```

Common issues:
- Missing required fields (name, email)
- Invalid YAML syntax (check indentation)
- Empty sections
- Weak action verbs

## Best Practices

### Content

- **Quantify everything:** Add metrics to all achievements
- **Action verbs:** Start bullets with powerful verbs (Architected, Delivered, Increased)
- **Keywords:** Match exact terminology from job descriptions
- **Concise:** 1-2 pages maximum
- **ATS-friendly:** Use standard headers, simple structure

### Workflow

1. **Keep YAML master:** Edit resume.yaml, generate PDFs as needed
2. **Version control:** Save YAML versions for different roles
3. **File naming:** Use `firstname_lastname_company.pdf` format
4. **Verify PDFs:** Always review generated PDF before submitting
5. **Test ATS:** Run `pdftotext resume.pdf` to verify text extraction

### Template Selection

- **Tech/AI/ML:** Modern template (clean, contemporary)
- **Finance/Consulting:** Classic template (traditional)
- **Design/Marketing:** Creative template (bold, visual)
- **Academia/Research:** Academic template (education-first)
- **Startups:** Modern or Creative templates

## Example YAML Resume

See `brent_skoumal_resume.yaml` for a complete example with:
- Professional summary
- 10+ years of experience
- Skills organized by category
- Multiple degrees
- Proper YAML structure

## Tips for Best Results

### Using Claude Code

1. **Be specific:** "Add metrics to my Sony role" is better than "improve resume"
2. **Iterate:** Ask Claude to refine specific sections
3. **Compare:** Generate multiple template PDFs to see what works best
4. **Validate:** Use the validation script before formatting

### ATS Optimization

1. **Standard headers:** Use "Experience", "Education", "Skills"
2. **Simple formatting:** Avoid tables, columns, graphics
3. **Keywords:** Mirror job description language
4. **File format:** Submit PDF (most compatible)
5. **Test extraction:** Verify text copies correctly from PDF

### Job Tailoring

1. **Read job description carefully:** Note required skills, keywords
2. **Identify gaps:** Ask Claude to find missing keywords
3. **Reorder bullets:** Put most relevant achievements first
4. **Update summary:** Align with specific role requirements
5. **Verify keywords:** Ensure exact matches for critical terms

## Support

For issues or questions:

1. **Check skill documentation:** Each skill has detailed SKILL.md
2. **Review references:** See `references/` directories for guides
3. **Validate YAML:** Use validation script to check structure
4. **Troubleshooting:** See troubleshooting section above
5. **Open issue:** Report bugs on GitHub

## Version History

### v1.0.0 (Current)
- Modern custom template with Source Sans Pro typography
- Enhanced color palette and font weight hierarchy
- All 4 templates fully functional and ATS-compatible
- Automatic MacTeX PATH detection for macOS
- Comprehensive troubleshooting guides
- YAML validation script
- Progressive disclosure with reference files

## License

MIT License - See LICENSE file for details.

LaTeX templates use standard packages and are freely available for personal and commercial use.

---

**Built with Claude Code**

Ready to optimize your resume? Clone this repo, open Claude Code, and start the conversation!
