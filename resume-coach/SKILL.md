---
name: resume-coach
description: Adaptive coaching to discover, expand, and articulate resume content through conversation. Persists insights to resume-state for iterative improvement.
---

# Resume Coach

Help users discover hidden achievements, articulate undersold experience, and expand weak content through adaptive conversation. Unlike rigid questionnaires, this skill follows the conversation naturally and adapts to what emerges.

## When to Activate

Trigger coaching when:
- User says "I don't know what to put" or "help me think of achievements"
- Resume content is thin (few bullets, vague language, missing metrics)
- User adding new experience and needs help articulating it
- Comparing resume to job posting reveals content gaps
- User has experience but hasn't documented it well
- Bullets use weak language ("responsible for", "worked on", "helped with")

## Adaptive Coaching Approach

**Do not** follow a rigid questionnaire. Instead:

### 1. Assess the Situation

Before asking questions, understand context:

```bash
# Check for existing sessions to resume
uv run resume-coach/scripts/session_manager.py resume

# If new session, review current resume state
uv run resume-state/scripts/get_active.py
```

Consider:
- What does the current resume YAML show? (Read it)
- Is there a job posting to compare against? (Check `jobs/` directory)
- What's the user's stated goal or concern?
- Any previous coaching sessions to build on?

### 2. Start Where It Matters Most

Based on assessment:

| Situation | Starting Point |
|-----------|----------------|
| Resume is thin overall | Explore recent/prominent roles first |
| Targeting specific job | Find gaps vs. job requirements |
| Specific bullet is weak | Dig into that one achievement |
| User mentions something | Follow that thread immediately |
| Adding new experience | Gather role context, then achievements |

### 3. Follow the Conversation

Ask **one question at a time**. Wait for response before next question.

**Natural flow pattern:**
1. Ask open question about impact or achievement
2. Listen for interesting details in response
3. Probe for specifics: numbers, timeline, scope, difficulty
4. If response reveals new thread, follow it
5. When topic exhausted, move to next area

**Pivot when:**
- User reveals unexpected experience ("Oh, I also did X")
- Answer suggests deeper story ("That sounds significant, tell me more")
- User shows enthusiasm about something ("You seem proud of that")

### 4. Capture Discoveries

As insights emerge, structure them:

```yaml
discoveries:
  - role: "Senior Engineer at ExampleCorp"
    raw_response: "I built the ticket triage system..."
    key_details:
      situation: "Support tickets taking 48 hours to resolve"
      action: "Built automated triage using Python and NLP"
      result: "Reduced to 4 hours, CSAT increased 1.4 points"
      metrics: ["92% improvement", "3.2 to 4.6 CSAT"]
    suggested_bullet: "Built automated ticket triage system using Python and NLP, reducing average resolution time from 48 hours to 4 hours (92% improvement)"
    status: draft
```

### 5. Validate and Integrate

After drafting content:
- Read back the suggested bullet to the user
- Confirm accuracy (dates, numbers, scope)
- Adjust language to match user's voice
- Mark as approved when confirmed

## Coaching Techniques

### Drawing Out Achievements

**Impact questions** (start here):
- "What's the biggest problem you solved in this role?"
- "What would have happened if you weren't there?"
- "What are you most proud of?"

**Scope questions** (after initial response):
- "How many people/users/customers did this affect?"
- "What was the budget/team size/timeline?"
- "Was this solo or did you lead others?"

**Metrics questions** (probe for numbers):
- "Do you have any numbers? Even rough estimates help."
- "What was the before/after comparison?"
- "How would you quantify the improvement?"

See `references/coaching_questions.md` for 200+ organized questions.

### Expanding Weak Bullets

When encountering vague content like "Worked on customer support improvements":

Dig into STAR components:
- **Situation**: "What was the context? What problem existed?"
- **Task**: "What were you specifically asked to do?"
- **Action**: "What did you actually do? Be specific."
- **Result**: "What happened? Include numbers if possible."

Then synthesize into a strong bullet.

See `references/star_templates.md` for expansion patterns by achievement type.

### Finding Missing Metrics

When users say "I don't have the numbers":

- Estimate magnitude: "Was it hundreds, thousands, or millions?"
- Compare: "How much faster/better than before?"
- Describe scope: "How many systems/teams/users involved?"
- Use alternatives: time saved, error reduction, coverage increase

See `references/metrics_guide.md` for estimation techniques.

### Industry-Specific Probing

Adapt questions to context:

- **Tech**: system scale, production impact, architecture decisions
- **Finance**: AUM, regulatory compliance, risk reduction
- **Healthcare**: patient outcomes, compliance, clinical workflows
- **E-commerce**: conversion rates, GMV, peak traffic handling

See `references/industry_prompts.md` for industry-specific questions.

## Session Management

### Starting a Session

1. Check for incomplete sessions:
   ```bash
   uv run resume-coach/scripts/session_manager.py resume
   ```

2. If resuming, review previous discoveries and pick up where left off

3. If new session, create initial structure:
   ```json
   {
     "status": "active",
     "context": {
       "resume_version": "v2",
       "target_role": "Senior Software Engineer",
       "job_posting": "jobs/google_swe.txt"
     },
     "focus": {
       "areas": [],
       "roles_explored": []
     },
     "discoveries": [],
     "gaps_identified": [],
     "next_steps": []
   }
   ```

### During the Session

- Ask one question, wait for response
- Capture key details from responses immediately
- Draft bullets as discoveries emerge
- Validate drafted bullets with user before moving on
- Update session status if pausing

### Saving a Session

When pausing or completing:

```bash
echo '<session_json>' | uv run resume-coach/scripts/session_manager.py save
```

Or save from file:
```bash
uv run resume-coach/scripts/session_manager.py save -f session.json
```

### Session Status Values

- `active` — Currently in conversation
- `paused` — User stepped away, can resume
- `complete` — Session wrapped up, discoveries captured

### Listing Sessions

```bash
uv run resume-coach/scripts/session_manager.py list
```

## Output

After coaching, produce:

### 1. Updated Resume YAML

Ready-to-merge content:

```yaml
experience:
  - company: "Example Corp"
    positions:
      - title: "Senior Engineer"
        dates: "Jan 2022 - Present"
        achievements:
          - "Built automated ticket triage system using Python and NLP, reducing average resolution time from 48 hours to 4 hours (92% improvement)"
          - "Led migration of 3 legacy services to Kubernetes, achieving 99.9% uptime and reducing infrastructure costs by $150K annually"
```

### 2. Session Summary

- Discoveries made (how many bullets created/expanded)
- Remaining gaps (what still needs attention)
- Suggested next steps (optimize, format, continue coaching)

## Integration with Other Skills

```
resume-state → resume-coach → resume-optimizer → resume-formatter
     ↓              ↓               ↓                  ↓
  Project     Content discovery  Polish language    Generate PDF
  version     & expansion        & add metrics
```

**Before coaching**: Ensure project exists and version is active
**After coaching**: Consider creating new version if significant changes, then optimize

## Tips for Effective Coaching

**Be patient**: Users often need multiple prompts to remember details

**Probe for numbers**: "About how many?" is better than accepting "some"

**Validate importance**: "What would have happened without this?" reveals true impact

**Use their words**: Match the user's vocabulary and communication style

**Celebrate discoveries**: Acknowledge when they uncover good content

**Follow energy**: If user shows enthusiasm, dig deeper there

## Reference Materials

- `references/coaching_questions.md` — Questions by achievement type, role level, industry
- `references/star_templates.md` — STAR expansion templates by achievement type
- `references/industry_prompts.md` — Industry-specific probing questions
- `references/metrics_guide.md` — Techniques for estimating missing metrics
