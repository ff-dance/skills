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
OUT_ROOT="${OUT_ROOT:-$REPO_ROOT/tmp/skillopt-runs/full}"
INSTALL_OVERLAY="${INSTALL_OVERLAY:-1}"

if [[ -z "$SKILLOPT_ROOT" ]]; then
  echo "Missing SKILLOPT_ROOT. Set it explicitly or place SkillOpt at ../SkillOpt." >&2
  exit 1
fi

if [[ ! -d "$SKILLOPT_ROOT" ]]; then
  echo "SkillOpt checkout not found: $SKILLOPT_ROOT" >&2
  exit 1
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python executable not found: $PYTHON_BIN" >&2
  exit 1
fi

if [[ "$INSTALL_OVERLAY" == "1" ]]; then
  "$REPO_ROOT/scripts/install_skillopt_overlay.sh"
fi

if [[ ! -f "$CONFIG_PATH" ]]; then
  echo "SkillOpt config not found: $CONFIG_PATH" >&2
  exit 1
fi

cd "$SKILLOPT_ROOT"

"$PYTHON_BIN" scripts/train.py \
  --config "$CONFIG_PATH" \
  --cfg-options "env.out_root=$OUT_ROOT" \
  "$@"
