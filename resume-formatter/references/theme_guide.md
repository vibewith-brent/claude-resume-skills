# Resume Formatter Theme Guide

## Overview

The resume-formatter skill includes 3 professionally designed Typst templates, each optimized for different use cases.

## Available Themes

### 1. Executive (`executive`)

**Best for:** Most professional roles, senior positions
**Style:** Clean hierarchy with navy/blue accents
**Features:**
- Professional layout with clear visual hierarchy
- Navy section headers with subtle underline
- Blue accent for dates and links
- Inline skills format (no pills/tags)
- Single-column, ATS-friendly

**Pros:**
- Professional and contemporary
- Great balance of density and whitespace
- ATS-compatible
- Works for most industries

**Cons:**
- Requires Inter font (or edit for fallback)

**Recommended for:**
- Software Engineers
- Data Scientists
- Product Managers
- Senior/Staff roles
- Most tech and business roles

---

### 2. Compact (`compact`)

**Best for:** Extensive experience, dense content
**Style:** Maximum density without sacrificing readability
**Features:**
- Tighter margins and spacing
- Smaller fonts (8-9pt)
- Gray section header badges
- Inline skills format
- Square bullet points

**Pros:**
- Fits more content per page
- Great for 10+ years experience
- Still ATS-compatible
- Clean despite density

**Cons:**
- May be too dense for some readers
- Smaller text may be harder to read

**Recommended for:**
- Senior/Staff+ engineers with extensive history
- Consultants with many projects
- Anyone with 10+ years relevant experience
- Roles requiring comprehensive skill lists

---

### 3. Minimal (`minimal`)

**Best for:** Clean, understated presentation
**Style:** Monochromatic with single blue accent
**Features:**
- Generous whitespace
- Subtle hierarchy (light gray accents)
- Clean section headers with thin lines
- Inline skills format
- Understated bullet points

**Pros:**
- Clean and professional
- Easy to read
- Works well printed in B&W
- Subtle and not distracting

**Cons:**
- Less visually distinctive
- May appear plain for creative roles

**Recommended for:**
- Design-adjacent roles (shows restraint)
- Roles where content speaks for itself
- When you want clean over flashy
- Print-heavy application processes

## Choosing the Right Template

**Decision tree:**

```
Do you have extensive experience (10+ years with many roles)?
  └─ YES → Use Compact
  └─ NO  → Continue

Do you want clean/understated look?
  └─ YES → Use Minimal
  └─ NO  → Use Executive (default)
```

## Customization

### Color Changes

**Executive template:**
Edit color definitions in `executive.typ.j2`:
```typst
#let primary = rgb("#1e3a5f")    // Navy - headers
#let accent = rgb("#0369a1")     // Blue - dates, links
#let muted = rgb("#64748b")      // Gray - secondary text
```

**Compact template:**
Edit color definitions in `compact.typ.j2`:
```typst
#let ink = rgb("#0f0f0f")        // Near-black
#let blue = rgb("#1d4ed8")       // Blue accent
#let cloud = rgb("#f3f4f6")      // Light gray backgrounds
```

**Minimal template:**
Edit color definitions in `minimal.typ.j2`:
```typst
#let black = rgb("#171717")      // Headers
#let accent = rgb("#2563eb")     // Blue accent
#let light = rgb("#a3a3a3")      // Muted elements
```

### Font Changes

**All templates:**
Change font and size in `#set text()`:
```typst
#set text(font: "Inter", size: 9pt)  // Change size to 8pt, 10pt, etc.
```

Alternative fonts:
```typst
#set text(font: "Helvetica")      // macOS default
#set text(font: "Arial")          // Windows default
#set text(font: "Liberation Sans") // Linux default
```

### Margin Adjustments

**All templates:**
```typst
#set page(
  paper: "us-letter",
  margin: (top: 0.4in, bottom: 0.35in, left: 0.5in, right: 0.5in)
)
```

### Section Order

Templates render sections in this order (if present in YAML):
1. Professional Summary / Profile
2. Experience
3. Skills
4. Education
5. Certifications (if present)
6. Projects (if present)
7. Publications (if present)
8. Awards (if present)
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

```bash
winget install --id Typst.Typst
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

**Symptom:** Content cut off or overlapping
**Solution:** Reduce content length, decrease font size, or adjust margins.

## Best Practices

1. **Preview before applying:** Generate PDF and review carefully
2. **Test in B&W:** Print or convert to grayscale to ensure readability
3. **Check PDF text:** Copy-paste text from PDF to verify proper extraction (ATS test)
4. **Stay under 2 pages:** Most roles expect 1-2 pages maximum
5. **Proofread:** Review final PDF carefully
6. **Keep YAML source:** Easier to update than editing Typst directly

## Template Comparison Matrix

| Feature | Executive | Compact | Minimal |
|---------|-----------|---------|---------|
| ATS-Friendly | ★★★★★ | ★★★★★ | ★★★★★ |
| Content Density | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| Visual Appeal | ★★★★☆ | ★★★☆☆ | ★★★★☆ |
| Print Quality | ★★★★★ | ★★★★★ | ★★★★★ |
| Best For | Most roles | Dense experience | Clean look |

## Advanced Customization

For more extensive template modifications, see Typst documentation:
- Page setup: https://typst.app/docs/reference/layout/page/
- Text styling: https://typst.app/docs/reference/text/text/
- Colors: https://typst.app/docs/reference/visualize/color/
- Layout: https://typst.app/docs/reference/layout/
