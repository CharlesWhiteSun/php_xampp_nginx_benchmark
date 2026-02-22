#!/usr/bin/env bash
set -euo pipefail

# Verify generated config.json does not contain placeholder tokens like CPU_50
# and that connection values are numeric.

tmpdir=$(mktemp -d)
RESULTS_DIR="$tmpdir"
export RESULTS_DIR
export DURATION=60
export TOTAL_DURATION=180
export PER_ENDPOINT_DURATION=60
export CONNECTIONS=50
export CPU_DURATION=60
export JSON_DURATION=60
export IO_DURATION=60
export CPU_CONNECTIONS=50
export JSON_CONNECTIONS=50
export IO_CONNECTIONS=50

config_path=$(bash "$(dirname "$0")/../generate_config_only.sh")

if grep -E 'CPU_|JSON_|IO_' "$config_path" >/dev/null; then
  echo "[FAIL] Found placeholder tokens in config.json"
  exit 1
fi

grep -q '"duration": 180' "$config_path" || { echo "[FAIL] duration mismatch"; exit 1; }
grep -q '"per_endpoint_duration": 60' "$config_path" || { echo "[FAIL] per_endpoint_duration mismatch"; exit 1; }
grep -q '"connections": 50' "$config_path" || { echo "[FAIL] connections mismatch"; exit 1; }
grep -q '"endpoint_params"' "$config_path" || { echo "[FAIL] endpoint_params missing"; exit 1; }
grep -Pzo '"cpu"\s*:\s*\{[^}]*"connections"\s*:\s*50' "$config_path" >/dev/null || { echo "[FAIL] cpu connections mismatch"; exit 1; }
grep -Pzo '"json"\s*:\s*\{[^}]*"connections"\s*:\s*50' "$config_path" >/dev/null || { echo "[FAIL] json connections mismatch"; exit 1; }
grep -Pzo '"io"\s*:\s*\{[^}]*"connections"\s*:\s*50' "$config_path" >/dev/null || { echo "[FAIL] io connections mismatch"; exit 1; }
echo "[PASS] config placeholder and values look correct"

rm -rf "$tmpdir"
