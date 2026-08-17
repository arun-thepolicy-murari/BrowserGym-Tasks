#!/usr/bin/env bash
set -euo pipefail
LOGS="${LOGS:-/logs}"
mkdir -p "$LOGS/verifier"
HERE="$(cd "$(dirname "$0")" && pwd)"
export LOGS
python3 "$HERE/score.py"
