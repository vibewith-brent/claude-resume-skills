# Typst as MacTeX Replacement: Investigation

## Summary

**Typst** is a modern, Rust-based typesetting system that can replace MacTeX/pdflatex for resume PDF generation. It offers dramatically faster compilation, easier installation, and a growing ecosystem of resume templates.

## Comparison

| Aspect | MacTeX (pdflatex) | Typst |
|--------|-------------------|-------|
| **Size** | ~4GB | ~20MB |
| **Install** | `brew install --cask mactex` (slow) | `brew install typst` (fast) |
| **Language** | TeX (1978) | Rust (2023) |
| **Compile speed** | Seconds | Milliseconds (incremental) |
| **Learning curve** | Steep | Gentle |
| **Error messages** | Cryptic | Clear, contextual |
| **Dependencies** | Many system packages | Single binary |

## Installation

```bash
# macOS
brew install typst

# Windows
winget install --id Typst.Typst

# From source (Rust required)
cargo install --locked typst-cli

# Docker
docker run ghcr.io/typst/typst:latest
```

## Resume Templates (Typst Universe)

| Template | Style | ATS-Friendly | Notes |
|----------|-------|--------------|-------|
| [basic-resume](https://typst.app/universe/package/basic-resume/) | Clean, minimal | Yes | Best starting point |
| [brilliant-cv](https://typst.app/universe/package/brilliant-cv/) | Professional | Yes + AI countermeasures | TOML config, multilingual |
| [modern-cv](https://typst.app/universe/package/modern-cv/) | Awesome-CV port | Yes | Roboto/Source Sans fonts |
| [moderner-cv](https://typst.app/universe/package/moderner-cv/) | moderncv port | Yes | FontAwesome icons |
| [clickworthy-resume](https://typst.app/universe/package/clickworthy-resume/) | Flexible | Yes | All params optional |
| [modernpro-cv](https://typst.app/universe/package/modernpro-cv/) | Deedy-inspired | Yes | Single/two-column |

## Typst Syntax Example

```typst
#import "@preview/basic-resume:0.2.9": *

#show: resume.with(
  author: "Jane Doe",
  email: "jane@example.com",
  github: "github.com/janedoe",
  linkedin: "linkedin.com/in/janedoe",
  accent-color: "#26428b",
  font: "New Computer Modern",
)

= Experience

#work(
  company: "Tech Corp",
  title: "Senior Engineer",
  dates: "2020 - Present",
  location: "San Francisco, CA",
)
- Led team of 5 engineers on distributed systems project
- Reduced latency by 40% through caching optimization
```

## Migration Path

### Option A: Direct Typst Templates
Replace LaTeX templates with native Typst `.typ` files. Leverage existing Typst Universe templates.

**Pros**: Clean architecture, best performance, native Typst features
**Cons**: Requires rewriting templates, learning Typst syntax

### Option B: YAML → Typst Pipeline
Keep YAML as data source, create Typst templates with Jinja2-style variable substitution.

**Pros**: Minimal changes to existing workflow, YAML schema preserved
**Cons**: Custom templating logic needed

### Option C: Pandoc Bridge
Use Pandoc to convert Markdown/YAML → Typst → PDF.

**Pros**: Pandoc handles conversion, format flexibility
**Cons**: Extra dependency, less control over output

## Recommended Approach

**Option B** is recommended for this project:

1. Keep existing YAML resume schema (no user-facing changes)
2. Create new Typst templates (`.typ.j2`) alongside LaTeX templates
3. New script: `yaml_to_typst.py` (mirrors `yaml_to_latex.py`)
4. Compile with `typst compile resume.typ resume.pdf`
5. Deprecate LaTeX templates over time

### Implementation Tasks

1. [ ] Add Typst installation check to formatter skill
2. [ ] Create `modern.typ.j2` template (port from `modern.tex.j2`)
3. [ ] Create `yaml_to_typst.py` script
4. [ ] Update SKILL.md with Typst commands
5. [ ] Test output quality against LaTeX versions
6. [ ] Create remaining templates (classic, academic, creative)
7. [ ] Update CLAUDE.md with new dependency options

## Performance Expectations

Based on [benchmarks](https://slhck.info/software/2025/10/25/typst-pdf-generation-xelatex-alternative.html):
- Single-page resume: <100ms (vs 2-5s for pdflatex)
- Incremental recompile: <50ms
- No auxiliary file cleanup needed (.aux, .log, .out)

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Template quality differs from LaTeX | Medium | Side-by-side testing, iterate on templates |
| Font availability | Low | Use bundled fonts or common system fonts |
| Typst breaking changes | Low | Pin to specific version |
| User adoption resistance | Low | Keep LaTeX as fallback option |

## References

- [Typst GitHub](https://github.com/typst/typst)
- [Typst Documentation](https://typst.app/docs/)
- [Typst Universe (templates)](https://typst.app/universe/)
- [Typst vs LaTeX comparison](https://all-dressed-programming.com/posts/amazing-typst/)
- [Pandoc + Typst integration](https://slhck.info/software/2025/10/25/typst-pdf-generation-xelatex-alternative.html)
