# Resume Skills for Claude Code

Six skills for resume management: extract PDF/DOCX → optimize content → format to PDF → review and iterate.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.com/code)

## Quick Install via Plugin Marketplace

Register this repo as a plugin marketplace, then install:

```
/plugin marketplace add vibewith-brent/claude-resume-skills
/plugin install resume-skills@resume-helper-skills
```

Or browse available plugins after registering:

1. Run `/plugin marketplace add vibewith-brent/claude-resume-skills`
2. Select **Browse and install plugins**
3. Select **resume-helper-skills**
4. Select **resume-skills**
5. Select **Install now**

After installation, use skills by natural language (e.g., "Extract my resume from resume.pdf").

**Prerequisite:** [Typst](https://typst.app) must be installed (`brew install typst`).

## Installation (Alternative Methods)

### Project Skills (Recommended)

Clone and open in Claude Code. Skills auto-load from `.claude/skills/`:

```bash
git clone https://github.com/vibewith-brent/claude-resume-skills.git
cd claude-resume-skills
brew install typst  # macOS (or: cargo install typst-cli)
```

### Personal Skills

Copy skills to your personal directory for use across all projects:

```bash
# Package and install to personal skills
uv run scripts/package_skills.py
unzip dist/resume-*.zip -d ~/.claude/skills/
```

### Prerequisites

- **Typst** — PDF compilation (~20MB, much lighter than LaTeX)
- **Python 3.10+** — Auto-managed by `uv`

## Skills

| Skill | Purpose |
|-------|---------|
| **resume-state** | Version control. Initialize projects, import files, branch versions, compare changes. *Use first.* |
| **resume-extractor** | Convert PDF/DOCX to structured YAML |
| **resume-optimizer** | Improve content: ATS optimization, metrics, keyword alignment, job tailoring |
| **resume-formatter** | Generate PDFs from YAML using Typst templates |
| **resume-reviewer** | Visual QA for compiled PDFs |
| **resume-template-maker** | Create custom Typst templates |

### Templates

| Template | Use Case |
|----------|----------|
| `executive` | Professional default — clean hierarchy, navy accents |
| `compact` | Dense content — maximum info per page |
| `minimal` | Understated — monochromatic, generous whitespace |

## Usage

Skills auto-select based on your request. Example workflow:

```
"Initialize project ml_engineer and import resume.pdf"
"Extract to YAML and optimize for ATS"
"Create version for Google, tailor for this job: [URL]"
"Generate PDF with executive template"
"Review the PDF"
```

CLI equivalents in each skill's `scripts/` directory.

## Structure

```
resume-*/              # Source of truth for each skill (SKILL.md + scripts/ + references/)
.claude/skills/        # Symlinks to resume-*/ (auto-loaded by Claude Code)
.resume_versions/      # Version store (projects, sources, versions)
```

Edit `resume-*/` directly. `.claude/skills/` contains symlinks.

## YAML Schema

**Required:** `contact`, `summary`, `experience`, `skills`, `education`

**Optional:** `certifications`, `projects`, `publications`, `awards`, `languages`, `volunteer`

Experience supports nested positions (multiple roles at same company). Full schema: `resume-extractor/references/resume_schema.yaml`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Skills not loading | Verify symlinks: `ls -la .claude/skills/` → restart Claude Code |
| Typst errors | Check `typst --version`; escape special chars in YAML |
| Content overflow | Reduce bullets (4-6/role), try `compact` template |
| State not found | Run `init_project.py <name>` |

## Development

```bash
uv sync                           # Install dependencies
uv run scripts/package_skills.py  # Package to dist/*.zip
```

### Adding Skills

1. Create `resume-newskill/SKILL.md`:
   ```yaml
   ---
   name: resume-newskill
   description: What it does and when to use it. Third person.
   ---
   ```
2. Add `scripts/` and `references/` as needed
3. Symlink: `ln -s ../resume-newskill .claude/skills/resume-newskill`

See [Skill Authoring Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills#authoring-best-practices).

## Contributing

PRs welcome. Areas of interest: additional templates, ATS scoring, job board integrations.

## License

MIT — see [LICENSE](LICENSE)

## Resources

- [Typst](https://typst.app) — Modern typesetting
- [Claude Code Skills](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) — Official docs
- [Anthropic Skills Repo](https://github.com/anthropics/skills) — Examples

---

[Issues](https://github.com/vibewith-brent/claude-resume-skills/issues) · [Discussions](https://github.com/vibewith-brent/claude-resume-skills/discussions)
