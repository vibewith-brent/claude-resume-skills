# Resume Formatter Troubleshooting Guide

## Table of Contents
- [Installation Issues](#installation-issues)
- [Compilation Errors](#compilation-errors)
- [PDF Quality Issues](#pdf-quality-issues)
- [Content Issues](#content-issues)

## Installation Issues

### "typst not found"

**Problem:** Typst not installed

**Solution:**

**macOS:**
```bash
brew install typst
```

**Linux:**
```bash
# Arch Linux
pacman -S typst

# Other Linux - download from GitHub releases
curl -L https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
sudo mv typst-x86_64-unknown-linux-musl/typst /usr/local/bin/
```

**Verify installation:**
```bash
typst --version
```

### Font not found

**Problem:** Template uses font not installed on system

**Solution:**

1. **Check available fonts:**
   ```bash
   # macOS
   system_profiler SPFontsDataType | grep "Full Name"

   # Linux
   fc-list : family
   ```

2. **Install Inter font** (used by modern template):
   - macOS: Download from Google Fonts, double-click to install
   - Linux: `sudo apt-get install fonts-inter` or download from Google Fonts

3. **Use fallback font** in template:
   ```typst
   #set text(font: ("Inter", "Helvetica", "Arial"))
   ```

## Compilation Errors

### Special characters causing errors

**Problem:** YAML contains characters that need escaping in Typst (`#`, `@`, `\`, `<`, `>`)

**Solution:**

The `yaml_to_typst.py` script auto-escapes special Typst characters. If errors persist:

1. Check for unusual Unicode characters in YAML
2. Replace curly quotes with straight quotes
3. Remove emoji or special symbols

**Manual fixes in YAML:**
```yaml
# Bad - contains # which is Typst code marker
comment: "Issue #123"
# Good (script will handle this, but if manual editing needed)
comment: "Issue \\#123"
```

### "expected ... found ..." syntax error

**Problem:** Typst syntax error in template

**Solution:**

1. **Check Typst output** for line number
2. **Common issues:**
   ```typst
   // Wrong: Missing space after #
   #let x=5  // Error
   #let x = 5  // Correct

   // Wrong: Mixing content and code modes
   #if true { text }  // Error
   #if true [ text ]  // Correct - use [] for content

   // Wrong: Unclosed brackets
   #text(fill: red[content]  // Error - missing )
   #text(fill: red)[content]  // Correct
   ```

3. **Try different template** (e.g., classic instead of modern)

### Content cut off or overlapping

**Problem:** Too much content for page

**Solution:**

**Priority order:**
1. **Reduce content** (remove older roles, reduce bullets)
2. **Decrease font size:**
   ```typst
   #set text(size: 9pt)  // Reduce from 10pt
   ```
3. **Adjust margins:**
   ```typst
   #set page(margin: (top: 0.4in, bottom: 0.3in, left: 0.5in, right: 0.5in))
   ```
4. **Switch to different template** (academic template handles multi-page better)

### Page overflow error

**Problem:** Content exceeds page boundaries

**Solution:**

1. **Reduce content length** (preferred)
2. **Enable page breaks** in template:
   ```typst
   #set page(height: auto)  // Auto-extend pages
   ```
3. **Use multi-page template** (academic)
4. **Remove sections** or reduce bullets per role

## PDF Quality Issues

### Fonts look wrong or missing

**Problem:** Font not available or not rendering

**Solution:**

1. **Check font availability:**
   ```bash
   typst fonts | grep -i "inter"
   ```

2. **Install required fonts** (see Installation Issues above)

3. **Use system fonts** that are always available:
   ```typst
   #set text(font: "Helvetica")  // macOS
   #set text(font: "Liberation Sans")  // Linux
   ```

### Colors don't print well

**Problem:** Colors look good on screen but poor when printed

**Solution:**

1. **Preview in grayscale** before printing:
   - Most PDF viewers have grayscale preview option

2. **Use Classic template** for maximum print compatibility (no colors)

3. **Adjust colors for print** in template:
   ```typst
   // Use darker colors for better print quality
   #let primary = rgb("#003366")  // Darker blue
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
   uv run scripts/compile_typst.py resume.typ
   ```

4. **Check for complex layouts** - sidebars and multi-column can confuse ATS

### Hyperlinks not working

**Problem:** Email/phone/URLs not clickable

**Solution:**

1. **Use link function** in template:
   ```typst
   #link("mailto:name@example.com")[name\@example.com]
   ```

2. **Verify links render** - some PDF viewers don't show clickable state

3. **Test in multiple viewers** (Preview, Adobe, browser)

## Content Issues

### Section not appearing in PDF

**Problem:** YAML section exists but doesn't render

**Solution:**

1. **Check YAML structure** matches schema:
   ```yaml
   # Correct
   experience:
     - company: "Company Name"
       positions:
         - title: "Job Title"
           dates: "Jan 2020 - Present"

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
   dates: "Jan 2020 - Dec 2022"

   # Also good
   dates: "January 2020 - Present"
   ```

2. **Check template date handling** - some templates expect specific formats

### Skills not grouping correctly

**Problem:** Skills section not organized by categories

**Solution:**

1. **Use categorized format in YAML:**
   ```yaml
   skills:
     Programming:
       - Python
       - Java
       - Go
     Cloud:
       - AWS
       - GCP
       - Azure
   ```

2. **Check template** supports categorized skills (modern and creative do)

3. **Fall back to simple list** if categories not supported:
   ```yaml
   skills:
     - Python
     - AWS
     - Docker
     - Kubernetes
   ```

## Debugging Tips

### Enable verbose Typst output

```bash
# Run typst directly for detailed error messages
typst compile resume.typ --diagnostic-format=short
```

### Check compilation output

```bash
# Typst shows errors inline during compilation
typst compile resume.typ 2>&1 | head -50
```

### Clean rebuild

```bash
# Remove generated files
rm -f resume.typ resume.pdf

# Regenerate Typst from YAML
uv run scripts/yaml_to_typst.py resume.yaml modern --output resume.typ

# Recompile
uv run scripts/compile_typst.py resume.typ
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
    positions:
      - title: "Test Title"
        dates: "Jan 2020 - Present"
        achievements:
          - "Test achievement"

education:
  - degree: "BS Computer Science"
    institution: "Test University"
    graduation_year: "2020"

skills:
  - Python
  - SQL
```

If minimal YAML works, gradually add sections back to identify problematic content.

## Getting Help

If issues persist:

1. **Check Typst output** for specific error messages
2. **Try different template** to isolate template vs. content issues
3. **Validate YAML syntax** using online YAML validator
4. **Test with minimal example** to reproduce issue
5. **Review template source** in `assets/templates/typst/` for customization needs
6. **Typst documentation**: https://typst.app/docs/
