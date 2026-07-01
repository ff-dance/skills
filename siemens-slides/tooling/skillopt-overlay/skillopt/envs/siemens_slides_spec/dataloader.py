from __future__ import annotations

import json
from pathlib import Path

from skillopt.datasets.base import SplitDataLoader


def _load_items(path: str) -> list[dict]:
    files = sorted(Path(path).glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No JSON files found in {path}")
    with files[0].open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {files[0]}")
    return data


def _reference_text(raw: dict) -> str:
    lines = [
        f"expected_page_question: {raw.get('expected_page_question', '')}",
        f"expected_reasoning_pattern: {raw.get('expected_reasoning_pattern', '')}",
        f"expected_overflow_recommendation: {raw.get('expected_overflow_recommendation', '')}",
    ]
    must_include = raw.get("must_include") or []
    must_avoid = raw.get("must_avoid") or []
    if must_include:
        lines.append("must_include:")
        lines.extend(f"- {item}" for item in must_include)
    if must_avoid:
        lines.append("must_avoid:")
        lines.extend(f"- {item}" for item in must_avoid)
    return "\n".join(lines).strip()


def _normalize(raw: dict) -> dict:
    return {
        "id": str(raw["id"]),
        "user_request": str(raw.get("user_request", "")),
        "source_material": str(raw.get("source_material", "")),
        "input_type": str(raw.get("input_type", "")),
        "expected_page_question": str(raw.get("expected_page_question", "")),
        "expected_reasoning_pattern": str(raw.get("expected_reasoning_pattern", "")),
        "must_include": list(raw.get("must_include") or []),
        "must_avoid": list(raw.get("must_avoid") or []),
        "expected_overflow_recommendation": str(raw.get("expected_overflow_recommendation", "")),
        "reference_text": _reference_text(raw),
        "task_type": str(raw.get("expected_reasoning_pattern") or raw.get("input_type") or "siemens-slides"),
        "task_description": str(raw.get("user_request", "")),
    }


class SiemensSlidesSpecDataLoader(SplitDataLoader):
    """Load chinese siemens-slides training tasks from split_dir."""

    def load_raw_items(self, data_path: str) -> list[dict]:
        with open(data_path, encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError(f"Expected a JSON array in {data_path}")
        return [_normalize(item) for item in data]

    def load_split_items(self, split_path: str) -> list[dict]:
        return [_normalize(item) for item in _load_items(split_path)]

