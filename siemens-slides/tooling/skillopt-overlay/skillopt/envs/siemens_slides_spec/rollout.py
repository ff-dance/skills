from __future__ import annotations

import json
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from skillopt.model import chat_optimizer, chat_target
from skillopt.prompts import load_prompt
from skillopt.utils import extract_json

_ALLOWED_HERO = {"Siemens Petrol", "Light Petrol", "Advanta Green", "Soft Green", "Soft Blue"}
_P0_PASS_THRESHOLD = 16


def _build_system(skill_content: str) -> str:
    skill_section = f"## Current Skill\n{skill_content.strip()}\n" if skill_content.strip() else ""
    return load_prompt("rollout_system", env="siemens_slides_spec").format(skill_section=skill_section)


def _build_user(item: dict) -> str:
    source_material = (item.get("source_material") or "").strip()
    source_block = source_material if source_material else "无补充材料。请仅基于用户请求完成规划。"
    return (
        "请先理解用户请求，再输出一个严格合法的中文 slide_spec JSON。\n\n"
        f"## 用户请求\n{item.get('user_request', '').strip()}\n\n"
        f"## 原始材料\n{source_block}\n\n"
        f"## 输入类型\n{item.get('input_type', '').strip()}\n"
    )


def _build_judge_user(item: dict, candidate: dict, raw_response: str) -> str:
    return (
        "请根据任务期望和候选 slide_spec 对该结果评分。\n\n"
        f"## 用户请求\n{item.get('user_request', '').strip()}\n\n"
        f"## 原始材料\n{(item.get('source_material') or '').strip()}\n\n"
        f"## 期望 page_question\n{item.get('expected_page_question', '').strip()}\n\n"
        f"## 期望 reasoning_pattern\n{item.get('expected_reasoning_pattern', '').strip()}\n\n"
        f"## 期望 overflow\n{item.get('expected_overflow_recommendation', '').strip()}\n\n"
        f"## must_include\n{json.dumps(item.get('must_include') or [], ensure_ascii=False, indent=2)}\n\n"
        f"## must_avoid\n{json.dumps(item.get('must_avoid') or [], ensure_ascii=False, indent=2)}\n\n"
        f"## 候选 slide_spec\n{json.dumps(candidate, ensure_ascii=False, indent=2)}\n\n"
        f"## 原始模型输出\n{raw_response.strip()}\n"
    )


def _write_json(path: str, payload: dict | list) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _run_linter(spec: dict, linter_path: str) -> tuple[bool, list[str]]:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(spec, handle, ensure_ascii=False, indent=2)
        temp_path = handle.name
    try:
        proc = subprocess.run(
            ["python3", linter_path, temp_path],
            check=False,
            capture_output=True,
            text=True,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        errors = [line.strip() for line in output.splitlines() if line.strip().startswith("-")]
        return proc.returncode == 0, errors
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


def _fallback_judge(candidate: dict, item: dict) -> dict:
    scores = {
        "action_title_strength": 0,
        "pattern_match": 0,
        "layout_fit": 0,
        "evidence_strength": 0,
        "ghost_readability": 0,
        "consulting_tone": 0,
        "overflow_handling": 0,
    }
    action_title = str(candidate.get("action_title", "")).strip()
    if action_title and not any(action_title.endswith(suffix) for suffix in ("分析", "介绍", "概况", "说明")):
        scores["action_title_strength"] = 2
    if candidate.get("reasoning_pattern") == item.get("expected_reasoning_pattern"):
        scores["pattern_match"] = 3
    if candidate.get("preferred_layout"):
        scores["layout_fit"] = 2
    if isinstance(candidate.get("key_evidence"), list) and candidate.get("key_evidence"):
        scores["evidence_strength"] = 2
    if candidate.get("supporting_points") and candidate.get("component_strategy"):
        scores["ghost_readability"] = 2
    if candidate.get("color_strategy", {}).get("body_text") == "Deep Blue":
        scores["consulting_tone"] = 2
    if candidate.get("overflow_recommendation") == item.get("expected_overflow_recommendation"):
        scores["overflow_handling"] = 3
    total = sum(scores.values())
    scores["total_score"] = total
    scores["summary"] = "Fallback heuristic judge used because LLM judge was disabled or unavailable."
    return scores


def _llm_judge(item: dict, candidate: dict, raw_response: str, max_completion_tokens: int) -> dict:
    system = load_prompt("judge_system", env="siemens_slides_spec")
    user = _build_judge_user(item, candidate, raw_response)
    response, _ = chat_optimizer(
        system=system,
        user=user,
        max_completion_tokens=max_completion_tokens,
        retries=3,
        stage="judge",
    )
    parsed = extract_json(response)
    if not isinstance(parsed, dict):
        raise ValueError("Judge did not return valid JSON")
    return parsed


def _extract_candidate(response: str) -> dict | None:
    parsed = extract_json(response)
    if not isinstance(parsed, dict):
        return None
    return parsed


def _has_takeaway_signal(candidate: dict) -> bool:
    text = json.dumps(candidate, ensure_ascii=False)
    return any(token in text for token in ("takeaway", "收束", "结论", "建议", "so what"))


def process_one(
    item: dict,
    out_root: str,
    skill_content: str,
    *,
    max_completion_tokens: int,
    judge_max_completion_tokens: int,
    linter_path: str,
    use_llm_judge: bool,
) -> dict:
    item_id = str(item["id"])
    pred_dir = os.path.join(out_root, "predictions", item_id)
    os.makedirs(pred_dir, exist_ok=True)

    system = _build_system(skill_content)
    user = _build_user(item)
    result = {
        "id": item_id,
        "task_description": item.get("user_request", ""),
        "task_type": item.get("task_type", "siemens-slides"),
        "instruction": item.get("user_request", ""),
        "hard": 0,
        "soft": 0.0,
        "predicted_answer": "",
        "response": "",
        "fail_reason": "",
        "agent_ok": False,
        "n_turns": 1,
        "reference_text": item.get("reference_text", ""),
        "target_system_prompt": system,
        "target_user_prompt": user,
    }

    try:
        response, _ = chat_target(
            system=system,
            user=user,
            max_completion_tokens=max_completion_tokens,
            retries=3,
            stage="rollout",
        )
        result["response"] = response
        result["agent_ok"] = True
        Path(os.path.join(pred_dir, "target_system_prompt.txt")).write_text(system, encoding="utf-8")
        Path(os.path.join(pred_dir, "target_user_prompt.txt")).write_text(user, encoding="utf-8")
        conversation = [{"type": "message", "turn": 1, "content": response}]
        candidate = _extract_candidate(response)
        if candidate is None:
            result["fail_reason"] = "target output is not valid JSON"
            conversation.append({"role": "system", "content": "[EVALUATION RESULT]\nJSON 解析失败。"})
            _write_json(os.path.join(pred_dir, "conversation.json"), conversation)
            return result

        result["predicted_answer"] = json.dumps(candidate, ensure_ascii=False, indent=2)
        _write_json(os.path.join(pred_dir, "candidate_slide_spec.json"), candidate)

        linter_pass, linter_errors = _run_linter(candidate, linter_path)
        if not linter_pass:
            result["fail_reason"] = "linter fail: " + "; ".join(error.lstrip("- ").strip() for error in linter_errors)
            conversation.append({"role": "system", "content": f"[EVALUATION RESULT]\nP0 Linter failed.\n{result['fail_reason']}"})
            _write_json(os.path.join(pred_dir, "conversation.json"), conversation)
            return result

        if use_llm_judge:
            try:
                judge = _llm_judge(item, candidate, response, judge_max_completion_tokens)
            except Exception as exc:  # noqa: BLE001
                judge = _fallback_judge(candidate, item)
                judge["summary"] = f"{judge.get('summary', '')} Judge fallback reason: {exc}"
        else:
            judge = _fallback_judge(candidate, item)

        total_score = int(judge.get("total_score") or 0)
        if not total_score:
            total_score = sum(
                int(judge.get(key) or 0)
                for key in (
                    "action_title_strength",
                    "pattern_match",
                    "layout_fit",
                    "evidence_strength",
                    "ghost_readability",
                    "consulting_tone",
                    "overflow_handling",
                )
            )
            judge["total_score"] = total_score

        footer_spec = candidate.get("footer_spec", {})
        color_strategy = candidate.get("color_strategy", {})
        pattern_match_score = int(judge.get("pattern_match") or 0)
        pattern_match = pattern_match_score >= 2
        overflow_match = candidate.get("overflow_recommendation") == item.get("expected_overflow_recommendation")
        hero_valid = color_strategy.get("hero_accent") in _ALLOWED_HERO
        footer_valid = (
            footer_spec.get("footer_family") == "advanta-content-footer"
            and footer_spec.get("logo_family") == "compact-content-page-logo"
        )
        takeaway_signal = _has_takeaway_signal(candidate)

        result["soft"] = round(total_score / 21.0, 4)
        result["hard"] = int(
            total_score >= _P0_PASS_THRESHOLD
            and pattern_match
            and overflow_match
            and hero_valid
            and footer_valid
            and takeaway_signal
        )
        if not result["hard"]:
            result["fail_reason"] = (
                f"judge score={total_score}/21; "
                f"pattern_match={pattern_match}; overflow_match={overflow_match}; "
                f"hero_valid={hero_valid}; footer_valid={footer_valid}; takeaway_signal={takeaway_signal}"
            )

        judge_detail = {
            "judge": judge,
            "pattern_match_score": pattern_match_score,
            "pattern_match": pattern_match,
            "overflow_match": overflow_match,
            "hero_valid": hero_valid,
            "footer_valid": footer_valid,
            "takeaway_signal": takeaway_signal,
            "hard": result["hard"],
            "soft": result["soft"],
            "fail_reason": result["fail_reason"],
        }
        _write_json(os.path.join(pred_dir, "judge_result.json"), judge_detail)
        conversation.append({"role": "system", "content": "[EVALUATION RESULT]\n" + json.dumps(judge_detail, ensure_ascii=False, indent=2)})
        _write_json(os.path.join(pred_dir, "conversation.json"), conversation)
        return result
    except Exception as exc:  # noqa: BLE001
        result["fail_reason"] = str(exc)
        _write_json(
            os.path.join(pred_dir, "conversation.json"),
            [{"role": "system", "content": f"[EVALUATION RESULT]\nRuntime failure: {exc}"}],
        )
        return result


def run_batch(
    *,
    items: list[dict],
    out_root: str,
    skill_content: str,
    workers: int = 4,
    max_completion_tokens: int = 8192,
    judge_max_completion_tokens: int = 4096,
    siemens_repo_root: str = "",
    linter_path: str = "",
    use_llm_judge: bool = True,
) -> list[dict]:
    os.makedirs(out_root, exist_ok=True)
    resolved_linter = linter_path or os.path.join(siemens_repo_root, "scripts", "skillopt_spec_lint.py")
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = [
            pool.submit(
                process_one,
                item,
                out_root,
                skill_content,
                max_completion_tokens=max_completion_tokens,
                judge_max_completion_tokens=judge_max_completion_tokens,
                linter_path=resolved_linter,
                use_llm_judge=use_llm_judge,
            )
            for item in items
        ]
    results = [future.result() for future in futures]
    _write_json(os.path.join(out_root, "rollouts.json"), results)
    return results
