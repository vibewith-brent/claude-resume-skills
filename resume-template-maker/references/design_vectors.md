# Design Vectors for Resume Templates

Multi-dimensional guidance for creating distinctive, professional resume templates. Each vector provides "mid-altitude" direction—specific enough to guide decisions, flexible enough to allow creativity.

---

## 0. Content Fitting (Do This First)

Before making aesthetic decisions, ensure content fits the target page count. This is the most important aspect of template customization.

### The Reality

Each person's resume content is unique. A template designed for 15 years of experience won't work for a new grad. Fitting content well requires tuning multiple parameters together.

### Tuning Parameters (Quick Reference)

| Parameter | Typst Location | Typical Range | Effect |
|-----------|---------------|---------------|--------|
| Page margins | `#set page(margin: ...)` | 0.5-0.75in | +/- 4-5 lines per 0.1in change |
| Body font size | `#set text(size: ...)` | 9-10.5pt | Major density change |
| Line height | `#set par(leading: ...)` | 0.5-0.7em | Subtle density change |
| Section gap | `#v(...)` between sections | 6-12pt | Cumulative over many sections |
| List spacing | `#set list(spacing: ...)` | 2-4pt | Adds up with many bullets |
| Name size | Name text size | 18-24pt | Visual impact vs. space |

### Fitting Strategies

**Too Much Content (Overflow)**
1. Reduce margins from 0.75in → 0.5in (biggest impact)
2. Reduce body font from 10pt → 9pt
3. Reduce section gaps
4. Reduce line height from 0.7em → 0.5em
5. Reduce bullets per role (content decision)

**Too Little Content (Sparse)**
1. Increase margins for executive feel
2. Increase section gaps for breathing room
3. Expand skills into categorized groups
4. Add optional sections (projects, volunteer, certifications)

### Page Break Management

For multi-page resumes:
```typst
// Force page break before a section
#pagebreak(weak: true)

// Keep section together (avoid orphans)
#block(breakable: false)[
  // Section content
]
```

Rules:
- Break after complete job entries, never mid-bullets
- Keep headers with their content (no header at page bottom)
- Aim for roughly equal density on each page

---

## 1. Typography

Typography establishes personality before a single word is read. Avoid defaulting to Computer Modern or generic sans-serif.

### Font Family Selection

**Serif Options** (traditional, authoritative, academic):
| Font | Character | Use Case |
|------|-----------|----------|
| TeX Gyre Termes | Times-equivalent, professional | Finance, law, consulting |
| TeX Gyre Pagella | Palatino-like, elegant | Academic, publishing |
| Libertinus Serif | Modern traditional, readable | General professional |
| EB Garamond | Classic, refined | Executive, traditional industries |

**Sans-Serif Options** (modern, clean, tech-forward):
| Font | Character | Use Case |
|------|-----------|----------|
| TeX Gyre Heros | Helvetica-like, neutral modern | Tech, startups, general |
| TeX Gyre Adventor | Avant Garde-like, geometric | Design, creative |
| Fira Sans | Technical, Mozilla heritage | Engineering, open source |
| Source Sans Pro | Adobe, highly readable | General modern |

**Display/Accent Options** (headers, name):
| Font | Character | Use Case |
|------|-----------|----------|
| Playfair Display | Elegant contrast | Creative, fashion, luxury |
| Montserrat | Geometric modern | Startups, tech |
| Raleway | Elegant sans | Design, marketing |
| Oswald | Bold condensed | Impact, headlines only |

### Font Pairing Patterns

**Classic Combinations**:
```
Name: Serif Bold (24-28pt)
Headers: Same Serif Bold (12-14pt)
Body: Same Serif Regular (10-11pt)
→ Cohesive, traditional
```

**Modern Combinations**:
```
Name: Sans Bold (24-28pt)
Headers: Sans Bold or Semibold (12-14pt)
Body: Sans Regular (10-11pt)
→ Clean, contemporary
```

**Contrast Combinations**:
```
Name: Display/Serif Bold (24-28pt)
Headers: Sans Bold (12-14pt)
Body: Sans or Serif Regular (10-11pt)
→ Dynamic, distinctive
```

### Size Hierarchy

Five-level hierarchy for clear visual structure:

| Level | Element | Size Range | Weight |
|-------|---------|------------|--------|
| 1 | Name | 22-28pt | Bold |
| 2 | Section Headers | 12-14pt | Bold |
| 3 | Job Titles/Degrees | 11-12pt | Bold or Semibold |
| 4 | Companies/Institutions | 10-11pt | Regular or Italic |
| 5 | Body/Bullets | 10-11pt | Regular |

### Weight Contrast

**High Contrast** (bold name, clear sections):
- Name: 700-800 weight
- Headers: 600-700 weight
- Body: 400 weight
- Effect: Strong hierarchy, scannable

**Low Contrast** (subtle, elegant):
- Name: 600 weight
- Headers: 500-600 weight
- Body: 400 weight
- Effect: Refined, sophisticated

---

## 2. Layout

Layout determines how information flows and how quickly key details are found.

### Layout Patterns

**Single Column** (most common, safest):
```
┌─────────────────────────┐
│         NAME            │
│    Contact Info Row     │
├─────────────────────────┤
│       Summary           │
├─────────────────────────┤
│      Experience         │
├─────────────────────────┤
│       Skills            │
├─────────────────────────┤
│      Education          │
└─────────────────────────┘
```
- Best for: Most resumes, ATS compatibility
- Density: Medium
- Scanning: Top-to-bottom

**Two Column** (efficient, modern):
```
┌─────────────────────────┐
│         NAME            │
│    Contact Info Row     │
├───────────┬─────────────┤
│  Skills   │ Experience  │
│           │             │
│  Educ.    │             │
│           │             │
│  Certs    │             │
└───────────┴─────────────┘
```
- Best for: Dense content, 1-page constraint
- Density: High
- Scanning: Z-pattern

**Sidebar** (visual interest, creative):
```
┌────────┬────────────────┐
│        │     NAME       │
│  Side  │   Summary      │
│  bar   ├────────────────┤
│        │  Experience    │
│ Skills │                │
│ Contact│                │
│ Educ.  │                │
└────────┴────────────────┘
```
- Best for: Creative roles, visual industries
- Density: Variable
- Scanning: Left anchor + main flow

### Section Ordering

**Standard** (most expected):
1. Contact/Name
2. Summary
3. Experience
4. Skills
5. Education
6. Optional sections

**Experience-First** (senior professionals):
1. Contact/Name
2. Experience
3. Skills
4. Education
5. Summary (or omit)

**Education-First** (academic, recent grads):
1. Contact/Name
2. Education
3. Research/Publications
4. Experience
5. Skills

**Skills-Forward** (technical roles):
1. Contact/Name
2. Technical Skills
3. Experience
4. Projects
5. Education

### Information Density

**Sparse** (executive, senior):
- 1 page, generous margins
- 3-4 bullets per role
- Breathing room between sections
- Focus on impact, not detail

**Balanced** (mid-career):
- 1-2 pages
- 4-6 bullets per role
- Moderate spacing
- Comprehensive but curated

**Dense** (early career, transitioning):
- Maximum content on 1-2 pages
- Tight margins (0.5-0.6in)
- Compact spacing
- Every relevant detail included

---

## 3. Whitespace

Whitespace creates rhythm, guides the eye, and signals professionalism.

### Margin Philosophy

**Generous** (0.75-1.0 inch):
- Signals: Confidence, seniority, editorial quality
- Use when: Senior roles, sparse content, visual impact priority
- Trade-off: Less content space

**Balanced** (0.6-0.75 inch):
- Signals: Professional, organized
- Use when: Standard resumes, balanced content
- Trade-off: None significant

**Efficient** (0.5-0.6 inch):
- Signals: Dense information, thoroughness
- Use when: 1-page constraint with lots of content
- Trade-off: Can feel cramped if not managed well

### Section Spacing

Define consistent rhythm:

```typst
// Example spacing system
#let section-gap = 0.9em      // Between major sections
#let subsection-gap = 0.5em   // Between jobs/degrees
#let item-gap = 0.2em         // Between bullets

// Usage:
#v(section-gap)
```

### Spacing Ratios

Golden ratio-inspired spacing:
- Section gap: 14-16pt
- Subsection gap: 8-10pt
- Item gap: 2-4pt
- Line height: 1.1-1.3x font size

### Visual Balance

**Top-Heavy** (bad):
```
┌─────────────────┐
│ ████████████████│ ← Dense
│ ████████████████│
│ ████████████████│
│                 │ ← Empty
│                 │
└─────────────────┘
```
Fix: Redistribute content, add optional sections, or reduce early sections.

**Bottom-Heavy** (bad):
```
┌─────────────────┐
│                 │ ← Empty
│ ████████████████│
│ ████████████████│ ← Dense
│ ████████████████│
│ ████████████████│
└─────────────────┘
```
Fix: Move key content up, expand summary, or add early sections.

**Balanced** (good):
```
┌─────────────────┐
│ ████████████    │
│   █████████████ │
│ ██████████████  │
│   ████████████  │
│ █████████       │
└─────────────────┘
```

---

## 4. Color

Color creates hierarchy, personality, and visual interest—but can also distract or fail in printing.

### Palette Sizes

**Monochrome** (1 color + black):
- Black for all text
- One accent for headers/lines
- Safest, most professional
- Works in all print scenarios

**Duotone** (2 colors + black):
- Primary: Headers, name
- Secondary: Accents, lines, links
- Black: Body text
- More visual interest, still conservative

**Full Palette** (3 colors + black):
- Primary: Name, major headers
- Secondary: Subheaders, accents
- Tertiary: Lines, backgrounds, subtle elements
- Maximum visual interest
- Use carefully to avoid distraction

### Industry Color Associations

| Industry | Primary Colors | Avoid |
|----------|---------------|-------|
| Tech | Blue, teal, gray | Pink, orange |
| Finance | Navy, burgundy, gold | Bright colors |
| Healthcare | Blue, green, white | Red (blood), black (death) |
| Creative | Bold, unique palettes | Safe/boring colors |
| Legal | Navy, black, burgundy | Casual colors |
| Academia | Muted, traditional | Flashy colors |
| Startup | Vibrant, modern | Corporate/stuffy |

### Color Usage Patterns

**Headers Only**:
```typst
#let primary = rgb("#005293")
// Apply only to section headers
#text(fill: primary, weight: "bold")[Experience]
```

**Headers + Accent Lines**:
```typst
// Headers and horizontal rules
#line(length: 100%, stroke: 0.5pt + primary)
```

**Headers + Links**:
```typst
#show link: it => text(fill: primary)[#it]
```

**Subtle Background** (advanced):
```typst
// Sidebar or header background
#rect(fill: lightgray)[...]
```

### Print Considerations

Always test that:
- Text remains readable in grayscale
- Colors don't waste ink (avoid large fills)
- Contrast is sufficient (4.5:1 minimum)
- Critical info isn't color-dependent

### Specific Color Recommendations

**Safe Professional Blues**:
```typst
#let navyblue = rgb("#003366")      // Very conservative
#let royalblue = rgb("#005293")     // Professional modern
#let teal = rgb("#008080")          // Tech-friendly
#let slate = rgb("#2F4F4F")         // Sophisticated
```

**Creative Options**:
```typst
#let coral = rgb("#FF7F50")         // Warm, approachable
#let forest = rgb("#228B22")        // Natural, grounded
#let plum = rgb("#8E4585")          // Distinctive, creative
#let rust = rgb("#B7410E")          // Bold, confident
```

**Neutral Grays** (for secondary elements):
```typst
#let darkgray = rgb("#404040")      // Body text alternative
#let mediumgray = rgb("#808080")    // Dates, secondary info
#let lightgray = rgb("#C8C8C8")     // Rules, backgrounds
```

---

## Combining Vectors

### Example: Modern Tech Resume

```
Typography: TeX Gyre Heros (sans-serif), high weight contrast
Layout: Single column, skills-forward
Whitespace: Balanced margins (0.7in), clear section breaks
Color: Teal primary (#008080), headers only
```

### Example: Traditional Finance Resume

```
Typography: TeX Gyre Termes (serif), moderate contrast
Layout: Single column, standard order
Whitespace: Generous (0.9in), professional breathing room
Color: Navy (#003366) or pure black, minimal usage
```

### Example: Creative Designer Resume

```
Typography: Playfair Display (name) + Source Sans Pro (body)
Layout: Sidebar with main content
Whitespace: Asymmetric, intentional gaps
Color: Custom palette matching personal brand
```

---

## Anti-Patterns to Avoid

1. **Default fonts** — System defaults signal lack of attention to design
2. **Random color** — Accent color should be intentional, not arbitrary
3. **Inconsistent spacing** — Mixed spacing looks unpolished
4. **Over-designed** — Too many fonts, colors, or elements overwhelms
5. **Under-designed** — No visual hierarchy makes scanning difficult
6. **Ignoring print** — Designs that only work on screen
7. **Trend-chasing** — Ultra-trendy designs age poorly
8. **Copying exactly** — Templates should be inspired by, not copied from
