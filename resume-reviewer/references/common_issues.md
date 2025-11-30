# Common LaTeX Resume Issues & Fixes

Known failure patterns in LaTeX resume compilation with specific solutions.

---

## 1. Content Overflow

### Symptom
Content extends beyond page margins, text cut off, or runs onto unwanted pages.

### Causes & Fixes

**Too many bullets per role**
```latex
% Problem: 8+ bullets per job
% Fix: Reduce to 4-6 most impactful bullets
% Or reduce spacing:
\setlength{\itemsep}{0pt}
\setlength{\parskip}{0pt}
```

**Long achievement bullets wrapping poorly**
```latex
% Fix: Reduce bullet text or adjust list margins
\begin{itemize}[leftmargin=*, labelsep=0.5em]
```

**Skills section too long**
```latex
% Fix: Use inline format instead of list
% Before:
\begin{itemize}
  \item Python
  \item JavaScript
\end{itemize}

% After:
\textbf{Languages:} Python, JavaScript, TypeScript, Go
```

**Margins too generous for content**
```latex
% Fix: Reduce margins (but not below 0.5in)
\usepackage[margin=0.6in]{geometry}
```

---

## 2. Inconsistent Spacing

### Symptom
Gaps between sections vary, some areas cramped while others have excess space.

### Causes & Fixes

**Mixed spacing commands**
```latex
% Problem: Using \vspace, \bigskip, \\[10pt] inconsistently
% Fix: Define consistent spacing commands
\newcommand{\sectionspacing}{\vspace{12pt}}
\newcommand{\itemspacing}{\vspace{4pt}}
```

**List environment adding extra space**
```latex
% Fix: Control list spacing globally
\usepackage{enumitem}
\setlist{nosep, leftmargin=*}

% Or per-list:
\begin{itemize}[topsep=0pt, partopsep=0pt, itemsep=2pt]
```

**Section command adding inconsistent space**
```latex
% Fix: Use titlesec for consistent section formatting
\usepackage{titlesec}
\titlespacing*{\section}{0pt}{12pt}{6pt}
```

---

## 3. Date Alignment Issues

### Symptom
Dates don't align on the right side, or dates on different lines don't match up.

### Causes & Fixes

**Using tabs or spaces for alignment**
```latex
% Problem: "Software Engineer \t\t Jan 2020 - Present"
% Fix: Use tabular or hfill

% Option 1: hfill
\textbf{Software Engineer} \hfill Jan 2020 - Present

% Option 2: tabular with fixed width
\begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
  \textbf{Software Engineer} & Jan 2020 - Present \\
\end{tabular*}
```

**Dates with different lengths**
```latex
% Problem: "Jan 2020 - Present" vs "Mar 2018 - Dec 2019"
% Fix: Use consistent date format or fixed-width column
\begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
  \textbf{Role} & \makebox[3cm][r]{Jan 2020 - Present} \\
\end{tabular*}
```

---

## 4. Font & Typography Issues

### Symptom
Fonts look wrong, inconsistent, or don't match intended design.

### Causes & Fixes

**TeX Gyre fonts not found**
```latex
% Fix: Ensure fontspec and fonts are available
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}  % Ensure MacTeX full install

% Fallback if font missing:
\IfFontExistsTF{TeX Gyre Heros}{
  \setsansfont{TeX Gyre Heros}
}{
  \setsansfont{Helvetica}  % macOS fallback
}
```

**Font size hierarchy unclear**
```latex
% Fix: Define clear hierarchy
\newcommand{\namefont}{\fontsize{24}{28}\selectfont\bfseries}
\newcommand{\sectionfont}{\fontsize{12}{14}\selectfont\bfseries}
\newcommand{\bodyfont}{\fontsize{10}{12}\selectfont}
```

**Special characters rendering incorrectly**
```latex
% Problem: Bullets show as boxes or wrong symbols
% Fix: Use explicit bullet character
\renewcommand{\labelitemi}{\textbullet}

% For en-dash in date ranges:
Jan 2020 -- Present  % Two hyphens = en-dash

% For proper quotes:
``quoted text''  % LaTeX style
% Or use csquotes package
```

---

## 5. Orphans & Widows

### Symptom
Section header alone at page bottom, or single line at page top.

### Causes & Fixes

**Section header orphaned**
```latex
% Fix: Keep header with following content
\usepackage{needspace}
\needspace{4\baselineskip}  % Before section command

% Or use titlesec
\titlespacing*{\section}{0pt}{12pt plus 2pt minus 2pt}{6pt}[0pt]

% Or manual prevention:
\section{Experience}
\nopagebreak
```

**Widow lines**
```latex
% Fix: Global penalties
\widowpenalty=10000
\clubpenalty=10000

% Or adjust content to fill/reduce page naturally
```

---

## 6. Column/Sidebar Issues

### Symptom
Two-column layouts misaligned, sidebar content doesn't match main content height.

### Causes & Fixes

**Columns not aligned at top**
```latex
% Fix: Use minipage with [t] alignment
\begin{minipage}[t]{0.3\textwidth}
  % Sidebar content
\end{minipage}%
\hfill
\begin{minipage}[t]{0.65\textwidth}
  % Main content
\end{minipage}
```

**Column gap inconsistent**
```latex
% Fix: Use consistent separation
\newlength{\columnsep}
\setlength{\columnsep}{0.05\textwidth}

\begin{minipage}[t]{0.3\textwidth}...\end{minipage}%
\hspace{\columnsep}%
\begin{minipage}[t]{0.65\textwidth}...\end{minipage}
```

**Sidebar too long/short**
```latex
% Fix: Adjust content distribution
% Move some skills to main area, or
% Use parbox for fixed-height sidebar
```

---

## 7. Color Issues

### Symptom
Colors don't render, wrong shade, or poor contrast.

### Causes & Fixes

**Color not defined**
```latex
% Fix: Define colors explicitly
\usepackage{xcolor}
\definecolor{primary}{RGB}{0, 82, 147}     % Dark blue
\definecolor{secondary}{RGB}{100, 100, 100} % Gray
\definecolor{accent}{HTML}{2E86AB}          % Teal
```

**Color too light for text**
```latex
% Problem: Light gray text hard to read
% Fix: Ensure sufficient contrast
% Text should be at least 4.5:1 contrast ratio
% Dark gray: RGB(51, 51, 51) or #333333
% Avoid anything lighter than RGB(100, 100, 100) for body text
```

**Colors don't print well**
```latex
% Fix: Test with grayscale preview
% Avoid pure color for critical info
% Use bold/size for emphasis, color as secondary
```

---

## 8. Compilation Errors

### Symptom
pdflatex fails, produces errors, or output is corrupted.

### Causes & Fixes

**Special characters not escaped**
```latex
% Problem: "Increased revenue by 50%" fails
% Fix: Escape special characters
Increased revenue by 50\%

% Characters requiring escape: # $ % & _ { } ~ ^
% Use latex_escape filter in Jinja2 templates
```

**Missing packages**
```latex
% Fix: Install full MacTeX or add specific packages
% Common packages needed:
\usepackage{geometry}    % Margins
\usepackage{fontspec}    % Custom fonts (XeLaTeX/LuaLaTeX)
\usepackage{xcolor}      % Colors
\usepackage{enumitem}    % List customization
\usepackage{titlesec}    % Section formatting
\usepackage{hyperref}    % Links
```

**Unicode characters**
```latex
% Problem: UTF-8 characters fail with pdflatex
% Fix: Use XeLaTeX or LuaLaTeX instead
% Or add inputenc:
\usepackage[utf8]{inputenc}
```

---

## 9. Hyperlink Issues

### Symptom
Links have visible boxes, wrong colors, or don't work.

### Causes & Fixes

**Ugly link boxes**
```latex
% Fix: Configure hyperref
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=black,
  urlcolor=primary,  % Your defined color
  pdfborder={0 0 0}  % Remove boxes
}
```

**Links not clickable**
```latex
% Fix: Use proper href
\href{mailto:email@example.com}{email@example.com}
\href{https://linkedin.com/in/profile}{LinkedIn}
```

---

## 10. Skills Section Formatting

### Symptom
Skills section looks cramped, hard to scan, or wastes space.

### Causes & Fixes

**Long list of individual skills**
```latex
% Problem: 20+ skills as bullet list takes too much space
% Fix: Use inline format with categories

\textbf{Languages:} Python, JavaScript, TypeScript, Go, SQL \\
\textbf{Frameworks:} React, FastAPI, Django, Node.js \\
\textbf{Tools:} Docker, Kubernetes, AWS, Git, PostgreSQL
```

**Skills in table won't fit**
```latex
% Fix: Use tabularx for flexible columns
\usepackage{tabularx}
\begin{tabularx}{\textwidth}{@{}l X@{}}
  \textbf{Languages} & Python, JavaScript, TypeScript, Go \\
  \textbf{Tools} & Docker, Kubernetes, AWS, Terraform \\
\end{tabularx}
```

**Skills categories not aligned**
```latex
% Fix: Use description list with fixed label width
\begin{description}[labelwidth=2cm, leftmargin=2.2cm]
  \item[Languages] Python, JavaScript, Go
  \item[Frameworks] React, FastAPI, Django
\end{description}
```
