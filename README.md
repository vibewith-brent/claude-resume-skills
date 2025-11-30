# Resume Helper Skills for Claude Code

Resume management suite: extract PDF/DOCX → optimize content → format to PDF → review and iterate.

## Quick Start

```bash
# Clone and install Typst
git clone https://github.com/vibewith-brent/claude-resume-skills.git
cd claude-resume-skills
brew install typst

# Open Claude Code - skills auto-load from .claude/skills/
```

## Skills

| Skill | Purpose |
|-------|---------|
| **resume-state** | Version control and project management |
| **resume-extractor** | PDF/DOCX → structured YAML |
| **resume-optimizer** | ATS optimization, metrics, keyword alignment |
| **resume-formatter** | YAML → Typst → PDF (5 templates) |
| **resume-reviewer** | Visual QA for compiled PDFs |
| **resume-template-maker** | Create custom templates |

## Templates

| Template | Use Case |
|----------|----------|
| modern | Tech, startups, general |
| modern-tech | Tech with teal accents, side-line headers |
| classic | Finance, law, consulting |
| academic | Research, academia |
| creative | Design, marketing |

## Usage

Talk to Claude naturally:

```
"Extract my resume from resume.pdf"
"Optimize for ATS and add metrics"
"Tailor for this job: [URL]"
"Generate PDF with modern-tech template"
"Review the PDF for issues"
```

### CLI Commands

```bash
# Version management
uv run .claude/skills/resume-state/scripts/init_project.py ml_engineer
uv run .claude/skills/resume-state/scripts/import_resume.py resume.pdf
uv run .claude/skills/resume-state/scripts/create_version.py --tag google --notes "For Google"
uv run .claude/skills/resume-state/scripts/list_versions.py

# Extraction
uv run .claude/skills/resume-extractor/scripts/extract_pdf.py resume.pdf

# PDF generation
uv run .claude/skills/resume-formatter/scripts/yaml_to_typst.py resume.yaml modern-tech -o resume.typ
uv run .claude/skills/resume-formatter/scripts/compile_typst.py resume.typ -o resume.pdf
```

## Installation

### Local Development (Recommended)

Clone the repo and open Claude Code in the directory. Skills auto-load via symlinks in `.claude/skills/`.

### Distribute as ZIP

Package skills for sharing:

```bash
uv run scripts/package_skills.py
# Creates dist/*.zip files per Anthropic's skill format
```

Install a packaged skill:
```bash
unzip dist/resume-formatter.zip -d ~/.claude/skills/
```

## Repository Structure

```
resume-*/                    # Skill source directories
├── SKILL.md                 # Skill definition (YAML frontmatter + instructions)
├── scripts/                 # Python utilities
├── references/              # Reference documentation
└── assets/                  # Templates, schemas

.claude/skills/              # Symlinks to resume-*/ (auto-loaded)
scripts/package_skills.py    # Package skills as distributable ZIPs
dist/                        # Packaged .zip files (generated, gitignored)
```

## Prerequisites

- **Claude Code** - [claude.ai/code](https://claude.ai/code)
- **Typst** - `brew install typst` (~20MB)
- **uv** - Auto-installed by Claude Code
- **Python packages** - Auto-installed via `uv sync`

## Troubleshooting

**Skills not loading:** Verify `.claude/skills/` contains symlinks, restart Claude Code.

**Typst errors:** Ensure Typst installed (`typst --version`), check font availability.

**Content overflow:** Reduce bullets per role (4-6 max), use optimizer to condense.

## License

MIT
