# LaTeX Patterns for Resume Templates

Code patterns for implementing common resume template features. Copy and adapt these patterns for new templates.

---

## Document Setup

### Basic Preamble
```latex
\documentclass[11pt,letterpaper]{article}
\usepackage[margin=0.7in]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{parskip}

% Disable page numbers
\pagestyle{empty}

% Color definitions
\definecolor{primary}{RGB}{0, 82, 147}
\definecolor{darkgray}{RGB}{64, 64, 64}
\definecolor{lightgray}{RGB}{200, 200, 200}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    urlcolor=primary,
    pdfborder={0 0 0}
}
```

### Font Setup (Sans-Serif)
```latex
\setmainfont{TeX Gyre Heros}[
    BoldFont = *-Bold,
    ItalicFont = *-Italic,
    BoldItalicFont = *-BoldItalic
]
```

### Font Setup (Serif)
```latex
\setmainfont{TeX Gyre Termes}[
    BoldFont = *-Bold,
    ItalicFont = *-Italic,
    BoldItalicFont = *-BoldItalic
]
```

### Font Setup (Mixed)
```latex
\setmainfont{Source Sans Pro}
\newfontfamily\headingfont{Playfair Display}
% Use: {\headingfont Name Here}
```

---

## Header/Name Section

### Centered Name with Contact Row
```latex
\begin{center}
    {\fontsize{24}{28}\selectfont\bfseries {{ contact.name | latex_escape }}}\\[8pt]
    {% if contact.title %}
    {\fontsize{12}{14}\selectfont {{ contact.title | latex_escape }}}\\[4pt]
    {% endif %}
    {\small
    {{ contact.email | latex_escape }}
    {% if contact.phone %} | {{ contact.phone | latex_escape }}{% endif %}
    {% if contact.location %} | {{ contact.location | latex_escape }}{% endif %}
    {% if contact.linkedin %} | \href{https://{{ contact.linkedin | latex_escape }}}{LinkedIn}{% endif %}
    {% if contact.github %} | \href{https://{{ contact.github | latex_escape }}}{GitHub}{% endif %}
    }
\end{center}
```

### Left-Aligned Name
```latex
{\fontsize{24}{28}\selectfont\bfseries {{ contact.name | latex_escape }}}\\[4pt]
{\small {{ contact.email | latex_escape }} | {{ contact.phone | latex_escape }} | {{ contact.location | latex_escape }}}
```

### Name with Colored Accent
```latex
{\fontsize{24}{28}\selectfont\bfseries\color{primary} {{ contact.name | latex_escape }}}
```

---

## Section Headers

### Simple Bold Header
```latex
\titleformat{\section}
    {\large\bfseries}
    {}
    {0pt}
    {}
\titlespacing*{\section}{0pt}{12pt}{6pt}
```

### Header with Underline
```latex
\titleformat{\section}
    {\large\bfseries}
    {}
    {0pt}
    {}
    [\vspace{-6pt}\rule{\textwidth}{0.5pt}]
\titlespacing*{\section}{0pt}{14pt}{8pt}
```

### Header with Colored Line
```latex
\titleformat{\section}
    {\large\bfseries\color{primary}}
    {}
    {0pt}
    {}
    [\vspace{-6pt}{\color{primary}\rule{\textwidth}{1pt}}]
```

### Header with Side Line
```latex
\titleformat{\section}
    {\large\bfseries}
    {}
    {0pt}
    {\color{primary}\rule[-2pt]{3pt}{12pt}\hspace{6pt}}
```

### All-Caps Header
```latex
\titleformat{\section}
    {\normalsize\bfseries\MakeUppercase}
    {}
    {0pt}
    {}
    [\vspace{-6pt}\rule{\textwidth}{0.5pt}]
```

---

## Experience Section

### Standard Experience Entry
```latex
{% for job in experience %}
\textbf{ {{ job.company | latex_escape }} }{% if job.location %}, {{ job.location | latex_escape }}{% endif %}\\
{% for position in job.positions %}
\textit{ {{ position.title | latex_escape }} } \hfill {{ position.dates | latex_escape }}
{% if position.achievements %}
\begin{itemize}[leftmargin=*, topsep=2pt, itemsep=1pt, parsep=0pt]
{% for achievement in position.achievements %}
    \item {{ achievement | latex_escape }}
{% endfor %}
\end{itemize}
{% endif %}
{% endfor %}
\vspace{8pt}
{% endfor %}
```

### Experience with Tabular Dates
```latex
{% for job in experience %}
\begin{tabular*}{\textwidth}{@{}l@{\extracolsep{\fill}}r@{}}
    \textbf{ {{ job.company | latex_escape }} } & {% if job.location %}{{ job.location | latex_escape }}{% endif %}
\end{tabular*}
{% for position in job.positions %}
\begin{tabular*}{\textwidth}{@{}l@{\extracolsep{\fill}}r@{}}
    \textit{ {{ position.title | latex_escape }} } & {{ position.dates | latex_escape }}
\end{tabular*}
{% if position.achievements %}
\begin{itemize}[leftmargin=12pt, topsep=2pt, itemsep=1pt]
{% for achievement in position.achievements %}
    \item {{ achievement | latex_escape }}
{% endfor %}
\end{itemize}
{% endif %}
{% endfor %}
\vspace{6pt}
{% endfor %}
```

### Compact Experience (No Bullets)
```latex
{% for job in experience %}
\textbf{ {{ job.company | latex_escape }} } | \textit{ {{ job.positions[0].title | latex_escape }} } \hfill {{ job.positions[0].dates | latex_escape }}\\
{{ job.positions[0].achievements | join(' ') | latex_escape }}\\[4pt]
{% endfor %}
```

---

## Skills Section

### Inline Skills by Category
```latex
{% for category, items in skills.items() %}
\textbf{ {{ category | latex_escape }}: } {{ items | join(', ') | latex_escape }}{% if not loop.last %}\\{% endif %}
{% endfor %}
```

### Skills as Table
```latex
\begin{tabular}{@{}l l@{}}
{% for category, items in skills.items() %}
\textbf{ {{ category | latex_escape }} } & {{ items | join(', ') | latex_escape }} \\
{% endfor %}
\end{tabular}
```

### Skills in Columns
```latex
\begin{minipage}[t]{0.48\textwidth}
{% for category, items in skills.items() %}
{% if loop.index <= (skills|length // 2 + skills|length % 2) %}
\textbf{ {{ category | latex_escape }}: } {{ items | join(', ') | latex_escape }}\\[2pt]
{% endif %}
{% endfor %}
\end{minipage}
\hfill
\begin{minipage}[t]{0.48\textwidth}
{% for category, items in skills.items() %}
{% if loop.index > (skills|length // 2 + skills|length % 2) %}
\textbf{ {{ category | latex_escape }}: } {{ items | join(', ') | latex_escape }}\\[2pt]
{% endif %}
{% endfor %}
\end{minipage}
```

### Skills as Tags/Pills (Advanced)
```latex
\newcommand{\skilltag}[1]{%
    \tikz[baseline=(char.base)]{
        \node[fill=lightgray,rounded corners=3pt,inner sep=3pt] (char) {\small #1};
    }%
}
% Usage in template:
{% for category, items in skills.items() %}
{% for item in items %}\skilltag{ {{ item | latex_escape }} } {% endfor %}
{% endfor %}
```

---

## Education Section

### Standard Education Entry
```latex
{% for edu in education %}
\textbf{ {{ edu.institution | latex_escape }} }{% if edu.location %}, {{ edu.location | latex_escape }}{% endif %} \hfill {{ edu.graduation_year | latex_escape }}\\
{{ edu.degree | latex_escape }}
{% if edu.gpa %} | GPA: {{ edu.gpa | latex_escape }}{% endif %}
{% if edu.honors %} | {{ edu.honors | latex_escape }}{% endif %}
{% if not loop.last %}\\[4pt]{% endif %}
{% endfor %}
```

### Education with Details List
```latex
{% for edu in education %}
\textbf{ {{ edu.institution | latex_escape }} } \hfill {{ edu.graduation_year | latex_escape }}\\
\textit{ {{ edu.degree | latex_escape }} }
{% if edu.gpa or edu.honors or edu.minor %}
\begin{itemize}[leftmargin=*, topsep=2pt, itemsep=0pt]
{% if edu.gpa %}\item GPA: {{ edu.gpa | latex_escape }}{% endif %}
{% if edu.honors %}\item {{ edu.honors | latex_escape }}{% endif %}
{% if edu.minor %}\item Minor: {{ edu.minor | latex_escape }}{% endif %}
\end{itemize}
{% endif %}
{% endfor %}
```

---

## Two-Column Layout

### Sidebar + Main Content
```latex
\begin{minipage}[t]{0.28\textwidth}
    % SIDEBAR CONTENT
    \section{Skills}
    {% for category, items in skills.items() %}
    \textbf{ {{ category | latex_escape }} }\\
    {{ items | join(', ') | latex_escape }}\\[6pt]
    {% endfor %}

    \section{Education}
    {% for edu in education %}
    \textbf{ {{ edu.institution | latex_escape }} }\\
    {{ edu.degree | latex_escape }}\\
    {{ edu.graduation_year | latex_escape }}\\[4pt]
    {% endfor %}
\end{minipage}%
\hfill
\begin{minipage}[t]{0.68\textwidth}
    % MAIN CONTENT
    \section{Experience}
    % ... experience entries
\end{minipage}
```

### Two Equal Columns
```latex
\begin{minipage}[t]{0.48\textwidth}
    % LEFT COLUMN
\end{minipage}%
\hfill
\begin{minipage}[t]{0.48\textwidth}
    % RIGHT COLUMN
\end{minipage}
```

---

## Optional Sections

### Certifications
```latex
{% if certifications %}
\section{Certifications}
{% for cert in certifications %}
\textbf{ {{ cert.name | latex_escape }} } | {{ cert.issuer | latex_escape }} \hfill {{ cert.date | latex_escape }}{% if not loop.last %}\\{% endif %}
{% endfor %}
{% endif %}
```

### Projects
```latex
{% if projects %}
\section{Projects}
{% for project in projects %}
\textbf{ {{ project.name | latex_escape }} }{% if project.url %} | \href{ {{ project.url }} }{Link}{% endif %} \hfill {{ project.dates | latex_escape }}\\
{{ project.description | latex_escape }}
{% if project.technologies %}\\
\textit{Technologies: {{ project.technologies | join(', ') | latex_escape }} }
{% endif %}
{% if not loop.last %}\\[6pt]{% endif %}
{% endfor %}
{% endif %}
```

### Publications
```latex
{% if publications %}
\section{Publications}
{% for pub in publications %}
{{ pub.authors | latex_escape }}. ``{{ pub.title | latex_escape }}.'' \textit{ {{ pub.venue | latex_escape }} }, {{ pub.date | latex_escape }}.{% if pub.url %} \href{ {{ pub.url }} }{Link}{% endif %}{% if not loop.last %}\\[4pt]{% endif %}
{% endfor %}
{% endif %}
```

### Awards
```latex
{% if awards %}
\section{Awards}
{% for award in awards %}
\textbf{ {{ award.name | latex_escape }} } | {{ award.issuer | latex_escape }} \hfill {{ award.date | latex_escape }}{% if not loop.last %}\\{% endif %}
{% endfor %}
{% endif %}
```

### Languages
```latex
{% if languages %}
\section{Languages}
{% for lang in languages %}
{{ lang.language | latex_escape }} ({{ lang.proficiency | latex_escape }}){% if not loop.last %}, {% endif %}
{% endfor %}
{% endif %}
```

---

## Visual Elements

### Horizontal Rule
```latex
\vspace{4pt}
{\color{lightgray}\rule{\textwidth}{0.5pt}}
\vspace{4pt}
```

### Colored Box Header
```latex
\colorbox{primary}{\parbox{\dimexpr\textwidth-2\fboxsep}{%
    \color{white}\centering\bfseries\large {{ contact.name | latex_escape }}
}}
```

### Vertical Line (Sidebar Border)
```latex
% In sidebar minipage:
\begin{minipage}[t]{0.28\textwidth}
...
\end{minipage}%
\hspace{0.02\textwidth}%
{\color{lightgray}\rule{0.5pt}{\textheight}}%
\hspace{0.02\textwidth}%
\begin{minipage}[t]{0.66\textwidth}
...
\end{minipage}
```

---

## Spacing Commands

### Consistent Spacing System
```latex
% Define in preamble
\newcommand{\sectionspace}{\vspace{12pt}}
\newcommand{\subsectionspace}{\vspace{6pt}}
\newcommand{\itemspace}{\vspace{2pt}}

% Usage
\section{Experience}
\sectionspace
% content
\subsectionspace
% more content
```

### Tight List Spacing
```latex
\setlist[itemize]{
    leftmargin=*,
    topsep=2pt,
    itemsep=1pt,
    parsep=0pt,
    partopsep=0pt
}
```

### Remove Paragraph Spacing
```latex
\setlength{\parskip}{0pt}
\setlength{\parindent}{0pt}
```

---

## Jinja2 Integration Notes

### Escape Filter (Required)
Always use `| latex_escape` on user content:
```latex
{{ contact.name | latex_escape }}
{{ achievement | latex_escape }}
```

### Conditional Sections
```latex
{% if certifications %}
\section{Certifications}
...
{% endif %}
```

### Loop with Index
```latex
{% for item in items %}
{% if not loop.last %}, {% endif %}
{% endfor %}
```

### Safe Default Values
```latex
{{ contact.phone | default('') | latex_escape }}
```

### Whitespace Control
```latex
{%- for item in items -%}  {# No extra whitespace #}
{{ item | latex_escape }}
{%- endfor -%}
```

---

## Complete Minimal Template

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage[margin=0.7in]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{parskip}

\pagestyle{empty}
\setmainfont{TeX Gyre Heros}
\definecolor{primary}{RGB}{0, 82, 147}
\hypersetup{colorlinks=true, urlcolor=primary}

\titleformat{\section}{\large\bfseries}{}{0pt}{}[\vspace{-6pt}\rule{\textwidth}{0.5pt}]
\titlespacing*{\section}{0pt}{12pt}{6pt}

\setlist[itemize]{leftmargin=*, topsep=2pt, itemsep=1pt, parsep=0pt}

\begin{document}

% HEADER
\begin{center}
{\fontsize{24}{28}\selectfont\bfseries {{ contact.name | latex_escape }}}\\[6pt]
{\small {{ contact.email | latex_escape }} | {{ contact.phone | latex_escape }} | {{ contact.location | latex_escape }}}
\end{center}

% SUMMARY
{% if summary %}
\section{Summary}
{{ summary | latex_escape }}
{% endif %}

% EXPERIENCE
\section{Experience}
{% for job in experience %}
\textbf{ {{ job.company | latex_escape }} } \hfill {{ job.location | latex_escape }}\\
{% for position in job.positions %}
\textit{ {{ position.title | latex_escape }} } \hfill {{ position.dates | latex_escape }}
\begin{itemize}
{% for achievement in position.achievements %}
\item {{ achievement | latex_escape }}
{% endfor %}
\end{itemize}
{% endfor %}
{% endfor %}

% SKILLS
\section{Skills}
{% for category, items in skills.items() %}
\textbf{ {{ category | latex_escape }}: } {{ items | join(', ') | latex_escape }}\\
{% endfor %}

% EDUCATION
\section{Education}
{% for edu in education %}
\textbf{ {{ edu.institution | latex_escape }} } \hfill {{ edu.graduation_year | latex_escape }}\\
{{ edu.degree | latex_escape }}{% if edu.gpa %} | GPA: {{ edu.gpa | latex_escape }}{% endif %}\\[4pt]
{% endfor %}

\end{document}
```
