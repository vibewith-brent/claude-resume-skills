#!/usr/bin/env python3
"""Generate structured coaching session templates for resume content discovery.

This script outputs coaching session structures (question banks, interview guides,
note templates) that Claude uses to conduct interactive coaching sessions. It does
NOT perform automated content generation; Claude uses these templates to guide
conversations that extract achievements and details from users.

Workflow:
    1. Run this script to generate a coaching session template
    2. Claude uses the template to conduct an interactive interview
    3. User responses are captured and structured
    4. Claude generates resume YAML content from the session notes

Usage:
    uv run resume-coach/scripts/coach_session.py <mode> [--yaml resume.yaml]
    uv run resume-coach/scripts/coach_session.py discovery --yaml resume.yaml
    uv run resume-coach/scripts/coach_session.py star --bullet "Worked on projects"
    uv run resume-coach/scripts/coach_session.py gap --job job_posting.txt

Modes:
    discovery    - Achievement discovery for existing roles
    update       - Add new experience (job, project, education)
    star         - Expand weak bullets using STAR framework
    gap          - Find missing content vs. job requirements
    skills       - Discover hidden/transferable skills

Examples:
    # Start achievement discovery session for current resume
    uv run resume-coach/scripts/coach_session.py discovery --yaml resume.yaml

    # Generate STAR expansion template for a specific bullet
    uv run resume-coach/scripts/coach_session.py star --bullet "Led team projects"

    # Generate gap analysis template comparing to job posting
    uv run resume-coach/scripts/coach_session.py gap --job job.txt --yaml resume.yaml

    # Start new experience interview
    uv run resume-coach/scripts/coach_session.py update --type experience
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Optional, Any
import yaml


class CoachingMode(str, Enum):
    """Coaching session modes."""
    DISCOVERY = "discovery"
    UPDATE = "update"
    STAR = "star"
    GAP = "gap"
    SKILLS = "skills"


class ExperienceType(str, Enum):
    """Types of experience to add."""
    JOB = "experience"
    PROJECT = "projects"
    EDUCATION = "education"
    CERTIFICATION = "certifications"
    VOLUNTEER = "volunteer"


@dataclass
class CoachingSession:
    """Structure for a coaching session."""
    mode: CoachingMode
    target: Optional[str] = None  # Company name, role, or bullet text
    questions: list[str] = field(default_factory=list)
    notes: dict[str, Any] = field(default_factory=dict)
    output_yaml: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


def load_resume_yaml(yaml_path: Path) -> dict:
    """Load resume YAML file."""
    if not yaml_path.exists():
        print(f"Error: Resume YAML not found: {yaml_path}", file=sys.stderr)
        sys.exit(1)

    with open(yaml_path) as f:
        return yaml.safe_load(f)


def load_question_bank(references_dir: Path, category: str) -> list[str]:
    """Load questions from reference files."""
    questions = []

    # Load from coaching_questions.md
    questions_file = references_dir / "coaching_questions.md"
    if questions_file.exists():
        with open(questions_file) as f:
            content = f.read()
            # Extract questions from markdown (lines starting with - or numbered)
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('- "') or line.startswith('* "'):
                    # Remove markdown list marker and quotes
                    question = line.split('"')[1] if '"' in line else line[2:]
                    questions.append(question)

    return questions


def generate_discovery_session(resume_data: dict, references_dir: Path) -> CoachingSession:
    """Generate achievement discovery session template."""
    session = CoachingSession(mode=CoachingMode.DISCOVERY)

    # Load question banks
    impact_questions = [
        "What's the biggest problem you solved in this role?",
        "What would have happened if you weren't there?",
        "What are you most proud of from this job?",
        "Did anything you do save time, money, or prevent problems?",
    ]

    scope_questions = [
        "How many people/users/customers did this affect?",
        "What was the budget/team size/timeline?",
        "Was this a solo effort or did you lead others?",
    ]

    metrics_questions = [
        "Do you have any numbers? Revenue, users, time saved, error reduction?",
        "Even rough estimates help - 'about 50%' is better than nothing",
        "What was the before/after comparison?",
    ]

    # Identify roles with weak content
    if 'experience' in resume_data:
        for company in resume_data['experience']:
            company_name = company.get('company', 'Unknown')
            for position in company.get('positions', []):
                title = position.get('title', 'Unknown')
                achievements = position.get('achievements', [])

                # Flag roles with few bullets or weak bullets
                if len(achievements) < 4:
                    session.notes[f"{company_name} - {title}"] = {
                        'current_bullets': achievements,
                        'bullet_count': len(achievements),
                        'needs_expansion': True,
                        'questions': impact_questions + scope_questions + metrics_questions
                    }

    session.questions = impact_questions + scope_questions + metrics_questions
    return session


def generate_star_session(bullet: str, references_dir: Path) -> CoachingSession:
    """Generate STAR expansion session for a weak bullet."""
    session = CoachingSession(mode=CoachingMode.STAR, target=bullet)

    session.questions = [
        "SITUATION: What was the context? What problem existed?",
        "TASK: What were you specifically asked to do?",
        "ACTION: What did you actually do? Be specific about your actions.",
        "RESULT: What happened? Include numbers if possible.",
    ]

    session.notes = {
        'original_bullet': bullet,
        'situation': '',
        'task': '',
        'action': '',
        'result': '',
        'expanded_bullet': ''
    }

    return session


def generate_gap_session(resume_data: dict, job_file: Optional[Path], references_dir: Path) -> CoachingSession:
    """Generate gap analysis session comparing resume to job requirements."""
    session = CoachingSession(mode=CoachingMode.GAP)

    job_requirements = []
    if job_file and job_file.exists():
        with open(job_file) as f:
            job_text = f.read()
            # Simple extraction - in practice, this would be more sophisticated
            session.notes['job_posting'] = job_text

    session.questions = [
        "For each missing requirement, ask:",
        "  - Have you done anything similar, even in a different context?",
        "  - Any projects (work or personal) using this skill/technology?",
        "  - Experience from previous roles that transfer?",
        "  - Education or self-study in this area?",
    ]

    return session


def generate_update_session(experience_type: ExperienceType, references_dir: Path) -> CoachingSession:
    """Generate guided interview for adding new experience."""
    session = CoachingSession(mode=CoachingMode.UPDATE, target=experience_type.value)

    if experience_type == ExperienceType.JOB:
        session.questions = [
            "BASIC INFO:",
            "  - Company name and your title?",
            "  - Start date and end date (or 'present')?",
            "  - Company location (city or remote)?",
            "  - Brief description of the company?",
            "",
            "ROLE OVERVIEW:",
            "  - What was your main responsibility?",
            "  - Who did you report to? Who reported to you?",
            "  - What team/department were you part of?",
            "",
            "KEY ACHIEVEMENTS (repeat 4-6 times):",
            "  - Describe a project or achievement",
            "  - What was the problem or goal?",
            "  - What did you specifically do?",
            "  - What was the result or impact?",
            "  - Any metrics or numbers?",
        ]

        session.notes = {
            'company': '',
            'title': '',
            'dates': '',
            'location': '',
            'description': '',
            'achievements': []
        }

    return session


def generate_skills_session(references_dir: Path) -> CoachingSession:
    """Generate hidden skills discovery session."""
    session = CoachingSession(mode=CoachingMode.SKILLS)

    session.questions = [
        "SIDE PROJECTS:",
        "  - Any personal projects, open source contributions, or hobby coding?",
        "  - Ever built something for friends/family?",
        "  - Any blogs, tutorials, or teaching you've done?",
        "",
        "VOLUNTEER WORK:",
        "  - Any volunteer experience that used professional skills?",
        "  - Board positions, mentoring, community organizing?",
        "",
        "EDUCATION/TRAINING:",
        "  - Recent courses, certifications, or self-study?",
        "  - Hackathons, conferences, workshops?",
        "",
        "TRANSFERABLE SKILLS:",
        "  - Previous careers that taught relevant skills?",
        "  - Management experience from non-work contexts?",
    ]

    return session


def print_session_template(session: CoachingSession, format: str = "markdown"):
    """Print the coaching session template."""
    if format == "json":
        print(json.dumps(session.to_dict(), indent=2))
        return

    # Markdown format
    print(f"# Coaching Session: {session.mode.value.title()}")
    print()

    if session.target:
        print(f"**Target**: {session.target}")
        print()

    print("## Questions")
    print()
    for q in session.questions:
        if q.strip() and not q.endswith(':'):
            print(f"- {q}")
        else:
            print(q)
    print()

    print("## Session Notes")
    print()
    print("```yaml")
    print(yaml.dump(session.notes, default_flow_style=False, sort_keys=False))
    print("```")
    print()

    print("## Next Steps")
    print()
    print("1. Conduct interview using questions above")
    print("2. Fill in session notes with user responses")
    print("3. Generate resume YAML from completed notes")
    print("4. Validate with user and integrate into resume")


def main():
    parser = argparse.ArgumentParser(
        description="Generate coaching session templates for resume content discovery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "mode",
        type=str,
        choices=[m.value for m in CoachingMode],
        help="Coaching session mode"
    )

    parser.add_argument(
        "--yaml",
        type=Path,
        help="Path to resume YAML file"
    )

    parser.add_argument(
        "--bullet",
        type=str,
        help="Bullet text to expand (for STAR mode)"
    )

    parser.add_argument(
        "--job",
        type=Path,
        help="Path to job posting file (for gap mode)"
    )

    parser.add_argument(
        "--type",
        type=str,
        choices=[t.value for t in ExperienceType],
        default="experience",
        help="Type of experience to add (for update mode)"
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["markdown", "json"],
        default="markdown",
        help="Output format"
    )

    args = parser.parse_args()

    # Find references directory
    script_dir = Path(__file__).parent.parent
    references_dir = script_dir / "references"

    if not references_dir.exists():
        print(f"Warning: References directory not found: {references_dir}", file=sys.stderr)

    # Generate session based on mode
    mode = CoachingMode(args.mode)

    if mode == CoachingMode.DISCOVERY:
        if not args.yaml:
            print("Error: --yaml required for discovery mode", file=sys.stderr)
            sys.exit(1)
        resume_data = load_resume_yaml(args.yaml)
        session = generate_discovery_session(resume_data, references_dir)

    elif mode == CoachingMode.STAR:
        if not args.bullet:
            print("Error: --bullet required for STAR mode", file=sys.stderr)
            sys.exit(1)
        session = generate_star_session(args.bullet, references_dir)

    elif mode == CoachingMode.GAP:
        if not args.yaml:
            print("Error: --yaml required for gap mode", file=sys.stderr)
            sys.exit(1)
        resume_data = load_resume_yaml(args.yaml)
        session = generate_gap_session(resume_data, args.job, references_dir)

    elif mode == CoachingMode.UPDATE:
        exp_type = ExperienceType(args.type)
        session = generate_update_session(exp_type, references_dir)

    elif mode == CoachingMode.SKILLS:
        session = generate_skills_session(references_dir)

    else:
        print(f"Error: Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)

    # Print the session template
    print_session_template(session, args.format)


if __name__ == "__main__":
    main()
