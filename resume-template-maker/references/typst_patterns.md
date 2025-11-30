# Typst Patterns for Resume Templates

Code patterns for implementing common resume template features. Copy and adapt these patterns for new templates.

---

## Document Setup

### Basic Preamble
```typst
#set page(
  paper: "us-letter",
  margin: (top: 0.5in, bottom: 0.5in, left: 0.6in, right: 0.6in)
)

#set text(font: "Inter", size: 10pt)
#set par(leading: 0.6em, justify: false)

// Disable page numbers (single page)
#set page(numbering: none)

// Color definitions
#let primary = rgb("#005293")
#let darkgray = rgb("#404040")
#let lightgray = rgb("#c8c8c8")

// Link styling
#show link: it => text(fill: primary)[#it]
```

### Font Setup (Sans-Serif)
```typst
#set text(font: "Inter", size: 10pt)
// Or fallback chain:
#set text(font: ("Inter", "Helvetica", "Arial"), size: 10pt)
```

### Font Setup (Serif)
```typst
#set text(font: "New Computer Modern", size: 10pt)
// Or:
#set text(font: ("Times New Roman", "Times"), size: 10pt)
```

### Font Setup (Mixed)
```typst
#set text(font: "Source Sans Pro", size: 10pt)
#let heading-font = "Playfair Display"
// Use: text(font: heading-font)[Name Here]
```

---

## Header/Name Section

### Centered Name with Contact Row
```typst
#align(center)[
  #text(size: 24pt, weight: "bold")[{{ contact.name | typst_escape }}]
  {% if contact.title %}
  #v(0.2em)
  #text(size: 12pt)[{{ contact.title | typst_escape }}]
  {% endif %}
  #v(0.2em)
  #text(size: 10pt)[
    {{ contact.email | typst_escape }}
    {% if contact.phone %} | {{ contact.phone | typst_escape }}{% endif %}
    {% if contact.location %} | {{ contact.location | typst_escape }}{% endif %}
    {% if contact.linkedin %} | #link("https://{{ contact.linkedin }}")[LinkedIn]{% endif %}
    {% if contact.github %} | #link("https://{{ contact.github }}")[GitHub]{% endif %}
  ]
]
```

### Left-Aligned Name
```typst
#text(size: 24pt, weight: "bold")[{{ contact.name | typst_escape }}]
#v(0.1em)
#text(size: 10pt)[{{ contact.email | typst_escape }} | {{ contact.phone | typst_escape }} | {{ contact.location | typst_escape }}]
```

### Name with Colored Accent
```typst
#text(size: 24pt, weight: "bold", fill: primary)[{{ contact.name | typst_escape }}]
```

---

## Section Headers

### Simple Bold Header
```typst
#let section(title) = {
  v(0.8em)
  text(size: 12pt, weight: "bold")[#title]
  v(0.3em)
}
```

### Header with Underline
```typst
#let section(title) = {
  v(0.8em)
  text(size: 12pt, weight: "bold")[#title]
  v(-0.3em)
  line(length: 100%, stroke: 0.5pt + lightgray)
  v(0.3em)
}
```

### Header with Colored Line
```typst
#let section(title) = {
  v(0.8em)
  text(size: 12pt, weight: "bold", fill: primary)[#title]
  v(-0.3em)
  line(length: 100%, stroke: 1pt + primary)
  v(0.3em)
}
```

### Header with Side Line
```typst
#let section(title) = {
  v(0.8em)
  box(
    inset: (left: 6pt),
    stroke: (left: 3pt + primary),
    text(size: 12pt, weight: "bold")[#title]
  )
  v(0.3em)
}
```

### All-Caps Header
```typst
#let section(title) = {
  v(0.8em)
  text(size: 11pt, weight: "bold")[#upper(title)]
  v(-0.3em)
  line(length: 100%, stroke: 0.5pt)
  v(0.3em)
}
```

---

## Experience Section

### Standard Experience Entry
```typst
{% for job in experience %}
#block[
  *{{ job.company | typst_escape }}*{% if job.location %}, {{ job.location | typst_escape }}{% endif %}

  {% for position in job.positions %}
  #grid(
    columns: (1fr, auto),
    [_{{ position.title | typst_escape }}_],
    [{{ position.dates | typst_escape }}]
  )
  {% if position.achievements %}
  #v(0.2em)
  {% for achievement in position.achievements %}
  - {{ achievement | typst_escape }}
  {% endfor %}
  {% endif %}
  {% endfor %}
]
#v(0.5em)
{% endfor %}
```

### Experience with Grid Dates
```typst
{% for job in experience %}
#grid(
  columns: (1fr, auto),
  [*{{ job.company | typst_escape }}*],
  [{% if job.location %}{{ job.location | typst_escape }}{% endif %}]
)
{% for position in job.positions %}
#grid(
  columns: (1fr, auto),
  [_{{ position.title | typst_escape }}_],
  [{{ position.dates | typst_escape }}]
)
{% if position.achievements %}
#list(
  {% for achievement in position.achievements %}
  [{{ achievement | typst_escape }}],
  {% endfor %}
)
{% endif %}
{% endfor %}
#v(0.5em)
{% endfor %}
```

### Compact Experience (No Bullets)
```typst
{% for job in experience %}
*{{ job.company | typst_escape }}* | _{{ job.positions[0].title | typst_escape }}_ #h(1fr) {{ job.positions[0].dates | typst_escape }}

{{ job.positions[0].achievements | join(' ') | typst_escape }}
#v(0.3em)
{% endfor %}
```

---

## Skills Section

### Inline Skills by Category
```typst
{% for category, items in skills.items() %}
*{{ category | typst_escape }}:* {{ items | join(', ') | typst_escape }}{% if not loop.last %} \{% endif %}
{% endfor %}
```

### Skills as Grid
```typst
#grid(
  columns: (auto, 1fr),
  row-gutter: 0.4em,
  column-gutter: 1em,
  {% for category, items in skills.items() %}
  [*{{ category | typst_escape }}*], [{{ items | join(', ') | typst_escape }}],
  {% endfor %}
)
```

### Skills in Columns
```typst
#grid(
  columns: (1fr, 1fr),
  gutter: 1em,
  [
    {% for category, items in skills.items() %}
    {% if loop.index <= (skills|length // 2 + skills|length % 2) %}
    *{{ category | typst_escape }}:* {{ items | join(', ') | typst_escape }} \
    {% endif %}
    {% endfor %}
  ],
  [
    {% for category, items in skills.items() %}
    {% if loop.index > (skills|length // 2 + skills|length % 2) %}
    *{{ category | typst_escape }}:* {{ items | join(', ') | typst_escape }} \
    {% endif %}
    {% endfor %}
  ]
)
```

### Skills as Tags/Pills
```typst
#let skill-tag(content) = box(
  fill: lightgray,
  radius: 3pt,
  inset: (x: 4pt, y: 2pt),
  text(size: 9pt)[#content]
)

// Usage:
{% for category, items in skills.items() %}
{% for item in items %}#skill-tag[{{ item | typst_escape }}] {% endfor %}
{% endfor %}
```

---

## Education Section

### Standard Education Entry
```typst
{% for edu in education %}
#grid(
  columns: (1fr, auto),
  [*{{ edu.institution | typst_escape }}*{% if edu.location %}, {{ edu.location | typst_escape }}{% endif %}],
  [{{ edu.graduation_year | typst_escape }}]
)
{{ edu.degree | typst_escape }}{% if edu.gpa %} | GPA: {{ edu.gpa | typst_escape }}{% endif %}{% if edu.honors %} | {{ edu.honors | typst_escape }}{% endif %}
{% if not loop.last %}#v(0.3em){% endif %}
{% endfor %}
```

### Education with Details List
```typst
{% for edu in education %}
#grid(
  columns: (1fr, auto),
  [*{{ edu.institution | typst_escape }}*],
  [{{ edu.graduation_year | typst_escape }}]
)
_{{ edu.degree | typst_escape }}_
{% if edu.gpa or edu.honors or edu.minor %}
#list(
  {% if edu.gpa %}[GPA: {{ edu.gpa | typst_escape }}],{% endif %}
  {% if edu.honors %}[{{ edu.honors | typst_escape }}],{% endif %}
  {% if edu.minor %}[Minor: {{ edu.minor | typst_escape }}],{% endif %}
)
{% endif %}
{% endfor %}
```

---

## Two-Column Layout

### Sidebar + Main Content
```typst
#grid(
  columns: (30%, 1fr),
  gutter: 5%,
  align: top,
  [
    // SIDEBAR
    #section[Skills]
    {% for category, items in skills.items() %}
    *{{ category | typst_escape }}* \
    {{ items | join(', ') | typst_escape }}
    #v(0.5em)
    {% endfor %}

    #section[Education]
    {% for edu in education %}
    *{{ edu.institution | typst_escape }}* \
    {{ edu.degree | typst_escape }} \
    {{ edu.graduation_year | typst_escape }}
    #v(0.3em)
    {% endfor %}
  ],
  [
    // MAIN CONTENT
    #section[Experience]
    // ... experience entries
  ]
)
```

### Two Equal Columns
```typst
#grid(
  columns: (1fr, 1fr),
  gutter: 1em,
  [
    // LEFT COLUMN
  ],
  [
    // RIGHT COLUMN
  ]
)
```

---

## Optional Sections

### Certifications
```typst
{% if certifications %}
#section[Certifications]
{% for cert in certifications %}
#grid(
  columns: (1fr, auto),
  [*{{ cert.name | typst_escape }}* | {{ cert.issuer | typst_escape }}],
  [{{ cert.date | typst_escape }}]
)
{% endfor %}
{% endif %}
```

### Projects
```typst
{% if projects %}
#section[Projects]
{% for project in projects %}
#grid(
  columns: (1fr, auto),
  [*{{ project.name | typst_escape }}*{% if project.url %} | #link("{{ project.url }}")[Link]{% endif %}],
  [{{ project.dates | typst_escape }}]
)
{{ project.description | typst_escape }}
{% if project.technologies %}
_Technologies: {{ project.technologies | join(', ') | typst_escape }}_
{% endif %}
#v(0.4em)
{% endfor %}
{% endif %}
```

### Publications
```typst
{% if publications %}
#section[Publications]
{% for pub in publications %}
{{ pub.authors | typst_escape }}. "{{ pub.title | typst_escape }}." _{{ pub.venue | typst_escape }}_, {{ pub.date | typst_escape }}.{% if pub.url %} #link("{{ pub.url }}")[Link]{% endif %}
#v(0.3em)
{% endfor %}
{% endif %}
```

### Awards
```typst
{% if awards %}
#section[Awards]
{% for award in awards %}
#grid(
  columns: (1fr, auto),
  [*{{ award.name | typst_escape }}* | {{ award.issuer | typst_escape }}],
  [{{ award.date | typst_escape }}]
)
{% endfor %}
{% endif %}
```

### Languages
```typst
{% if languages %}
#section[Languages]
{% for lang in languages %}{{ lang.language | typst_escape }} ({{ lang.proficiency | typst_escape }}){% if not loop.last %}, {% endif %}{% endfor %}
{% endif %}
```

---

## Visual Elements

### Horizontal Rule
```typst
#v(0.3em)
#line(length: 100%, stroke: 0.5pt + lightgray)
#v(0.3em)
```

### Colored Box Header
```typst
#rect(
  width: 100%,
  fill: primary,
  inset: 8pt,
)[
  #align(center)[
    #text(fill: white, weight: "bold", size: 18pt)[{{ contact.name | typst_escape }}]
  ]
]
```

### Vertical Line (Sidebar Border)
```typst
#grid(
  columns: (28%, 0.5pt, 1fr),
  gutter: 2%,
  [
    // Sidebar content
  ],
  line(
    start: (0%, 0%),
    end: (0%, 100%),
    stroke: 0.5pt + lightgray
  ),
  [
    // Main content
  ]
)
```

---

## Spacing Commands

### Consistent Spacing System
```typst
// Define at top of template
#let section-gap = 0.8em
#let item-gap = 0.3em
#let entry-gap = 0.5em

// Usage
#v(section-gap)
// content
#v(item-gap)
// more content
```

### Tight List Spacing
```typst
#set list(
  indent: 0.5em,
  body-indent: 0.5em,
  spacing: 0.4em,
  tight: true
)
```

### Remove Paragraph Spacing
```typst
#set par(leading: 0.5em, spacing: 0.5em)
```

---

## Jinja2 Integration Notes

### Escape Filter (Required)
Always use `| typst_escape` on user content:
```typst
{{ contact.name | typst_escape }}
{{ achievement | typst_escape }}
```

### Conditional Sections
```typst
{% if certifications %}
#section[Certifications]
...
{% endif %}
```

### Loop with Index
```typst
{% for item in items %}
{% if not loop.last %}, {% endif %}
{% endfor %}
```

### Safe Default Values
```typst
{{ contact.phone | default('') | typst_escape }}
```

### Whitespace Control
```typst
{%- for item in items -%}  // No extra whitespace
{{ item | typst_escape }}
{%- endfor -%}
```

---

## Complete Minimal Template

```typst
// Page setup
#set page(paper: "us-letter", margin: (x: 0.6in, y: 0.5in))
#set text(font: "Inter", size: 10pt)
#set par(leading: 0.6em)
#set page(numbering: none)

// Colors
#let primary = rgb("#005293")
#let lightgray = rgb("#c8c8c8")

// Section helper
#let section(title) = {
  v(0.7em)
  text(size: 12pt, weight: "bold")[#title]
  v(-0.3em)
  line(length: 100%, stroke: 0.5pt + lightgray)
  v(0.3em)
}

// Link styling
#show link: it => text(fill: primary)[#it]

// HEADER
#align(center)[
  #text(size: 24pt, weight: "bold")[{{ contact.name | typst_escape }}]
  #v(0.2em)
  #text(size: 10pt)[{{ contact.email | typst_escape }} | {{ contact.phone | typst_escape }} | {{ contact.location | typst_escape }}]
]

// SUMMARY
{% if summary %}
#section[Summary]
{{ summary | typst_escape }}
{% endif %}

// EXPERIENCE
#section[Experience]
{% for job in experience %}
#grid(columns: (1fr, auto),
  [*{{ job.company | typst_escape }}*],
  [{{ job.location | typst_escape }}]
)
{% for position in job.positions %}
#grid(columns: (1fr, auto),
  [_{{ position.title | typst_escape }}_],
  [{{ position.dates | typst_escape }}]
)
{% for achievement in position.achievements %}
- {{ achievement | typst_escape }}
{% endfor %}
{% endfor %}
#v(0.4em)
{% endfor %}

// SKILLS
#section[Skills]
{% for category, items in skills.items() %}
*{{ category | typst_escape }}:* {{ items | join(', ') | typst_escape }}
{% endfor %}

// EDUCATION
#section[Education]
{% for edu in education %}
#grid(columns: (1fr, auto),
  [*{{ edu.institution | typst_escape }}*],
  [{{ edu.graduation_year | typst_escape }}]
)
{{ edu.degree | typst_escape }}{% if edu.gpa %} | GPA: {{ edu.gpa | typst_escape }}{% endif %}
#v(0.3em)
{% endfor %}
```
