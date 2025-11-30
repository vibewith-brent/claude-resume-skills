#!/usr/bin/env python3
"""
Validate resume YAML structure and content quality.

Usage:
    uv run --with pyyaml scripts/validate_yaml.py resume.yaml
"""

import sys
import yaml
from pathlib import Path


def load_yaml(filepath):
    """Load and parse YAML file."""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return data, None
    except yaml.YAMLError as e:
        return None, f"YAML syntax error: {e}"
    except FileNotFoundError:
        return None, f"File not found: {filepath}"


def validate_structure(data):
    """Validate required fields and structure."""
    errors = []
    warnings = []

    # Required top-level fields
    required_fields = ['contact', 'summary', 'experience', 'education', 'skills']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")

    # Validate contact info
    if 'contact' in data:
        contact_required = ['name', 'email']
        for field in contact_required:
            if field not in data['contact'] or not data['contact'][field]:
                errors.append(f"Missing contact.{field}")

    # Validate experience structure
    if 'experience' in data and isinstance(data['experience'], list):
        for i, exp in enumerate(data['experience']):
            if not isinstance(exp, dict):
                errors.append(f"experience[{i}] must be a dict")
                continue

            exp_required = ['company', 'title', 'start_date']
            for field in exp_required:
                if field not in exp or not exp[field]:
                    errors.append(f"experience[{i}] missing {field}")

            if 'achievements' in exp:
                if not isinstance(exp['achievements'], list):
                    errors.append(f"experience[{i}].achievements must be a list")
                elif not exp['achievements']:
                    warnings.append(f"experience[{i}].achievements is empty")

    # Validate education structure
    if 'education' in data and isinstance(data['education'], list):
        for i, edu in enumerate(data['education']):
            if not isinstance(edu, dict):
                errors.append(f"education[{i}] must be a dict")
                continue

            edu_required = ['degree', 'university', 'year']
            for field in edu_required:
                if field not in edu or not edu[field]:
                    warnings.append(f"education[{i}] missing {field}")

    # Validate skills
    if 'skills' in data:
        if not isinstance(data['skills'], (list, dict)):
            errors.append("skills must be a list or dict")

    return errors, warnings


def validate_content_quality(data):
    """Check for content quality issues."""
    warnings = []
    suggestions = []

    # Check summary length
    if 'summary' in data and isinstance(data['summary'], str):
        summary = data['summary']
        if len(summary) < 100:
            warnings.append("Professional summary is quite short (< 100 chars)")
        elif len(summary) > 800:
            warnings.append("Professional summary is quite long (> 800 chars)")

    # Check experience bullets
    if 'experience' in data and isinstance(data['experience'], list):
        weak_verbs = ['worked', 'helped', 'responsible', 'participated', 'involved', 'assisted']

        for i, exp in enumerate(data['experience']):
            if 'achievements' not in exp or not isinstance(exp['achievements'], list):
                continue

            company = exp.get('company', f'Company {i}')

            for j, bullet in enumerate(exp['achievements']):
                if not isinstance(bullet, str):
                    continue

                bullet_lower = bullet.lower()

                # Check for weak verbs
                for weak_verb in weak_verbs:
                    if bullet_lower.startswith(weak_verb):
                        suggestions.append(
                            f"{company} bullet {j+1}: Starts with weak verb '{weak_verb}' "
                            f"- consider stronger action verb"
                        )
                        break

                # Check for metrics (very basic)
                has_number = any(char.isdigit() for char in bullet)
                has_percent = '%' in bullet or 'percent' in bullet_lower
                has_dollar = '$' in bullet

                if not (has_number or has_percent or has_dollar):
                    suggestions.append(
                        f"{company} bullet {j+1}: Consider adding quantifiable metrics "
                        f"(time, cost, scale, quality)"
                    )

                # Check length
                if len(bullet) > 300:
                    suggestions.append(
                        f"{company} bullet {j+1}: Very long (>300 chars) - consider splitting or condensing"
                    )

    return warnings, suggestions


def validate_resume(filepath):
    """Run all validations on resume YAML."""
    print(f"Validating: {filepath}\n")

    # Load YAML
    data, error = load_yaml(filepath)
    if error:
        print(f"❌ FATAL ERROR: {error}")
        return False

    print("✓ YAML syntax is valid\n")

    # Validate structure
    struct_errors, struct_warnings = validate_structure(data)

    if struct_errors:
        print(f"❌ STRUCTURE ERRORS ({len(struct_errors)}):")
        for error in struct_errors:
            print(f"  - {error}")
        print()
        return False
    else:
        print("✓ Required structure is valid\n")

    if struct_warnings:
        print(f"⚠️  STRUCTURE WARNINGS ({len(struct_warnings)}):")
        for warning in struct_warnings:
            print(f"  - {warning}")
        print()

    # Validate content quality
    content_warnings, suggestions = validate_content_quality(data)

    if content_warnings:
        print(f"⚠️  CONTENT WARNINGS ({len(content_warnings)}):")
        for warning in content_warnings:
            print(f"  - {warning}")
        print()

    if suggestions:
        print(f"💡 SUGGESTIONS ({len(suggestions)}):")
        for suggestion in suggestions[:10]:  # Limit to first 10
            print(f"  - {suggestion}")
        if len(suggestions) > 10:
            print(f"  ... and {len(suggestions) - 10} more suggestions")
        print()

    # Summary
    total_issues = len(struct_warnings) + len(content_warnings) + len(suggestions)
    if total_issues == 0:
        print("✓ No issues found - resume YAML looks good!")
    else:
        print(f"Found {total_issues} suggestions/warnings (no critical errors)")

    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run --with pyyaml scripts/validate_yaml.py resume.yaml")
        sys.exit(1)

    filepath = sys.argv[1]
    success = validate_resume(filepath)
    sys.exit(0 if success else 1)
