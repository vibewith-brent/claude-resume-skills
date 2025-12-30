# Resume Skills for Claude Code

Seven skills for resume management: extract PDF/DOCX → optimize content → format to PDF → generate cover letters → review and iterate.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.com/code)

## Installation

```bash
/plugin marketplace add https://github.com/vibewith-brent/claude-resume-skills
/plugin install resume-skills@resume-helper-skills
```

After installation, use skills via natural language (e.g., "Extract my resume from resume.pdf").

### Updating Skills

```bash
/plugin update resume-skills@resume-helper-skills
```

After updating, **restart Claude Code** or start a new conversation to load the updated skills.

### Prerequisite

[Typst](https://typst.app) must be installed (`brew install typst`).

## Skills

| Skill | Purpose |
|-------|---------|
| **resume-state** | Version control. Initialize projects, import files, branch versions, compare changes. *Use first.* |
| **resume-extractor** | Convert PDF/DOCX to structured YAML |
| **resume-optimizer** | Improve content: ATS optimization, metrics, keyword alignment, job tailoring |
| **resume-formatter** | Generate PDFs from YAML using Typst templates |
| **resume-coverletter** | Generate cover letters matching resume template styling |
| **resume-reviewer** | Visual QA templates — Claude views PDF and fills in checklist |
| **resume-template-maker** | Create custom Typst templates |

### Templates

| Template | Use Case |
|----------|----------|
| `executive` | Professional default — clean hierarchy, navy accents |
| `tech-modern` | Modern/creative — deep lavender, pill skills, Carlito font, single-page optimized |
| `modern-dense` | Maximum density — categorized inline skills, 20-25 bullets, strategic spacing |
| `compact` | Dense content — maximum info per page |
| `minimal` | Understated — monochromatic, generous whitespace |

## Usage

Skills auto-select based on your request. Example workflow:

```
"Initialize project ml_engineer and import resume.pdf"
"Extract to YAML and optimize for ATS"
"Create version for Google, tailor for this job: [URL]"
"Generate PDF with executive template"
"Write a cover letter for this role"
"Review the PDF"
```

CLI equivalents in each skill's `scripts/` directory.

## Structure

```
resume-*/              # Skill directories (SKILL.md + scripts/ + references/)
.claude-plugin/        # Plugin marketplace configuration
.resume_versions/      # Version store (projects, sources, versions)
```

## YAML Schema

**Required:** `contact`

**Recommended:** `summary`, `experience`, `skills`, `education`

**Optional:** `certifications`, `projects`, `publications`, `awards`, `languages`, `volunteer`

Experience supports nested positions (multiple roles at same company). Full schema: `resume-extractor/references/resume_schema.yaml`

The formatter validates YAML against the schema before rendering. Use `--skip-validation` for legacy formats:

```bash
uv run resume-formatter/scripts/yaml_to_typst.py resume.yaml executive --skip-validation
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Skills not loading | Check `/plugin list`; reinstall with `/plugin install resume-skills@resume-helper-skills` |
| Schema validation failed | Fix YAML structure per error messages, or use `--skip-validation` for legacy formats |
| Typst errors | Check `typst --version`; escape special chars in YAML |
| Content overflow | Reduce bullets (4-6/role), try `compact` template |
| State not found | Run `init_project.py <name>` |

## Development

```bash
uv sync              # Install dependencies
uv sync --extra dev  # Include test dependencies
```

### Testing

```bash
uv run pytest tests/           # Run all tests
uv run pytest tests/ -v        # Verbose output
uv run pytest tests/ --cov     # With coverage
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
3. Add skill path to `.claude-plugin/marketplace.json`

See [Skill Authoring Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills#authoring-best-practices).

## Contributing

PRs welcome. Areas of interest: additional templates, ATS scoring, job board integrations.

## License

MIT — see [LICENSE](LICENSE)

## Resources

- [Typst](https://typst.app) — Modern typesetting
- [Claude Code Skills](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) — Official docs
- [Claude Code Plugins](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/plugins) — Plugin marketplace docs

---

[Issues](https://github.com/vibewith-brent/claude-resume-skills/issues) · [Discussions](https://github.com/vibewith-brent/claude-resume-skills/discussions)
