# Error Handling Reference

Common errors across the resume skills suite with causes and solutions.

---

## YAML Validation Errors

### Schema Validation

**Error:** `ValidationError: contact.email - value is not a valid email address`

**Cause:** Pydantic validation failed on a field.

**Solution:** Check the YAML field against the schema in `resume-extractor/scripts/schema.py`. Common issues:
- Email missing `@` or domain
- URL missing protocol
- Empty required fields

**Example fix:**
```yaml
# Wrong
email: "john.doe"

# Correct
email: "john.doe@example.com"
```

---

**Error:** `Required field missing: 'experience'`

**Cause:** A required section is missing from the YAML.

**Solution:** Add the missing section. Required sections:
- `contact` (with `name`, `email`)
- `experience` (list with `company`, `positions`)
- `skills` (dictionary of category → skills)
- `education` (list with `institution`, `degree`)

---

**Error:** `YAML syntax error at line X`

**Cause:** Invalid YAML syntax.

**Common causes:**
- Unquoted strings containing colons (`:`)
- Inconsistent indentation
- Missing quotes around special characters

**Solution:**
```yaml
# Wrong - colon breaks parsing
title: Senior Engineer: Platform Team

# Correct - quote strings with colons
title: "Senior Engineer: Platform Team"
```

---

## Typst Compilation Errors

### Character Escaping

**Error:** `unexpected token` or `expected expression`

**Cause:** Special Typst characters not escaped in YAML content.

**Characters requiring escape:** `#`, `@`, `\`, `<`, `>`, `_`, `*`, `` ` ``, `~`, `^`

**Solution:** The `typst_escape` filter handles this automatically. Ensure:
1. All user content uses `| typst_escape` filter
2. URLs use `| url_escape` filter

**Example in template:**
```typst
{{ contact.name | typst_escape }}
#link("mailto:{{ contact.email | url_escape }}")[{{ contact.email | typst_escape }}]
```

---

**Error:** `unknown font family`

**Cause:** Font specified in template not installed on system.

**Solution:**
1. Check installed fonts: `fc-list | grep -i "fontname"`
2. Use system fonts with fallback chain:
```typst
#set text(font: ("Inter", "Helvetica", "Arial"))
```

---

**Error:** `file not found` or `cannot read file`

**Cause:** Typst can't find an included file or font.

**Solution:**
1. Check file paths are relative to the `.typ` file
2. Ensure fonts are installed system-wide
3. Use absolute paths if necessary

---

### Content Overflow

**Error:** No error, but content cut off at page edge

**Cause:** Too much content for the page with current margins/spacing.

**Solutions:**
1. Reduce content (fewer bullets per role)
2. Decrease margins:
   ```typst
   #set page(margin: (x: 0.5in, y: 0.4in))
   ```
3. Reduce font sizes:
   ```typst
   #set text(size: 9pt)
   ```
4. Tighten list spacing:
   ```typst
   #set list(spacing: 0.3em)
   ```

---

## State Management Errors

### Project Errors

**Error:** `No project specified and no active project set`

**Cause:** No `-p/--project` flag provided and no active project.

**Solution:**
```bash
# Initialize a project first
uv run resume-state/scripts/init_project.py my-resume

# Or specify project explicitly
uv run resume-state/scripts/list_versions.py -p my-resume
```

---

**Error:** `Project not found: X`

**Cause:** Project doesn't exist or wrong name.

**Solution:**
```bash
# List existing projects
ls .resume_versions/projects/

# Check for typos in project name
```

---

**Error:** `Active version not found: vN`

**Cause:** `project.json` references a version that doesn't exist on disk.

**Solution:**
1. Check versions directory:
   ```bash
   ls .resume_versions/projects/<name>/versions/
   ```
2. Edit `project.json` to fix `active_version`
3. Or create missing version directory with `resume.yaml`

---

### Version ID Errors

**Error:** `Invalid version ID format: 'X'. Expected format: v1, v2, v3, ...`

**Cause:** Version ID doesn't match pattern `^v(\d+)$`.

**Solution:** Use lowercase `v` followed by number:
- Valid: `v1`, `v2`, `v10`
- Invalid: `1`, `V1`, `v1.0`, `version1`

---

## Extraction Errors

### PDF Extraction

**Error:** `Cannot extract text from PDF`

**Cause:** PDF is image-based (scanned) or encrypted.

**Solution:**
1. Check if PDF is scanned: Open and try to select text
2. If scanned, use OCR software first (Tesseract, Adobe)
3. If encrypted, remove password protection first

---

**Error:** `Multi-column layout detected - text may be interleaved`

**Cause:** PDF has complex multi-column layout.

**Solution:**
1. Review extracted text carefully
2. Manually reorder content if needed
3. Consider extracting from DOCX if available

---

### DOCX Extraction

**Error:** `Not a valid DOCX file`

**Cause:** File is not a valid DOCX or is corrupted.

**Solution:**
1. Check file extension is `.docx` (not `.doc`)
2. Try opening in Word to verify
3. Re-save document as DOCX

---

## Network Errors

### Job Posting Fetch

**Error:** `HTTP error: 429 Too Many Requests`

**Cause:** Rate limited by the website.

**Solution:** Script will retry with exponential backoff. If persistent:
1. Wait before retrying
2. Use `--cache-dir` to avoid repeat fetches

---

**Error:** `Warning: LinkedIn requires JavaScript`

**Cause:** JS-heavy site can't be scraped with simple HTTP.

**Solution:** For sites like LinkedIn, Workday, Lever:
1. Open job posting in browser
2. Copy text manually
3. Save to file
4. Use that file instead of URL

---

**Error:** `Request timed out after multiple retries`

**Cause:** Network issues or site is down.

**Solution:**
1. Check internet connection
2. Verify URL is accessible in browser
3. Try again later
4. Use cached copy if available

---

## Environment Errors

### Dependencies

**Error:** `ModuleNotFoundError: No module named 'pdfplumber'`

**Cause:** Python dependencies not installed.

**Solution:**
```bash
uv sync
```

---

### Typst

**Error:** `typst: command not found`

**Cause:** Typst not installed.

**Solution:**
```bash
brew install typst  # macOS
# or see typst.app for other platforms
```

---

**Error:** `Permission denied` when running scripts

**Cause:** Script not executable.

**Solution:**
```bash
chmod +x script.py
# Or run via uv:
uv run script.py
```

---

## Debug Tips

### Enable Verbose Output

Most scripts support `--verbose` or write to stderr:
```bash
uv run script.py 2>&1 | tee debug.log
```

### Check Intermediate Files

When PDF generation fails:
1. Keep the `.typ` file: `uv run yaml_to_typst.py ... -o debug.typ`
2. Try compiling manually: `typst compile debug.typ`
3. Check for Typst errors in specific lines

### Validate YAML First

Before formatting, always validate:
```bash
uv run resume-optimizer/scripts/validate_yaml.py resume.yaml
```

### Check State Consistency

```bash
# View project state
cat .resume_versions/projects/<name>/project.json | jq .

# Verify version directories exist
ls -la .resume_versions/projects/<name>/versions/

# Get active version path
uv run resume-state/scripts/get_active.py
```

---

## Error Patterns by Skill

| Skill | Common Errors | First Check |
|-------|---------------|-------------|
| resume-extractor | No text extracted | PDF/DOCX format |
| resume-optimizer | Validation failures | YAML syntax |
| resume-formatter | Compile errors | Character escaping |
| resume-state | Project not found | Store location |
| resume-reviewer | PDF not readable | File exists |
| resume-template-maker | Template syntax | Jinja2/Typst syntax |
