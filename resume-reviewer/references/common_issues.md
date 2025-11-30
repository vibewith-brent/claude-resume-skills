# Common Typst Resume Issues & Fixes

Known failure patterns in Typst resume compilation with specific solutions.

---

## 1. Content Overflow

### Symptom
Content extends beyond page margins, text cut off, or runs onto unwanted pages.

### Causes & Fixes

**Too many bullets per role**
```typst
// Problem: 8+ bullets per job
// Fix: Reduce to 4-6 most impactful bullets
// Or reduce spacing:
#set list(spacing: 0.5em)
```

**Long achievement bullets wrapping poorly**
```typst
// Fix: Reduce bullet text or adjust list margins
#set list(indent: 0.5em, body-indent: 0.5em)
```

**Skills section too long**
```typst
// Fix: Use inline format instead of list
// Before:
- Python
- JavaScript

// After:
*Languages:* Python, JavaScript, TypeScript, Go
```

**Margins too generous for content**
```typst
// Fix: Reduce margins (but not below 0.5in)
#set page(margin: (x: 0.5in, y: 0.5in))
```

---

## 2. Inconsistent Spacing

### Symptom
Gaps between sections vary, some areas cramped while others have excess space.

### Causes & Fixes

**Mixed spacing commands**
```typst
// Problem: Using v(), parbreak(), pagebreak() inconsistently
// Fix: Define consistent spacing
#let section-gap = 0.8em
#let item-gap = 0.3em

// Use consistently:
#v(section-gap)
```

**List environment adding extra space**
```typst
// Fix: Control list spacing globally
#set list(spacing: 0.4em, tight: true)

// Or per-list:
#list(spacing: 0.3em)[
  - Item 1
  - Item 2
]
```

**Section command adding inconsistent space**
```typst
// Fix: Use function for consistent sections
#let section(title) = {
  v(0.8em)
  text(weight: "bold", size: 12pt)[#title]
  v(0.3em)
  line(length: 100%, stroke: 0.5pt)
  v(0.4em)
}
```

---

## 3. Date Alignment Issues

### Symptom
Dates don't align on the right side, or dates on different lines don't match up.

### Causes & Fixes

**Using spaces for alignment**
```typst
// Problem: "Software Engineer     Jan 2020 - Present"
// Fix: Use grid or h(1fr)

// Option 1: h(1fr) for push-right
[*Software Engineer* #h(1fr) Jan 2020 - Present]

// Option 2: grid with columns
#grid(
  columns: (1fr, auto),
  [*Software Engineer*], [Jan 2020 - Present]
)
```

**Dates with different lengths**
```typst
// Problem: "Jan 2020 - Present" vs "Mar 2018 - Dec 2019"
// Fix: Use fixed-width box or consistent format
#box(width: 10em, align(right)[Jan 2020 - Present])
```

---

## 4. Font & Typography Issues

### Symptom
Fonts look wrong, inconsistent, or don't match intended design.

### Causes & Fixes

**System font not found**
```typst
// Fix: Use available system fonts
#set text(font: "Inter")  // Must be installed on system

// Fallback chain:
#set text(font: ("Inter", "Helvetica", "Arial"))
```

**Font size hierarchy unclear**
```typst
// Fix: Define clear hierarchy
#let name-size = 24pt
#let section-size = 14pt
#let body-size = 10pt

#set text(size: body-size)
```

**Special characters rendering incorrectly**
```typst
// Problem: Bullets show wrong
// Fix: Define explicit bullet
#set list(marker: [•])

// For en-dash in date ranges:
Jan 2020 #sym.dash.en Present
// Or just use double hyphen: Jan 2020 -- Present
```

---

## 5. Orphans & Widows

### Symptom
Section header alone at page bottom, or single line at page top.

### Causes & Fixes

**Section header orphaned**
```typst
// Fix: Keep header with following content using block
#block(breakable: false)[
  == Experience
  #v(0.3em)
  // First job entry
]

// Or use weak page break prevention
#set heading(supplement: none)
#show heading: it => block(breakable: false)[#it]
```

**Widow lines**
```typst
// Fix: Adjust content length or use blocks
#block(breakable: false)[
  // Keep related content together
]
```

---

## 6. Column/Sidebar Issues

### Symptom
Two-column layouts misaligned, sidebar content doesn't match main content height.

### Causes & Fixes

**Columns not aligned at top**
```typst
// Fix: Use grid with top alignment
#grid(
  columns: (30%, 65%),
  gutter: 5%,
  align: top,
  [
    // Sidebar content
  ],
  [
    // Main content
  ]
)
```

**Column gap inconsistent**
```typst
// Fix: Use consistent gutter
#let col-gap = 5%

#grid(
  columns: (30%, 1fr),
  gutter: col-gap,
  [...],
  [...]
)
```

**Sidebar too long/short**
```typst
// Fix: Adjust content distribution
// Move some skills to main area
// Or use place() for absolute positioning
```

---

## 7. Color Issues

### Symptom
Colors don't render, wrong shade, or poor contrast.

### Causes & Fixes

**Color not defined**
```typst
// Fix: Define colors explicitly
#let primary = rgb("#005293")     // Dark blue
#let secondary = rgb("#646464")   // Gray
#let accent = rgb("#2E86AB")      // Teal

#text(fill: primary)[Colored text]
```

**Color too light for text**
```typst
// Problem: Light gray text hard to read
// Fix: Ensure sufficient contrast
// Text should be at least 4.5:1 contrast ratio
// Dark gray: rgb("#333333")
// Avoid anything lighter than rgb("#646464") for body text
```

**Colors don't print well**
```typst
// Fix: Test with grayscale preview
// Avoid pure color for critical info
// Use bold/size for emphasis, color as secondary
```

---

## 8. Compilation Errors

### Symptom
Typst fails, produces errors, or output is corrupted.

### Causes & Fixes

**Special characters not escaped**
```typst
// Problem: Raw # or @ in text
// Fix: Escape with backslash
Increased revenue by 50\%
Email: user\@example.com
Issue \#123

// Characters requiring escape: # @ \ < >
// Use typst_escape filter in Jinja2 templates
```

**Syntax errors**
```typst
// Problem: Invalid Typst syntax
// Fix: Check for common issues:

// Wrong: Missing space after #
#text[hello]  // correct
#text[hello]  // also correct

// Wrong: Unclosed brackets
#text(fill: red[text]  // missing )
#text(fill: red)[text]  // correct

// Wrong: Content in code mode
#let x = text  // wrong
#let x = [text]  // correct for content
```

**Unicode handling**
```typst
// Typst handles UTF-8 natively
// No special packages needed
// Just use characters directly: é, ñ, 中文
```

---

## 9. Hyperlink Issues

### Symptom
Links have visible boxes, wrong colors, or don't work.

### Causes & Fixes

**Link styling**
```typst
// Fix: Configure link appearance
#show link: it => text(fill: primary)[#it]

// Or underline:
#show link: it => underline(text(fill: primary)[#it])
```

**Links not working**
```typst
// Fix: Use proper link syntax
#link("mailto:email@example.com")[email\@example.com]
#link("https://linkedin.com/in/profile")[LinkedIn]
```

---

## 10. Skills Section Formatting

### Symptom
Skills section looks cramped, hard to scan, or wastes space.

### Causes & Fixes

**Long list of individual skills**
```typst
// Problem: 20+ skills as bullet list takes too much space
// Fix: Use inline format with categories

*Languages:* Python, JavaScript, TypeScript, Go \
*Frameworks:* React, FastAPI, Django, Node.js \
*Tools:* Docker, Kubernetes, AWS, Git, PostgreSQL
```

**Skills in grid won't fit**
```typst
// Fix: Use grid with flexible columns
#grid(
  columns: (auto, 1fr),
  gutter: 0.5em,
  [*Languages*], [Python, JavaScript, TypeScript, Go],
  [*Tools*], [Docker, Kubernetes, AWS, Terraform],
)
```

**Skills categories not aligned**
```typst
// Fix: Use terms list or grid with fixed first column
#grid(
  columns: (6em, 1fr),
  row-gutter: 0.4em,
  [*Languages*], [Python, JavaScript, Go],
  [*Frameworks*], [React, FastAPI, Django],
)
```
