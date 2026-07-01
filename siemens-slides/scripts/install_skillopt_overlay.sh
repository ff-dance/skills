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
OVERLAY_ROOT="${OVERLAY_ROOT:-$REPO_ROOT/tooling/skillopt-overlay}"

function require_path() {
  local path="$1"
  local label="$2"
  if [[ ! -e "$path" ]]; then
    echo "$label not found: $path" >&2
    exit 1
  fi
}

if [[ -z "$SKILLOPT_ROOT" ]]; then
  echo "Missing SKILLOPT_ROOT. Set it explicitly or place SkillOpt at ../SkillOpt." >&2
  exit 1
fi

require_path "$SKILLOPT_ROOT" "SkillOpt root"
require_path "$OVERLAY_ROOT" "SkillOpt overlay"

mkdir -p \
  "$SKILLOPT_ROOT/configs/_base_" \
  "$SKILLOPT_ROOT/configs/siemens_slides_spec" \
  "$SKILLOPT_ROOT/scripts" \
  "$SKILLOPT_ROOT/skillopt/engine" \
  "$SKILLOPT_ROOT/skillopt/model" \
  "$SKILLOPT_ROOT/skillopt/envs"

cp -f "$OVERLAY_ROOT/configs/_base_/default.yaml" "$SKILLOPT_ROOT/configs/_base_/default.yaml"
cp -f "$OVERLAY_ROOT/scripts/eval_only.py" "$SKILLOPT_ROOT/scripts/eval_only.py"
cp -f "$OVERLAY_ROOT/scripts/train.py" "$SKILLOPT_ROOT/scripts/train.py"
cp -f "$OVERLAY_ROOT/skillopt/config.py" "$SKILLOPT_ROOT/skillopt/config.py"
cp -f "$OVERLAY_ROOT/skillopt/engine/trainer.py" "$SKILLOPT_ROOT/skillopt/engine/trainer.py"
cp -f "$OVERLAY_ROOT/skillopt/model/__init__.py" "$SKILLOPT_ROOT/skillopt/model/__init__.py"
cp -f "$OVERLAY_ROOT/skillopt/model/azure_openai.py" "$SKILLOPT_ROOT/skillopt/model/azure_openai.py"

rm -rf "$SKILLOPT_ROOT/skillopt/envs/siemens_slides_spec"
cp -R "$OVERLAY_ROOT/skillopt/envs/siemens_slides_spec" "$SKILLOPT_ROOT/skillopt/envs/"

REPO_ROOT_ESCAPED="${REPO_ROOT//\//\\/}"
sed "s|__REPO_ROOT__|$REPO_ROOT_ESCAPED|g" \
  "$OVERLAY_ROOT/configs/siemens_slides_spec/default.yaml.template" \
  >"$SKILLOPT_ROOT/configs/siemens_slides_spec/default.yaml"

echo "[done] installed SkillOpt overlay into $SKILLOPT_ROOT"
