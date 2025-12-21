"""Pydantic models for resume YAML validation.

These models match the structure defined in references/resume_schema.yaml
and provide type-safe validation for resume data.
"""

from typing import Optional, Union

from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator


class Contact(BaseModel):
    """Contact information section."""

    name: str = Field(..., min_length=1, description="Full name")
    title: Optional[str] = Field(None, description="Professional title or current role")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    location: Optional[str] = Field(None, description="City, State")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL or username")
    github: Optional[str] = Field(None, description="GitHub profile URL or username")
    website: Optional[str] = Field(None, description="Personal website URL")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v


class Position(BaseModel):
    """A single position/role within a company."""

    title: str = Field(..., min_length=1, description="Job title")
    dates: str = Field(..., description="Date range (e.g., 'Jan 2020 - Present')")
    achievements: list[str] = Field(
        default_factory=list, description="List of achievements/responsibilities"
    )

    @field_validator("achievements")
    @classmethod
    def validate_achievements(cls, v: list[str]) -> list[str]:
        if not v:
            return v
        for achievement in v:
            if not achievement.strip():
                raise ValueError("Achievement cannot be empty")
        return v


class Experience(BaseModel):
    """A single company with one or more positions."""

    company: str = Field(..., min_length=1, description="Company name")
    location: Optional[str] = Field(None, description="City, State")
    positions: list[Position] = Field(..., min_length=1, description="List of positions")


class Education(BaseModel):
    """Education entry."""

    institution: str = Field(..., min_length=1, description="University or school name")
    degree: str = Field(..., min_length=1, description="Degree type and major")
    graduation_year: Optional[str] = Field(None, description="Graduation year")
    location: Optional[str] = Field(None, description="City, State")
    gpa: Optional[str] = Field(None, description="GPA (e.g., '3.8/4.0')")
    honors: Optional[str] = Field(None, description="Honors or distinctions")
    minor: Optional[str] = Field(None, description="Minor field of study")


class Certification(BaseModel):
    """Professional certification."""

    name: str = Field(..., min_length=1, description="Certification name")
    issuer: Optional[str] = Field(None, description="Issuing organization")
    date: Optional[str] = Field(None, description="Issue date")
    credential_id: Optional[str] = Field(None, description="Credential ID")
    url: Optional[str] = Field(None, description="Verification URL")


class Project(BaseModel):
    """Project entry."""

    name: str = Field(..., min_length=1, description="Project name")
    dates: Optional[str] = Field(None, description="Date range")
    description: Optional[str] = Field(None, description="Brief description")
    technologies: list[str] = Field(default_factory=list, description="Technologies used")
    achievements: list[str] = Field(default_factory=list, description="Key achievements")
    url: Optional[str] = Field(None, description="Project URL")


class Publication(BaseModel):
    """Publication entry."""

    title: str = Field(..., min_length=1, description="Publication title")
    authors: Optional[str] = Field(None, description="Author list")
    venue: Optional[str] = Field(None, description="Journal or conference name")
    date: Optional[str] = Field(None, description="Publication date")
    url: Optional[str] = Field(None, description="DOI or URL")


class Award(BaseModel):
    """Award or honor."""

    name: str = Field(..., min_length=1, description="Award name")
    issuer: Optional[str] = Field(None, description="Issuing organization")
    date: Optional[str] = Field(None, description="Award date")
    description: Optional[str] = Field(None, description="Brief description")


class Language(BaseModel):
    """Language proficiency."""

    language: str = Field(..., min_length=1, description="Language name")
    proficiency: Optional[str] = Field(
        None, description="Proficiency level (Native/Fluent/Professional/Conversational/Basic)"
    )

    @field_validator("proficiency")
    @classmethod
    def validate_proficiency(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        valid_levels = {"native", "fluent", "professional", "conversational", "basic"}
        if v.lower() not in valid_levels:
            # Allow but warn - don't fail for non-standard levels
            pass
        return v


class Volunteer(BaseModel):
    """Volunteer experience."""

    organization: str = Field(..., min_length=1, description="Organization name")
    role: Optional[str] = Field(None, description="Volunteer role")
    dates: Optional[str] = Field(None, description="Date range")
    description: Optional[str] = Field(None, description="Brief description")
    achievements: list[str] = Field(default_factory=list, description="Contributions")


# Skills can be either a dict of category -> list[str] or category -> str
SkillsType = dict[str, Union[list[str], str]]


class Resume(BaseModel):
    """Complete resume model with all sections."""

    # Required sections
    contact: Contact = Field(..., description="Contact information")

    # Strongly recommended but optional
    summary: Optional[str] = Field(None, description="Professional summary (2-5 sentences)")
    experience: list[Experience] = Field(
        default_factory=list, description="Work experience"
    )
    skills: Optional[SkillsType] = Field(None, description="Skills organized by category")
    education: list[Education] = Field(default_factory=list, description="Education history")

    # Optional sections
    certifications: list[Certification] = Field(
        default_factory=list, description="Professional certifications"
    )
    projects: list[Project] = Field(default_factory=list, description="Notable projects")
    publications: list[Publication] = Field(
        default_factory=list, description="Publications"
    )
    awards: list[Award] = Field(default_factory=list, description="Awards and honors")
    languages: list[Language] = Field(
        default_factory=list, description="Language proficiencies"
    )
    volunteer: list[Volunteer] = Field(
        default_factory=list, description="Volunteer experience"
    )

    model_config = {"extra": "allow"}  # Allow unknown fields for forward compatibility


def validate_resume(data: dict) -> tuple[Resume, list[str]]:
    """Validate resume data and return model with warnings.

    Args:
        data: Resume data dictionary (typically loaded from YAML)

    Returns:
        Tuple of (validated Resume model, list of warning messages)

    Raises:
        pydantic.ValidationError: If required fields are missing or invalid
    """
    warnings = []

    # Check for recommended but missing sections
    if not data.get("summary"):
        warnings.append("Missing 'summary' section - strongly recommended")
    if not data.get("experience"):
        warnings.append("Missing 'experience' section - strongly recommended")
    if not data.get("skills"):
        warnings.append("Missing 'skills' section - strongly recommended")
    if not data.get("education"):
        warnings.append("Missing 'education' section - strongly recommended")

    # Check for weak action verbs in achievements
    weak_verbs = {"helped", "worked", "responsible", "participated", "assisted"}
    for exp in data.get("experience", []):
        for pos in exp.get("positions", []):
            for achievement in pos.get("achievements", []):
                first_word = achievement.split()[0].lower().rstrip(",.:;")
                if first_word in weak_verbs:
                    warnings.append(
                        f"Weak verb '{first_word}' in achievement: {achievement[:50]}..."
                    )

    resume = Resume.model_validate(data)
    return resume, warnings


if __name__ == "__main__":
    # Example usage
    import sys

    import yaml

    if len(sys.argv) < 2:
        print("Usage: python schema.py <resume.yaml>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = yaml.safe_load(f)

    try:
        resume, warnings = validate_resume(data)
        print(f"Valid resume for: {resume.contact.name}")
        if warnings:
            print("\nWarnings:")
            for w in warnings:
                print(f"  - {w}")
    except Exception as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)
