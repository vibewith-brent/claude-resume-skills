# Resume Helper Skills for Claude Code

Professional resume management suite for Claude Code: extract from PDF/DOCX, optimize for ATS and target roles, format to professional PDFs with 4 designer templates.

## Features

- **Extract**: Convert PDF/DOCX resumes to structured, editable YAML format
- **Optimize**: Enhance content with ATS compatibility, quantifiable metrics, and keyword alignment
- **Format**: Generate professional PDFs with 4 industry-optimized LaTeX templates

## Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/vibewith-brent/claude-resume-skills.git
cd claude-resume-skills

# 2. Install MacTeX (required for PDF generation)
brew install --cask mactex

# 3. Open Claude Code in this directory
# Skills auto-load from .claude/skills/ and are ready to use
```

## Prerequisites

### Required

1. **Claude Code** - Download from [claude.ai/claude-code](https://claude.ai/claude-code)
2. **MacTeX** (for PDF generation):
   ```bash
   brew install --cask mactex
   ```

   Verify installation:
   ```bash
   pdflatex --version
   ```

   > **Note:** MacTeX is ~4GB. For minimal install: `brew install --cask mactex-no-gui` (100MB)

### Auto-Installed

- **uv** - Python package manager (installed by Claude Code)
- **Python packages** - Defined in `pyproject.toml`, installed automatically via `uv sync`:
  - `pdfplumber`, `python-docx` (extractor)
  - `pyyaml`, `requests`, `beautifulsoup4` (optimizer)
  - `jinja2`, `pyyaml` (formatter)

## Installation

### Option 1: Plugin Marketplace (Recommended)

Register this repo as a Claude Code plugin marketplace:

```
/plugin marketplace add vibewith-brent/claude-resume-skills
```

Install the resume skills bundle:

```
/plugin install resume-skills
```

All three skills are now available globally in any Claude Code project.

### Option 2: Local Development

Clone and use locally for development or customization:

```bash
git clone https://github.com/vibewith-brent/claude-resume-skills.git
cd claude-resume-skills
```

Open Claude Code in this directory. Skills auto-load from `.claude/skills/`.

### Option 3: Manual Global Install

Install skills globally by unzipping to Claude's skills directory:

```bash
unzip resume-extractor.skill -d ~/Library/Application\ Support/Claude/skills/resume-extractor
unzip resume-optimizer.skill -d ~/Library/Application\ Support/Claude/skills/resume-optimizer
unzip resume-formatter.skill -d ~/Library/Application\ Support/Claude/skills/resume-formatter
```

## Usage

Talk to Claude Code in natural language. Skills activate automatically based on your request.

### Extract Resume from PDF/DOCX

```
"Extract my resume from resume.pdf to YAML format"
```

**What happens:**
1. Text extracted from PDF/DOCX
2. Content parsed into structured YAML
3. Saved as `firstname_lastname_resume.yaml`

### Optimize Resume Content

```
"Optimize my resume: add metrics, strengthen bullets, ensure ATS compatibility"
```

**What happens:**
1. Weak action verbs identified and replaced
2. Quantifiable metrics added to achievements
3. ATS guidelines applied
4. Professional summary updated
5. Improved YAML provided

### Tailor for Specific Job

```
"Tailor my resume for this job: [paste job URL or description]"
```

**What happens:**
1. Job requirements analyzed
2. Keyword gaps identified
3. Bullets reordered by relevance
4. Keywords integrated naturally
5. Job-specific YAML provided

### Generate Professional PDF

```
"Convert my resume YAML to PDF using the modern template"
```

**What happens:**
1. YAML converted to LaTeX
2. Compiled to PDF with pdflatex
3. Professional resume ready to submit

## Templates

| Template | Best For | Style |
|----------|----------|-------|
| **modern** | Tech, AI/ML, Software Engineering | Clean sans-serif, blue accents, TeX Gyre Heros typography |
| **creative** | Design, Marketing, Startups | Bold blue header, colorful section dividers |
| **classic** | Finance, Law, Consulting | Traditional serif, conservative black/white |
| **academic** | Research, Academia, Science | Education-first, publication-focused |

### Template Commands

```
# Generate with specific template
"Generate PDF with modern template"

# Compare all templates
"Generate PDFs with all 4 templates so I can compare"

# Get template recommendation
"Which template is best for AI engineering roles?"
```

## Complete Workflow

End-to-end example: PDF resume → optimized → tailored → formatted PDF

```
1. "Extract my resume from old_resume.pdf"
   → Creates old_resume.yaml

2. "Optimize this resume: add metrics and strengthen impact"
   → Creates optimized_resume.yaml

3. "Tailor my resume for this Senior ML Engineer role: [job URL]"
   → Creates tailored_resume.yaml

4. "Generate PDF with modern template"
   → Creates tailored_resume.pdf
```

## Direct Commands

For users who prefer CLI over conversational interface:

### Extract PDF to YAML
```bash
uv run resume-extractor/scripts/extract_pdf.py resume.pdf
```

### Extract DOCX to YAML
```bash
uv run resume-extractor/scripts/extract_docx.py resume.docx
```

### Validate YAML Structure
```bash
uv run resume-optimizer/scripts/validate_yaml.py resume.yaml
```

### Generate PDF from YAML
```bash
# Step 1: Convert YAML to LaTeX
uv run resume-formatter/scripts/yaml_to_latex.py resume.yaml modern -o resume.tex

# Step 2: Compile LaTeX to PDF
uv run resume-formatter/scripts/compile_latex.py resume.tex -o resume.pdf
```

### One-Liner PDF Generation
```bash
uv run resume-formatter/scripts/yaml_to_latex.py resume.yaml modern -o resume.tex && \
uv run resume-formatter/scripts/compile_latex.py resume.tex -o resume.pdf
```

## Repository Structure

```
claude-resume-skills/
├── .claude-plugin/
│   └── marketplace.json              # Plugin marketplace config
│
├── .claude/skills/                   # Skills for local development
│   ├── resume-extractor/
│   ├── resume-formatter/
│   └── resume-optimizer/
│
├── resume-extractor/                 # Extractor source
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── extract_pdf.py
│   │   └── extract_docx.py
│   └── references/
│       └── resume_schema.yaml
│
├── resume-optimizer/                 # Optimizer source
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
├── resume-formatter/                 # Formatter source
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── yaml_to_latex.py
│   │   └── compile_latex.py
│   ├── references/
│   │   ├── theme_guide.md
│   │   ├── troubleshooting.md
│   │   └── examples.md
│   └── assets/templates/latex/
│       ├── modern.tex.j2             # TeX Gyre Heros, modern design
│       ├── creative.tex.j2           # Bold blue header
│       ├── classic.tex.j2            # Traditional serif
│       └── academic.tex.j2           # Research-focused
│
├── resume-extractor.skill            # Packaged skills (ZIP)
├── resume-optimizer.skill
├── resume-formatter.skill
│
├── README.md
├── LICENSE
└── .gitignore
```

## Troubleshooting

### Skills Not Loading

**Verify directory structure:**
```bash
pwd                    # Should show: .../claude-resume-skills
ls .claude/skills/     # Should list: resume-extractor, resume-formatter, resume-optimizer
```

**Restart Claude Code:**
1. Close Claude Code completely
2. Navigate to repo directory in terminal
3. Reopen Claude Code

**Verify skills are available:**
```
"What skills do you have available?"
```

### pdflatex Not Found

**Install MacTeX:**
```bash
brew install --cask mactex
```

**Verify installation:**
```bash
pdflatex --version
```

**If still not found, manually add to PATH:**
```bash
export PATH="/Library/TeX/texbin:$PATH"
```

Add to `~/.zshrc` for persistence:
```bash
echo 'export PATH="/Library/TeX/texbin:$PATH"' >> ~/.zshrc
```

### LaTeX Compilation Errors

**Missing LaTeX packages:**
```bash
# Uninstall minimal version
brew uninstall --cask mactex-no-gui

# Install full version
brew install --cask mactex
```

**Content too long (exceeds page limit):**
- Use resume-optimizer to condense bullets
- Aim for 1-2 pages maximum
- Remove older or less relevant positions
- Prioritize most impactful achievements

**Font errors with modern template:**
- TeX Gyre Heros is included with standard MacTeX installation
- If issues persist, use `classic` template (standard fonts only)

### YAML Validation Errors

**Validate structure:**
```bash
uv run resume-optimizer/scripts/validate_yaml.py resume.yaml
```

**Common issues:**
- Missing required fields (`name`, `email`)
- Invalid YAML syntax (indentation errors)
- Empty sections (remove or populate)
- Weak action verbs (use optimizer to strengthen)

## Best Practices

### Content Quality

- **Quantify achievements**: Add specific metrics (%, $, time saved, users impacted)
- **Strong action verbs**: Start bullets with Architected, Delivered, Increased, Reduced, etc.
- **Keywords**: Match exact terminology from target job descriptions
- **Brevity**: Keep to 1-2 pages; prioritize recent and relevant experience
- **Specificity**: Replace vague descriptions with concrete outcomes

### Workflow

1. **YAML as source of truth**: Edit `resume.yaml`, generate PDFs as needed
2. **Version control**: Create job-specific YAML files (`resume_google.yaml`, `resume_meta.yaml`)
3. **File naming**: Use `firstname_lastname_company.pdf` format
4. **Review before sending**: Always inspect generated PDF for formatting issues
5. **ATS testing**: Verify text extraction with `pdftotext resume.pdf -` (should be readable)

### Template Selection

- **Tech/AI/ML/Software**: Modern (contemporary, clean sans-serif)
- **Finance/Consulting/Law**: Classic (traditional, conservative)
- **Design/Marketing/UX**: Creative (bold, visual hierarchy)
- **Academia/Research**: Academic (education-first, publications)
- **Startups**: Modern or Creative

### ATS Optimization

1. **Standard section headers**: Use "Experience", "Education", "Skills" (not "Work History", "Background")
2. **Simple formatting**: Avoid tables, multi-column layouts, text boxes, graphics
3. **Keyword matching**: Mirror exact phrases from job description where accurate
4. **PDF format**: Submit PDF (not DOCX) for consistent rendering
5. **Test extraction**: Verify text copies cleanly from PDF

### Job Tailoring

1. **Analyze job description**: Note required vs. preferred skills
2. **Keyword gap analysis**: Ask Claude to identify missing keywords
3. **Reorder bullets**: Place most relevant achievements first
4. **Customize summary**: Align professional summary with role requirements
5. **Verify keyword integration**: Ensure natural incorporation (avoid keyword stuffing)

## Support

**Skill documentation**: Each skill has detailed `SKILL.md` with instructions

**Reference guides**: Check `references/` directories for:
- ATS guidelines
- Action verb lists
- Impact patterns
- Job tailoring strategies
- Template selection guide
- Troubleshooting tips

**Validate YAML**: Use validation script before formatting:
```bash
uv run resume-optimizer/scripts/validate_yaml.py resume.yaml
```

**Report issues**: [Open an issue on GitHub](https://github.com/vibewith-brent/claude-resume-skills/issues)

## Version History

### v1.1.0

- Simplified modern template using TeX Gyre Heros (Helvetica-like) typography
- Removed moderncv dependency for easier installation
- Improved pdflatex path detection on macOS
- Updated documentation and examples
- All templates use standard LaTeX packages

### v1.0.0

- Initial release with 4 templates
- MacTeX PATH auto-detection for macOS
- Plugin marketplace support
- Comprehensive reference documentation
- YAML validation script
- MIT License

## License

MIT License - See [LICENSE](LICENSE) file for details.

LaTeX templates use standard packages and are freely available for personal and commercial use.
