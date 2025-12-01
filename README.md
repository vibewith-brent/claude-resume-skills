# Resume Skills for Claude Code

Six skills for managing resumes in Claude Code: extract from PDF/DOCX, optimize content, format to PDF, review output, create custom templates, and manage versions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.com/code)

## Features

- Version control for managing multiple resume variants
- Typst PDF generation (~20MB, no LaTeX required)
- Natural language interface
- 3 professional templates included
- Complete workflow from extraction to final PDF

## Installation

### Option 1: Plugin Marketplace (Recommended)

Register this repository as a plugin source in Claude Code:

```bash
# In Claude Code, run:
/add-plugin-source https://github.com/YOUR_USERNAME/claude-resume-skills
```

Then enable the skills in Settings → Skills.

### Option 2: Local Development

Clone the repository and open Claude Code in the directory. Skills auto-load via symlinks in `.claude/skills/`:

```bash
git clone https://github.com/YOUR_USERNAME/claude-resume-skills.git
cd claude-resume-skills
brew install typst  # macOS
# Open Claude Code here - skills will auto-load
```

### Option 3: Individual Skills

Package and install specific skills as ZIP files:

```bash
# Package all skills
uv run scripts/package_skills.py

# Install a single skill
unzip dist/resume-formatter.zip -d ~/.claude/skills/
```

## Prerequisites

- **Claude Code** - [claude.com/code](https://claude.com/code)
- **Typst** - PDF compilation engine (~20MB)
  ```bash
  # macOS
  brew install typst

  # Linux
  cargo install typst-cli

  # Windows
  winget install --id Typst.Typst

  # Verify installation
  typst --version
  ```
- **Python 3.10+** - Auto-managed by `uv` (included with Claude Code)

## Skills

### resume-state
Version control and project management. Initialize projects, import original files, create versions before making changes, switch between variants, compare differences, and export for submission.

Use this skill first when working with resumes.

```
"Initialize a project called software_engineer"
"Import my resume from resume.pdf"
"Create a new version for the Google application"
"Show me all versions"
"Compare v1 and v2"
```

**Key commands:**
- `init_project.py <name>` - Create new project
- `import_resume.py <file>` - Import PDF/DOCX as v1
- `create_version.py --tag <tag>` - Branch new version
- `list_versions.py` - Show version history
- `switch_version.py <id>` - Change active version
- `diff_versions.py <a> <b>` - Compare versions

### resume-extractor
Convert existing resumes from PDF or DOCX to editable YAML format. Handles multi-column layouts, nested positions, and complex formatting.

```
"Extract my resume from resume.pdf"
"Convert this DOCX to YAML"
```

**Key commands:**
- `extract_pdf.py <file>` - Extract from PDF
- `extract_docx.py <file>` - Extract from DOCX

**Output:** Structured YAML following canonical schema in `references/resume_schema.yaml`

### resume-optimizer
Improve resume content with quantified achievements, strong action verbs, ATS-friendly formatting, and keyword optimization. Fetch job postings to tailor content for specific roles.

```
"Optimize this resume for ATS"
"Add metrics to my achievements"
"Tailor this for the job at [URL]"
"Check if this resume is ATS-friendly"
```

**Key commands:**
- `validate_yaml.py <file>` - Check YAML structure
- `fetch_job_posting.py <url>` - Download job description

**References:**
- `action_verbs.yaml` - Strong action verbs by category
- `ats_guidelines.md` - ATS optimization best practices
- `impact_patterns.md` - Quantification templates

### resume-formatter
Generate professionally formatted PDFs from YAML. Choose from 3 templates optimized for different use cases.

```
"Generate a PDF with the executive template"
"Create PDFs with all three templates so I can compare"
"Format this resume with the compact template"
```

**Templates:**

| Template | Best For | Style |
|----------|----------|-------|
| **executive** | Most professional roles, senior positions | Clean hierarchy, navy accents, balanced whitespace |
| **compact** | Extensive experience, dense content | Maximum density, tight spacing, small headers |
| **minimal** | Clean, understated presentation | Monochromatic, generous whitespace, subtle hierarchy |

**Key commands:**
- `yaml_to_typst.py <yaml> <template> -o <typ>` - Convert to Typst
- `compile_typst.py <typ> -o <pdf>` - Compile to PDF

**One-liner:**
```bash
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py resume.yaml executive -o resume.typ && \
uv run .claude/skills/resume-formatter/scripts/compile_typst.py resume.typ -o resume.pdf
```

### resume-reviewer
Evaluate compiled resumes against a structured checklist: typography, layout, spacing, visual hierarchy, ATS compatibility, content quality, and print readiness.

```
"Review this PDF for issues"
"Check if this resume looks professional"
"Evaluate the layout and spacing"
```

**Evaluation criteria:**
- Typography (font choices, sizing, consistency)
- Layout (margins, alignment, balance)
- Spacing (section separation, line height, whitespace)
- Visual hierarchy (emphasis, scanning, organization)
- ATS compatibility (text extraction, parsability)
- Content quality (clarity, conciseness, impact)
- Print readiness (grayscale, contrast, page breaks)

**Reference:** `references/visual_qa_checklist.md`

### resume-template-maker
Create custom Typst templates using structured design principles. Define typography, layout, whitespace, and color schemes for different industries and styles.

```
"Create a tech industry template with a modern feel"
"Design a minimal template for creative roles"
"Make a template with more color"
```

**Design vectors:**
- Typography (font pairings, sizing, weights)
- Layout (grid systems, margins, columns)
- Whitespace (breathing room, section separation)
- Color (professional palettes by industry)

**References:**
- `references/design_vectors.md` - Typography and layout guidance
- `references/industry_themes.md` - Industry-specific recommendations

**Workflow:**
1. Define design parameters (industry, style preferences)
2. Generate `.typ.j2` template
3. Compile with sample resume
4. Review with resume-reviewer
5. Adjust based on feedback
6. Repeat until QA passes

## Quick Start

### Complete Workflow Example

```
# 1. Initialize and import
"Initialize a project called ml_engineer"
"Import my resume from resume.pdf"

# 2. Extract and optimize
"Extract the PDF to YAML"
"Optimize the YAML for ATS and add metrics"

# 3. Tailor for a job
"Create a new version for the Google ML role"
"Tailor the resume for this job: https://careers.google.com/jobs/results/123"

# 4. Generate PDF
"Generate a PDF with the executive template"

# 5. Review
"Review the PDF for any issues"

# 6. Iterate if needed
"Update the YAML to fix those spacing issues"
"Regenerate the PDF"
```

### Command-Line Workflow

```bash
# Version management
uv run .claude/skills/resume-state/scripts/init_project.py ml_engineer
uv run .claude/skills/resume-state/scripts/import_resume.py resume.pdf
uv run .claude/skills/resume-state/scripts/create_version.py --tag google --notes "For Google"

# Extract
uv run .claude/skills/resume-extractor/scripts/extract_pdf.py resume.pdf > resume.yaml

# Validate
uv run .claude/skills/resume-optimizer/scripts/validate_yaml.py resume.yaml

# Format
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py resume.yaml executive -o resume.typ
uv run .claude/skills/resume-formatter/scripts/compile_typst.py resume.typ -o resume.pdf

# Compare versions
uv run .claude/skills/resume-state/scripts/diff_versions.py v1 v2
```

## Repository Structure

```
claude-resume-skills/
├── .claude-plugin/
│   └── marketplace.json       # Plugin marketplace configuration
├── .claude/
│   └── skills/                # Symlinks to resume-*/ (auto-loaded)
├── resume-extractor/          # PDF/DOCX → YAML extraction
│   ├── SKILL.md               # Skill definition
│   ├── scripts/
│   │   ├── extract_pdf.py
│   │   └── extract_docx.py
│   └── references/
│       └── resume_schema.yaml # Canonical YAML structure
├── resume-optimizer/          # Content optimization
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── validate_yaml.py
│   │   └── fetch_job_posting.py
│   └── references/
│       ├── action_verbs.yaml
│       ├── ats_guidelines.md
│       └── impact_patterns.md
├── resume-formatter/          # YAML → Typst → PDF
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── yaml_to_typst.py
│   │   └── compile_typst.py
│   └── assets/
│       └── templates/typst/   # Jinja2 templates (.typ.j2)
│           ├── executive.typ.j2
│           ├── compact.typ.j2
│           └── minimal.typ.j2
├── resume-reviewer/           # PDF quality assessment
│   ├── SKILL.md
│   └── references/
│       └── visual_qa_checklist.md
├── resume-template-maker/     # Custom template creation
│   ├── SKILL.md
│   └── references/
│       ├── design_vectors.md
│       └── industry_themes.md
├── resume-state/              # Version and project management
│   ├── SKILL.md
│   └── scripts/
│       ├── init_project.py
│       ├── import_resume.py
│       ├── create_version.py
│       ├── list_versions.py
│       ├── switch_version.py
│       ├── get_active.py
│       ├── export_version.py
│       └── diff_versions.py
├── scripts/
│   └── package_skills.py      # Package skills as distributable ZIPs
├── dist/                      # Packaged .zip files (generated)
├── CLAUDE.md                  # Project guidance for Claude Code
├── pyproject.toml             # Python dependencies (uv-managed)
├── uv.lock                    # Locked dependencies
└── README.md
```

**Single source of truth:** Edit `resume-*/` directories directly. `.claude/skills/` contains symlinks for auto-loading.

## YAML Resume Schema

Required sections:
- `contact` - Name, email, phone, location, links
- `summary` - Professional summary (2-3 sentences)
- `experience` - Work history with nested positions
- `skills` - Technical skills by category
- `education` - Degrees and certifications

Optional sections:
- `certifications` - Professional certifications
- `projects` - Notable projects
- `publications` - Publications and presentations
- `awards` - Awards and recognition
- `languages` - Language proficiency
- `volunteer` - Volunteer experience

**Experience structure** (handles multiple roles at same company):
```yaml
experience:
  - company: "Company Name"
    location: "City, State"
    positions:
      - title: "Senior Software Engineer"
        dates: "Jan 2022 - Present"
        achievements:
          - "Led team of 5 engineers to deliver X, resulting in Y impact"
          - "Architected Z system, reducing costs by 40%"
      - title: "Software Engineer"
        dates: "Jan 2020 - Dec 2021"
        achievements:
          - "Built feature A, improving metric B by 30%"
```

Full schema reference: `resume-extractor/references/resume_schema.yaml`

## Version Management

Projects are stored in `.resume_versions/` with complete version history:

```
.resume_versions/
├── config.json                    # Active project setting
└── projects/
    └── ml_engineer/
        ├── project.json           # Version history + metadata
        ├── sources/               # Original PDFs/DOCXs (immutable)
        │   └── resume_original.pdf
        ├── versions/
        │   ├── v1/
        │   │   ├── resume.yaml
        │   │   └── extracted_text.txt
        │   └── v2_google/
        │       ├── resume.yaml
        │       ├── resume.typ
        │       └── resume.pdf
        └── jobs/                  # Cached job postings
            └── google_ml_123.txt
```

**Store location search order:**
1. `RESUME_VERSIONS_PATH` environment variable (if set)
2. `.resume_versions/` in current directory or parent directories
3. `~/.resume_versions/` (global fallback)

This allows running commands from anywhere in your project or using a global store for all projects.

## Troubleshooting

### Skills Not Loading

Verify `.claude/skills/` symlinks point to `resume-*/` directories:
```bash
ls -la .claude/skills/
```

Restart Claude Code after verifying symlinks exist.

### Typst Compilation Errors

Check Typst installation:
```bash
typst --version
```

Common issues:
- **Special characters in YAML** - Properly escape colons, quotes, etc.
- **Missing required fields** - Run `validate_yaml.py` to check schema
- **Font not found** - Templates use Inter (usually available)

### Content Overflow

Resume too long for one page:
1. Reduce achievements to 4-6 bullets per role
2. Use `resume-optimizer` to condense
3. Try the `compact` template
4. Remove oldest/least relevant roles

### State Not Found

If version commands fail:
```bash
# Check if project exists
uv run .claude/skills/resume-state/scripts/list_versions.py

# Verify store location
find ~ -name ".resume_versions" -type d

# Initialize if missing
uv run .claude/skills/resume-state/scripts/init_project.py <name>
```

### Permission Errors

Ensure scripts are executable:
```bash
chmod +x .claude/skills/*/scripts/*.py
```

## Development

### Environment Setup

```bash
# Install dependencies
uv sync

# Verify Python version
python --version  # Should be >=3.10
```

### Package Skills for Distribution

```bash
# Package all skills
uv run scripts/package_skills.py

# Package specific skill
uv run scripts/package_skills.py resume-formatter

# List available skills
uv run scripts/package_skills.py --list

# Custom output directory
uv run scripts/package_skills.py --output custom-dist/
```

Output: `dist/*.zip` files ready for sharing or marketplace upload.

### Adding New Skills

1. Create `resume-newskill/` directory
2. Add `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: resume-newskill
   description: Clear description of what this skill does and when to use it (200 char max)
   version: 1.0.0
   dependencies: python>=3.10, pyyaml>=6.0
   ---
   ```
3. Add instructions in Markdown below frontmatter
4. Create symlink: `ln -s ../resume-newskill .claude/skills/resume-newskill`
5. Add to `SKILL_DIRS` in `scripts/package_skills.py`
6. Update `.claude-plugin/marketplace.json`
7. Test in Claude Code

### Modifying Templates

Templates are Jinja2 files (`.typ.j2`) in `resume-formatter/assets/templates/typst/`:

1. Edit the `.typ.j2` template file
2. Test with sample YAML:
   ```bash
   uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py \
     test.yaml custom-template -o test.typ
   uv run .claude/skills/resume-formatter/scripts/compile_typst.py \
     test.typ -o test.pdf
   ```
3. Review with `resume-reviewer` skill
4. Iterate until QA passes

**Template features:**
- `typst_escape` filter for special character handling
- Conditional sections (only render if data exists)
- Nested position support for experience
- Configurable colors, fonts, margins

## Contributing

Contributions welcome! Areas of interest:
- Additional templates (industry-specific, regional styles)
- Enhanced ATS detection and scoring
- Job board integrations for tailoring
- Resume analytics and insights
- Multi-language support

**Process:**
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation (SKILL.md, README.md, CLAUDE.md)
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- **Typst** - Modern typesetting system ([typst.app](https://typst.app))
- **Claude Code** - AI-powered coding assistant ([claude.com/code](https://claude.com/code))
- **Anthropic Skills** - Skill framework and examples ([github.com/anthropics/skills](https://github.com/anthropics/skills))

## Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/claude-resume-skills/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/claude-resume-skills/discussions)
- **Claude Code Help:** [support.claude.com](https://support.claude.com)

---

Built with Claude Code | [View on GitHub](https://github.com/YOUR_USERNAME/claude-resume-skills)
