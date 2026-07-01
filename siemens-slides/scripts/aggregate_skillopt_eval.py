#!/usr/bin/env python3
"""Aggregate one or more SkillOpt eval run directories into a stable summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_rollouts(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON array")
    return payload


def compute_scores(results: list[dict[str, Any]]) -> tuple[float, float]:
    if not results:
        return 0.0, 0.0
    hard = sum(float(item.get("hard", 0.0)) for item in results) / len(results)
    soft = sum(float(item.get("soft", 0.0)) for item in results) / len(results)
    return hard, soft


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_root", help="Eval root that contains repeat_*/rollouts.json or rollouts.json")
    parser.add_argument(
        "--output",
        help="Optional output JSON path. Defaults to <input_root>/aggregate_summary.json",
    )
    args = parser.parse_args()

    input_root = Path(args.input_root).resolve()
    if not input_root.exists():
        raise SystemExit(f"Input root does not exist: {input_root}")

    repeat_dirs = sorted(
        path for path in input_root.glob("repeat_*") if (path / "rollouts.json").is_file()
    )
    if not repeat_dirs:
        if (input_root / "rollouts.json").is_file():
            repeat_dirs = [input_root]
        else:
            raise SystemExit(f"No rollouts.json found under {input_root}")

    per_repeat: list[dict[str, Any]] = []
    per_item: dict[str, dict[str, Any]] = {}

    for repeat_dir in repeat_dirs:
        rollouts = load_rollouts(repeat_dir / "rollouts.json")
        hard, soft = compute_scores(rollouts)
        per_repeat.append(
            {
                "name": repeat_dir.name,
                "path": str(repeat_dir),
                "n_items": len(rollouts),
                "hard": hard,
                "soft": soft,
            }
        )
        for result in rollouts:
            item_id = str(result.get("id", "unknown"))
            bucket = per_item.setdefault(
                item_id,
                {
                    "task_type": result.get("task_type", ""),
                    "hard_votes": [],
                    "soft_scores": [],
                    "fail_reasons": [],
                },
            )
            bucket["hard_votes"].append(int(result.get("hard", 0)))
            bucket["soft_scores"].append(float(result.get("soft", 0.0)))
            bucket["fail_reasons"].append(result.get("fail_reason", ""))

    hard_scores = [entry["hard"] for entry in per_repeat]
    soft_scores = [entry["soft"] for entry in per_repeat]
    item_count = len(per_item)
    majority_threshold = len(per_repeat) / 2.0

    unstable_items = []
    majority_pass_count = 0
    unanimous_pass_count = 0
    unanimous_fail_count = 0

    for item_id, bucket in sorted(per_item.items()):
        votes = bucket["hard_votes"]
        pass_count = sum(votes)
        pass_rate = pass_count / len(votes)
        majority_pass = pass_count > majority_threshold
        unanimous_pass = pass_count == len(votes)
        unanimous_fail = pass_count == 0
        mean_soft = sum(bucket["soft_scores"]) / len(bucket["soft_scores"])
        bucket["pass_count"] = pass_count
        bucket["pass_rate"] = pass_rate
        bucket["majority_pass"] = majority_pass
        bucket["unanimous_pass"] = unanimous_pass
        bucket["unanimous_fail"] = unanimous_fail
        bucket["mean_soft"] = mean_soft
        bucket["unstable"] = not (unanimous_pass or unanimous_fail)
        if bucket["unstable"]:
            unstable_items.append(item_id)
        if majority_pass:
            majority_pass_count += 1
        if unanimous_pass:
            unanimous_pass_count += 1
        if unanimous_fail:
            unanimous_fail_count += 1

    summary = {
        "input_root": str(input_root),
        "repeats": len(per_repeat),
        "n_items": item_count,
        "hard_scores": hard_scores,
        "soft_scores": soft_scores,
        "hard_mean": sum(hard_scores) / len(hard_scores),
        "soft_mean": sum(soft_scores) / len(soft_scores),
        "majority_hard": (majority_pass_count / item_count) if item_count else 0.0,
        "unanimous_hard": (unanimous_pass_count / item_count) if item_count else 0.0,
        "unanimous_fail_rate": (unanimous_fail_count / item_count) if item_count else 0.0,
        "unstable_items": unstable_items,
        "per_repeat": per_repeat,
        "per_item": dict(sorted(per_item.items())),
    }

    output_path = Path(args.output).resolve() if args.output else input_root / "aggregate_summary.json"
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
