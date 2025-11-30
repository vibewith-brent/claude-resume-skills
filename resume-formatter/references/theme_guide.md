# Resume Formatter Theme Guide

## Overview

The resume-formatter skill includes 4 professionally designed Typst templates, each optimized for different industries and personal styles.

## Available Themes

### 1. Modern (`modern`)

**Best for:** Tech, startups, creative industries
**Style:** Clean, professional, Inter font typography
**Features:**
- Modern layout with blue accents
- Blue accent color with gray subtext
- Professional section headers with thin underlines
- Two-column skills layout
- Hyperlinked email and contact info

**Pros:**
- Most ATS-friendly template
- Professional yet contemporary
- Great for tech roles
- Compact (fits more content)
- Fast compilation with Typst

**Cons:**
- Requires Inter font (or edit for fallback)

**Recommended for:**
- Software Engineers
- Data Scientists
- Product Managers
- Tech industry roles

---

### 2. Classic (`classic`)

**Best for:** Finance, consulting, law, traditional industries
**Style:** Traditional, conservative, minimal formatting
**Features:**
- Simple single-column layout
- No colors or graphics (black/white)
- Traditional section headers with horizontal rules
- Maximum readability
- New Computer Modern font

**Pros:**
- Maximum ATS compatibility
- Professional and conservative
- Easy to customize
- Works with any font

**Cons:**
- Less visually distinctive
- May appear bland for creative roles

**Recommended for:**
- Finance roles
- Consulting positions
- Legal professions
- Government/military
- Traditional corporate environments

---

### 3. Academic (`academic`)

**Best for:** Research, academia, scientific roles
**Style:** Formal, publication-focused
**Features:**
- Emphasis on education and publications sections
- Numbered publication lists
- Research interests section
- Page numbers
- Multi-page support

**Pros:**
- Designed for academic conventions
- Highlights research and publications
- Multi-page friendly with page numbers
- Clear hierarchy

**Cons:**
- Too formal for most industry roles
- Not optimized for brevity

**Recommended for:**
- Academic positions (faculty, postdoc)
- Research scientist roles
- PhD candidates
- Roles emphasizing publications

---

### 4. Creative (`creative`)

**Best for:** Design, marketing, creative industries
**Style:** Bold, modern, color-accented
**Features:**
- Colored header bar
- Blue and gray color scheme
- Visual section separators
- Modern Inter typography
- Hyperlinked contact info

**Pros:**
- Visually distinctive
- Shows design sensibility
- Modern and engaging
- Good for portfolio roles

**Cons:**
- Colors may not print well in B&W
- Some ATS systems struggle with graphics
- Less conservative

**Recommended for:**
- UX/UI Designers
- Marketing roles
- Creative positions
- Startups
- Roles emphasizing visual design

## Choosing the Right Template

**Decision tree:**

```
Are you applying to academia or research roles?
  └─ YES → Use Academic
  └─ NO  → Continue

Is the industry traditional/conservative (finance, law, consulting)?
  └─ YES → Use Classic
  └─ NO  → Continue

Is the role creative (design, marketing, UX)?
  └─ YES → Use Creative
  └─ NO  → Use Modern (default for tech/general)
```

## Customization

### Color Changes

**Modern template:**
Edit color definitions in `modern.typ.j2`:
```typst
#let headerblue = rgb("#0066cc")
#let dateblue = rgb("#0066cc")
#let subtextgray = rgb("#787878")
#let linegray = rgb("#c8c8c8")
```

**Creative template:**
Edit color definitions in `creative.typ.j2`:
```typst
#let primary = rgb("#0066cc")    // Main accent color
#let accent = rgb("#333333")      // Secondary color
#let lightgray = rgb("#f0f0f0")   // Background accents
```

### Font Changes

**All templates:**
Change font and size in `#set text()`:
```typst
#set text(font: "Inter", size: 10pt)  // Change size to 9pt, 11pt, etc.
```

Alternative fonts:
```typst
#set text(font: "Helvetica")      // macOS default
#set text(font: "Arial")          // Windows default
#set text(font: "Liberation Sans") // Linux default
#set text(font: "New Computer Modern") // TeX-like serif
```

### Margin Adjustments

**All templates:**
```typst
#set page(
  paper: "us-letter",
  margin: (top: 0.5in, bottom: 0.5in, left: 0.6in, right: 0.6in)
)
```

### Section Order

Templates render sections in this order (if present in YAML):
1. Professional Summary / Profile / Research Interests
2. Professional Experience / Experience
3. Skills / Core Competencies / Technical Skills
4. Education
5. Certifications (if present)
6. Projects / Research Projects (if present)
7. Publications (if present)
8. Awards & Honors (if present)
9. Languages (if present)

To change order, edit the template file section blocks.

## Typst Installation

### macOS

```bash
brew install typst
```

### Linux

**Arch Linux:**
```bash
pacman -S typst
```

**Ubuntu/Debian (via binary):**
```bash
curl -L https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
sudo mv typst-x86_64-unknown-linux-musl/typst /usr/local/bin/
```

### Windows

Download from GitHub releases:
- https://github.com/typst/typst/releases

Or via cargo:
```bash
cargo install typst-cli
```

## Troubleshooting

### Font Not Found

**Symptom:** "font 'Inter' not found" warning
**Solution:** Install Inter from Google Fonts, or change template to use system font:
```typst
#set text(font: ("Inter", "Helvetica", "Arial"))
```

### Compilation Errors

**Symptom:** Special characters causing errors
**Solution:** The yaml_to_typst.py script escapes special Typst characters automatically. If you see errors, check for unescaped `#`, `@`, `\`, `<`, `>` in your YAML.

**Symptom:** "expected ... found ..." syntax error
**Solution:** Check for unclosed brackets or wrong content/code mode usage.

**Symptom:** Content cut off or overlapping
**Solution:** Reduce content length, decrease font size, or adjust margins.

### PDF Generation Issues

**Symptom:** PDF not generated
**Solution:** Check Typst error output. Typst compiles in single pass.

**Symptom:** Fonts look wrong
**Solution:** Ensure fonts are installed on system. Run `typst fonts` to see available fonts.

## Best Practices

1. **Preview before applying:** Generate PDF and review carefully
2. **Test in B&W:** Print or convert to grayscale to ensure readability
3. **Check PDF text:** Copy-paste text from PDF to verify proper extraction (ATS test)
4. **Stay under 2 pages:** Most roles expect 1-2 pages maximum
5. **Proofread:** Review final PDF carefully
6. **Keep YAML source:** Easier to update than editing Typst directly

## Template Comparison Matrix

| Feature | Modern | Classic | Academic | Creative |
|---------|--------|---------|----------|----------|
| ATS-Friendly | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| Visual Appeal | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★★ |
| Conservative | ★★★☆☆ | ★★★★★ | ★★★★★ | ★☆☆☆☆ |
| Content Density | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★★★☆ |
| Easy Customization | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| Compilation Speed | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ |
| Print Quality | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ |
| Digital Quality | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ |

## Advanced Customization

For more extensive template modifications, see Typst documentation:
- Page setup: https://typst.app/docs/reference/layout/page/
- Text styling: https://typst.app/docs/reference/text/text/
- Colors: https://typst.app/docs/reference/visualize/color/
- Layout: https://typst.app/docs/reference/layout/
