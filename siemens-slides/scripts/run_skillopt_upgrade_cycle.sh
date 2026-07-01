#!/bin/zsh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL_ENV_FILE="${LOCAL_ENV_FILE:-$REPO_ROOT/.env.skillopt.local}"

if [[ -f "$LOCAL_ENV_FILE" ]]; then
  set -a
  source "$LOCAL_ENV_FILE"
  set +a
fi

function detect_skillopt_root() {
  local sibling_root="$REPO_ROOT/../SkillOpt"
  if [[ -d "$sibling_root" ]]; then
    echo "$sibling_root"
  fi
}

SKILLOPT_ROOT="${SKILLOPT_ROOT:-$(detect_skillopt_root)}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
CONFIG_PATH="${CONFIG_PATH:-$SKILLOPT_ROOT/configs/siemens_slides_spec/default.yaml}"
MODEL="${MODEL:-gpt-5.4}"

REPO_SKILL_PATH="${REPO_SKILL_PATH:-$REPO_ROOT/SKILL.md}"
SEED_SKILL_PATH="${SEED_SKILL_PATH:-$SKILLOPT_ROOT/skillopt/envs/siemens_slides_spec/skills/initial.md}"

RUN_NAME="${RUN_NAME:-upgrade-cycle-$(date +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$REPO_ROOT/tmp/skillopt-runs/$RUN_NAME}"
TRAIN_OUT="$OUT_ROOT/train"
PRECHECK_OUT="$OUT_ROOT/precheck"
VERIFY_OUT="$OUT_ROOT/verify"

PRECHECK_REPEATS="${PRECHECK_REPEATS:-1}"
VERIFY_REPEATS="${VERIFY_REPEATS:-1}"
SELECTION_REPEATS="${SELECTION_REPEATS:-3}"
TEST_REPEATS="${TEST_REPEATS:-1}"
TRAIN_NUM_EPOCHS="${TRAIN_NUM_EPOCHS:-1}"
FAILURE_ONLY="${FAILURE_ONLY:-true}"
RUN_TRAIN="${RUN_TRAIN:-1}"
PROMOTE_TO_REPO="${PROMOTE_TO_REPO:-1}"
TRAIN_CONTINUE_ON_ERROR="${TRAIN_CONTINUE_ON_ERROR:-1}"
INSTALL_OVERLAY="${INSTALL_OVERLAY:-1}"

function require_path() {
  local path="$1"
  local label="$2"
  if [[ ! -e "$path" ]]; then
    echo "$label not found: $path" >&2
    exit 1
  fi
}

function require_env() {
  local key="$1"
  if [[ -z "${(P)key:-}" ]]; then
    echo "Missing required env var: $key" >&2
    exit 1
  fi
}

function truthy() {
  case "${1:l}" in
    1|true|yes|on) return 0 ;;
    *) return 1 ;;
  esac
}

function run_eval_once() {
  local split="$1"
  local skill_path="$2"
  local out_dir="$3"

  mkdir -p "$out_dir"
  (
    cd "$SKILLOPT_ROOT"
    "$PYTHON_BIN" scripts/eval_only.py \
      --config "$CONFIG_PATH" \
      --skill "$skill_path" \
      --split "$split" \
      --cfg-options \
        "env.limit=0" \
        "env.out_root=$out_dir" \
        "model.optimizer=$MODEL" \
        "model.target=$MODEL"
  )
}

function run_eval_repeats() {
  local split="$1"
  local skill_path="$2"
  local out_root="$3"
  local repeats="$4"

  mkdir -p "$out_root"
  local repeat
  for repeat in $(seq 1 "$repeats"); do
    local repeat_dir="$out_root/repeat_$(printf '%02d' "$repeat")"
    echo "[eval] split=$split repeat=$repeat/$repeats -> $repeat_dir"
    run_eval_once "$split" "$skill_path" "$repeat_dir"
  done

  "$PYTHON_BIN" "$REPO_ROOT/scripts/aggregate_skillopt_eval.py" \
    "$out_root" \
    --output "$out_root/aggregate_summary.json" \
    >/dev/null
}

function train_cycle() {
  local exit_code=0
  mkdir -p "$TRAIN_OUT"
  set +e
  (
    cd "$SKILLOPT_ROOT"
    "$PYTHON_BIN" scripts/train.py \
      --config "$CONFIG_PATH" \
      --cfg-options \
        "train.num_epochs=$TRAIN_NUM_EPOCHS" \
        "gradient.failure_only=$FAILURE_ONLY" \
        "env.limit=0" \
        "env.out_root=$TRAIN_OUT" \
        "evaluation.selection_repeats=$SELECTION_REPEATS" \
        "evaluation.test_repeats=$TEST_REPEATS" \
        "model.optimizer=$MODEL" \
        "model.target=$MODEL"
  ) >"$TRAIN_OUT/train.log" 2>&1
  exit_code=$?
  set -e

  echo "$exit_code" >"$TRAIN_OUT/train.exit_code"
  if [[ "$exit_code" -ne 0 ]]; then
    echo "[warn] train.py exited with code $exit_code" >&2
    if ! truthy "$TRAIN_CONTINUE_ON_ERROR"; then
      cat "$TRAIN_OUT/train.log" >&2
      exit "$exit_code"
    fi
  fi
}

function copy_if_exists() {
  local src="$1"
  local dst="$2"
  if [[ -f "$src" ]]; then
    cp -f "$src" "$dst"
  fi
}

function json_get() {
  local path="$1"
  local expr="$2"
  "$PYTHON_BIN" - <<'PY' "$path" "$expr"
import json, sys
path, expr = sys.argv[1], sys.argv[2]
obj = json.load(open(path, encoding="utf-8"))
value = obj
for part in expr.split("."):
    if not part:
        continue
    if isinstance(value, dict):
        value = value.get(part)
    else:
        value = None
        break
print("" if value is None else value)
PY
}

if [[ -z "$SKILLOPT_ROOT" ]]; then
  echo "Missing SKILLOPT_ROOT. Set it explicitly or place SkillOpt at ../SkillOpt." >&2
  exit 1
fi

require_path "$SKILLOPT_ROOT" "SkillOpt root"
require_path "$REPO_SKILL_PATH" "Repo skill"
require_env "AZURE_OPENAI_ENDPOINT"
require_env "AZURE_OPENAI_API_KEY"
require_env "AZURE_OPENAI_AUTH_MODE"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python executable not found: $PYTHON_BIN" >&2
  exit 1
fi

if truthy "$INSTALL_OVERLAY"; then
  "$REPO_ROOT/scripts/install_skillopt_overlay.sh"
fi

require_path "$CONFIG_PATH" "SkillOpt config"
require_path "$SEED_SKILL_PATH" "SkillOpt seed skill"

mkdir -p "$OUT_ROOT"

cp -f "$REPO_SKILL_PATH" "$OUT_ROOT/repo_skill_before.md"
cp -f "$REPO_SKILL_PATH" "$SEED_SKILL_PATH"
cp -f "$REPO_SKILL_PATH" "$OUT_ROOT/seed_skill_synced.md"

echo "[sync] repo skill -> SkillOpt seed"
run_eval_repeats "valid_seen" "$SEED_SKILL_PATH" "$PRECHECK_OUT/valid_seen" "$PRECHECK_REPEATS"
run_eval_repeats "valid_unseen" "$SEED_SKILL_PATH" "$PRECHECK_OUT/valid_unseen" "$PRECHECK_REPEATS"

BEST_SKILL_PATH="$SEED_SKILL_PATH"
if truthy "$RUN_TRAIN"; then
  echo "[train] start SkillOpt cycle"
  train_cycle
  if [[ -f "$TRAIN_OUT/best_skill.md" ]]; then
    BEST_SKILL_PATH="$TRAIN_OUT/best_skill.md"
  fi
fi

cp -f "$BEST_SKILL_PATH" "$OUT_ROOT/best_skill_selected.md"

if truthy "$PROMOTE_TO_REPO"; then
  cp -f "$BEST_SKILL_PATH" "$REPO_SKILL_PATH"
  cp -f "$REPO_SKILL_PATH" "$SEED_SKILL_PATH"
fi

cp -f "$REPO_SKILL_PATH" "$OUT_ROOT/repo_skill_after.md"

echo "[verify] repo skill"
run_eval_repeats "valid_seen" "$REPO_SKILL_PATH" "$VERIFY_OUT/valid_seen" "$VERIFY_REPEATS"
run_eval_repeats "valid_unseen" "$REPO_SKILL_PATH" "$VERIFY_OUT/valid_unseen" "$VERIFY_REPEATS"

PRECHECK_SEEN_HARD="$(json_get "$PRECHECK_OUT/valid_seen/aggregate_summary.json" "hard_mean")"
PRECHECK_UNSEEN_HARD="$(json_get "$PRECHECK_OUT/valid_unseen/aggregate_summary.json" "hard_mean")"
VERIFY_SEEN_HARD="$(json_get "$VERIFY_OUT/valid_seen/aggregate_summary.json" "hard_mean")"
VERIFY_UNSEEN_HARD="$(json_get "$VERIFY_OUT/valid_unseen/aggregate_summary.json" "hard_mean")"

cat >"$OUT_ROOT/summary.md" <<EOF
# SkillOpt Upgrade Cycle

- run_name: \`$RUN_NAME\`
- model: \`$MODEL\`
- repo_skill: \`$REPO_SKILL_PATH\`
- seed_skill: \`$SEED_SKILL_PATH\`
- best_skill_selected: \`$BEST_SKILL_PATH\`
- run_train: \`$RUN_TRAIN\`
- promote_to_repo: \`$PROMOTE_TO_REPO\`
- precheck_repeats: \`$PRECHECK_REPEATS\`
- selection_repeats: \`$SELECTION_REPEATS\`
- test_repeats: \`$TEST_REPEATS\`
- verify_repeats: \`$VERIFY_REPEATS\`

## Precheck

- valid_seen hard_mean: \`$PRECHECK_SEEN_HARD\`
- valid_unseen hard_mean: \`$PRECHECK_UNSEEN_HARD\`

## Verify

- valid_seen hard_mean: \`$VERIFY_SEEN_HARD\`
- valid_unseen hard_mean: \`$VERIFY_UNSEEN_HARD\`

## Key Outputs

- summary: \`$OUT_ROOT/summary.md\`
- precheck valid_seen: \`$PRECHECK_OUT/valid_seen/aggregate_summary.json\`
- precheck valid_unseen: \`$PRECHECK_OUT/valid_unseen/aggregate_summary.json\`
- verify valid_seen: \`$VERIFY_OUT/valid_seen/aggregate_summary.json\`
- verify valid_unseen: \`$VERIFY_OUT/valid_unseen/aggregate_summary.json\`
- train log: \`$TRAIN_OUT/train.log\`
EOF

echo "[done] summary -> $OUT_ROOT/summary.md"
echo "[done] verify valid_seen hard_mean=$VERIFY_SEEN_HARD"
echo "[done] verify valid_unseen hard_mean=$VERIFY_UNSEEN_HARD"
