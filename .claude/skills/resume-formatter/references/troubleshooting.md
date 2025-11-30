# Resume Formatter Troubleshooting Guide

## Table of Contents
- [Installation Issues](#installation-issues)
- [Compilation Errors](#compilation-errors)
- [PDF Quality Issues](#pdf-quality-issues)
- [Content Issues](#content-issues)

## Installation Issues

### "pdflatex not found"

**Problem:** LaTeX distribution not installed

**Solution:**

**macOS:**
```bash
# Full installation (3.9 GB) - includes all packages
brew install --cask mactex

# OR minimal installation (100 MB) - may need additional packages
brew install --cask mactex-no-gui
```

**Linux (Ubuntu/Debian):**
```bash
# Full installation
sudo apt-get install texlive-full

# OR minimal installation
sudo apt-get install texlive-latex-base texlive-latex-extra
```

**Verify installation:**
```bash
pdflatex --version
```

### "Package not found" errors

**Problem:** Missing LaTeX package

**Solution:**

**Identify missing package** from error message (e.g., `fontawesome.sty`):

**macOS:**
```bash
sudo tlmgr install fontawesome
```

**Linux:**
```bash
sudo apt-cache search <package-name>
sudo apt-get install texlive-<relevant-package>
```

## Compilation Errors

### Special characters causing errors

**Problem:** YAML contains characters that need escaping in LaTeX (`&`, `%`, `$`, `#`, `_`, `{`, `}`)

**Solution:**

The `yaml_to_latex.py` script auto-escapes special LaTeX characters. If errors persist:

1. Check for unusual Unicode characters in YAML
2. Replace curly quotes with straight quotes
3. Remove emoji or special symbols
4. Use ASCII alternatives for accented characters (or use proper LaTeX encoding)

**Manual fixes in YAML:**
```yaml
# Bad
company: "AT&T"
# Good (script will handle this, but if manual editing needed)
company: "AT\\&T"
```

### "Dimension too large" error

**Problem:** Content overflowing page boundaries

**Solution:**

1. **Reduce content length** (preferred)
2. **Decrease font size:**
   ```latex
   \documentclass[10pt,a4paper]{...}  % Change from 11pt to 10pt
   ```
3. **Adjust margins:**
   ```latex
   \usepackage[scale=0.90]{geometry}  % Increase from 0.85
   ```
4. **Remove sections** or reduce bullets per role

### "Undefined control sequence" error

**Problem:** LaTeX command not recognized or typo in template

**Solution:**

1. Check error line number in LaTeX output
2. Verify package is installed for the command
3. Check for typos in custom template modifications
4. Try different template (e.g., classic instead of modern)

### Content cut off or overlapping

**Problem:** Too much content for page

**Solution:**

**Priority order:**
1. **Reduce content** (remove older roles, reduce bullets)
2. **Decrease font size:**
   ```latex
   \documentclass[10pt,a4paper]{...}
   ```
3. **Adjust margins:**
   ```latex
   % Modern template
   \usepackage[scale=0.90]{geometry}

   % Other templates
   \usepackage[margin=0.5in]{geometry}
   ```
4. **Switch to different template** (academic template handles multi-page better)

### "Emergency stop" error

**Problem:** Critical LaTeX compilation failure

**Solution:**

1. Check `.log` file for specific error:
   ```bash
   cat resume.log | grep -A 5 "!"
   ```
2. Common causes:
   - Missing `\end{document}`
   - Unmatched braces `{}`
   - Missing required package
   - Corrupted template file

3. Regenerate LaTeX from YAML to get clean template

## PDF Quality Issues

### Fonts look wrong or blurry

**Problem:** Missing font packages or incorrect PDF viewer

**Solution:**

1. **Ensure complete LaTeX installation** with font packages:
   ```bash
   # macOS
   sudo tlmgr install collection-fontsrecommended

   # Linux
   sudo apt-get install texlive-fonts-recommended
   ```

2. **Try different PDF viewer** (some viewers render fonts poorly)

3. **Use different template** if font issues persist

### Colors don't print well

**Problem:** Colors look good on screen but poor when printed

**Solution:**

1. **Preview in grayscale** before printing:
   - Most PDF viewers have grayscale preview option

2. **Use Classic template** for maximum print compatibility (no colors)

3. **Adjust colors for print** in template:
   ```latex
   % Use darker colors for better print quality
   \definecolor{primarycolor}{RGB}{0,51,102}  % Darker blue
   ```

4. **Test print** on actual printer before final submission

### Text not extractable (ATS issue)

**Problem:** Copy-paste from PDF doesn't work or produces garbled text

**Solution:**

1. **Test extraction:**
   ```bash
   pdftotext resume.pdf - | head -20
   ```

2. **Use ATS-friendly templates:**
   - Classic (best)
   - Modern (good)
   - Avoid Creative or heavily formatted templates for ATS submission

3. **Regenerate PDF** if extraction fails:
   ```bash
   # Clean up auxiliary files first
   rm -f resume.aux resume.log resume.out
   # Recompile
   uv run scripts/compile_latex.py resume.tex
   ```

4. **Check for corrupted template** - try different template

### Hyperlinks not working

**Problem:** Email/phone/URLs not clickable

**Solution:**

1. **Ensure hyperref package** is loaded in template:
   ```latex
   \usepackage{hyperref}
   ```

2. **Use Creative template** (has best hyperlink support)

3. **Manual hyperlink** in YAML if needed:
   ```yaml
   email: \href{mailto:name@example.com}{name@example.com}
   ```

## Content Issues

### Section not appearing in PDF

**Problem:** YAML section exists but doesn't render

**Solution:**

1. **Check YAML structure** matches schema:
   ```yaml
   # Correct
   experience:
     - company: "Company Name"
       title: "Job Title"

   # Wrong
   experience:
     company: "Company Name"  # Missing list structure
   ```

2. **Verify section name** matches template expectations

3. **Check for YAML syntax errors:**
   ```bash
   uv run -c "import yaml; yaml.safe_load(open('resume.yaml'))"
   ```

4. **Try different template** (some templates handle missing sections differently)

### Bullets not rendering correctly

**Problem:** Bullet points missing or formatted wrong

**Solution:**

1. **Check YAML bullet list format:**
   ```yaml
   # Correct
   achievements:
     - "First bullet point"
     - "Second bullet point"

   # Wrong
   achievements: "Single string not a list"
   ```

2. **Escape special characters** in bullet text

3. **Regenerate from YAML** to get clean template

### Date formatting issues

**Problem:** Dates not displaying correctly

**Solution:**

1. **Use consistent format in YAML:**
   ```yaml
   # Good
   start_date: "Jan 2020"
   end_date: "Dec 2022"

   # Also good
   start_date: "January 2020"
   end_date: "Present"
   ```

2. **Check template date handling** - some templates expect specific formats

3. **Manual formatting** if needed:
   ```yaml
   dates: "Jan 2020 - Dec 2022"  # Full date string
   ```

### Skills not grouping correctly

**Problem:** Skills section not organized by categories

**Solution:**

1. **Use categorized format in YAML:**
   ```yaml
   skills:
     - category: "Programming"
       items: ["Python", "Java", "Go"]
     - category: "Cloud"
       items: ["AWS", "GCP", "Azure"]
   ```

2. **Check template** supports categorized skills (modern and creative do)

3. **Fall back to simple list** if categories not supported:
   ```yaml
   skills: ["Python", "AWS", "Docker", "Kubernetes"]
   ```

## Debugging Tips

### Enable verbose LaTeX output

```bash
# Run pdflatex directly for detailed error messages
pdflatex -interaction=nonstopmode resume.tex
```

### Check intermediate files

```bash
# View log file for detailed errors
less resume.log

# View aux file for structure issues
cat resume.aux
```

### Clean rebuild

```bash
# Remove all generated files
rm -f resume.aux resume.log resume.out resume.pdf

# Regenerate LaTeX from YAML
uv run scripts/yaml_to_latex.py resume.yaml modern --output resume.tex

# Recompile
uv run scripts/compile_latex.py resume.tex
```

### Test with minimal YAML

Create minimal test resume to isolate issue:

```yaml
contact:
  name: "Test Name"
  email: "test@example.com"

summary: "Test summary."

experience:
  - company: "Test Company"
    title: "Test Title"
    start_date: "Jan 2020"
    end_date: "Present"
    achievements:
      - "Test achievement"

education:
  - degree: "BS"
    major: "Computer Science"
    university: "Test University"
    year: "2020"

skills:
  - "Python"
  - "SQL"
```

If minimal YAML works, gradually add sections back to identify problematic content.

## Getting Help

If issues persist:

1. **Check LaTeX log file** for specific error messages
2. **Try different template** to isolate template vs. content issues
3. **Validate YAML syntax** using online YAML validator
4. **Test with minimal example** to reproduce issue
5. **Review template source** in `assets/templates/latex/` for customization needs
