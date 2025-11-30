# Industry-Specific Resume Themes

Targeted design guidance for specific industries and roles. Each theme defines the four design vectors calibrated for industry expectations.

---

## Technology & Software Engineering

### Design DNA
- **Vibe**: Clean, efficient, modern but not flashy
- **Signal**: "I care about craft and clarity"

### Vector Configuration

**Typography**:
- Sans-serif primary (TeX Gyre Heros, Fira Sans, Source Sans Pro)
- Monospace for technical skills if desired
- Medium weight contrast
- Clean, readable at all sizes

**Layout**:
- Single column or skills sidebar
- Technical skills prominent (top or sidebar)
- Projects section common
- GitHub/portfolio links visible

**Whitespace**:
- Balanced to efficient (0.6-0.75in margins)
- Dense bullet points acceptable
- Clear section separation
- Scannable structure

**Color**:
- Blues, teals, grays
- Single accent color
- Avoid flashy or corporate-stuffy
- Dark mode friendly colors (good contrast)

### Example Configuration
```latex
% Tech template setup
\usepackage{fontspec}
\setmainfont{Source Sans Pro}
\definecolor{accent}{RGB}{0, 128, 128}  % Teal
\usepackage[margin=0.65in]{geometry}
```

---

## Finance, Banking & Consulting

### Design DNA
- **Vibe**: Conservative, polished, trustworthy
- **Signal**: "I understand institutional expectations"

### Vector Configuration

**Typography**:
- Serif preferred (TeX Gyre Termes, EB Garamond)
- Or conservative sans (Helvetica-like)
- Moderate weight contrast
- Traditional size hierarchy

**Layout**:
- Single column only
- Standard section order
- No creative layouts
- Education can be prominent (target school matters)

**Whitespace**:
- Generous margins (0.75-1.0in)
- Clean breathing room
- Elegant, not cramped
- Quality over quantity impression

**Color**:
- Navy blue, burgundy, or black only
- Minimal color usage
- Monochrome acceptable and often preferred
- Must print perfectly in B&W

### Example Configuration
```latex
% Finance template setup
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}
\definecolor{accent}{RGB}{0, 51, 102}  % Navy
\usepackage[margin=0.85in]{geometry}
```

---

## Creative, Design & Marketing

### Design DNA
- **Vibe**: Distinctive, visually compelling, personality-forward
- **Signal**: "I have an eye for design and brand"

### Vector Configuration

**Typography**:
- Display fonts for name acceptable
- Creative pairings (serif + sans)
- Strong weight contrast
- Typography as expression

**Layout**:
- Sidebar or asymmetric layouts welcome
- Visual hierarchy emphasized
- Creative section treatments
- Portfolio/work samples prominent

**Whitespace**:
- Intentional, asymmetric spacing
- White space as design element
- Can break conventional patterns
- Breathing room shows confidence

**Color**:
- Personal brand colors encouraged
- Multi-color palettes acceptable
- Bold choices differentiate
- Should match portfolio aesthetic

### Example Configuration
```latex
% Creative template setup
\usepackage{fontspec}
\setmainfont{Source Sans Pro}
\newfontfamily\headingfont{Playfair Display}
\definecolor{primary}{RGB}{183, 65, 14}   % Rust
\definecolor{secondary}{RGB}{47, 79, 79}  % Slate
\usepackage[margin=0.7in]{geometry}
```

---

## Academia & Research

### Design DNA
- **Vibe**: Scholarly, thorough, credible
- **Signal**: "I'm a serious researcher with strong credentials"

### Vector Configuration

**Typography**:
- Serif strongly preferred (Palatino-like, Garamond)
- Traditional academic appearance
- Moderate contrast
- Readable for detailed content

**Layout**:
- Education first
- Publications section prominent
- Research experience detailed
- Can be longer (2+ pages acceptable)

**Whitespace**:
- Moderate margins
- Dense content acceptable
- Clear section structure
- Functional over aesthetic

**Color**:
- Minimal (black or dark blue)
- Monochrome common
- Color viewed as unnecessary
- Focus on content, not presentation

### Example Configuration
```latex
% Academic template setup
\usepackage{fontspec}
\setmainfont{TeX Gyre Pagella}  % Palatino-like
\definecolor{accent}{RGB}{0, 0, 0}  % Black
\usepackage[margin=0.75in]{geometry}
```

---

## Healthcare & Medical

### Design DNA
- **Vibe**: Professional, trustworthy, competent
- **Signal**: "I'm reliable and detail-oriented"

### Vector Configuration

**Typography**:
- Clean, highly readable fonts
- Sans or serif both acceptable
- Moderate contrast
- Accessibility matters

**Layout**:
- Standard single column
- Credentials/certifications prominent
- Licenses section important
- Clinical experience highlighted

**Whitespace**:
- Balanced, organized
- Clear sections
- Not too dense
- Professional appearance

**Color**:
- Blues, greens, white associations
- Avoid red (blood), black (death)
- Calming, professional palette
- Conservative usage

### Example Configuration
```latex
% Healthcare template setup
\usepackage{fontspec}
\setmainfont{Source Sans Pro}
\definecolor{accent}{RGB}{0, 105, 148}  % Medical blue
\usepackage[margin=0.7in]{geometry}
```

---

## Legal

### Design DNA
- **Vibe**: Ultra-conservative, precise, traditional
- **Signal**: "I respect tradition and pay attention to detail"

### Vector Configuration

**Typography**:
- Serif required (Times-like, Garamond)
- Conservative sizes
- Traditional hierarchy
- No creative fonts

**Layout**:
- Single column only
- Standard section order
- Bar admission prominent
- Publications/articles if relevant

**Whitespace**:
- Generous, unhurried
- Classic proportions
- Quality paper implication
- Refined spacing

**Color**:
- Black or navy only
- Minimal color usage
- Monochrome preferred
- Absolutely no bright colors

### Example Configuration
```latex
% Legal template setup
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}
\definecolor{accent}{RGB}{0, 0, 0}  % Black
\usepackage[margin=0.9in]{geometry}
```

---

## Startups & Entrepreneurship

### Design DNA
- **Vibe**: Modern, energetic, results-focused
- **Signal**: "I'm adaptable, impactful, and get things done"

### Vector Configuration

**Typography**:
- Modern sans-serif
- Can be distinctive/unique
- Strong hierarchy
- Personality welcome

**Layout**:
- Flexible, modern layouts
- Impact metrics prominent
- Growth/results emphasized
- Projects and side ventures included

**Whitespace**:
- Efficient but not cramped
- Modern spacing
- Quick scanning priority
- Action-oriented feel

**Color**:
- Modern palette
- Bold accents acceptable
- Should feel current/fresh
- Avoid corporate-stuffy

### Example Configuration
```latex
% Startup template setup
\usepackage{fontspec}
\setmainfont{Montserrat}
\definecolor{accent}{RGB}{46, 134, 171}  % Modern teal
\usepackage[margin=0.6in]{geometry}
```

---

## Government & Public Sector

### Design DNA
- **Vibe**: Straightforward, organized, compliant
- **Signal**: "I understand bureaucratic requirements"

### Vector Configuration

**Typography**:
- Standard, readable fonts
- Nothing unusual
- Clear hierarchy
- Functional focus

**Layout**:
- Standard format
- Often specific requirements (federal resumes)
- May need to be longer/detailed
- Clearances and certifications prominent

**Whitespace**:
- Balanced
- Clear organization
- Scannable
- Often dense with required info

**Color**:
- Conservative (navy, black)
- Often monochrome required
- No creative colors
- Plain is preferred

### Example Configuration
```latex
% Government template setup
\usepackage{fontspec}
\setmainfont{TeX Gyre Heros}
\definecolor{accent}{RGB}{0, 51, 102}  % Navy
\usepackage[margin=0.75in]{geometry}
```

---

## Non-Profit & Social Impact

### Design DNA
- **Vibe**: Purpose-driven, approachable, competent
- **Signal**: "I care about mission and can deliver results"

### Vector Configuration

**Typography**:
- Warm, approachable fonts
- Sans-serif often preferred
- Accessible
- Not corporate

**Layout**:
- Standard with flexibility
- Impact/outcomes emphasized
- Volunteer work valued
- Mission alignment shown

**Whitespace**:
- Balanced, friendly
- Not too formal
- Inviting appearance
- Organized but warm

**Color**:
- Earthy, warm tones
- Organization brand colors if applying to specific org
- Greens, oranges, warm blues
- Avoid corporate cold

### Example Configuration
```latex
% Non-profit template setup
\usepackage{fontspec}
\setmainfont{Source Sans Pro}
\definecolor{accent}{RGB}{34, 139, 34}  % Forest green
\usepackage[margin=0.7in]{geometry}
```

---

## Executive & C-Suite

### Design DNA
- **Vibe**: Polished, strategic, high-impact
- **Signal**: "I operate at the highest level"

### Vector Configuration

**Typography**:
- Premium, refined fonts
- Elegant serif or clean sans
- Subtle contrast
- Sophisticated appearance

**Layout**:
- Single column, spacious
- Executive summary prominent
- Board positions included
- Streamlined, not dense

**Whitespace**:
- Very generous
- Confident spacing
- Quality over quantity
- Less is more

**Color**:
- Minimal, sophisticated
- Black, navy, or single refined accent
- Never flashy
- Understated elegance

### Example Configuration
```latex
% Executive template setup
\usepackage{fontspec}
\setmainfont{EB Garamond}
\definecolor{accent}{RGB}{47, 79, 79}  % Slate
\usepackage[margin=1.0in]{geometry}
```

---

## Career Transition / General

### Design DNA
- **Vibe**: Competent, adaptable, transferable skills focus
- **Signal**: "My skills translate to your needs"

### Vector Configuration

**Typography**:
- Clean, professional, neutral
- Works across industries
- Sans-serif safer for transitions
- Moderate everything

**Layout**:
- Skills-forward
- Transferable experience highlighted
- Functional or hybrid format
- Summary important

**Whitespace**:
- Balanced, professional
- Standard spacing
- Neither too creative nor too conservative
- Safe middle ground

**Color**:
- Professional but not industry-specific
- Blue is universally safe
- Single accent
- Conservative usage

### Example Configuration
```latex
% Transition template setup
\usepackage{fontspec}
\setmainfont{Source Sans Pro}
\definecolor{accent}{RGB}{0, 82, 147}  % Professional blue
\usepackage[margin=0.7in]{geometry}
```

---

## Quick Reference Table

| Industry | Font Style | Layout | Margins | Colors |
|----------|-----------|--------|---------|--------|
| Tech | Sans | Single/Sidebar | 0.6-0.7in | Blues, teals |
| Finance | Serif | Single | 0.8-1.0in | Navy, black |
| Creative | Mixed | Flexible | 0.7in | Brand colors |
| Academic | Serif | Single | 0.75in | Minimal |
| Healthcare | Sans/Serif | Single | 0.7in | Blues, greens |
| Legal | Serif | Single | 0.9in | Black only |
| Startup | Sans | Flexible | 0.6in | Modern palette |
| Government | Sans/Serif | Single | 0.75in | Navy, black |
| Non-Profit | Sans | Single | 0.7in | Warm colors |
| Executive | Serif | Single | 1.0in | Minimal |
