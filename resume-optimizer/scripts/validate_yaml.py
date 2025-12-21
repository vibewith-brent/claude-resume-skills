#!/usr/bin/env python3
"""Validate resume YAML structure and content quality.

Usage:
    uv run scripts/validate_yaml.py resume.yaml
    uv run scripts/validate_yaml.py resume.yaml --json
    uv run scripts/validate_yaml.py resume.yaml --strict
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

# Import Pydantic schema if available
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "resume-extractor" / "scripts"))
    from schema import Resume, validate_resume as pydantic_validate
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False


def load_yaml(filepath: Path) -> tuple[dict | None, str | None]:
    """Load and parse YAML file."""
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)
        return data, None
    except yaml.YAMLError as e:
        return None, f"YAML syntax error: {e}"
    except FileNotFoundError:
        return None, f"File not found: {filepath}"


def validate_structure(data: dict) -> tuple[list[str], list[str]]:
    """Validate required fields and structure."""
    errors = []
    warnings = []

    # Required top-level fields
    required_fields = ["contact"]
    recommended_fields = ["summary", "experience", "education", "skills"]

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")

    for field in recommended_fields:
        if field not in data or not data[field]:
            warnings.append(f"Missing recommended field: {field}")

    # Validate contact info
    if "contact" in data and isinstance(data["contact"], dict):
        contact = data["contact"]
        if "name" not in contact or not contact["name"]:
            errors.append("Missing contact.name")
        if "email" not in contact or not contact["email"]:
            warnings.append("Missing contact.email (recommended)")

    # Validate experience structure (using correct schema: company -> positions)
    if "experience" in data and isinstance(data["experience"], list):
        for i, exp in enumerate(data["experience"]):
            if not isinstance(exp, dict):
                errors.append(f"experience[{i}] must be a dict")
                continue

            if "company" not in exp or not exp["company"]:
                errors.append(f"experience[{i}] missing company")

            # Check for positions array (correct schema)
            if "positions" in exp:
                if not isinstance(exp["positions"], list):
                    errors.append(f"experience[{i}].positions must be a list")
                else:
                    for j, pos in enumerate(exp["positions"]):
                        if not isinstance(pos, dict):
                            errors.append(f"experience[{i}].positions[{j}] must be a dict")
                            continue
                        if "title" not in pos or not pos["title"]:
                            errors.append(f"experience[{i}].positions[{j}] missing title")
                        if "dates" not in pos or not pos["dates"]:
                            warnings.append(f"experience[{i}].positions[{j}] missing dates")
                        if "achievements" in pos:
                            if not isinstance(pos["achievements"], list):
                                errors.append(
                                    f"experience[{i}].positions[{j}].achievements must be a list"
                                )
                            elif not pos["achievements"]:
                                warnings.append(
                                    f"experience[{i}].positions[{j}].achievements is empty"
                                )
            else:
                # Legacy format without positions - just warn
                warnings.append(
                    f"experience[{i}] uses legacy format; recommend using positions array"
                )

    # Validate education structure (using correct schema: institution, not university)
    if "education" in data and isinstance(data["education"], list):
        for i, edu in enumerate(data["education"]):
            if not isinstance(edu, dict):
                errors.append(f"education[{i}] must be a dict")
                continue

            if "institution" not in edu or not edu["institution"]:
                # Check for legacy 'university' field
                if "university" in edu:
                    warnings.append(
                        f"education[{i}] uses 'university' - rename to 'institution'"
                    )
                else:
                    warnings.append(f"education[{i}] missing institution")

            if "degree" not in edu or not edu["degree"]:
                warnings.append(f"education[{i}] missing degree")

    # Validate skills
    if "skills" in data:
        if not isinstance(data["skills"], (list, dict)):
            errors.append("skills must be a list or dict")

    return errors, warnings


def validate_content_quality(data: dict) -> tuple[list[str], list[str]]:
    """Check for content quality issues."""
    warnings = []
    suggestions = []

    # Check summary length
    if "summary" in data and isinstance(data["summary"], str):
        summary = data["summary"]
        if len(summary) < 100:
            warnings.append("Professional summary is quite short (< 100 chars)")
        elif len(summary) > 800:
            warnings.append("Professional summary is quite long (> 800 chars)")

    # Check experience bullets
    weak_verbs = {"worked", "helped", "responsible", "participated", "involved", "assisted"}

    if "experience" in data and isinstance(data["experience"], list):
        for exp in data["experience"]:
            if not isinstance(exp, dict):
                continue

            company = exp.get("company", "Unknown")
            positions = exp.get("positions", [])

            # Handle legacy format without positions
            if not positions and "achievements" in exp:
                positions = [{"title": exp.get("title", ""), "achievements": exp["achievements"]}]

            for pos in positions:
                if not isinstance(pos, dict):
                    continue

                achievements = pos.get("achievements", [])
                if not isinstance(achievements, list):
                    continue

                for j, bullet in enumerate(achievements):
                    if not isinstance(bullet, str):
                        continue

                    bullet_lower = bullet.lower()
                    first_word = bullet_lower.split()[0] if bullet_lower.split() else ""

                    # Check for weak verbs
                    if first_word.rstrip(",.;:") in weak_verbs:
                        suggestions.append(
                            f"{company}: Starts with weak verb '{first_word}' - "
                            f"consider stronger action verb"
                        )

                    # Check for metrics
                    has_number = any(char.isdigit() for char in bullet)
                    has_percent = "%" in bullet or "percent" in bullet_lower
                    has_dollar = "$" in bullet

                    if not (has_number or has_percent or has_dollar):
                        suggestions.append(
                            f"{company}: Consider adding quantifiable metrics "
                            f"(time, cost, scale, quality)"
                        )

                    # Check length
                    if len(bullet) > 300:
                        suggestions.append(
                            f"{company}: Bullet is long (>300 chars) - consider condensing"
                        )

    return warnings, suggestions


def validate_with_pydantic(data: dict) -> tuple[list[str], list[str]]:
    """Validate using Pydantic schema if available."""
    if not PYDANTIC_AVAILABLE:
        return [], ["Pydantic validation not available (schema.py not found)"]

    try:
        _, warnings = pydantic_validate(data)
        return [], warnings
    except Exception as e:
        return [f"Pydantic validation error: {e}"], []


def run_validation(filepath: Path, use_json: bool = False, strict: bool = False) -> bool:
    """Run all validations on resume YAML."""
    results = {
        "file": str(filepath),
        "valid": True,
        "errors": [],
        "warnings": [],
        "suggestions": [],
    }

    # Load YAML
    data, error = load_yaml(filepath)
    if error:
        results["valid"] = False
        results["errors"].append(error)
        if use_json:
            print(json.dumps(results, indent=2))
        else:
            print(f"[ERROR] {error}")
        return False

    # Validate structure
    struct_errors, struct_warnings = validate_structure(data)
    results["errors"].extend(struct_errors)
    results["warnings"].extend(struct_warnings)

    if struct_errors:
        results["valid"] = False

    # Validate content quality
    content_warnings, suggestions = validate_content_quality(data)
    results["warnings"].extend(content_warnings)
    results["suggestions"].extend(suggestions)

    # Pydantic validation
    pydantic_errors, pydantic_warnings = validate_with_pydantic(data)
    results["errors"].extend(pydantic_errors)
    results["warnings"].extend(pydantic_warnings)

    if pydantic_errors:
        results["valid"] = False

    # Strict mode: treat warnings as errors
    if strict and results["warnings"]:
        results["valid"] = False

    # Output
    if use_json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Validating: {filepath}\n")

        if results["valid"]:
            print("[OK] YAML syntax is valid\n")
        else:
            print("[FAIL] Validation failed\n")

        if results["errors"]:
            print(f"[ERRORS] ({len(results['errors'])}):")
            for error in results["errors"]:
                print(f"  - {error}")
            print()

        if results["warnings"]:
            print(f"[WARNINGS] ({len(results['warnings'])}):")
            for warning in results["warnings"]:
                print(f"  - {warning}")
            print()

        if results["suggestions"]:
            print(f"[SUGGESTIONS] ({len(results['suggestions'])}):")
            for suggestion in results["suggestions"][:10]:
                print(f"  - {suggestion}")
            if len(results["suggestions"]) > 10:
                print(f"  ... and {len(results['suggestions']) - 10} more")
            print()

        total_issues = len(results["warnings"]) + len(results["suggestions"])
        if results["valid"] and total_issues == 0:
            print("[OK] No issues found - resume YAML looks good!")
        elif results["valid"]:
            print(f"[OK] Valid with {total_issues} suggestions/warnings")
        else:
            print(f"[FAIL] {len(results['errors'])} errors found")

    return results["valid"]


def main():
    parser = argparse.ArgumentParser(
        description="Validate resume YAML structure and content quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/validate_yaml.py resume.yaml
  uv run scripts/validate_yaml.py resume.yaml --json
  uv run scripts/validate_yaml.py resume.yaml --strict
        """,
    )
    parser.add_argument("file", type=Path, help="Resume YAML file to validate")
    parser.add_argument(
        "--json", "-j", action="store_true", help="Output results as JSON"
    )
    parser.add_argument(
        "--strict", "-s", action="store_true", help="Treat warnings as errors"
    )

    args = parser.parse_args()

    if not args.file.exists():
        print(f"[ERROR] File not found: {args.file}")
        sys.exit(1)

    success = run_validation(args.file, use_json=args.json, strict=args.strict)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
