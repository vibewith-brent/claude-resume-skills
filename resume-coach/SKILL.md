---
name: resume-coach
description: Help users discover, create, and expand resume content through guided questions. Use when adding new experience, filling content gaps, or helping users articulate achievements they've undersold.
---

# Resume Coach Skill

Help users discover hidden achievements, create new content, and expand existing bullets through interview-style questioning. This skill fills the gap between extraction (what's already written) and optimization (improving existing content).

## When to Use

**Content Discovery:**
- User says "I don't know what to put" or "I can't think of achievements"
- Resume feels thin or undersells the user's experience
- User has skills/experience not reflected in current resume
- Targeting a role that requires experience they have but haven't documented

**Content Updates:**
- User wants to add recent work experience
- User changed roles or companies
- User completed new projects, certifications, or education

**Content Expansion:**
- Bullets are vague ("worked on projects")
- Missing metrics and impact
- Missing context (the "so what?")

**Gap Analysis:**
- Comparing resume to job description reveals missing content
- User has the experience but hasn't articulated it

## Core Philosophy

**Problem**: People undersell themselves. They forget achievements, discount skills, and write weak bullets like "responsible for X" instead of "delivered Y resulting in Z."

**Solution**: Ask targeted questions that draw out specific details, then help structure responses into strong resume content.

## Coaching Modes

### 1. Achievement Discovery

For each role, ask probing questions:

```
IMPACT QUESTIONS:
- "What's the biggest problem you solved in this role?"
- "What would have happened if you weren't there?"
- "What are you most proud of from this job?"
- "Did anything you do save time, money, or prevent problems?"

SCOPE QUESTIONS:
- "How many people/users/customers did this affect?"
- "What was the budget/team size/timeline?"
- "Was this a solo effort or did you lead others?"

METRICS QUESTIONS:
- "Do you have any numbers? Revenue, users, time saved, error reduction?"
- "Even rough estimates help - 'about 50%' is better than nothing"
- "What was the before/after comparison?"

SKILLS QUESTIONS:
- "What tools or technologies did you use?"
- "Did you learn anything new for this project?"
- "What soft skills did this require? (leadership, communication, negotiation)"
```

### 2. Experience Updates

Guided flow for adding new experience:

```
BASIC INFO:
- Company name and your title?
- Start date and end date (or "present")?
- Company location (city or remote)?
- Brief description of the company (optional)?

ROLE OVERVIEW:
- What was your main responsibility?
- Who did you report to? Who reported to you?
- What team/department were you part of?

KEY ACHIEVEMENTS (repeat 4-6 times):
- Describe a project or achievement
- What was the problem or goal?
- What did you specifically do?
- What was the result or impact?
- Any metrics or numbers?

SKILLS USED:
- Technical skills?
- Tools and platforms?
- Soft skills demonstrated?
```

### 3. STAR Expansion

Take weak bullets and expand using STAR framework:

```
ORIGINAL: "Worked on customer support improvements"

SITUATION: "What was the context? What problem existed?"
→ "Customer support tickets were taking 48 hours to resolve"

TASK: "What were you specifically asked to do?"
→ "Reduce resolution time and improve customer satisfaction"

ACTION: "What did you actually do? Be specific."
→ "Built automated triage system using Python, created knowledge base, trained team"

RESULT: "What happened? Numbers if possible."
→ "Reduced resolution time to 4 hours (92% improvement), CSAT increased from 3.2 to 4.6"

EXPANDED: "Built automated ticket triage system using Python and NLP, reducing average resolution time from 48 hours to 4 hours (92% improvement) and increasing customer satisfaction scores from 3.2 to 4.6"
```

### 4. Gap Analysis

Compare resume to job requirements:

```
JOB REQUIRES: "Experience with distributed systems"
RESUME SHOWS: Nothing explicit

DISCOVERY QUESTIONS:
- "Have you worked on systems that run across multiple servers?"
- "Any experience with microservices, message queues, or load balancing?"
- "Have you dealt with data that needs to be consistent across locations?"

→ User reveals they built a multi-region caching layer
→ Create new bullet capturing this experience
```

### 5. Hidden Skills Discovery

Find skills in unexpected places:

```
SIDE PROJECTS:
- "Any personal projects, open source contributions, or hobby coding?"
- "Ever built something for friends/family?"
- "Any blogs, tutorials, or teaching you've done?"

VOLUNTEER WORK:
- "Any volunteer experience that used professional skills?"
- "Board positions, mentoring, community organizing?"

EDUCATION/TRAINING:
- "Recent courses, certifications, or self-study?"
- "Hackathons, conferences, workshops?"

TRANSFERABLE SKILLS:
- "Previous careers that taught relevant skills?"
- "Management experience from non-work contexts?"
```

## Workflow

### Step 1: Assess Current State

```
READ current resume YAML
IDENTIFY:
- Roles with few/weak bullets
- Missing metrics across all roles
- Skills gap vs. target role (if provided)
- Recency (when was this last updated?)
```

### Step 2: Choose Coaching Mode

| Situation | Mode |
|-----------|------|
| Thin resume overall | Achievement Discovery for each role |
| Recent job change | Experience Updates |
| Weak bullets | STAR Expansion |
| Targeting specific role | Gap Analysis |
| Career changer | Hidden Skills Discovery |

### Step 3: Conduct Interview

- Ask questions one topic at a time
- Wait for user response before next question
- Capture details in notes
- Probe for specifics and metrics

### Step 4: Generate Content

```yaml
# New or expanded bullet
experience:
  - company: "Example Corp"
    positions:
      - title: "Senior Engineer"
        achievements:
          - "Built automated ticket triage system using Python and NLP, reducing average resolution time from 48 hours to 4 hours (92% improvement)"
```

### Step 5: Validate with User

- Read back the generated content
- Confirm accuracy
- Adjust language to match user's voice
- Integrate into resume YAML

## Question Bank

See `references/coaching_questions.md` for complete question bank organized by:
- Role type (IC, Manager, Executive)
- Industry (Tech, Finance, Healthcare, etc.)
- Skill category (Technical, Leadership, Communication)
- Achievement type (Cost savings, Growth, Quality, Speed)

## Integration with Other Skills

```
resume-extractor → resume-coach → resume-optimizer
     ↓                  ↓               ↓
  Raw content    Expanded content   Polished content
```

**Before coaching**: "Managed team projects"

**After coaching**: "Led cross-functional team of 8 engineers and designers to deliver mobile app redesign, reducing user drop-off by 34% and increasing daily active users from 50K to 85K"

**After optimization**: "Led 8-person cross-functional team delivering mobile app redesign that reduced user drop-off 34% and grew DAU from 50K to 85K (+70%)"

## Output

After coaching session, provide:

1. **New/Updated YAML** - Ready to merge into resume
2. **Session Notes** - Key details captured for reference
3. **Remaining Gaps** - What still needs attention
4. **Suggested Next Steps** - Optimize, format, or continue coaching

## Tips for Effective Coaching

**Be patient**: Users often need multiple prompts to remember details

**Probe for numbers**: "About how many?" is better than accepting "some" or "several"

**Validate importance**: "What would have happened without this?" reveals true impact

**Use their words**: Match the user's vocabulary and communication style

**Celebrate progress**: Acknowledge when they uncover good content

## References

- `references/coaching_questions.md` — Complete question bank by category
- `references/star_templates.md` — STAR expansion templates by achievement type
- `references/industry_prompts.md` — Industry-specific probing questions
- `references/metrics_guide.md` — How to estimate missing metrics
