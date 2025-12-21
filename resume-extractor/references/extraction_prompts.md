# Resume Extraction Prompts

Structured prompts for extracting resume content from raw text to YAML format.

## Overview

After extracting raw text from a PDF/DOCX, use these prompts to guide parsing into the YAML schema. Each section has specific extraction rules and validation criteria.

---

## Section 1: Contact Information

### Extraction Prompt

```
From the extracted text, identify and extract contact information:

1. **Full Name**: Look for the largest/boldest text at the top, or text on its own line that appears to be a name (First Last or First Middle Last format).

2. **Professional Title**: Often appears directly below the name. Look for job titles, "Senior/Lead/Staff" prefixes, or role descriptions.

3. **Email**: Search for text matching email pattern (contains @ and domain).

4. **Phone**: Look for patterns like (XXX) XXX-XXXX, XXX-XXX-XXXX, or +1 XXX XXX XXXX.

5. **Location**: City, State format. Often near phone/email. May be "City, ST" or "City, State".

6. **LinkedIn**: Look for "linkedin.com/in/" or just the username portion.

7. **GitHub**: Look for "github.com/" or just the username.

8. **Website**: Any other URL that appears to be a personal website.

Output in this exact YAML format:
```yaml
contact:
  name: "Full Name"
  title: "Professional Title"  # optional
  email: "email@example.com"
  phone: "(XXX) XXX-XXXX"
  location: "City, State"  # optional
  linkedin: "linkedin.com/in/username"  # optional
  github: "github.com/username"  # optional
  website: "https://example.com"  # optional
```

### Validation Rules
- Name is required
- Email should contain @ and valid domain
- Phone should be normalized to consistent format
- LinkedIn/GitHub should be just the profile path, not full URL

---

## Section 2: Professional Summary

### Extraction Prompt

```
Extract the professional summary section. Look for:

1. Section headers like: "Summary", "Profile", "Professional Summary", "About", "Overview"

2. A paragraph (2-5 sentences) that describes:
   - Years of experience and expertise areas
   - Key skills and competencies
   - Industry or domain focus
   - Value proposition or career highlights

3. This is typically 100-400 characters.

Output in YAML format:
```yaml
summary: |
  [Multi-line summary text here.
  Second sentence continues.
  Third sentence if present.]
```

### Validation Rules
- Should be 2-5 sentences
- Should mention experience level or years
- Should highlight 2-4 key skills
- Use YAML literal block style (|) for multi-line text

---

## Section 3: Work Experience

### Extraction Prompt

```
Extract work experience entries. For each position, identify:

1. **Company Name**: Organization name, not department or team.

2. **Location**: City, State where role was performed (if listed).

3. **Position(s)**: One company may have multiple positions (promotions).
   - Job Title
   - Date Range: Look for "Month Year - Month Year" or "Year - Present"
   - Achievements: Bullet points describing accomplishments

4. **Achievement Bullets**: Look for:
   - Lines starting with bullets (•, -, *, ◦)
   - Action verbs at the start
   - Metrics and numbers
   - Technologies mentioned

For companies with multiple roles, nest them under positions array.

Output format:
```yaml
experience:
  - company: "Company Name"
    location: "City, State"  # optional
    positions:
      - title: "Senior Role"
        dates: "Jan 2022 - Present"
        achievements:
          - "Achievement starting with action verb and including metrics"
          - "Another achievement with quantifiable results"
      - title: "Previous Role at Same Company"
        dates: "Jun 2020 - Dec 2021"
        achievements:
          - "Achievement from earlier role"
```

### Validation Rules
- Each company requires: company name, at least one position
- Each position requires: title, dates, at least one achievement
- Dates should be consistent format (e.g., "Jan 2020 - Dec 2022")
- Achievements should start with action verbs

---

## Section 4: Education

### Extraction Prompt

```
Extract education entries. For each degree, identify:

1. **Institution Name**: University, college, or school name.

2. **Degree**: Full degree name (e.g., "Bachelor of Science, Computer Science").

3. **Graduation Year**: Year of completion or expected graduation.

4. **Optional Fields**:
   - Location: City, State
   - GPA: Format as "X.X/4.0" if listed
   - Honors: Summa Cum Laude, Dean's List, etc.
   - Minor: Secondary field of study

Order by most recent first.

Output format:
```yaml
education:
  - institution: "University Name"
    degree: "Degree Type, Major"
    graduation_year: "2020"
    location: "City, State"  # optional
    gpa: "3.8/4.0"  # optional
    honors: "Magna Cum Laude"  # optional
    minor: "Minor Field"  # optional
```

### Validation Rules
- Each entry requires: institution, degree
- Graduation year should be a 4-digit year
- GPA should be normalized to X.X/4.0 format if present

---

## Section 5: Skills

### Extraction Prompt

```
Extract technical and professional skills. Organize by category.

Common categories:
- Programming Languages
- Frameworks & Libraries
- Cloud & Infrastructure
- Databases
- Tools & Platforms
- Data Science / ML
- Soft Skills / Leadership

Look for:
1. Skills sections with category headers
2. Comma-separated lists
3. Bullet lists under category headers
4. Skills mentioned inline in experience (less reliable)

Group related skills together logically.

Output format:
```yaml
skills:
  "Programming Languages":
    - Python
    - JavaScript
    - Go
  "Frameworks":
    - React
    - FastAPI
    - Django
  "Cloud & Infrastructure":
    - AWS
    - Docker
    - Kubernetes
```

### Validation Rules
- At least 3-5 skill categories
- Skills should be specific (not "Programming" but "Python, Java")
- Remove outdated technologies unless relevant
- Order categories by importance to target role

---

## Section 6: Optional Sections

### Certifications Prompt

```
Extract professional certifications:

```yaml
certifications:
  - name: "Certification Name"
    issuer: "Issuing Organization"
    date: "Month Year"
    credential_id: "ABC123"  # optional
    url: "https://verify.example.com"  # optional
```

### Projects Prompt

```
Extract notable projects:

```yaml
projects:
  - name: "Project Name"
    dates: "Jan 2023 - Mar 2023"
    description: "Brief description of the project"
    technologies:
      - Tech1
      - Tech2
    achievements:
      - "Key outcome or metric"
    url: "https://github.com/..."  # optional
```

### Publications Prompt

```
Extract publications (papers, articles):

```yaml
publications:
  - title: "Publication Title"
    authors: "First Author, Second Author, Your Name"
    venue: "Conference or Journal Name"
    date: "Year"
    url: "https://doi.org/..."  # optional
```

### Awards Prompt

```
Extract awards and honors:

```yaml
awards:
  - name: "Award Name"
    issuer: "Organization"
    date: "Year"
    description: "Brief description"  # optional
```

### Languages Prompt

```
Extract language proficiencies:

```yaml
languages:
  - language: "English"
    proficiency: "Native"
  - language: "Spanish"
    proficiency: "Professional"
```

Proficiency levels: Native, Fluent, Professional, Conversational, Basic

### Volunteer Prompt

```
Extract volunteer experience:

```yaml
volunteer:
  - organization: "Organization Name"
    role: "Volunteer Role"
    dates: "Jan 2020 - Present"
    description: "Brief description"
    achievements:
      - "Contribution or outcome"
```

---

## Extraction Checklist

Before finalizing YAML:

- [ ] Contact section has name and at least email
- [ ] Summary is 2-5 sentences
- [ ] All experience entries have company, positions with titles/dates/achievements
- [ ] Achievements start with action verbs
- [ ] Education has institution and degree
- [ ] Skills are organized by category
- [ ] Dates are consistent format throughout
- [ ] YAML syntax is valid (proper indentation, quoting)
- [ ] Special characters are properly escaped (colons, quotes)
- [ ] No empty sections - omit if not present in source

---

## Common Extraction Issues

### Multi-Column Layouts
PDF extraction may interleave columns. Look for:
- Dates on wrong lines
- Skills mixed with experience
- Contact info scattered

Solution: Reorder based on context clues (dates near job titles, skills grouped logically).

### Date Parsing
Various formats seen:
- "January 2020 - Present"
- "Jan '20 - Dec '22"
- "2020 - 2022"
- "2020-01 to 2022-12"

Normalize to: "Mon YYYY - Mon YYYY" or "Mon YYYY - Present"

### Merged Company/Title
Sometimes text runs together:
"Software Engineer at Google" should become:
- title: "Software Engineer"
- company: "Google"

### Missing Section Headers
Some resumes lack explicit headers. Use context:
- Bullet lists after job titles = achievements
- Comma-separated tech terms = skills
- University names with degrees = education
