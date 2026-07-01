#!/usr/bin/env python3
"""Deterministic P0 linter for siemens-slides slide_spec artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = [
    "page_question",
    "action_title",
    "reasoning_pattern",
    "key_evidence",
    "l2_hero_choice",
    "supporting_points",
    "preferred_layout",
    "component_strategy",
    "footer_spec",
    "color_strategy",
    "overflow_recommendation",
    "degrade_mode",
]

BANNED_TITLE_SUFFIXES = ("分析", "介绍", "概况", "说明")
ALLOWED_HERO_ACCENTS = {
    "Siemens Petrol",
    "Light Petrol",
    "Advanta Green",
    "Soft Green",
    "Soft Blue",
}
ALLOWED_OVERFLOW = {
    "single-page",
    "suggest-split",
    "compressed-single-page",
    "multi-page-orchestration",
}
ALLOWED_DEGRADE = {"none", "brief-only", "image-plus-brief"}


def load_payload(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list):
        if not all(isinstance(item, dict) for item in payload):
            raise ValueError("JSON array must contain only objects")
        return payload
    raise ValueError("JSON must be an object or an array of objects")


def as_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def lint_spec(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in spec:
            errors.append(f"missing required field: {field}")

    if errors:
        return errors

    if not as_non_empty_string(spec["page_question"]):
        errors.append("page_question must be a non-empty string")
    else:
        page_question = spec["page_question"].strip()
        if "\n" in page_question:
            errors.append("page_question must be a single line")
        if page_question.count("？") + page_question.count("?") > 1:
            errors.append("page_question appears to contain multiple questions")

    if not as_non_empty_string(spec["action_title"]):
        errors.append("action_title must be a non-empty string")
    else:
        action_title = spec["action_title"].strip()
        if any(action_title.endswith(suffix) for suffix in BANNED_TITLE_SUFFIXES):
            errors.append("action_title ends with a banned weak-title suffix")

    if not as_non_empty_string(spec["reasoning_pattern"]):
        errors.append("reasoning_pattern must be a non-empty string")

    if not isinstance(spec["key_evidence"], list) or not spec["key_evidence"]:
        errors.append("key_evidence must be a non-empty list")
    elif not all(as_non_empty_string(item) for item in spec["key_evidence"]):
        errors.append("key_evidence must contain only non-empty strings")

    if not as_non_empty_string(spec["l2_hero_choice"]):
        errors.append("l2_hero_choice must be a non-empty string")

    if not isinstance(spec["supporting_points"], list) or not (3 <= len(spec["supporting_points"]) <= 5):
        errors.append("supporting_points must be a list with 3 to 5 items")
    elif not all(as_non_empty_string(item) for item in spec["supporting_points"]):
        errors.append("supporting_points must contain only non-empty strings")

    if not as_non_empty_string(spec["preferred_layout"]):
        errors.append("preferred_layout must be a non-empty string")

    if not as_non_empty_string(spec["component_strategy"]):
        errors.append("component_strategy must be a non-empty string")

    footer_spec = spec["footer_spec"]
    if not isinstance(footer_spec, dict):
        errors.append("footer_spec must be an object")
    else:
        footer_required = {
            "page_number": "Page X",
            "brand_mark": "SIEMENS",
            "footer_family": "advanta-content-footer",
            "logo_family": "compact-content-page-logo",
            "text_alignment": "left",
        }
        for field, expected in footer_required.items():
            if footer_spec.get(field) != expected:
                errors.append(f"footer_spec.{field} must equal {expected}")
        if not as_non_empty_string(footer_spec.get("footer_text")):
            errors.append("footer_spec.footer_text must be a non-empty string")

    color_strategy = spec["color_strategy"]
    if not isinstance(color_strategy, dict):
        errors.append("color_strategy must be an object")
    else:
        if color_strategy.get("body_text") != "Deep Blue":
            errors.append("color_strategy.body_text must equal Deep Blue")
        if color_strategy.get("hero_accent") not in ALLOWED_HERO_ACCENTS:
            errors.append("color_strategy.hero_accent is not an allowed brand token")
        if color_strategy.get("risk_accent") != "Risk Orange":
            errors.append("color_strategy.risk_accent must equal Risk Orange")

    if spec["overflow_recommendation"] not in ALLOWED_OVERFLOW:
        errors.append("overflow_recommendation is not allowed")

    if spec["degrade_mode"] not in ALLOWED_DEGRADE:
        errors.append("degrade_mode is not allowed")

    known_issues = spec.get("known_issues", [])
    if known_issues != []:
        if not isinstance(known_issues, list) or not all(as_non_empty_string(item) for item in known_issues):
            errors.append("known_issues must be an array of non-empty strings when provided")

    validation_result = spec.get("validation_result")
    if validation_result is not None and validation_result not in {
        "pending",
        "pass",
        "pass_with_warning",
        "fail_retry",
        "fail_degraded",
    }:
        errors.append("validation_result is not allowed")

    if re.search(r"\b(MECE|reasoning pattern|layout type)\b", spec["action_title"], re.IGNORECASE):
        errors.append("action_title must not expose internal method words")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint one or more slide_spec JSON files.")
    parser.add_argument("paths", nargs="+", help="JSON file paths to lint")
    args = parser.parse_args()

    total_errors = 0
    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            specs = load_payload(path)
        except Exception as exc:  # noqa: BLE001
            print(f"{path}: invalid JSON payload: {exc}")
            total_errors += 1
            continue

        for index, spec in enumerate(specs, start=1):
            errors = lint_spec(spec)
            label = f"{path}#{index}" if len(specs) > 1 else str(path)
            if errors:
                total_errors += len(errors)
                print(f"{label}: FAIL")
                for error in errors:
                    print(f"  - {error}")
            else:
                print(f"{label}: PASS")

    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
