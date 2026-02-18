#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
SCRIPT="$ROOT_DIR/start_benchmark.ps1"

require_line() {
  pattern="$1"
  label="$2"
  if ! grep -Fq "$pattern" "$SCRIPT"; then
    echo "[FAIL] missing preset line for $label: $pattern" >&2
    exit 1
  fi
}

require_line '$Config1_Duration = 180' 'quick duration'
require_line '$Config1_Connections = 100' 'quick connections'
require_line '$Config2_Duration = 600' 'pre-commit duration'
require_line '$Config2_Connections = 300' 'pre-commit connections'
require_line '$Config3_Duration = 900' 'bottleneck duration'
require_line '$Config3_Connections_R1 = 300' 'bottleneck round1'
require_line '$Config3_Connections_R2 = 600' 'bottleneck round2'
require_line '$Config3_Connections_R3 = 1000' 'bottleneck round3'
require_line '$Config4_Duration = 1800' 'pre-prod duration'
require_line '$Config4_Connections = 800' 'pre-prod connections'
require_line '$Config5_Duration = 28800' 'soak duration'
require_line '$Config5_Connections = 700' 'soak connections'
require_line '$Config6_Duration = 28800' 'extreme duration'
require_line '$Config6_Connections = 1000' 'extreme connections'
require_line '$Config7_Name = "Custom Parameters"' 'custom option as final entry'

echo "[PASS] test_start_benchmark_presets.sh"
